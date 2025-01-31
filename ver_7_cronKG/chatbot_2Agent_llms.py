import openai
import sys, os
from openai import OpenAI
import json
import csv
import argparse
import numpy as np
from collections import defaultdict
import pickle
import re
import prompt_main
import prompt_sub
import subagent as sa
from models import LLMBot
from collections import defaultdict
from difflib import get_close_matches

            
def reasoning(model,subagent,claim,iter_limit,initial_prompt, label, sub_prompt ,KG, entities):
            
    chatbot = LLMBot(model, temperature=0.95, top_p=0.95, max_tokens=2000)
   
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
            
            prompt, result, triples, relations, get_rel_state, new_entites = client_answer(claim,subagent,response, label, gold_set,gold_relations,sub_prompt, KG, gold_entities)
            
            if len(triples) > 0:
                gold_set+=triples
            if get_rel_state==1:
                gold_relations += relations
            if len(new_entites)>0:
                gold_entities+=new_entites 
        
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
    
def client_answer(claim,subagent,response, label, gold_set,gold_relations,sub_prompt, KG, gold_entities):
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
    
            get_rel_state, result = getRelations(helper_str, KG, gold_entities)
            prompt +=  "\n" + result
            if get_rel_state==1:
                relations += "\n" + result
            #return prompt, result, []
            
            
        elif 'exploreKG' in helper_str:
            result, result_prompt = exploreKGs(helper_str, KG, gold_entities)
            prompt += "\n" + result_prompt
            triples += result
            
            #For matching entities
            new_entities += find_new_entity(triples)
            #return prompt, triples, triples
        
            
        elif 'Verification' in helper_str:
            sub_answer, case, result = verification(subagent,claim,gold_set,gold_relations,sub_prompt)
            prompt += "\n" +sub_answer
            
            #f.write(f"CASE COUNT:{case}")
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



def getRelations(helper_str, KG, gold_entities): 
    
    relations = []
    state=0
    try:
        entity = helper_str.split("getRelation[")[1].split("]")[0].strip()[1:-1]
        #Entity matching
        matched_entity = match_and_replace_single(entity, gold_entities)
        print(f"Before :{entity}, matched:{matched_entity}")
        
        subgraphs = KG[matched_entity]
        for graph in subgraphs:
            rel = graph[1]
            if rel not in relations:
                relations.append(rel)
        if len(relations) ==0:
            state=0
            return state,f"Do not change the format of entity {entity} in helper function."
            
        else:
            state=1
            return state,'Relations_list["' + matched_entity + '"] = ' + str(relations)
    
    except:
        return state,"You gave wrong format of getRelations() function. Follow the format of examples."
    


def exploreKGs(helper_str, KG, gold_entities):

    triples=[]
    result_prompt = ''
    try: 
        entity = helper_str.split("exploreKG[")[1].split("]=")[0].strip()[1:-1]
        relations = helper_str.split('=[')[1].split(']')[0].strip().split(', ')
        #Entity matching
        matched_entity = match_and_replace_single(entity, gold_entities)
        print(f"Before :{entity}, matched:{matched_entity}")

        subgraphs = KG[matched_entity]
        existing_relations = []
        for graph in subgraphs:
            exist_rel = graph[1]
            if exist_rel not in existing_relations:
                existing_relations.append(exist_rel) 
        
        for rel in relations:
            rel = rel[1:-1]
            print(f"Relation :{rel}")
            if (rel not in existing_relations) and ('~' + rel) not in existing_relations:
                result_prompt += f"'The relation you chose '{rel}' does not exist.Choose from the following list."
                result_prompt += 'Relations_list["' + matched_entity + '"] = ' + str(existing_relations)
            
            for sub_graph in KG[matched_entity]:
                if rel == sub_graph[1]:
                    triples.append(sub_graph)
        
        if len(triples) >= 50:
            triples = triples[:50]
        if len(triples)==0:
            result_prompt += f"Choose other relations based refer to the Relations_list Or follow the format of Entity {entity} and Relations"
        
        else:
            result_prompt += ', '.join(str(sublist) for sublist in triples)
    except : 
        result_prompt += "You gave wrong format of exploreKGs() function. Follow the format of examples."

    

    return triples, result_prompt


def verification(subagent,claim,gold_set,gold_relations,sub_prompt):
    sub_response, case, prediction =sa.feedback(subagent,claim,gold_set,gold_relations,sub_prompt)
    return sub_response, case, prediction

def score(predict, label,f):
    per_score = len(label)
    abs, correct, wrong =0,0,0
    
    if 'abstain' in str(predict).lower():
        abs+=1

    else:
        new_pred_list, new_label_list = [],[]
        predict_list = predict.strip().split(',')
        for pred in predict_list:
            pred_tmp = re.sub(r"[^a-zA-Z0-9]", "", pred.lower())
            pred_tmp = pred_tmp.strip()
            new_pred_list.append(pred_tmp)
        for lab in label:
            if type(lab)==int:
                lab_tmp = f'{lab}'
                new_label_list.append(lab_tmp)
                continue
            else:
                lab_tmp = re.sub(r"[^a-zA-Z0-9]", "", lab.lower())
                lab_tmp = lab_tmp.strip()
                new_label_list.append(lab_tmp)

        print(f"predict:{new_pred_list}\nlabel:{new_label_list}")
        for new_pred in new_pred_list:
            if new_pred in new_label_list:
                correct += 1/per_score
            else:
                wrong += 1/per_score
                    
    
    return abs, correct, wrong

def make_data():
    print("Making dataset")
    gt_pth = "/nfs_edlab/smjo/KG-gpt2/wikidata_big"
    split = 'test'
    filename = os.path.join(gt_pth, 'questions/{split}.pickle'.format(split=split) )
    questions = pickle.load(open(filename, 'rb'))
    
    KG_pth = os.path.join(gt_pth, 'kg/full.txt')
    entid_2_txt_pth = os.path.join(gt_pth, 'kg/wd_id2entity_text.txt')
    relid_2_txt_pth = os.path.join(gt_pth, 'kg/wd_id2relation_text.txt')
    kg_dataset = open(KG_pth, 'r').readlines()
    entid2txt = open(entid_2_txt_pth,'r').readlines()
    relid2txt = open(relid_2_txt_pth,'r').readlines()

    entid2txt_dict, relid2txt_dict = {},{}
    non_exist_ent, non_exist_rel = 0,0
    for line in entid2txt:
        line = line.rstrip()
        try :
            id, ent = line.split('\t')
        except :
            non_exist_ent+=1
            continue
        entid2txt_dict[id] = ent
        
    for line in relid2txt:
        line = line.rstrip()
        try: 
            id, rel = line.split('\t')
        except :
            non_exist_rel+=1
            continue
        relid2txt_dict[id] = rel
        
    non_exist_graph =0
    full_KG = defaultdict(list)
    for line in kg_dataset:
        line = line.rstrip()
        head_id, rel_id, tail_id, start_time, end_time = line.split('\t')
        try: 
            head = entid2txt_dict[head_id]
            rel = relid2txt_dict[rel_id]
            inverse_rel = '~'+rel
            tail = entid2txt_dict[tail_id]
        except:
            non_exist_graph+=1
            continue
        full_KG[head].append([head, rel, tail ,start_time, end_time])
        full_KG[tail].append([tail, inverse_rel, head, start_time, end_time])
    
    return full_KG, entid2txt_dict, relid2txt_dict

def parsing_question(question_path,entid2txt_dict,relid2txt_dict):
    with open(question_path, 'r') as f:
        qa_dict = json.load(f)

    qa_list = []
    for sample in qa_dict:
        tmp ={}
        given_qa = sample['question']
        answer_list = sample['answers']
        entities = sample['entities']
        relations = sample['relations']
            
        new_answer_list=[]
        if sample['answer_type'] == 'entity':
            for answer in answer_list:
                new_answer_list.append(entid2txt_dict[answer])
        else:
            for answer in answer_list:
                new_answer_list.append(answer)
        relation_list, entity_list = [],[]
        
        
        for ent in entities:
            entid_2_ent = entid2txt_dict[ent]
            entity_list.append(entid_2_ent)
            given_qa = given_qa.replace(ent, entid_2_ent)
        for rel in relations:
            relid_2_rel = relid2txt_dict[rel]
            relation_list.append(relid_2_rel)
            
        tmp['question'] = given_qa
        tmp['answers'] = new_answer_list
        tmp['relations'] = relation_list
        tmp['given_entities'] = entity_list
        qa_list.append(tmp)
        
    return qa_list


    
if __name__ == "__main__":
    
    #python chatbot_2Agent.py --type time_join --prompt pr_1 --model gpt-3.5
    parser = argparse.ArgumentParser()
    #parser.add_argument("--type", type=str, default="before_after")
    parser.add_argument("--prompt", type=str, default='pr_1')
    parser.add_argument("--percentage", type=int, default=10)
    parser.add_argument("--model", type = str, default='mistral-small')
    parser.add_argument("--subagent", type=str, default='gpt-4o')
    args = parser.parse_args()
    
    if args.prompt =='pr_1': 
        sub_prompt = prompt_sub.pr_1 
        main_prompt = prompt_main.pr_1
        save_path = f"./results_final/2Agent/{args.model}/sub_{args.subagent}/result_pr1/"
    elif args.prompt =='pr_2': 
        sub_prompt = prompt_sub.pr_2
        main_prompt = prompt_main.pr_2
        save_path = f"./results_final/2Agent/{args.model}/sub_{args.subagent}/result_pr2/"
    else : 
        sub_prompt = prompt_sub.pr_3
        main_prompt = prompt_main.pr_3
        save_path = f"./results_final/2Agent/{args.model}/sub_{args.subagent}/result_pr3/"
        
    
    
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    
    full_KG, entid2txt_dict, relid2txt_dict = make_data()
    time_join_question_path = "/nfs_edlab/smjo/KG-gpt2/wikidata_big/questions/time_join.json"
    simple_time_question_path = "/nfs_edlab/smjo/KG-gpt2/wikidata_big/questions/simple_time.json"
    simple_entity_question_path = "/nfs_edlab/smjo/KG-gpt2/wikidata_big/questions/simple_entity.json"
    time_join_qa_list = parsing_question(time_join_question_path,entid2txt_dict, relid2txt_dict) #3832
    simple_time_qa_list = parsing_question(simple_time_question_path,entid2txt_dict, relid2txt_dict)    #5046
    simple_entity_qa_list = parsing_question(simple_entity_question_path,entid2txt_dict, relid2txt_dict)    #7812
    
    qa_list_dict = [time_join_qa_list,simple_time_qa_list,simple_entity_qa_list]
    if args.percentage ==10:
        qid_list_dict = {0:[10*i for i in range(250)] , 1:[10*i for i in range(500)], 2:[10*i for i in range(700)]}
        #qid_list_dict = {0: [10*i for i in range(2)] , 1:[10*i for i in range(2)], 2:[10*i for i in range(2)]}
    elif args.percentage ==20:
        qid_list_dict = {0:[10*i for i in range(383*2)] , 1:[10*i for i in range(504*2)], 2:[10*i for i in range(780*2)]}
    
    result = {}
    questions_dict = {}
    entity_set_dict = {}
    label_set_dict = {}
    types_dict ={}
    
    
    
    iter_num_list=[]
    answer_list= [['qid','prediction','gt_label']]
    iter_limit_result = [['iterlimit', 'metric1','metric2','metric3']]
    
    
    iter_limit_list = [10]
    order =0
    for iter_limit in iter_limit_list:
        print(f"iter limit:{iter_limit}")
        total_correct, total_abs,total_wrong =0,0,0
        for qa_list in qa_list_dict:
            qid_list = qid_list_dict[order]
            
            #with open(os.path.join(save_path, f"result.txt"),'a') as f:
            for qid in qid_list:

                print(f"Qid:{qid}")
                question = qa_list[qid]['question']
                label = qa_list[qid]['answers']
                entities = qa_list[qid]['given_entities']
                
                #f.write(f"\n\n\nQid:{qid}\nQuestion :{question}")
                #f.write(f"GT entity:{entities}")
                
                prompt = main_prompt.replace('<<<Question>>>', question).replace('<<<Entity set>>>', str(entities))
                
                prediction, iter_num = reasoning(args.model, args.subagent, question, iter_limit,prompt, label,sub_prompt,KG = full_KG, entities=entities)
                

                
                ff = open(os.path.join(save_path, f"Only_answer.csv"),'a')
                writer= csv.writer(ff)
                writer.writerow([qid, prediction, label])
                ff.close()
                
        order +=1

                    

