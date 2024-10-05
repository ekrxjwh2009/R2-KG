import openai
import sys, os
from openai import OpenAI
import json
import csv
import argparse
import re
import dbpedia_sparql as db
import numpy as np

initial_prompt = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use below helper functions to find the evidence for finding labels.

<Helper functions>
1. getRelation(entity): Returns the list of relations connected to the entities.
2. exploreKG(entity) = [list of relations]: Returns the corresponding tail entities in graph data starts from single entity in given entity and given relation.
3. Verification([list of entities]): After getting enough evidence after exploreKG() helper function and if verification can be done, call this function with labels.

You must follow the exact format of the given helper function.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for my response. If response has made, continue your 'Statement and Helper function' task.
Importantly, you have to use inverse relation if you need. For example, if you want to find films starred by certain actors (when only actors were given), you have to use 'starred_actors' relation.

Here are some examples.

Example 1)
Claim: what genres do the films that share actors with [Man of Steel] fall under?
Given Entity: ['Man of Steel']

[ChatGPT]
Statement : I need the relations linked with the given entity.
Helper function : getRelation('Man of Steel')
[User]
Execution result : Relation_list('Man of Steel') = ['release_year', 'starred_actors', 'written_by', 'has_tags', 'directed_by']
[ChatGPT]
Statement : First, to solve the claim, I have to know the actors starred in ‘Man of Steel’.
Helper function : exploreKG('Man of Steel')=['starred_actors']
[User]
Execution result : ['Man of Steel', 'starred_actors', 'michael_shannon'], ['Man of Steel', 'starred_actors', 'henry_cavill'], ['Man of Steel', 'starred_actors', 'amy_adams'], ['Man of Steel', 'starred_actors', 'diane_lane']
[ChatGPT]
Statement : Next, I need films starred by previous given actors. To find the films, I need relations linked with the actors.
Helper function : getRelation('michael_shannon') ## getRelation('henry_cavill') ## getRelation('amy_adams') ## getRelation('diane_lane')
[User]
Execution result : Relation_list('michael_shannon') = ['has_tags', 'starred_actors'], Relation_list('henry_cavill') = ['starred_actors'], Relation_list('amy_adams') = ['has_tags', 'starred_actors'], getRelations('diane_lane') = ['has_tags', 'starred_actors']
[ChatGPT]
Statement : To get the films starred by previous actors, I need to explore the graph with each actors and related relations.
Helper function : exploreKG('michael_shannon')=['starred_actors'] ## exploreKG('henry_cavill')=['starred_actors'] ## exploreKG('amy_adams')=['starred_actors'] ## exploreKG('diane_lane')=['starred_actors']
[User]
Execution result : ['michael_shannon', 'starred_actors', 'bug'], ['michael_shannon', 'starred_actors', 'machine_gun_preacher'], ['michael_shannon', 'starred_actors', 'young_ones'], ['michael_shannon', 'starred_actors', 'the_missing_person'], ['henry_cavill', 'starred_actors', 'immortals'], ['henry_cavill', 'starred_actors', 'blood_creek'], ['henry_cavill', 'starred_actors', 'the_cold_light_of_day'], ['amy_adams', 'starred_actors', 'moonlight_serenade'], ['amy_adams', 'starred_actors', 'american_hustle'], ['amy_adams', 'starred_actors', 'sunshine_cleaning'], ['amy_adams', 'starred_actors', 'the_fighter'], ['diane_lane', 'starred_actors', 'wild_bill'], ['diane_lane', 'starred_actors', 'the_glass_house'], ['diane_lane', 'starred_actors', 'jumper']
[ChatGPT]
Statement : To get the genres of the these films, I need to find the relations linked with all the films from previous step.
Helper function : getRelation('bug') ## getRelation('machine_gun_preacher') ## getRelation('young_ones') ## getRelation('the_missing_person') ## getRelation('immortals') ## getRelation('blood_creek') ## getRelation('the_cold_light_of_day') ## getRelation('moonlight_serenade') ## getRelation('american_hustle') ## getRelation('sunshine_cleaning') ## getRelation('the_fighter') ## getRelation('wild_bill') ## getRelation('the_glass_house') ## getRelation('jumper')
[User]
Execution result : Relation_list('bug') = ['starred_actors', 'has_tags', 'written_by', 'release_year', 'has_genre', 'directed_by'], Relation_list('machine_gun_preacher') = ['starred_actors', 'has_tags', 'written_by', 'release_year', 'has_genre', 'directed_by'], Relation_list('young_ones') = ['starred_actors', 'has_genre', 'release_year'], Relation_list('the_missing_person') = ['starred_actors', 'written_by', 'release_year', 'has_genre'], Relation_list('immortals') = 'starred_actors', 'has_tags', 'release_year', 'has_genre', 'in_language'], Relation_list('blood_creek') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('the_cold_light_of_day') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('moonlight_serenade') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('american_hustle') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('sunshine_cleaning') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('the_fighter') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('wild_bill') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('the_glass_house') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('jumper') = ['starred_actors', 'has_tags', 'release_year', 'directed_by']
[ChatGPT]
Statement : To get the genres of the films, I need to explore the graph with each films and related relations.
Helper function : exploreKG('bug')=['has_genre'] ## exploreKG('machine_gun_preacher')=['has_genre'] ## exploreKG('young_ones')=['has_genre'] ## exploreKG('the_missing_person')=['has_genre'] ## exploreKG('immortals')=['has_genre'] ## exploreKG('blood_creek')=['has_genre'] ## exploreKG('the_cold_light_of_day')=['has_genre'] ## exploreKG('moonlight_serenade')=['has_genre'] ## exploreKG('american_hustle')=['has_genre'] ## exploreKG('sunshine_cleaning')=['has_genre'] ## exploreKG('the_fighter')=['has_genre'] ## exploreKG('wild_bill')=['has_genre'] ## exploreKG('the_glass_house')=['has_genre'] ## exploreKG('jumper')=[]
[User]
Execution result : ['bug', 'has_genre', 'horror'], ['machine_gun_preacher', 'has_genre', 'action'], ['young_ones', 'has_genre', 'action'], ['the_missing_person', 'has_genre', 'mystery'], ['the_missing_person', 'has_genre', 'drama'], ['the_missing_person', 'has_genre', 'comedy'], ['immortals', 'has_genre', 'fantasy'], ['blood_creek', 'has_genre', 'horror'], ['the_cold_light_of_day', 'has_genre', 'action'], ['moonlight_serenade', 'has_genre', 'romance'], ['moonlight_serenade', 'has_genre', 'drama'], ['moonlight_serenade', 'has_genre', 'musical'], ['american_hustle', 'has_genre', 'crime'], ['american_hustle', 'has_genre', 'drama'], ['sunshine_cleaning', 'has_genre', 'drama'], ['sunshine_cleaning', 'has_genre', 'comedy'], ['the_fighter', 'has_genre', 'drama'], ['the_fighter', 'has_genre', 'sport'], ['wild_bill', 'has_genre', 'western'], ['the_glass_house', 'has_genre', 'thriller']
[ChatGPT]
Statement : Now I get the genres of the films that share actors with 'Man of Steel'. The answer of the claim is as follows.
['horror', 'action', 'mystery', 'drama', 'comedy', 'fantasy', 'romance', 'musical', 'crime', 'sport', 'western', 'thriller']
Helper function : Verification(['horror', 'action', 'mystery', 'drama', 'comedy', 'fantasy', 'romance', 'musical', 'crime', 'sport', 'western', 'thriller'])


Example 2)
Claim: who are the actors in the films written by [John Travis]?
Given entity: ["John Travis"]

Statement : I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function : getRelation('John Travis')
[User]
Execution result : Relation_list('John Travis') = ['written_by']
[ChatGPT]
Statement : Now, to find the films that 'John Travis' written, I need to explore the graph from 'John Travis' with related relations.
Helper function : exploreKG('John Travis')=['written_by']
[User]
Execution result : ['John Travis', 'written_by', 'the_haunting_of_molly_hartley']
[ChatGPT]
Statement : Now, we have to find the actors in the previous given film.
Helper function : getRelation('the_haunting_of_molly_hartley')
[User]
Execution result : Relation_list('the_haunting_of_molly_hartley') = ['has_genre', 'starred_actors', 'directed_by', 'release_year', 'written_by']
[ChatGPT]
Statement : To get the actors in the film, I need to explore the graph with the film and related relations.
Helper function : exploreKG('the_haunting_of_molly_hartley')=['starred_actors']
[User]
Execution result : ['the_haunting_of_molly_hartley', 'starred_actors', 'haley_bennett'], ['the_haunting_of_molly_hartley', 'starred_actors', 'chace_crawford'], ['the_haunting_of_molly_hartley', 'starred_actors', 'jake_weber']
[ChatGPT]
Statement : Now I get the actors of the films written by 'John Travis'. The answer of the claim is as follows.
['haley_bennett', 'chace_crawford', 'jake_weber']
Helper function : Verification(['haley_bennett', 'chace_crawford', 'jake_weber'])

Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>
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
            assistant_response = response.choices[0].message.content.strip()
            
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
    engine = "gpt-4o-mini-2024-07-18"
    chatbot = OpenAIBot(engine, client)

    iter_limit=15

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
        f.write(f"\n************************************Iteration:{i}***********************************")
        f.write("\n"+response)
    
    if i==iter_limit-1:
        result = 'Abstain'   
        
    return result, i
        
        
def client_answer(response, label):
    result = None
    #called multi helper functions
    #if not response.startswith('getRelation', 11) or not response.startswith('exploreKG',11) or not response.startswith('Verify', 11):
    #    prompt = '[Server]\nYou gave wrong format. Call the helper function again follow the right format'
    #    return prompt, result
    helper_ftn_calls = split_functions(response)
    prompt = '\n[User]\nExecution result : '
    
    for ftn in helper_ftn_calls:
        if 'getRelation' in ftn:
            try :
                entity = ftn.split("getRelation(")[1].split(")")[0][1:-1]
                result = get_relation(entity)
                if len(result)==0:
                    prompt+= "\nDo not change the format of entity in helper function."
                else:
                    prompt += f"\nRelation_list({entity}) = {result}"
            except :
                prompt += '\nYou gave wrong format. Call the helper function again follow the right format'
        elif 'exploreKG' in ftn:
            try:
                entity = ftn.split("exploreKG(")[1].split(")=")[0][1:-1]
                relations = ftn.split("=[")[1].split("]")[0].strip().split(', ')
                result = explore_kg(entity, relations)      #entity, string of relation list
                if len(result) ==0 :
                    prompt += "\nChoose another relations Or follow the format of Entity and Relations"
                else:
                    prompt += f"\n{', '.join([str(triple) for triple in result])}"
            except:
                prompt = '\nYou gave wrong format. Call the helper function again follow the right format'
        elif 'Verification' in ftn:
            try:
                result = ftn.split("Verification(")[1].split(")")[0][1:-1]
                prompt += f"\nDone!!Prediction:{result}\nReal label:{label}"
            except:
                prompt += '\nYou gave wrong format. Call the helper function again follow the right format'
        else:
            prompt += '\nYou gave wrong format. Call the helper function again follow the right format'
    return prompt, result


def split_functions(response):
    helper_ftn_calls=[]
    response = response.replace("[ChatGPT]\n",'')
    statement = response.split("Statement : ")[0].split("Helper function : ")[0]
    functions = response.split("Helper function : ")[1]
    if '##' in functions:
        helper_ftn_calls = functions.split(' ## ')
    else :
        helper_ftn_calls = [functions]
    return helper_ftn_calls

def preprocess_ent(ent):
    if (ent[0]=='"' and ent[-1]=='"') or (ent[0]=="'" and ent[-1]=="'"):
        return ent[1:-1].replace(' ', '_').lower()
    else:
        return ent.replace(' ', '_').lower()

def get_relation(entity):
    #print(f"befor enetity:{entity}")
    entity = preprocess_ent(entity)
    #print(f"after entity:{entity}")
    relation_list = db.getRelationsFromEntity(entity)
    #print(f"reltaion list of called fucntion:{relation_list}")
    return relation_list

def explore_kg(entity, relations):
    #print(f"entity:{entity}, relations:{relations}")
    entity = preprocess_ent(entity)
    triple_sets= []
    for rel in relations:
        rel = rel[1:-1]
        #print(f"looking entity:{entity}, relation:{rel}")
        tails = db.getEntityFromEntRel(entity, rel)
        for tail in tails:
            tmp = [entity,rel,tail]
            triple_sets.append(tmp)
    #print(f'triple sets:{triple_sets}')
    return triple_sets

def score(predict, label,f):
    per_score = len(label)
    abs, correct, wrong =0,0,0
    print(f"predict:{predict}\nlabel:{label}")
    if 'abstain' in str(predict).lower():
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
                correct = 1/per_score
            else:
                wrong += 1/per_score
                    
    
    return abs, correct, wrong
    
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("type", type=str, default="one_hop")
    args = parser.parse_args()
    
    
    save_path = f"./with_reasoning_result"
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    
    if args.type=='one_hop':
        file_pth = "/home/smjo/share_code/metaqa/data/onehop_test_set.jsonl"
    elif args.type =='two_hop':
        file_pth = "/home/smjo/share_code/metaqa/data/twohop_test_set.jsonl"
    elif args.type == 'three_hop':
        file_pth = "/home/smjo/share_code/metaqa/data/threehop_test_set.jsonl"
    else:
        print("wrong argument")
    
    result = {}
    questions_dict = {}
    entity_set_dict = {}
    label_set_dict = {}
    types_dict ={}
    answer_list = []
    
    with open(os.path.expanduser(file_pth)) as f:
        for line in f:
            if not line:
                continue
            q = json.loads(line)
            questions_dict[q["question_id"]] = q["question"]
            entity_set_dict[q["question_id"]] = q["entity_set"]
            label_set_dict[q["question_id"]] = q["Label"]
    
            
    iter_num_list=[]
    total_correct, total_abs,total_wrong, total_sample =0,0,0,0
    answer_list= [['qid','correct','wrong','prediction','gt_label']]
    with open(os.path.join(save_path,f"{args.type}.txt"),'a') as f:
        for qid, question in questions_dict.items():
            if qid >2000:
                break
            if qid%20 !=0:
                continue
            print(f"Qid:{qid}")
            question = questions_dict[qid]
            label = label_set_dict[qid]
            entities = entity_set_dict[qid]
            
            f.write(f"\n\n\nQid:{qid}\nQuestion :{question}")
            f.write(f"GT entity:{entities}")
            
            prompt = initial_prompt.replace('<<<<CLAIM>>>>', question).replace('<<<<GT_ENTITY>>>>', str(entities))
            
            prediction, iter_num = reasoning(prompt, label,f)
            abs, correct, wrong= score(prediction,label,f)
            total_correct += correct
            total_wrong += wrong
            total_abs += abs
            total_sample +=1
            iter_num_list.append(iter_num)
            answer_list.append([qid,correct,wrong,str(prediction), str(label)])
        
        if (total_sample - total_abs) ==0 :
            metric1=0
        else:
            metric1 = (total_sample - total_abs ) /  total_sample
        if total_correct==0:
            metric2 =0
        else:
            metric2 = total_correct / (total_sample - total_abs)
        if (total_correct-total_wrong)==0 :
            metric3 =0
        else:
            metric3 = (total_correct-total_wrong) / (total_sample - total_abs)

        f.write(f"\n\n\nTotal sample:{total_sample}, Total_Correct:{total_correct}, Total_Wrong:{total_wrong}, Total_abstain:{total_abs}")
        f.write(f"metric1:{metric1}, metric2:{metric2}, metric3 :{metric3}")
        f.write(f"avg iter:{np.average(iter_num_list)}\n max_iter:{np.max(iter_num_list)}\n min_iter:{np.min(iter_num_list)}")
        
    f= open(f"./with_reasoning_result/only_answer_{args.type}.csv",'w')
    writer= csv.writer(f)
    writer.writerows(answer_list)
    f.close()