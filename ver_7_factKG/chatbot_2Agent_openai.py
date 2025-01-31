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
import dbpedia_sparql as db
import prompts
import subagent as sa
import prompts_main
from difflib import get_close_matches

###################ADD###########################
#1. wrong relation select --> show relation list again
#2. sub agent can refer triple sets and relation lists.
#3. Call function one by one


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
            response = self.client.chat.completions.create( model=self.engine, messages=self.conversation, temperature= 0.95, top_p = 0.95)
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
            
def reasoning(model,subagent,claim,iter_limit,initial_prompt, label, f, sub_prompt,entities):
        # Validate subagent
    valid_subagents = ['gpt-4o', 'gpt-4o-mini']
    if subagent not in valid_subagents:
        raise ValueError(f"Invalid subagent: {subagent}. Must be one of {valid_subagents}.")
    print(f"[DEBUG] reasoning - Received subagent: {subagent}")
    
    
    
    if model == 'gpt-4o-mini': engine = "gpt-4o-mini-2024-07-18"
    elif model == 'gpt-4o' : engine = "gpt-4o-2024-08-06"
    chatbot = OpenAIBot(engine, client)

    
    gold_set =[]
    gold_relations =''
    gold_entities =[]
    for i in range(iter_limit):
        
        # Get Prompt from User
        if i == 0:
            prompt = initial_prompt
            gold_entities += entities
        else:
            #prompt = input()
            
            prompt, result, triples, relations, get_rel_state, new_entites = client_answer(claim,subagent,response, label, gold_set,gold_relations,f, sub_prompt, gold_entities)
            
            if len(triples) > 0:
                gold_set+=triples
            if get_rel_state==1:
                gold_relations += relations
            if len(new_entites)>0:
                gold_entities+=new_entites  
        
        if i>0:    
            f.write(prompt)
            print(prompt)
        # User can stop the chat by sending 'End Chat' as a Prompt
        if 'Done!!' in prompt:
        
            break

        # Generate and Print the Response from ChatBot
        response = chatbot.generate_response(prompt)
        f.write(f"\n************************************Iteration:{i}***********************************")
        f.write("\n"+response)
        print(f"\n************************************Iteration:{i}***********************************")
        print("\n"+response)
    
    if i==iter_limit-1:
        result = 'Abstain'   
        
    return result, i
        
        
def client_answer(claim,subagent,response, label, gold_set,gold_relations,f, sub_prompt, gold_entities):
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
            sub_answer, case, result = verification(subagent,claim,gold_set,gold_relations,f, sub_prompt)
            prompt += "\n" +sub_answer
            
            f.write(f"CASE COUNT:{case}")
            #return prompt, prediction, []
        else:
            prompt += '\nYou gave wrong format. Call the helper function again follow the right format'
            result =''
    
    return prompt, result, triples, relations, get_rel_state, new_entities
    
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
        functions = response.split("Helper function:")[1]
        if '##' in functions:
            helper_ftn_calls = functions.split(' ## ')
        else :
            helper_ftn_calls = [functions]
        prompt ='\n[User]\nExecution result :'
        return helper_ftn_calls, prompt
        
    except:
        #prompt = "\n[User]\nYou gave wrong format of Statement and Helper function."
        print("wrong format of call function")
        
    try : 
        response = response.replace("[Your Task]\n",'')
        functions = response.split("Helper function :")[1]
        if '##' in functions:
            helper_ftn_calls = functions.split(' ## ')
        else :
            helper_ftn_calls = [functions]
        prompt ='\n[User]\nExecution result :'
        
        return helper_ftn_calls, prompt
    
    except:
        print("wrong format of call functions")
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
                

def verification(subagent,claim,gold_set,gold_relations,f, sub_prompt):

    sub_response, case, prediction =sa.feedback(subagent,claim,gold_set,gold_relations,f,sub_prompt)
    return sub_response, case, prediction
    
    
    
    

def score(predict, label,f):
    abs, correct, wrong =0,0,0
    #f.write(f"predict:{predict.lower()}, lable:{label.lower()}")
    print(f"predict:{predict.lower()}, lable:{label.lower()}")
    if 'abstain' in predict.lower():
        abs+=1
    elif predict.lower() == label.lower():
        correct+=1
    else:
        wrong +=1
    #LLM abs개수, correct 개수
    return abs, correct, wrong
    
if __name__ == "__main__":
    
    #python chatbot_1by1_with_sub.py --type multi_hop --subagent 2option_beta --data test --model gpt-4o-mini
    parser = argparse.ArgumentParser()
    parser.add_argument("--percentage", type=int, default=10)
    parser.add_argument("--subagent", type=str, default="gpt-4o")
    parser.add_argument("--model", type = str, default= "gpt-4o-mini")
    args = parser.parse_args()
    
    save_path = f"results_final/2Agent/{args.model}/sub_{args.subagent}"
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
    sub_prompt = prompts.sub_agent_2option_beta
    
    iter_num_list=[]
    iter_limit_list = [15]
    metric_result = [['iterlimit','mtr1','mtr2','mtr3']]
    
    for iter_limit in iter_limit_list:
        print(f'iter limit:{iter_limit}')
        total_correct, total_abs,total_wrong =0,0,0
        answer_list= [['qid','prediction','gt_label']]
        with open(os.path.join(save_path, f"Iter_{iter_limit}.txt"),'a') as f:
        
            for qid in qid_list:
                print(f"Qid:{qid}")
                question = questions_dict[qid]
                label = label_set_dict[qid]
                entities = entity_set_dict[qid]
                
                f.write(f"\n\n\nQid:{qid}\nQuestion :{question}")
                f.write(f"GT entity:{entities}")
                #print(f"GT entity:{entities}")
                
                prompt = prompts_main.pr_1.replace('<<<<CLAIM>>>>', question).replace('<<<<GT_ENTITY>>>', str(entities))

                prediction, iter_num = reasoning(args.model,args.subagent ,question,iter_limit,prompt, label,f, sub_prompt, entities)
                abs, correct, wrong= score(str(prediction), str(label[0]),f)
                total_correct += correct
                total_wrong += wrong
                total_abs += abs
                iter_num_list.append(iter_num)
                answer_list.append([qid, str(prediction), str(label[0])])

            ff = open(os.path.join(save_path, f"{iter_limit}_only_result.csv"),'w')
            writer = csv.writer(ff)
            writer.writerows(answer_list)
            ff.close()
        
