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
import prompt_oneAgent
from models import OpenAIBot

#openai.api_key = "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"
#client = OpenAI(api_key=openai.api_key)


            
def reasoning(model, engine, claim, initial_prompt, label, f,KG):
            
      
    if model =="gpt" : 
        engine="gpt-4o-mini-2024-07-18"
        #engine="gpt-3.5-turbo-0125"
    elif model=='mixtral': engine = "open-mixtral-8x22b"

    chatbot = OpenAIBot(model,engine, 0.95, 0.95)

    iter_limit=10
    gold_set =[]
    gold_relations =''
    for i in range(iter_limit):
        
        # Get Prompt from User
        if i == 0:
            prompt = initial_prompt
        else:
            #prompt = input()
            
            prompt, result, triples, relations, get_rel_state = client_answer(claim,response, label, gold_set,gold_relations,f,KG)
            
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
        
def split_functions(response):
    helper_ftn_calls=[]
    prompt=''
    try:
        response = response.replace("[ChatGPT]\n",'')
        statement = response.split("Statement : ")[0].split("Helper function")[0]
        functions = response.split("Helper function")[1]
        if '##' in functions:
            helper_ftn_calls = functions.split(' ## ')
        else :
            helper_ftn_calls = [functions]
        prompt ='\n[User]\nExecution result :'
        
    except:
        prompt = "\n[User]\nYou gave wrong format of Statement and Helper function."
        
    return helper_ftn_calls, prompt
    
def client_answer(claim,response, label, gold_set,gold_relations,f, KG):
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
    
            get_rel_state, result = getRelations(helper_str, KG)
            prompt +=  "\n" + result
            if get_rel_state==1:
                relations += "\n" + result
            #return prompt, result, []
            
            
        elif 'exploreKG' in helper_str:
            result, result_prompt = exploreKGs(helper_str, KG)
            prompt += "\n" + result_prompt
            triples += result
            #return prompt, triples, triples
        
            
        elif 'Verification' in helper_str:
            verify_prompt, result = verification(helper_str, KG)
            prompt += verify_prompt
            

            #return prompt, prediction, []
        else:
            prompt += '\nYou gave wrong format. Call the helper function again follow the right format'
            result =''
    
    return prompt, result, triples, relations, get_rel_state
    
def getRelations(helper_str, KG): 
    
    relations = []
    state=0
    try:
        entity = helper_str.split("getRelation[")[1].split("]")[0].strip()[1:-1]
        subgraphs = KG[entity]
        for graph in subgraphs:
            rel = graph[1]
            if rel not in relations:
                relations.append(rel)
        if len(relations) ==0:
            state=0
            return state,f"Do not change the format of entity {entity} in helper function."
            
        else:
            state=1
            return state,'Relations_list["' + entity + '"] = ' + str(relations)
    
    except:
        return state,"You gave wrong format of getRelations() function. Follow the format of examples."
    


def exploreKGs(helper_str, KG):

    triples=[]
    result_prompt = ''
    try: 
        entity = helper_str.split("exploreKG[")[1].split("]=")[0].strip()[1:-1]
        relations = helper_str.split('=[')[1].split(']')[0].strip().split(', ')

        subgraphs = KG[entity]
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
                result_prompt += 'Relations_list["' + entity + '"] = ' + str(existing_relations)
            
            for sub_graph in KG[entity]:
                if rel == sub_graph[1]:
                    triples.append(sub_graph)
        
        if len(triples)==0:
            result_prompt += f"Choose other relations based refer to the Relations_list Or follow the format of Entity {entity} and Relations"
        
        else:
            result_prompt += ', '.join(str(sublist) for sublist in triples)
    except : 
        result_prompt += "You gave wrong format of exploreKGs() function. Follow the format of examples."

    

    return triples, result_prompt


def verification(helper_str, KG):
    try : 
        result = helper_str.split("Verification[")[1].split("]")[0]
        prompt = f"\nDone!!Prediction:{result}\nReal label:{label}"
    except:
        prompt = '\nYou gave wrong format. Call the verification function again follow the right format'
                
    return prompt, result

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
                correct = 1/per_score
            else:
                wrong += 1/per_score
                    
    
    return abs, correct, wrong

def make_data():
    print("Making dataset")
    gt_pth = "/home/smjo/KG-gpt2_cronKG/CronQA_data/wikidata_big/"
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
    ### Multi Prompts
    #python chatbot_oneAgent.py --type simple_entity --model gpt --engine gpt-4o-mini
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", type=str, default="simple_entity")
    #parser.add_argument("--prompt", type=str, default='pr_1')
    parser.add_argument("--model", type = str, default="gpt")
    parser.add_argument("--engine", type=str, default="gpt-4o-mini")
    args = parser.parse_args()
    

    prompt_list = [prompt_oneAgent.pr_1,prompt_oneAgent.pr_2, prompt_oneAgent.pr_3]
    
    question_path = f"/home/smjo/KG-gpt2_cronKG/CronQA_data/wikidata_big/questions/{args.type}.json"
    save_path = f"./results/multi_Prompts/{args.engine}"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    
    full_KG, entid2txt_dict, relid2txt_dict = make_data()
    qa_list = parsing_question(question_path,entid2txt_dict, relid2txt_dict)
    
    result = {}
    questions_dict = {}
    entity_set_dict = {}
    label_set_dict = {}
    types_dict ={}
    
    total_correct, total_abs,total_wrong =0,0,0
    
    iter_num_list=[]
    answer_list= [['qid','prediction','gt_label']]
    qid_list = [10*i for i in range(100)]
    
    for pr_id,main_prompt in enumerate(prompt_list):

        with open(os.path.join(save_path, f"result_{args.type}.txt"),'a') as f:
            for qid in qid_list:

                print(f"Qid:{qid}")
                question = qa_list[qid]['question']
                label = qa_list[qid]['answers']
                entities = qa_list[qid]['given_entities']
                
                f.write(f"\n\n\nQid:{qid}\nQuestion :{question}")
                f.write(f"GT entity:{entities}")
                
                prompt = main_prompt.replace('<<<Question>>>', question).replace('<<<Entity set>>>', str(entities))
                
                prediction, iter_num = reasoning(args.model, args.engine, question, prompt, label,f, KG = full_KG)
                
                abs, correct, wrong= score(str(prediction), label,f)
                total_correct += correct
                total_wrong += wrong
                total_abs += abs
                iter_num_list.append(iter_num)
                
                tmp_pth = os.path.join(save_path,f"{pr_id}")
                if not os.path.exists(tmp_pth):
                    os.mkdir(tmp_pth)
                ff = open(os.path.join(tmp_pth, f"only_result_{args.type}.csv"),'a')
                writer= csv.writer(ff)
                writer.writerow([qid, prediction, label])
                ff.close()

                
            total_sample = len(qid_list)

            '''
            if (total_sample - total_abs ) ==0 :
                metric1=0
            else:
                metric1 = (total_sample - total_abs ) /  total_sample
            if total_correct==0:
                metric2 =0
            else :
                metric2 = total_correct/  (total_sample - total_abs)
                
            if (total_correct-total_wrong)==0 :
                metric3 =0
            else:
                metric3 = (total_correct-total_wrong) / (total_sample - total_abs)

            f.write(f"\n\n\nTotal sample:{total_sample}, Total_Correct:{total_correct}, Total_Wrong:{total_wrong}, Total_abstain:{total_abs}\n")
            f.write(f"mrtric1:{metric1}\n mertric2:{metric2}\n metric3:{metric3}")
            f.write(f"avg iter:{np.average(iter_num_list)}\n max_iter:{np.max(iter_num_list)}\n min_iter:{np.min(iter_num_list)}")
            '''
