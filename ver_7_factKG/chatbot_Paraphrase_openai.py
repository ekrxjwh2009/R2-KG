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
import prompt_oneAgent
import paraphraser
from difflib import get_close_matches

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
            
def reasoning(model,claim,initial_prompt, label, entities,f):
            
    if model == 'gpt-4o-mini': engine = "gpt-4o-mini-2024-07-18"
    elif model == 'gpt-4o' : engine = "gpt-4o-2024-08-06"
    chatbot = OpenAIBot(engine, client)

    iter_limit=15
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
            
            prompt, result, triples, relations, get_rel_state, new_entites = client_answer(claim,response, label, gold_set,gold_relations,gold_entities,f)
            
            if len(triples) > 0:
                gold_set+=triples
            if get_rel_state==1:
                gold_relations += relations
            if len(new_entites)>0:
                gold_entities+=new_entites    
            
        
        if i>0:    
            f.write(prompt)
            f.write(f"Gold entites:{gold_entities}")
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
        
        
def client_answer(claim,response, label, gold_set,gold_relations,gold_entities,f):
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
            verify_prompt, result = verification(helper_str, label)
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
                

def verification(helper_str, label):
    
    try : 
        result = helper_str.split("Verification[")[1].split("]")[0]
        prompt = f"\nDone!!Prediction:{result}\nReal label:{label}"
    except:
        prompt = '\nYou gave wrong format. Call the verification function again follow the right format'
                
    return prompt, result
    
    
    
    

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
    
    #python chatbot_oneAgent.py --type existence --num_iter 15 --model gpt-3.5 --data test

    parser = argparse.ArgumentParser()
    parser.add_argument("--percentage", type=int, default=10)
    parser.add_argument("--model", type = str, default= "gpt-4o-mini")
    args = parser.parse_args()
    
    save_path = f"results_final/Paraphrase/{args.model}/"
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

    
    # 데이터 저장 경로
    claim_path = f"./results_final/Paraphrase/{args.model}/paraphrased_claims.json"
    save_path = f"./results_final/Paraphrase/{args.model}/Processed"

    ensemble_answer_list = [['qid', 'predictions', 'gt_label']]  # CSV에 저장할 결과 초기화
    iter_num_list = []

    if not os.path.exists(claim_path):
        os.makedirs(os.path.dirname(claim_path), exist_ok=True)
        paraphrased_claims = []
        
        for qid in qid_list:  # Paraphrase를 3개 QID에 대해 처리
            print(f"Processing Qid: {qid}")
            question = questions_dict[qid]
            label = label_set_dict[qid]
            entities = entity_set_dict[qid]

            # Paraphrase 생성
            paraphrase_claims = paraphraser.paraphrase(question)
            processed = {
                'qid': qid,
                'question': question,
                'label': label,
                'entities': entities,
                'claims': paraphrase_claims
            }
            paraphrased_claims.append(processed)

        # Paraphrased 결과를 JSON으로 저장
        save_to_json(paraphrased_claims, claim_path)

    else:
        # 저장된 paraphrase 결과를 JSON에서 로드
        paraphrased_claims = load_from_json(claim_path)

    # 저장된 데이터를 사용해 문장별 처리
    for processed in paraphrased_claims:
        qid = processed['qid']
        print(qid)
        question = processed['question']
        paraphrase_claims = processed['claims']
        label = processed['label']
        entities = processed['entities']

        trial_predictions = []  # 각 QID에 대한 trial별 예측 결과 저장

        for trial_idx, paraphrased_question in enumerate(paraphrase_claims):
            print(f"qid:{qid}, {paraphrased_question}")
            
            
            # Trial별 텍스트 파일 (추적용)
            paraphrase_file = os.path.join(save_path, f"trial_{trial_idx}_paraphrases.txt")
            os.makedirs(os.path.dirname(paraphrase_file), exist_ok=True)

            with open(paraphrase_file, 'a', encoding='utf-8') as f:
                f.write(f"QID: {qid}\n")
                f.write(f"Original Question: {question}\n")
                f.write(f"Paraphrased Question: {paraphrased_question}\n")
                f.write(f"Given entities:{entities}")

                # Reasoning 수행
                main_prompt = (
                    prompt_oneAgent.pr_1
                    .replace('<<<<CLAIM>>>>', paraphrased_question)
                    .replace('<<<<GT_ENTITY>>>>', str(entities))
                )
                prediction, iter_num = reasoning(args.model, paraphrased_question, main_prompt, label, entities ,f)
                iter_num_list.append(iter_num)
                trial_predictions.append(prediction)

                f.write(f"Prediction: {prediction}\n")
                f.write(f"Ground Truth: {label[0]}\n\n")
                print(f"Prediction:{prediction}")

        # QID별로 예측 결과와 Ground Truth 추가
        ensemble_answer_list.append([qid, trial_predictions, str(label[0])])

        # 최종 결과를 하나의 CSV에 저장
        result_csv = os.path.join(save_path, "all_trials_results.csv")
        os.makedirs(os.path.dirname(result_csv), exist_ok=True)
        with open(result_csv, 'a', newline='', encoding='utf-8') as ff:
            writer = csv.writer(ff)
            #writer.writerow(['qid', 'predictions', 'gt_label'])  # 헤더 작성
            writer.writerow([qid, trial_predictions, str(label[0])])








    
     



        
