import openai
from openai import OpenAI
import dbpedia_sparql as db
import json
import os
import time
import itertools
import copy
from sparql_baseline_gpt35 import retrieval_relation_parse_answer
from sparql_baseline_gpt35 import open_file
from tqdm import tqdm
import query_form_with_rel_forV3 as sparql
import factKG_chatversion as fc
# Initialize the OpenAI client
openai.api_key = "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"
client = OpenAI(api_key=openai.api_key)
# Define the long initial prompt with triple quotes
initial_prompt = """
Your role is to verify whether the claim is True or False based on the graph data. You can call helper functions to find the sub-graph used as evidence for verification.
You can decide whether to answer the claim or not. If it's difficult to find evidence even after searching through the KG, you can choose not to answer. 
However, if you decide to answer because there's enough evidence, you can choose either True or False.
Some claims might be True if there is actual evidence in the triple set from the graph data. Other claims might be False because the actual evidence triple set does not exist in the graph or does not match the claim.
I will give you a claim and a set of Given_entities for reference. However, some entities in the claim may not be included in the Given_entities. You can explore the graph and infer entities using helper functions.
When you provide your reasoning and call a helper function, you can use the following format, and I will give you the execution result. Note: you should align with entities that actually exist in the graph. Do not change the format of the entity or relation, including '~'.
Important: You must follow the format when you call helper functions.

Helper Functions
1.getRelation(entity): Returns the list of relations linked to the entity. You can choose several relations from the list that seem related to the claim.
2.exploreKG(entity: [relation_1,relation_2, ... relation_K]): Returns the triple set around the entity. For example, [entity, relation_1, tail entity], [entity, relation_2, tail entity], etc.
3.confidenceCheck([head, relation, tail],[head, relation, tail]...): Checks your selections used in the getRelation() and exploreKG() functions. If you think you chose unsuitable relations from the execution result of getRelation(), or if you need more information about another entity, your judgment was wrong. In this case, you need to use the helper functions again to get the right information.
4.Verify('true' or 'false' or 'Abstain'): If you can judge the claim as True/False, select 'Try', and if you decide not to answer due to insufficient evidence, select 'Abstain'.


Here is an example

Example )
Claim :  The theater was operated by the company located in Newyork has 200 employess.
Given entity : ['NewYork', '200']

[ChatGPT]
Reasoning : I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function : getRelation('NewYork') ## getRelation('200')
[Server]
Execution result :  Relation_list('NewYork') = ['countryName','~location','Citizenship','headQuarters'], Relation_list('200') = ['MountHeight','~countOf','~employeeNumber']
[ChatGPT]
Reasoning : I need the information about 'The theater' and 'the Company'. Let's look around the given entities to find out.
Helper function : exploreKG('NewYork' :['~location', 'headQuarters', 'Citizenship']) ## exploreKG('200': ['~countOf', '~employeeNumber', 'MountHeight'])
[Server]
Execution result : ['NewYork','~location','Central Park'], ['NewYork','headQuarters','Dominic Corporation'], ['NewYork','Citizenship','permanent resident'], ['200','~countOf','quoted ratio'], ['200','~employeeNumber','Barrymore Theatre']
[ChatGPT]
Reasoning :  Now, I'll check the steps are going right way. I think that 'Citizenship' for entity 'NewYork' doesn't need for claim. Also, 'MountHeight' for entity '200' doesn't need for claim.
Helper fuctions : confidenceCheck([['NewYork','~location','Central Park'], ['NewYork','headQuarters','Dominic Corporation'], ['NewYork','Citizenship','permanent resident'], ['200','~countOf','quoted ratio'], ['200','~employeeNumber','Barrymore Theatre']])
[Server]
Execution result : Choose relations you need to look again.
[ChatGPT]
Reasoning : Reflecting the inspection , I'll require the helper function again.
Helper function : exploreKG('NewYork' :['~location', 'headQuarters']) ## exploreKG('200': ['~countOf', '~employeeNumber'])
[Server]
Execution result : ['NewYork','~location','Central Park'], ['NewYork','headQuarters','Dominic Corporation'], ['200','~countOf','quoted ratio'], ['200','~employeeNumber','Barrymore Theatre']
[ChatGPT]
Reasoning : 'The theater' of the claim might indicates 'Barrymore Theatre' and 'the company' of claim might indicate 'Dominic Coporation'. Let's look around these entities.
Helper function : getRelation('Barrymore Theatre') ## getRelation('Dominic Coporation')
[Server]
Execution result : Relation_list('Barrymore Theatre') = ['openDate','GoogleRate','employeeNumber','owner','operatedBy','~Operator'],  Relation_list('Dominic Corporation') = ['Operator','item','location','startDate']
[ChatGPT]
Reasoning : To verify the relation between 'the theater' and 'the company', we need to focus on 'Barrymore Theatre' with 'operatedBy', '~Operator' and 'Dominic Corporation' with 'Operator'.
Helper function : exploreKG('Barrymore Theatre' : ['openDate', 'GoogleRate']) ## exploreKG('Dominic Corporation' :['Operator'])
[Server]
Execution result : ['Barrymore Theatre','openDate','1988-02-13'], ['Barrymore Theatre','GoogleRate','3.8'], ['Dominic Corporation','Operator','Berrymore Theatre']
[ChatGPT]
Reasoning :  Now, I'll check the steps are going right way. I think I left out a necesary relations for entity 'Barrymore Theatre'. Also, I chose wrong relation for entity 'Dominic Corporation'.
Helper function : confidenceCheck(['Barrymore Theatre', 'openDate', '1988-02-13'], ['Barrymore Theatre', 'GoogleRate', '3.8'], ['Dominic Corporation', 'Operator', 'Berrymore Theatre'])
[Server]
Execution result : Choose relations you need to look again.
[ChatGPT]
Reasoning : Reflecting the inspection , I'll require the helper function again.
Helper function : exploreKG('Barrymore Theatre' : ['operatedBy', '~Operator']) ## exploreKG('Dominic Corporation' :['Operator'])
[Server]
Execution result : ['Berrymore Theatre','operatedBy','Dominic Corporation'], ['Barrymore Theatre','~Operator','Dominic Corporation'], ['Dominic Corporation','Operator','Berrymore Theatre']
[ChatGPT]
Reasoning : Now the information are enough to verify. The structure of claim is as follows. [['200', '~employeeNumber', 'Barrymore Theatre'], ['Barrymore Theatre', '~Operator', 'Dominic Corporation'], ['NewYork', 'headQuarters', 'Dominic Corporation']]. So the claim is True.
Helper function : Verify('true')

Now, it's your turn.
Claim : <<<Question>>>
Given entity: <<<Entity set>>>

Let's start the process. Please give me the reasoning and helper function, then I will return you the execution result.
"""

def ask_openai(message, message_history):
    # Append user message to message history
    message_history.append({"role": "user", "content": message})

    # Call OpenAI API to get the assistant's response
    response = client.chat.completions.create(
        #model="gpt-4-turbo",
        #model = "gpt-3.5-turbo-0125",
        model = "gpt-4o",
        messages=message_history,
        temperature=0.2,
        top_p = 0.1
    )

    # Get assistant's message
    assistant_message = response.choices[0].message.content

    # Append assistant message to message history
    message_history.append({"role": "assistant", "content": assistant_message})

    return assistant_message, message_history

def main(prompt):
    message_history = [{"role": "system", "content": prompt}]
    #print("[ChatGPT]\nLet's start the process. Please provide the execution results for the helper functions as requested.")
    
    iter=0
    status ='keep'
    while True:
        iter +=1
        if iter>30:
            break
        
        assistant_message, message_history = ask_openai("", message_history)
        #print(f"[ChatGPT]\n: {assistant_message}")

        # Parse the helper function requests from the assistant's message
        if "Helper function" in assistant_message:
            helper_function_calls = function_split(assistant_message)

            
            execution_result = ''
            for call in helper_function_calls:
                #print(f"call:{call}")
                
                if "getRelation" in call :
                    try:
    
                        entity = call.split("getRelation(")[1].split(")")[0][1:-1]
                        result = get_relation(entity)
                        execution_result +=f"[Server]\nExecution result: Relation_list({entity}) = {result}\n"
                    except:
                        execution_result +=f"[Server]\nThe format of helper function you required is wrong. Please call it again.\n"
                elif "exploreKG" in call :
                    try: 
                        entity = call.split("exploreKG(")[1].split(": ")[0][1:-1]
                        relations = call.split(": [")[1].split("])")[0].strip().split(', ')
                        result = explore_kg(entity, relations)      #entity, string of relation list
                        execution_result += f"[Server]\nExecution result: {', '.join([str(triple) for triple in result])}\n"
                    except:
                        execution_result +=f"[Server]\nThe format of helper function you required is wrong. Please call it again.\n"

                elif "confidenceCheck" in call:
                    execution_result += f"[Server]\nChoose relations you need to look again.\n"
                    
                elif "Verify" in call :
                    
                    try:
                        answer = call.split("Verify('")[1].split("')")[0]
                        result = verify(answer)
                        return answer
                        
                    except:
                        execution_result +=f"[Server]\nThe format of helper function you required is wrong. Please call it again.\n"

       
                
                

            # Provide the execution result back to the assistant
            #print(f"{execution_result}")
            assistant_message, message_history = ask_openai(execution_result, message_history)
            #print(f"[ChatGPT]\n{assistant_message}")
            
        else:
            continue
    if iter >30:
        #print("More than 30 iteration!!!!!!!!!!!")
        answer = 'Abstain'

    return answer

def get_relation(entity):
    #print(f'entity:{str(entity)}')
    #entity = "\"" + entity+"\""
    relation_list = db.getRelationsFromEntity(entity)
    #print(f"reltaion list of called fucntion:{relation_list}")
    return relation_list

def explore_kg(entity, relations):
    #print(f"entity:{entity}, relations:{relations}")
    triple_sets= []
    for rel in relations:
        rel = rel[1:-1]
        tails = db.getEntityFromEntRel(entity, rel)
        for tail in tails:
            tmp = [entity,rel,tail]
            triple_sets.append(tmp)
    #print(f'triple sets:{triple_sets}')
    return triple_sets

def function_split(assistant_message):
    if 'exploreKG' in assistant_message:
        if '##' in assistant_message:
            helper_function_calls = assistant_message.split("Helper function: ")[1].split(' ## ')
        else:
            helper_function_calls = [assistant_message.split("Helper function: ")[1]]
    elif 'getRelation' in assistant_message:
        if '##' in assistant_message:
            helper_function_calls = assistant_message.split("Helper function: ")[1].split(' ## ')
        else:
            helper_function_calls = [assistant_message.split("Helper function: ")[1]]
    elif 'Verify' in assistant_message:
        helper_function_calls = [assistant_message.split("Helper function: ")[1]]
    else:
        helper_function_calls = [assistant_message.split("Helper function: ")[1]]
    
  
    return helper_function_calls

def verify(answer):
    #print(f"[Final verification]\nThe claim is {answer}")
    return

def score(predict, label):

    print(f"predict:{predict.lower()}, lable:{label.lower()}")
    if 'abstain' in predict.lower():
        score =0
    elif predict.lower() == label.lower():
        score =1
    else:
        score = 0
    print(f"score is :{score}")
    return score

if __name__ == "__main__":
    
    result = {}
    questions_dict = {}
    entity_set_dict = {}
    label_set_dict = {}
    types_dict ={}
    
    with open("/home/smjo/share_code/factkg/data/extracted_dev_set.jsonl") as f:
        for line in f:
            if not line:
                continue
            q = json.loads(line)

            questions_dict[q["question_id"]] = q["question"]
            entity_set_dict[q["question_id"]] = q["entity_set"]
            label_set_dict[q["question_id"]] = q["Label"]
            types_dict[q['question_id']] = q["types"] 
    
    total_score =0
    qid_list = [ 474, 480, 483, 487, 489, 490, 492, 501, 512, 516, 531, 533, 536, 541, 542, 543, 546, 548, 553, 555, 559, 564, 578, 612, 613, 619, 624, 640, 643, 644, 661, 665, 678, 683, 689, 690, 696, 703, 742, 754, 761, 764, 776, 779, 780, 786, 793, 795, 796, 799, 801, 805, 811, 831, 837, 852, 854, 855, 876, 883, 897, 908, 914, 929, 936, 938, 952, 984, 986, 987, 993, 996, 997, 1005, 1016, 1018, 1020, 1026, 1035, 1043, 1063, 1066, 1067, 1068, 1090, 1094, 1097, 1099, 1100, 1116, 1121, 1127, 1134, 1140, 1145, 1151, 1152, 1157, 1158, 1159, 1161, 1163, 1173, 1191, 1193, 1208, 1212, 1233, 1246, 1268, 1273, 1281, 1294, 1295, 1324, 1340, 1360, 1373, 1380, 1390, 1397, 1406, 1416, 1417, 1423, 1427, 1428, 1429, 1438, 1456, 1473, 1484, 1489, 1491, 1502, 1536, 1539, 1541, 1543, 1554, 1557, 1563, 1565]
    #qid_list =  [450, 456, 465, 467, 473]
    for qid in qid_list:
        question = questions_dict[qid]
        label = label_set_dict[qid]
        entities = entity_set_dict[qid]
        
        print(f"\n\n\n\nQuestion :{question}")
        print(f"GT entity:{entities}")
        
        prompt = initial_prompt.replace('<<<Question>>>', question).replace('<<<Entity set>>>', str(entities))
        
        prediction =main(prompt)
        rel_score= score(str(prediction), str(label[0]))
        total_score += rel_score
        
    print(f"reliablility score :{total_score/len(qid_list)}")