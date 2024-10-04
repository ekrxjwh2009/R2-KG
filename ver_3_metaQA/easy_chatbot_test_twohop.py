import openai
import sys, os
from openai import OpenAI
import json
import re
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import dbpedia_sparql as db

initial_prompt = """
Your role is to answer the question based on the graph data. 
You must call helper functions to find the sub-graph used as evidence for verification.
If you decide to answer because there's enough evidence, you can answer all possible answers.
I will give you a claim and a set of Given_entities for reference. However, some entities in the claim may not be included in the Given_entities. You can explore the graph and infer entities using helper functions.
When you answer, you must only call helper functions following the format like example. 
Important: You must follow the format when you call helper functions. Do not change the format of the entity or relation, including '~'.

<Helper functions>
1. getRelation(entity) : returns the list of relations linked to the entity. You can choose several relation from the list that looks related to the claim.
2. exploreKG(entity : [relation_1, relation_2,...relation_K]) : returns the triple set around the entity. [entity, relation_1, tail entity], [entity, relation_2, tail entity]..etc.
3. Verify([list os answer]) : If you done verification, we can end the chat.

When you think the evidence art enough to verify the claim, please give me the structure of claim.
Here is the example.

Example 1)
Claim : what are the languages spoken in the movies written by [The Beekeeper] writers?
Given Entity : ['The Beekeeper'] 

[ChatGPT]
getRelation('The Beekeeper')
[Server]
Relation_list('The Beekeeper')=['has_genre', 'in_language', 'written_by', 'directed_by', 'release_year']
[ChatGPT]
exploreKG('The Beekeeper': ['written_by'])
[Server]
["the_beekeeper",'written_by','theodoros_angelopoulos']
[ChatGPT]
getRelation('theodoros_angelopoulos')
[Server]
Relation_list('theodoros_angelopoulos') =['~written_by', '~directed_by']
[ChatGPT]
exploreKG('theodoros_angelopoulos': ['~written_by'])
[Server]
['theodoros_angelopoulos','~written_by','the_suspended_step_of_the_stork'],['theodoros_angelopoulos', '~written_by', 'voyage_to_cythera'],
['theodoros_angelopoulos', '~written_by', 'the_travelling_players'],['theodoros_angelopoulos', '~written_by', 'the_beekeeper'],
['theodoros_angelopoulos', '~written_by', 'the_dust_of_time']
[ChatGPT]
getRelation('the_suspended_step_of_the_stork') ## getRelation('voyage_to_cytheram') ## getRelation('the_dust_of_time')
[Server]
Relation_list('the_suspended_step_of_the_stork') = ['directed_by','release_year','in_language','written_by'], Relation_list('voyage_to_cytheram') =[],
Relation_list('the_travelling_players') = ['has_genre','in_language','written_by',directed_by','release_year'],
Relation_list('the_dust_of_time') = ['has_genre','in_language','written_by','starred_actors','directed_by','release_year']
[ChatGPT]
exploreKG('the_suspended_step_of_the_stork': ['in_language', 'release_year']) ## exploreKG('the_travelling_players': ['in_language']) ## exploreKG('the_dust_of_time': [in_language'])
[Server]
['the_suspended_step_of_the_stork','in_language','greek'], ['the_suspended_step_of_the_stork', 'release_year', '2003'] ,['the_travelling_players','in_language','English'], ['the_dust_of_time', 'has_genre', 'romance'] ,['the_dust_of_time', 'in_language', 'greek']
[ChatGPT]
Verify(['Greek, English'])

Now, it's your turn.
Claim : <<<Question>>>
Given entity: <<<Entity set>>>
Let's start the process. 
"""


openai.api_key = "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"
client = OpenAI(api_key=openai.api_key)

class OpenAIBot:
    def __init__(self,engine, client):
        # Initialize conversation with a system message
        self.conversation = [{"role": "system", "content": "You are a helpful assistant."}]
        self.engine = engine
        self.client = client
    def add_message(self, role, content):
        # Adds a message to the conversation.
        self.conversation.append({"role": role, "content": content})
    def generate_response(self, prompt):
        # Add user prompt to conversation
        self.add_message("user", prompt)

        try:
            # Make a request to the API using the chat-based endpoint with conversation context
            response = self.client.chat.completions.create( model=self.engine, messages=self.conversation, temperature= 0.2)
            # Extract the response
            assistant_response = "[ChatGPT]\n"+response.choices[0].message.content.strip()
            
            # Add assistant response to conversation
            self.add_message("assistant", assistant_response)
            # Return the response
            return assistant_response
        #except:
        #    print('Error Generating Response!')
        except openai.APIError as e:
            #Handle API error here, e.g. retry or log
            print(f"OpenAI API returned an API Error: {e}")
            return f"OpenAI API returned an API Error: {e}"
            
def reasoning(initial_prompt, label, f):
            
    #engine="gpt-3.5-turbo-0125"         
    engine = "gpt-4o"
    chatbot = OpenAIBot(engine, client)

    iter_limit=30

    for i in range(iter_limit):
        # Get Prompt from User
        if i == 0:
            prompt = initial_prompt
        else:
            #prompt = input()
            prompt, result = client_answer(response, label)
            
        f.write(prompt)
        # User can stop the chat by sending 'End Chat' as a Prompt
        if 'Done!!' in prompt:
            break

        # Generate and Print the Response from ChatBot
        response = chatbot.generate_response(prompt)
        f.write(response)
    
    if i==iter_limit-1:
        result = 'Abstain'   
        
    return result
        
        
def client_answer(response, label):
    result = None
    #called multi helper functions
    #if not response.startswith('getRelation', 11) or not response.startswith('exploreKG',11) or not response.startswith('Verify', 11):
    #    prompt = '[Server]\nYou gave wrong format. Call the helper function again follow the right format'
    #    return prompt, result
    if '##' in response:
        helper_ftn_calls = response.split(' ## ')
    #calle on helper function
    else:
        helper_ftn_calls = [response]
    
    for ftn in helper_ftn_calls:
        if 'getRelation' in ftn:
            try :
                entity = ftn.split("getRelation(")[1].split(")")[0][1:-1]
                result = get_relation(entity)
                prompt = f"\n[Server]\nRelation_list({entity}) = {result}"
            except :
                prompt = '\n[Server]\nYou gave wrong format. Call the helper function again follow the right format'
        elif 'exploreKG' in ftn:
            try:
                entity = ftn.split("exploreKG(")[1].split(": ")[0][1:-1]
                relations = ftn.split(": [")[1].split("])")[0].strip().split(', ')
                result = explore_kg(entity, relations)      #entity, string of relation list
                prompt = f"\n[Server]\n{', '.join([str(triple) for triple in result])}"
            except:
                prompt = '\n[Server]\nYou gave wrong format. Call the helper function again follow the right format'
        elif 'Verify' in ftn:
            try:
                result = ftn.split("Verify(")[1].split(")")[0]
                prompt = f"\nDone!!Prediction:{result}, Real label:{label}"
            except:
                prompt = '\n[Server]\nYou gave wrong format. Call the helper function again follow the right format'
        else:
            prompt = '\n[Server]\nYou gave wrong format. Call the helper function again follow the right format'
    return prompt, result
    
def get_relation(entity):
    entity = entity.replace(' ','_').lower()
    relation_list = db.getRelationsFromEntity(entity)
    #print(f"reltaion list of called fucntion:{relation_list}")
    return relation_list

def explore_kg(entity, relations):
    #print(f"entity:{entity}, relations:{relations}")
    entity = entity.replace(' ','_').lower()
    triple_sets= []
    for rel in relations:
        rel = rel[1:-1]
        tails = db.getEntityFromEntRel(entity, rel)
        for tail in tails:
            tmp = [entity,rel,tail]
            triple_sets.append(tmp)
    #print(f'triple sets:{triple_sets}')
    return triple_sets

def score(predict, label,f):
    per_score = len(label)
    abs, correct, wrong =0,0,0
    print(f"predict:{predict}, lable:{label}")
    if 'abstain' in predict.lower():
        abs+=1

    else:
        new_pred_list, new_label_list = [],[]
        predict_list = predict.split(', ')
        for pred in predict_list:
            pred_tmp = re.sub(r"[^a-zA-Z0-9]", "", pred.lower())
            new_pred_list.append(pred_tmp)
        for lab in label:
            lab_tmp = re.sub(r"[^a-zA-Z0-9]", "", lab.lower())
            new_label_list.append(lab_tmp)

        for new_pred in new_pred_list:
            if new_pred in new_label_list:
                correct += 1/per_score
            else:
                wrong += 1/per_score
                    

    return abs, correct, wrong
    
if __name__ == "__main__":
    
    result = {}
    questions_dict = {}
    entity_set_dict = {}
    label_set_dict = {}
    types_dict ={}
    answer_list = []
    
    with open(os.path.expanduser(f"/home/smjo/share_code/metaqa/data/twohop_test_set.jsonl")) as f:
        for line in f:
            if not line:
                continue
            q = json.loads(line)
            questions_dict[q["question_id"]] = q["question"]
            entity_set_dict[q["question_id"]] = q["entity_set"]
            label_set_dict[q["question_id"]] = q["Label"]
    
            
    
    total_correct, total_abs,total_wrong, total_sample =0,0,0,0
    
    with open("/home/smjo/share_code/metaqa/unified/ver_0/result_twohop.txt",'a') as f:
        for qid, question in questions_dict.items():
            if qid > 10000:
                break
            if qid %20 !=0:
                continue
            print(f"Qid:{qid}")
            question = questions_dict[qid]
            label = label_set_dict[qid]
            entities = entity_set_dict[qid]
            
            f.write(f"\n\n\nQid:{qid}\nQuestion :{question}")
            f.write(f"GT entity:{entities}")
            
            prompt = initial_prompt.replace('<<<Question>>>', question).replace('<<<Entity set>>>', str(entities))
            
            prediction = reasoning(prompt, label,f)
            abs, correct, wrong= score(prediction,label,f)
            total_correct += correct
            total_wrong += wrong
            total_abs += abs
            total_sample+=1

 
        if (total_sample - total_abs) ==0 :
            metric1=0
        else:
            metric1 = (total_sample - total_abs ) /  total_sample
        if (total_correct-total_wrong)==0 :
            metric2 =0
        else:
            metric2 = (total_correct-total_wrong) / (total_sample - total_abs)
        f.write("\n\n\ntwohop")
        f.write(f"Total sample:{total_sample}, Total_Correct:{total_correct}, Total_Wrong:{total_wrong}, Total_abstain:{total_abs}")
        f.write(f"mrtric1:{metric1}, mertric2:{metric2}")