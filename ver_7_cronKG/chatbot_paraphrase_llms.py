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
import paraphraser
import pickle
from models import LLMBot
from difflib import get_close_matches
            
def reasoning(model,claim, initial_prompt, label,iter_limit,KG, entities):
            
    chatbot = LLMBot(model, temperature=0.95, top_p=0.95, max_tokens=2000)

    iter_limit=10
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
            
            prompt, result, triples, relations, get_rel_state, new_entities = client_answer(claim,response, label, gold_set,gold_relations,KG, gold_entities)
            
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
    
def client_answer(claim,response, label, gold_set,gold_relations,KG,gold_entities):
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
    
            get_rel_state, result = getRelations(helper_str, KG,gold_entities)
            prompt +=  "\n" + result
            if get_rel_state==1:
                relations += "\n" + result
            #return prompt, result, []
            
            
        elif 'exploreKG' in helper_str:
            result, result_prompt = exploreKGs(helper_str, KG,gold_entities)
            prompt += "\n" + result_prompt
            triples += result
            
            #For matching entities
            new_entities += find_new_entity(triples)
            #return prompt, triples, triples
        
            
        elif 'Verification' in helper_str:
            verify_prompt, result = verification(helper_str, KG)
            prompt += verify_prompt
            

            #return prompt, prediction, []
        else:
            prompt += '\nYou gave wrong format. Call the helper function again follow the right format'
            result =''
    
    return prompt, result, triples, relations, get_rel_state,new_entities


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



def verification(helper_str, KG):
    if ' ## ' in helper_str:
        helper_str = helper_str.split(' ## ')[0]
    try : 
        result = helper_str.split("Verification[")[1].split("]")[0]
        prompt = f"\nDone!!Prediction:{result}\nReal label:{label}"
    except:
        result =''
        prompt = '\nYou gave wrong format. Call the verification function again follow the right format'
                
    return prompt, result

def score(predict, label):
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
    gt_pth = "/nfs_edlab/smjo/KG-gpt2/wikidata_big/"
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

# 경로와 파일 관리 함수
def save_to_json(data, file_path):
    """JSON 파일에 데이터를 저장"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_from_json(file_path):
    """JSON 파일에서 데이터를 로드"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


if __name__ == "__main__":
    
    #python chatbot_paraphrase.py --type time_join --model gpt --engine gpt-3.5
    parser = argparse.ArgumentParser()
    parser.add_argument("--percentage", type=int, default=10)
    parser.add_argument("--model", type = str, default='mistral-small')

    args = parser.parse_args()
    
    save_path = f'./results_final/Paraphrase/{args.model}/'
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
        #qid_list_dict = {0: [10*i for i in range(1)] , 1:[10*i for i in range(1)], 2:[10*i for i in range(1)]}
    elif args.percentage ==20:
        qid_list_dict = {0:[10*i for i in range(383*2)] , 1:[10*i for i in range(504*2)], 2:[10*i for i in range(780*2)]}
    
    
    result = {}
    questions_dict = {}
    entity_set_dict = {}
    label_set_dict = {}
    types_dict ={}
    
    
    
    # 데이터 저장 경로
    claim_path = f"./results_final/Paraphrase/gpt-4o-mini/paraphrased_claims.json" #already made before
    save_path = f"./results_final/Paraphrase/{args.model}/Processed"

    # paraphrase 처리
    if not os.path.exists(claim_path):
        os.makedirs(os.path.dirname(claim_path), exist_ok=True)
        paraphrased_claims = []

        order = 0
        for qa_list in qa_list_dict:
            qid_list = qid_list_dict[order]
            for qid in qid_list:
                question = qa_list[qid]['question']
                label = qa_list[qid]['answers']
                entities = qa_list[qid]['given_entities']

                paraphrase_claims = paraphraser.paraphrase(question)
                processed = {
                    'qid': qid,
                    'question': question,
                    'label': label,
                    'entities': entities,
                    'claims': paraphrase_claims
                }
                paraphrased_claims.append(processed)
            order += 1

        # JSON 파일에 저장
        save_to_json(paraphrased_claims, claim_path)

    else:
        # JSON 파일에서 로드
        paraphrased_claims = load_from_json(claim_path)

    # 저장된 데이터 처리
    iter_limit=10
    iter_num_list = []
    for processed in paraphrased_claims[1356:]:
        qid = processed['qid']
        paraphrase_claims = processed['claims']
        q = processed['question']
        entities = processed['entities']
        label = processed['label']

        for p, question in enumerate(paraphrase_claims):
            print(question)
            # 텍스트 파일 저장
            paraphrase_file = os.path.join(save_path, f"paraphrase_{p}.txt")
            os.makedirs(os.path.dirname(paraphrase_file), exist_ok=True)
            #with open(paraphrase_file, 'w', encoding='utf-8') as f:
                #f.write(f"\n\n\nQuestion: {q}")
                #f.write(f"\nGT entity: {entities}")

            # Reasoning 처리
            prompt = prompt_oneAgent.pr_1.replace('<<<Question>>>', question).replace('<<<Entity set>>>', str(entities))
            prediction, iter_num = reasoning(args.model, question,prompt, label,iter_limit,KG = full_KG, entities=entities)

            iter_num_list.append(iter_num)

            # 결과 CSV 저장
            result_csv = os.path.join(save_path, f"only_result_{p}.csv")
            os.makedirs(os.path.dirname(result_csv), exist_ok=True)
            with open(result_csv, 'a', newline='', encoding='utf-8') as ff:
                writer = csv.writer(ff)
                writer.writerow([qid,prediction, label])
                    
        


        

