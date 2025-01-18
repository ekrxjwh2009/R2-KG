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
import subagent as sa
import prompts_main
import prompts_sub
import models


###################ADD###########################
#1. wrong relation select --> show relation list again
#2. sub agent can refer triple sets and relation lists.
#3. Call function one by one
#4. one claim --> 3 different prompts for main agent (Pr1,2,4)
#5. 3 trial result ensemble



def reasoning(model,claim,initial_prompt, label, f, sub_prompt):
            
    if model =="gpt" : engine="gpt-4o-mini-2024-07-18"
    elif model=='mixtral': engine = "open-mixtral-8x22b"
    
    chatbot = models.OpenAIBot(model, engine)

    iter_limit=15
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
        response = response.replace("[ChatBot]\n",'')
        response = "[ChatBot]\n" + response
        statement = response.split("Statement")[0].split("Helper function")[0]
        functions = response.split("Helper function")[1]
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
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", type=str, default="existence")
    parser.add_argument("--num_iter", type = int, default = "15")
    parser.add_argument("--model", type = str, default= "gpt")
    args = parser.parse_args()
    
    #save_path = f"./result"
    save_path = f"mixtral_result_{args.type}_{args.model}_maxiter_{args.num_iter}_multicalls_temp0"
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    
        
        
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
            

    if args.type == 'existence': qid_list = sample_number.existence
    elif args.type =="num1" : qid_list = sample_number.num1
    elif args.type =='multi_claim' : qid_list = sample_number.multi_claim_v2
    elif args.type =="multi_hop" : qid_list = sample_number.multi_hop
    else:
        print("Wrong argument")
    

    
    
    sub_prompt = prompts_sub.sub_1

    iter_num_list=[]
    total_correct,total_wrong, total_abs =0,0,0
    ensemble_answer_list = [['qid','prediction','gt_label']]
    for qid in qid_list:
        
        print(f"Qid:{qid}")
        question = questions_dict[qid]
        label = label_set_dict[qid]
        entities = entity_set_dict[qid]
        answer_list =[]
        prompts_list = [prompts_main.pr_1, prompts_main.pr_2, prompts_main.pr_4]
        
        for p in range(len(prompts_list)):
            with open(os.path.join(save_path, f"prompt_{p}.txt"), 'a') as f:
 
                
                f.write(f"\n\n\nQid:{qid}\nQuestion :{question}")
                f.write(f"GT entity:{entities}")
                print(f"Trial:{p}")
                print(f"GT entity:{entities}")
                
                main_prompt = prompts_list[p].replace('<<<<CLAIM>>>>', question).replace('<<<<GT_ENTITY>>>', str(entities))
                
                prediction, iter_num = reasoning(args.model,question,main_prompt, label,f, sub_prompt)
                iter_num_list.append(iter_num)
                answer_list.append(prediction)
            
                f.close()
    
                
        #print(f"Answer list:{answer_list}")         
        ###############ensemble
        abs_cnt, co_cnt, wr_cnt =0,0,0
        for pred in answer_list:
            abs, correct, wrong= score(str(pred), str(label[0]))
            abs_cnt += abs
            co_cnt +=correct
            wr_cnt+=wrong
        ensemble_answer_list.append([qid, answer_list, str(label[0])])
        
        if co_cnt == 3:
            total_correct +=1
        elif wr_cnt ==3:
            total_wrong+=1
        else:
            total_abs+=1

            
    
    with open(os.path.join(save_path, f"Metric_score.txt"), 'a') as f:
        if (len(qid_list) - total_abs ) ==0 :
            metric1=0
        else:
            metric1 = (len(qid_list) - total_abs ) /  len(qid_list)
        if total_correct==0:
            metric2 =0
        else :
            metric2 = total_correct/  (len(qid_list) - total_abs)
            
        if (total_correct-total_wrong)==0 :
            metric3 =0
        else:
            metric3 = (total_correct-total_wrong) / (len(qid_list) - total_abs)

        f.write(f"\n\n\nTotal sample:{len(qid_list)}, Total_Correct:{total_correct}, Total_Wrong:{total_wrong}, Total_abstain:{total_abs}\n")
        f.write(f"mrtric1:{metric1}\n mertric2:{metric2}\n metric3:{metric3}")
        f.write(f"avg iter:{np.average(iter_num_list)}\n max_iter:{np.max(iter_num_list)}\n min_iter:{np.min(iter_num_list)}")
        
    f= open(os.path.join(save_path, f"only_result.csv"),'w')
    writer= csv.writer(f)
    writer.writerows(ensemble_answer_list)
    f.close()
     



        
