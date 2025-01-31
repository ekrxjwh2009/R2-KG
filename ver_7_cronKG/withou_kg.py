import openai
import sys, os
import ast
from openai import OpenAI
import json
import csv
import argparse
import numpy as np
import re
import pandas as pd
import itertools
import pickle
from collections import defaultdict
from difflib import get_close_matches

openai.api_key = "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"
client = OpenAI(api_key=openai.api_key)

def generate_batch_responses(qid_list, questions_dict, labels_set_dict, output_csv, batch_size):
    responses = {}
    # 저장 경로 확인 (디렉토리가 아니라면 자동 생성)
    output_dir = os.path.dirname(output_csv)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    # QID를 batch_size씩 묶음 (남은 데이터도 처리)
    batch_list = [qid_list[i:i + batch_size] for i in range(0, len(qid_list), batch_size)]
    
    for idx,batch in enumerate(batch_list):
        print(idx, len(batch_list))
        batch_questions = {qid: questions_dict[qid] for qid in batch}
        
        # Prompt 생성
        prompt = """Your task is to answer the following questions.
Please note that the unit is not important. (e.g. "98400" is also same as 98.4kg)
If you think the question has multiple answers, give all of the answers.

Now, let's answer the following questions. Please return the results in the format like this:
{"qid1" : ["answer1", "answer2"], "qid2" : ["answer1"], "qid3" : ["answer1", "answer2", "answer3", ...] ...}

Questions:
"""
        for qid, question in batch_questions.items():
            prompt += f'"{qid}": "{question}",\n'
        
        prompt = prompt.strip(",\n")  # 마지막 쉼표 제거
        prompt += "\n\nAnswer in following format \"qid\" : [list of answers] :\n"
        
        # OpenAI API 호출
        response = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[{"role": "system", "content": "You are an AI verifying claims."},
                      {"role": "user", "content": prompt}]
        )
        
        # 응답을 직접 파싱
        response_content =  response.choices[0].message.content.strip()
        #print(f"API 응답 확인:\n{response_content}\n")
    
        try:
            parsed_response = eval(response_content)  # JSON 대신 eval()로 직접 리스트 처리
            for qid, answers in parsed_response.items():
                responses[qid] = ", ".join(answers)  # 리스트를 문자열로 변환하여 저장
        except Exception as e:
            print(f"응답 파싱 오류: {e}")
            
            
    # CSV 파일 저장 (qid, response, gt_label)
    df = pd.DataFrame([(qid, responses.get(str(qid), "Unknown"), labels_set_dict.get(qid, ["Unknown"])[0]) for qid in qid_list],
                      columns=["qid", "response", "gt_label"])
    df.to_csv(output_csv, index=False)
    
    return responses

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
    
    questions_dict = {}
    entity_set_dict = {}
    label_set_dict = {}
    types_dict ={}
    
    save_path = "/nfs_edlab/smjo/KG-gpt2/ver_7_cronKG/results_final/without_kg"
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
    qid_list_dict = {0:[10*i for i in range(250)] , 1:[10*i for i in range(500)], 2:[10*i for i in range(700)]}

    new_questions_dict, new_label_dict={},{}
    new_qid_list =[]
    idx =0
    for order,qa_list in enumerate(qa_list_dict):
        qid_list = qid_list_dict[order]
        for qid in qid_list:
            question = qa_list[qid]['question']
            label = qa_list[qid]['answers']
            
            new_qid_list.append(idx)
            new_questions_dict[idx] = question
            new_label_dict[idx] = [label]
            idx+=1
            
        
        
        
    responses = generate_batch_responses(new_qid_list, new_questions_dict,new_label_dict,os.path.join(save_path, "only_result.csv" ),batch_size=30)



