import openai
import sys, os
import ast
from openai import OpenAI
import json
import csv
import argparse
import sample_number
import numpy as np
import re
import prompts
import dbpedia_sparql as db
import subagent as sa
import prompts_main
from difflib import get_close_matches

openai.api_key = "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"
client = OpenAI(api_key=openai.api_key)

class OpenAIBot:
    def __init__(self,engine, client, top_p, temperature):
        # Initialize conversation with a system message
        self.conversation = [{"role": "system", "content": "You are a helpful assistant."}]
        self.engine = engine
        self.client = client
        self.top_p= top_p
        self.temperature = temperature
    def add_message(self, role, content):
        # Adds a message to the conversation.

        self.conversation.append({"role": role, "content": content})
    def generate_response(self, prompt):
        # Add user prompt to conversation
        self.add_message("user", prompt)

        try:
            # Make a request to the API using the chat-based endpoint with conversation context
            response = self.client.chat.completions.create( model=self.engine, messages=self.conversation, temperature= self.temperature, top_p = self.top_p)
            # Extract the response
            #print(response)
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
         
def reasoning(model,subagent ,claim,iter_limit,initial_prompt, label,sub_prompt, entities, top_p, temperature):
            
    if model =='gpt-4o-mini': engine = "gpt-4o-mini-2024-07-18"
    elif model == 'gpt-4o': engine = "gpt-4o-2024-08-06"
    chatbot = OpenAIBot(engine, client, top_p, temperature)
   
    gold_set =[]
    gold_relations =''
    gold_entities =[]
    iter_limit =15
    for i in range(iter_limit):
        
        # Get Prompt from User
        if i == 0:
            prompt = initial_prompt
            gold_entities += entities
        else:
            #prompt = input()
            
            prompt, result, triples, relations, get_rel_state, new_entities = client_answer(claim,subagent,response, label, gold_set,gold_relations, gold_entities)
            
            if len(triples) > 0:
                gold_set+=triples
            if get_rel_state==1:
                gold_relations += relations
            if len(new_entities)>0:
                gold_entities+=new_entities 
        
        #if i>0:    
        #    f.write(prompt)
        # User can stop the chat by sending 'End Chat' as a Prompt
        if 'Done!!' in prompt:
        
            break

        # Generate and Print the Response from ChatBot
        response = chatbot.generate_response(prompt)
        #f.write(f"\n************************************Iteration:{i}***********************************")
        #f.write("\n"+response)
    
    if i==iter_limit-1:
        result = 'Abstain'   
        
    return result, i
        
        
def client_answer(claim,subagent,response, label, gold_set,gold_relations,gold_entities):
    #prompt, result, triples
    result = None
    #called multi helper functions
    #if not response.startswith('getRelation', 11) or not response.startswith('exploreKG',11) or not response.startswith('Verify', 11):
    #    prompt = '[Server]\nYou gave wrong format. Call the helper function again follow the right format'
    #    return prompt, result

    helper_ftn_calls, prompt = split_functions(response)
    triples = []
    new_entities=[]
    relations = ""
    get_rel_state=0
    for helper_str in helper_ftn_calls:
        
        
        if 'getRelation' in helper_str:
    
            get_rel_state, result = getRelations(helper_str,gold_entities)
            prompt +=  "\n" + result
            if get_rel_state==1:
                relations += "\n" + result
                
            #return prompt, result, []
            
            
        elif 'exploreKG' in helper_str:
            result, result_prompt = exploreKGs(helper_str,gold_entities)
            prompt += "\n" + result_prompt
            triples += result
            
            #For matching entities
            new_entities += find_new_entity(triples)
            #return prompt, triples, triples
        
            
        elif 'Verification' in helper_str:
            verify_prompt,case, result = verification(subagent,claim,gold_set,gold_relations, sub_prompt)
            prompt += verify_prompt
            #return prompt, prediction, []
        else:
            prompt += '\nYou gave wrong format. Call the helper function again follow the right format'
            result =''
    
    return prompt, result, triples, relations, get_rel_state , new_entities

def find_new_entity(triples):
    new_entities = []
    for triple_set in triples:
        head, rel, tail = triple_set[0], triple_set[1], triple_set[1]
        if head not in new_entities:
            new_entities.append(head)
        if tail not in new_entities:
            new_entities.append(tail)
    
    return new_entities

def match_and_replace_single(parsed_entity, gold_entities):

    # Find the closest match from gold_entities
    matches = get_close_matches(parsed_entity, gold_entities, n=1, cutoff=0.6)  # Adjust cutoff as needed
    if matches:
        return matches[0]  # Return the closest match
    return parsed_entity  # Return the original if no match is found 

def retrieval_relation_parse_answer(rel):
    
    post_rel = re.sub('[-=+,#/\?:^.@*\"※ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', '', rel)
    return post_rel 

def split_functions(response):
    helper_ftn_calls=[]
    prompt=''
    try:
        response = response.replace("[Your Task]\n",'')
        statement = response.split("Statement")[0].split("Helper function : ")[0]
        functions = response.split("Helper function")[1]
        if '##' in functions:
            helper_ftn_calls = functions.split(' ## ')
        else :
            helper_ftn_calls = [functions]
        prompt ='\n[User]\nExecution result :'
        
    except:
        prompt = "\n[User]\nYou gave wrong format of Statement and Helper function."
        
    return helper_ftn_calls, prompt


def getRelations(helper_str,gold_entities):
    relations = []
    state = 0
    try:
        entity = helper_str.split("getRelation[")[1].split("]")[0].strip()[1:-1]
        #Entity matching
        matched_entity = match_and_replace_single(entity, gold_entities)
        print(f"Before :{entity}, matched:{matched_entity}")
        
        relations += db.getRelationsFromEntity(matched_entity)
        relations += db.getRelationsFromEntity('"' + matched_entity + '"')
        if len(relations) ==0 :
            state=0
            return state,f"Do not change the format of entity {entity} in helper function."
        else:
            state=1
            return state,'Relations_list["' + matched_entity + '"] = ' + str(relations)
    except:
        return state,"You gave wrong format of getRelations() function. Follow the format of examples."


def exploreKGs(helper_str,gold_entities):
    triples= []
    result_prompt = ''
    try: 
        ent = helper_str.split("exploreKG[")[1].split("]=")[0].strip()[1:-1]
        relations = helper_str.split('=[')[1].split(']')[0].strip().split(', ')
        #Entity matching
        matched_entity = match_and_replace_single(ent, gold_entities)
        print(f"Before :{ent}, matched:{matched_entity}")
    
        if len(db.getRelationsFromEntity(matched_entity)) < len(db.getRelationsFromEntity('"' + matched_entity + '"')):
            matched_entity = '"' + matched_entity + '"'
            
        for rel in relations:
            rel = retrieval_relation_parse_answer(rel)
            ###check if the LLM required non-existing relations
            existing_relations = db.getRelationsFromEntity(matched_entity)
            if (rel not in existing_relations) and ('~' + rel) not in existing_relations:
                #result_prompt += f"""The relation you chose '{rel}' does not exist. Choose from the following list. Relations_list["' + {ent} + '"] = ' + {str(existing_relations)}"""
                result_prompt += f"'The relation you chose '{rel}' does not exist.Choose from the following list."
                result_prompt += 'Relations_list["' + matched_entity + '"] = ' + str(existing_relations)
            
            
            tails = []
            if rel[0] == '~':
                tails += db.getEntityFromEntRel(matched_entity, rel)
                tails += db.getEntityFromEntRel(matched_entity, rel.split('~')[1])
            else:
                tails += db.getEntityFromEntRel(matched_entity, rel)
                tails += db.getEntityFromEntRel(matched_entity, '~' + rel)
            
            for tail in tails:
                triples.append([matched_entity, rel, tail])
        
        if len(triples) >= 50:
            triples = triples[:50]
        
        if len(triples)==0:
            result_prompt += f"Choose other relations based refer to the Relations_list Or follow the format of Entity {ent} and Relations"
        
        else:
            result_prompt += ', '.join(str(sublist) for sublist in triples)
        
    except:
        result_prompt += "You gave wrong format of exploreKGs() function. Follow the format of examples."

    
    return triples, result_prompt



def verification(subagent,claim,gold_set,gold_relations,sub_prompt):

    sub_response, case, prediction =sa.feedback(subagent,claim,gold_set,gold_relations,sub_prompt)
    return sub_response, case, prediction
    
    
    
    

def score(predict, label):
    abs, correct, wrong =0,0,0
    #f.write(f"predict:{predict.lower()}, lable:{label.lower()}")
    print(f"Scoring!!!!!!predict:{predict.lower()}, label:{label.lower()}")
    if 'abstain' in predict.lower():
        abs+=1
    elif predict.lower() == label.lower():
        correct+=1
    else:
        wrong +=1
    #LLM abs개수, correct 개수
    return abs, correct, wrong
    
if __name__ == "__main__":
    
    #python chatbot_oneAgent.py --type existence --num_iter 15 --model gpt-3.5 --data test

    parser = argparse.ArgumentParser()
    parser.add_argument("--percentage", type=int, default=10)
    parser.add_argument("--model", type = str, default= "gpt-4o-mini")
    parser.add_argument("--subagent", type=str, default="gpt-4o")
    args = parser.parse_args()
    
    save_path = f"results_final/2Agent+Parameter_ensemble/{args.model}/"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    result = {}
    questions_dict = {}
    entity_set_dict = {}
    label_set_dict = {}
    types_dict ={}
    
    f= open("/nfs_edlab/smjo/share_code/factkg/data/extracted_test_set.jsonl")

    for line in f:
        if not line:
            continue
        q = json.loads(line)

        questions_dict[q["question_id"]] = q["question"]
        entity_set_dict[q["question_id"]] = q["entity_set"]
        label_set_dict[q["question_id"]] = q["Label"]
        types_dict[q['question_id']] = q["types"] 
    f.close()

    if args.percentage == 10 : qid_list = sample_number.percentage_10
    elif args.percentage == 20 : qid_list = sample_number.percentagee_20
    prompt = prompts_main.pr_1
    sub_prompt = prompts.sub_agent_2option_beta
    parameter_list ={"top_p":[0.3, 0.7, 0.95], "temp":[0.5, 1.0, 1.5]}

    iter_num_list=[]
    total_correct,total_wrong, total_abs =0,0,0
    ensemble_answer_list = [['qid','prediction','gt_label']]
    
    iter_limit = 15
    for combi in range(3):
        if combi ==0: continue
        top_p = parameter_list["top_p"][combi]
        temp = parameter_list["temp"][combi]
        if combi==1 or combi==2:
            qid_list = qid_list[:623]
        for qid in qid_list:
        
            print(f"Qid:{qid}")
            question = questions_dict[qid]
            label = label_set_dict[qid]
            entities = entity_set_dict[qid]
            answer_list =[]

            main_prompt = prompt.replace('<<<<CLAIM>>>>', question).replace('<<<<GT_ENTITY>>>', str(entities))
            #reasoning(model,claim,initial_prompt, label,entities, f)
            prediction, iter_num = reasoning(args.model,args.subagent ,question,iter_limit,prompt, label,sub_prompt, entities, top_p, temp)
            iter_num_list.append(iter_num)
            answer_list.append(prediction)
                
            ensemble_answer_list = [qid, answer_list, str(label[0])]
            ff= open(os.path.join(save_path, f"only_result_top_p_{top_p}_temp_{temp}.csv"),'a')
            writer= csv.writer(ff)
            writer.writerow(ensemble_answer_list)
            ff.close()



    
     



        
