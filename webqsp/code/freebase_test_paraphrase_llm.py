### Differences in Freebase Knowledge Base
# 1. No inverse relation
# 2. MID conversion
# 3. CVT node handling (Remove duplicated entity such as MetaQA 2, 3hop case)


import openai
import sys, os
from openai import OpenAI
import json
import csv
import argparse
import numpy as np
import re
import ast
import freebase_sparql as db
import subagent as sa
import time
from prompt import freebase_main_agent_singlestep, freebase_main_agent_multistep_stop_sig, freebase_main_agent_multistep_2_stop_sig, freebase_main_agent_multistep_3_stop_sig, freebase_main_agent_multistep_4_stop_sig, freebase_main_agent_multistep_5_stop_sig
from model import LLMBot
from paraphraser import paraphrase

openai.api_key = "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"
client = OpenAI(api_key=openai.api_key)

class OpenAIBot:
    def __init__(self, engine, client, temperature, top_p):
        # Initialize conversation with a system message
        self.conversation = [{"role": "system", "content": "You are a helpful assistant."}]
        self.engine = engine
        self.client = client
        self.temperature = temperature
        self.top_p = top_p

    def add_message(self, role, content):
        # Adds a message to the conversation.

        self.conversation.append({"role": role, "content": content})
    def generate_response(self, prompt):
        # Add user prompt to conversation
        self.add_message("user", prompt)

        try:
            # Make a request to the API using the chat-based endpoint with conversation context
            response = self.client.chat.completions.create( model=self.engine, messages=self.conversation, temperature=self.temperature, top_p = self.top_p)
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

class Information:
    def __init__(self, qid, claim, gt_entity, label):
        self.qid = qid
        self.claim = claim
        self.gt_entity = gt_entity
        self.label = label
        self.mid_dict = {gt_entity[0]: gt_entity[1]}
        self.rel_dict = {}
        self.entrel = []
        self.state = 0 # For exploreKG totally miss to find the answer
        self.gold_set = []

    def setState(self, state):
        self.state = state
    
    def addEvidence(self, triples):
        self.gold_set += triples
            
def reasoning(info, claim, initial_prompt, label, max_iter, model, temperature, top_p, f):
            
    # engine= "gpt-3.5-turbo"
    # engine = "gpt-4o-mini"
    engine = model
    # chatbot = OpenAIBot(engine, client, temperature, top_p)
    chatbot = LLMBot(engine, temperature, top_p, 2000)
    # info = Information()

    iter_limit = max_iter
    flag = False

    for i in range(iter_limit + 1):
        
        # Get Prompt from User
        if i == 0:
            prompt = initial_prompt
        else:
            #prompt = input()
            info.state = 0
            prompt, result = client_answer(claim, response, label, info, f)
            # if info.state == -1:
            #     f.write(f"\nDuplicated Entity-Relation pair!")
            #     break
            f.write(prompt)
            
        # f.write(prompt)
        # User can stop the chat by sending 'End Chat' as a Prompt
        if 'Done!!' in prompt:
            flag = True
            break

        # Generate and Print the Response from ChatBot
        f.write(f"\n************************************Iteration:{i}************************************")

        response = chatbot.generate_response(prompt)
        print(response)
        time.sleep(2)

        if response == None or 'Error' in response:
            return 'Error', i

        f.write("\n"+response)
        f.write(f"---")

    
    if flag == False:
        result = 'Abstain'
        
    return result, i
        
        
def client_answer(claim, response, label, info, f):
    # print(response)
    if response.count('[ChatGPT]') > 1:
        prompt = '\n[User]\nExecution result: ' + '\nYou should wait for the [User] response after calling helper function.'
        return prompt, []

    result = None
    #called multi helper functions
    #if not response.startswith('getRelation', 11) or not response.startswith('exploreKG',11) or not response.startswith('Verify', 11):
    #    prompt = '[Server]\nYou gave wrong format. Call the helper function again follow the right format'
    #    return prompt, result

    helper_ftn_calls = []
    helper_ftn_calls = split_functions(response)
    prompt = '\n[User]\nExecution result: '

    if len(helper_ftn_calls) == 0:
        prompt += '\nYou gave wrong format. Call the helper function again follow the right format'

    for helper_str in helper_ftn_calls:
        if 'getRelation' in helper_str:
    
            result = getRelations(helper_str, info)
            prompt +=  "\n" + result
            #return prompt, result, []

        elif 'exploreKG' in helper_str:
            # print(helper_str)
            result, result_prompt = exploreKGs(helper_str, info)
            if info.state == 0:
                prompt += f"Choose other relations based refer to the Relations_list Or follow the format of Entity and Relations"
            else:
                if prompt == '': continue
                prompt += "\n" + result_prompt
            # triples += result
            info.addEvidence(result)
            #return prompt, triples, triples
                
        elif 'Verification' in helper_str:
            try:
                # result = helper_str.split("Verification[")[1].split("]")[0]
                result = helper_str.split("Verification[")[1].split("]]")[0] + ']'
                prompt += f"\nDone!!\nPrediction : {result}\nReal label :{label}"
            except:
                prompt += '\nYou gave wrong format. Call the helper function again follow the right format'
            # sub_answer, case, result = verification(claim, info.gold_set, f)
            # prompt += "\n" +sub_answer
            
            # f.write(f"CASE COUNT:{case}")
            #return prompt, prediction, []
        else:
            prompt += '\nYou gave wrong format. Call the helper function again follow the right format'
    
    return prompt, result
    
def retrieval_relation_parse_answer(rel):
    
    post_rel = re.sub('[-=+,#/\?:^@*\"※ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', '', rel)
    return post_rel 

def retrieval_relation_parse_answer2(rel):
    for r in range(len(rel)):
        post_rel = re.sub('[-=+,#/\?:^@*\"※ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', '', rel[r])
        rel[r] = post_rel
    return rel

def split_functions(response):
    helper_ftn_calls=[]
    response = response.replace("[ChatGPT]\n",'')
    # statement = response.split("Statement : ")[0].split("Helper function : ")[0]
    try:
        functions = response.split("Helper function: ")[1].split("\n<Wait For User Response>")[0]
        if '##' in functions:
            helper_ftn_calls = functions.split(' ## ')
        else :
            helper_ftn_calls = [functions]
        return helper_ftn_calls
    except:
        return helper_ftn_calls

def getRelations(helper_str, info):
    relations = []
    try:
        entity = helper_str.split("getRelation[")[1].split("]")[0].strip()[1:-1]
        # print(entity, info.mid_dict)
        # Additional Handling for MID
        if entity in info.mid_dict.keys(): mid = info.mid_dict[entity]
        else: raise NotImplementedError
        relations += db.getRelationsFromEntity(mid)
        rels = []
        # print(relations)
        for rel in relations:
            rel_keyword = rel.split('/')[-1]
            rels.append('~' + rel_keyword) if rel[0] == '~' else rels.append(rel_keyword)
            if rel_keyword in info.rel_dict.keys():
                continue
            else:
                if rel[0] == '~':
                    info.rel_dict[rel_keyword] = '~'.join(rel.split('~')[1:])
                else:
                    info.rel_dict[rel_keyword] = rel
        
        if len(relations) ==0 :
            return f"Do not change the format of entity {entity} ({mid}) in helper function."
        else:
            return 'Relations_list["' + entity + '"] = ' + str(rels)
    except:
        return "You gave wrong format of getRelation[] function. Follow the format of examples."
    

def exploreKGs(helper_str, info):
    triples= []
    result_prompt = ''
    try: 
        ent = helper_str.split("exploreKG[")[1].split("]=")[0].strip()[1:-1]
        # exploreKG[mid]=[rel]
        # exploreKG[name]=[rel]
        # print(ent, info.mid_dict)
        ent_mid = info.mid_dict[ent]

        relations = helper_str.split('=[')[1].split(']')[0].strip().split(', ')
            
        for rel in relations:
            rel = retrieval_relation_parse_answer(rel)
            # print('entrel : ', ent_mid, rel)

            # if (ent, rel) in info.entrel:
            #     info.setState(-1)
            #     return [], result_prompt
            # else: info.entrel.append((ent, rel))

            tails = []
            tails += db.getEntityFromEntRel(ent_mid, rel)
            
            # print('tails : ', tails)
            for tail in tails:
                name = db.mid2name(tail)
                if name in list(info.gt_entity): continue
                # CVT node or Name converted entity
                info.mid_dict[name] = tail
                triples.append([ent, rel, name])
                
        if len(triples) == 0:
            pass
            # result_prompt += f"Choose other relations based refer to the Relations_list Or follow the format of Entity {ent} and Relations"
        
        else:
            info.state = 1
            result_prompt += ', '.join(str(sublist) for sublist in triples)
        
    except:
        result_prompt += "You gave wrong format of exploreKG[] function. Follow the format of examples."

    

    return triples, result_prompt


def verification(claim, gold_set, f):
    
    sub_response, case, prediction = sa.feedback(claim, gold_set, f)
    return sub_response, case, prediction


def score(predict, label,f):
    try:
        predict = ast.literal_eval(predict)
        label = ast.literal_eval(label)
    except:
        print('error')
        return 1, 0, 0
    abs, correct, wrong = 0, 0, 0

    f.write(f"\npredict : {predict}, label:{label}")
    print(f"predict : {predict}, label:{label}")

    if 'Abstain' in predict:
        abs+=1
        return abs, correct, wrong
    
    for p in predict:
        if p in label:
            correct = 1
            wrong = 0
            break
        else:
            wrong = 1
    #LLM abs개수, correct 개수
    return abs, correct, wrong
    
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", type=str, default="train")
    parser.add_argument("--num_iter", type = int, default = "15")
    parser.add_argument("--model", type = str, default= "Qwen-14B")
    parser.add_argument("--prompt", type = str, default= "initial_prompt")
    parser.add_argument("--temp", type = float, default = 1.0)
    parser.add_argument("--top_p", type = float, default = 0.5)
    parser.add_argument("--paraphrase_num", type = int, default = 5)
    args = parser.parse_args()
    
    if args.model == 'Qwen-14B':
        save_path = f"./webqsp/100samples/model_variant_result_20241122/Qwen-2.5-14B-Instruct/paraphrase"
    elif args.model == 'Qwen-32B':
        save_path = f"./webqsp/100samples/model_variant_result_20241122/Qwen-2.5-32B-Instruct/paraphrase"
    elif args.model == 'llama':
        save_path = f"./webqsp/100samples/model_variant_result_20241122/Meta-Llama-3.1-70B-Instruct/paraphrase"
    elif args.model == 'Mistral-Small':
        save_path = f"./webqsp/100samples/model_variant_result_20241122/Mistral-Small-Instruct-2409-t16384/paraphrase"
        
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    
    # Load prompt
    if args.prompt == 'initial_prompt':
        prompt_template = freebase_main_agent_multistep_stop_sig
    elif args.prompt == 'prompt2':
        prompt_template = freebase_main_agent_multistep_2_stop_sig
    elif args.prompt == 'prompt3':
        prompt_template = freebase_main_agent_multistep_3_stop_sig
    elif args.prompt == 'prompt4':
        prompt_template = freebase_main_agent_multistep_4_stop_sig
    elif args.prompt == 'prompt5':
        prompt_template = freebase_main_agent_multistep_5_stop_sig
    
    # Load model
    if args.model == 'Qwen-14B':
        model_name = "Qwen/Qwen2.5-14B-Instruct"
    elif args.model == 'Qwen-32B':
        model_name = "Qwen/Qwen2.5-32B-Instruct"
    elif args.model == 'chatgpt':
        model_name = "gpt-4o-mini"
    elif args.model == 'Mistral-Small':
        model_name = "mistralai/Mistral-Small-Instruct-2409"
    elif args.model == 'llama':
        model_name = "meta-llama/Meta-Llama-3.1-70B-Instruct"

    result = {}
    questions_dict = {}
    entity_set_dict = {}
    label_set_dict = {}
    types_dict ={}
    
    with open("./WebQSP.test.json", 'r') as f:
        data = json.load(f)
        questions = data['Questions']
        
        for q in questions:
            questions_dict[q["QuestionId"]] = q["RawQuestion"]
            entity_set_dict[q["QuestionId"]] = (q["Parses"][0]['TopicEntityName'], q["Parses"][0]['TopicEntityMid'])
            labels = []
            for a in q["Parses"][0]['Answers']:
                # labels.append((a['EntityName'], a['AnswerArgument']))
                labels.append(a['EntityName'])

            label_set_dict[q["QuestionId"]] = labels
            
    total_correct, total_abs, total_wrong = 0, 0, 0

    
    iter_num_list=[]

    paraphrase_num = args.paraphrase_num

    for i in range(paraphrase_num):
        result_file = os.path.join(save_path, f"only_answer_{args.type}_{args.model}_maxiter_{args.num_iter}_prompt_{args.prompt}_stop_sig_temp_{args.temp}_topp_{args.top_p}_paraphrase_{i}.csv")
        result_file_csv = open(result_file, 'a')
        answer_list= [['qid','prediction','gt_label']]
        # answer_list= [['qid','correct','wrong','prediction','gt_label']]
        result_file_csv.write(','.join(answer_list[0]) + '\n')
        result_file_csv.close()

    a = 0
    for qid, question in questions_dict.items():
        a += 1
        if a % 20 != 0: continue
        if a > 2000:
            break

        # Paraphrase the question
        paraphrase_list = paraphrase(question)

        for i in range(paraphrase_num):
            question = paraphrase_list[i]

            with open(os.path.join(save_path, f"result_{args.type}_{args.model}_maxiter_{args.num_iter}_prompt_{args.prompt}_stop_sig_temp_{args.temp}_topp_{args.top_p}_paraphrase_{i}.txt"),'a') as f:
                print(f"Qid : {qid}")
                # question = questions_dict[qid]
                label = label_set_dict[qid]
                entities = entity_set_dict[qid]

                print(question, entities[0], label)

                info = Information(qid, question, entities, label)
                
                f.write(f"\n\n\nQid : {qid}\nQuestion : {question}\n")
                f.write(f"GT entity : {entities}")
                
                prompt = prompt_template.replace('<<<<CLAIM>>>>', question).replace('<<<<GT_ENTITY>>>', str(entities[0]))
                
                prediction, iter_num = reasoning(info, question, prompt, label, args.num_iter, model_name, args.temp, args.top_p, f)
                abs, correct, wrong= score(str(prediction), str(label),f)
                total_correct += correct
                total_wrong += wrong
                total_abs += abs
                iter_num_list.append(iter_num)
                answer_list.append([qid, str(prediction), str(label)])
                print('abstain : ', total_abs, 'correct : ', total_correct, 'wrong : ', total_wrong)
                f.close()

            with open(os.path.join(save_path, f"only_answer_{args.type}_{args.model}_maxiter_{args.num_iter}_prompt_{args.prompt}_stop_sig_temp_{args.temp}_topp_{args.top_p}_paraphrase_{i}.csv"), 'a') as f:
                writer = csv.writer(f)
                writer.writerow(answer_list[-1])

        # total_sample = total_correct + total_abs

        # if total_sample == total_abs :
        #     metric1 = 0
        # else:
        #     metric1 = (total_sample - total_abs) / total_sample

        # if total_correct == 0:
        #     metric2 = 0
        # else :
        #     metric2 = total_correct / (total_sample - total_abs)
            
        # if (total_correct - total_wrong) == 0 :
        #     metric3 = 0
        # else:
        #     metric3 = (total_correct - total_wrong) / (total_sample - total_abs)
                
            
        # with open(os.path.join(save_path, f"result_{args.type}_{args.model}_maxiter_{args.num_iter}_prompt_{args.prompt}_stop_sig_temp_{args.temp}_topp_{args.top_p}_paraphrase_{i}.txt"),'a') as f:
        # # with open(os.path.join(save_path, f"result_{args.type}_4omini.txt"),'a') as f:
        #     f.write(f"\n\n\nTotal sample:{total_sample}, Total_Correct:{total_correct}, Total_Wrong:{total_wrong}, Total_abstain:{total_abs}\n")
        #     f.write(f"\nmetric1:{metric1}\nmetric2:{metric2}\nmetric3:{metric3}")
        #     f.write(f"\navg iter:{np.average(iter_num_list)}\nmax_iter:{np.max(iter_num_list)}\nmin_iter:{np.min(iter_num_list)}")
        
    # f= open(f"./webqsp/only_answer_{args.type}_{args.model}_maxiter_{args.num_iter}_50trial.csv",'w')

    # writer= csv.writer(f)
    # writer.writerows(answer_list)
    # f.close()