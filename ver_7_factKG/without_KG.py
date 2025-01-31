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
import pandas as pd
import subagent as sa
import itertools
import prompts_main
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
        prompt = """You should verify the claim based on the evidence set.
Please note that the unit is not important. (e.g. "98400" is also same as 98.4kg)
Choose one of {True, False}.

Now, let's verify the following claims. Please return the results in the JSON format like this:
{"qid1": "True", "qid2": "False", ...}

Claims:
"""
        for qid, question in batch_questions.items():
            prompt += f'"{qid}": "{question}",\n'
        
        prompt = prompt.strip(",\n")  # 마지막 쉼표 제거
        prompt += "\n\nAnswer in JSON format:\n"
        
        # OpenAI API 호출
        response =client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[{"role": "system", "content": "You are an AI verifying claims."},
                      {"role": "user", "content": prompt}]
        )
        
        # 응답을 직접 파싱 (괄호 제거 후 ',' 기준 분할)
        response_content = response.choices[0].message.content.strip()
        print(f"API 응답 확인:\n{response_content}\n")
        
        response_content = response_content.strip('{}')  # 양끝 괄호 제거
        pairs = response_content.split(',')  # 콤마 기준으로 분리
        
        for pair in pairs:
            qid, answer = pair.split(':')
            qid = qid.strip().replace('"', '')  # QID 정리
            answer = answer.strip().replace('"', '')  # 답변 정리
            responses[qid] = answer
    
    # CSV 파일 저장 (qid, response, gt_label)
    df = pd.DataFrame([(qid, responses.get(str(qid), "Unknown"), labels_set_dict.get(qid, ["Unknown"])[0]) for qid in qid_list],
                      columns=["qid", "response", "gt_label"])
    df.to_csv(output_csv, index=False)
    
    return responses

if __name__ == "__main__":
    
    questions_dict = {}
    entity_set_dict = {}
    label_set_dict = {}
    types_dict ={}
    
    save_path = "/nfs_edlab/smjo/KG-gpt2/ver_7_factKG/results_final/without_kg"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
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



    qid_list = sample_number.percentage_10
    #qid_list=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] 
    questions_dict = {qid: f"Some claim related to {qid}" for qid in qid_list}  # 질문 목록
    responses = generate_batch_responses(qid_list, questions_dict,label_set_dict,os.path.join(save_path, "only_result.csv" ),batch_size=30)



