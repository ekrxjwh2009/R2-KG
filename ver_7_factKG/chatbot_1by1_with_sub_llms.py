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
from models import LLMBot

###################ADD###########################
#1. wrong relation select --> show relation list again
#2. sub agent can refer triple sets and relation lists.
#3. Call function one by one

            
def reasoning(model,claim,iter_limit,initial_prompt, label, f, sub_prompt):
            
    chatbot = LLMBot(model, temperature=0.95, top_p=0.95, max_tokens=2000)

    
    gold_set =[]
    gold_relations =''
    for i in range(iter_limit):
        
        # Get Prompt from User
        if i == 0:
            prompt = initial_prompt
        else:
            #prompt = input()
            
            prompt, result, triples, relations, get_rel_state = client_answer(claim,response, label, gold_set,gold_relations,f, sub_prompt)
            
            if len(triples) > 0:
                gold_set+=triples
            if get_rel_state==1:
                gold_relations += relations
        
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
        
        
def client_answer(claim,response, label, gold_set,gold_relations,f, sub_prompt):
    #prompt, result, triples
    result = None
    #called multi helper functions
    #if not response.startswith('getRelation', 11) or not response.startswith('exploreKG',11) or not response.startswith('Verify', 11):
    #    prompt = '[Server]\nYou gave wrong format. Call the helper function again follow the right format'
    #    return prompt, result

    helper_ftn_calls, prompt = split_functions(response)
    triples = []
    relations = ""
    get_rel_state=0
    for helper_str in helper_ftn_calls:
        
        
        if 'getRelation' in helper_str:
    
            get_rel_state, result = getRelations(helper_str)
            prompt +=  "\n" + result
            if get_rel_state==1:
                relations += "\n" + result
            #return prompt, result, []
            
            
        elif 'exploreKG' in helper_str:
            result, result_prompt = exploreKGs(helper_str)
            prompt += "\n" + result_prompt
            triples += result
            #return prompt, triples, triples
        
            
        elif 'Verification' in helper_str:
            sub_answer, case, result = verification(claim,gold_set,gold_relations,f, sub_prompt)
            prompt += "\n" +sub_answer
            
            f.write(f"CASE COUNT:{case}")
            #return prompt, prediction, []
        else:
            prompt += '\nYou gave wrong format. Call the helper function again follow the right format'
            result =''
    
    return prompt, result, triples, relations, get_rel_state
    

def retrieval_relation_parse_answer(rel):
    
    post_rel = re.sub('[-=+,#/\?:^.@*\"※ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', '', rel)
    return post_rel 

def split_functions(response):
    helper_ftn_calls=[]
    prompt=''
    try:
        response = response.replace("[Your Task]\n",'')
        statement = response.split("Statement : ")[0].split("Helper function : ")[0]
        functions = response.split("Helper function : ")[1]
        if '##' in functions:
            helper_ftn_calls = functions.split(' ## ')
        else :
            helper_ftn_calls = [functions]
        prompt ='\n[User]\nExecution result :'
        
    except:
        prompt = "\n[User]\nYou gave wrong format of Statement and Helper function."
        
    return helper_ftn_calls, prompt


def getRelations(helper_str):
    relations = []
    state = 0
    try:
        entity = helper_str.split("getRelation[")[1].split("]")[0].strip()[1:-1]
        relations += db.getRelationsFromEntity(entity)
        relations += db.getRelationsFromEntity('"' + entity + '"')
        if len(relations) ==0 :
            state=0
            return state,f"Do not change the format of entity {entity} in helper function."
        else:
            state=1
            return state,'Relations_list["' + entity + '"] = ' + str(relations)
    except:
        return state,"You gave wrong format of getRelations() function. Follow the format of examples."


def exploreKGs(helper_str):
    triples= []
    result_prompt = ''
    try: 
        ent = helper_str.split("exploreKG[")[1].split("]=")[0].strip()[1:-1]
        relations = helper_str.split('=[')[1].split(']')[0].strip().split(', ')
    
        if len(db.getRelationsFromEntity(ent)) < len(db.getRelationsFromEntity('"' + ent + '"')):
            ent = '"' + ent + '"'
            
        for rel in relations:
            rel = retrieval_relation_parse_answer(rel)
            ###check if the LLM required non-existing relations
            existing_relations = db.getRelationsFromEntity(ent)
            if (rel not in existing_relations) and ('~' + rel) not in existing_relations:
                #result_prompt += f"""The relation you chose '{rel}' does not exist. Choose from the following list. Relations_list["' + {ent} + '"] = ' + {str(existing_relations)}"""
                result_prompt += f"'The relation you chose '{rel}' does not exist.Choose from the following list."
                result_prompt += 'Relations_list["' + ent + '"] = ' + str(existing_relations)
            
            
            tails = []
            if rel[0] == '~':
                tails += db.getEntityFromEntRel(ent, rel)
                tails += db.getEntityFromEntRel(ent, rel.split('~')[1])
            else:
                tails += db.getEntityFromEntRel(ent, rel)
                tails += db.getEntityFromEntRel(ent, '~' + rel)
            
            for tail in tails:
                triples.append([ent, rel, tail])
                
        if len(triples)==0:
            result_prompt += f"Choose other relations based refer to the Relations_list Or follow the format of Entity {ent} and Relations"
        
        else:
            result_prompt += ', '.join(str(sublist) for sublist in triples)
        
    except:
        result_prompt += "You gave wrong format of exploreKGs() function. Follow the format of examples."


    return triples, result_prompt
                

def verification(claim,gold_set,gold_relations,f, sub_prompt):
    
    sub_response, case, prediction =sa.feedback(claim,gold_set,gold_relations,f,sub_prompt)
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
    
    #python chatbot_1by1_with_sub_llms.py --type num1 --subagent 2option_beta --data test --model mistral-small
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", type=str, default="existence")
    #parser.add_argument("--subagent", type=str, default="2option_beta")
    parser.add_argument("--data", type =str, default="test")
    parser.add_argument("--model", type = str, default= "mistral-small")
    args = parser.parse_args()
    
    save_path = f"./results_{args.data}/{args.model}/sub_4omini"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    result = {}
    questions_dict = {}
    entity_set_dict = {}
    label_set_dict = {}
    types_dict ={}
    
    if args.data =='dev':
        f= open("/nfs_edlab/smjo/share_code/factkg/data/extracted_train_set.jsonl")
    elif args.data =='test':
        f= open("/nfs_edlab/smjo/share_code/factkg/data/extracted_test_set.jsonl")
    else : 
        print('Wrong argument')
    for line in f:
        if not line:
            continue
        q = json.loads(line)

        questions_dict[q["question_id"]] = q["question"]
        entity_set_dict[q["question_id"]] = q["entity_set"]
        label_set_dict[q["question_id"]] = q["Label"]
        types_dict[q['question_id']] = q["types"] 
    f.close()
            

    if args.type == 'existence': qid_list = sample_number.existence
    elif args.type =="num1" : qid_list = sample_number.num1
    elif args.type =='multi_claim' : qid_list = sample_number.multi_claim
    elif args.type =="multi_hop" : qid_list = sample_number.multi_hop
    else:
        print("Wrong argument")
    
    sub_prompt = prompts.sub_agent_2option_beta
    iter_num_list=[]
    iter_limit_list = [15]

    
    for iter_limit in iter_limit_list:
        print(f'iter limit:{iter_limit}')
        total_correct, total_abs,total_wrong =0,0,0
        answer_list= [['qid','prediction','gt_label']]
        with open(os.path.join(save_path, f"Iter_{iter_limit}_{args.type}.txt"),'a') as f:
        
            for qid in qid_list:
                print(f"Qid:{qid}")
                question = questions_dict[qid]
                label = label_set_dict[qid]
                entities = entity_set_dict[qid]
                
                f.write(f"\n\n\nQid:{qid}\nQuestion :{question}")
                f.write(f"GT entity:{entities}")
                #print(f"GT entity:{entities}")
                
                prompt = prompts_main.pr_1.replace('<<<<CLAIM>>>>', question).replace('<<<<GT_ENTITY>>>', str(entities))

                prediction, iter_num = reasoning(args.model, question,iter_limit,prompt, label,f, sub_prompt)
                abs, correct, wrong= score(str(prediction), str(label[0]),f)
                total_correct += correct
                total_wrong += wrong
                total_abs += abs
                iter_num_list.append(iter_num)
                answer_list.append([qid, str(prediction), str(label[0])])



            ff = open(os.path.join(save_path, f"{iter_limit}_only_result_{args.type}.csv"),'w')
            writer = csv.writer(ff)
            writer.writerows(answer_list)
            ff.close()
        
        


    