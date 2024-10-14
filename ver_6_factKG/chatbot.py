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
            response = self.client.chat.completions.create( model=self.engine, messages=self.conversation, temperature= 0.3, top_p = 0.1)
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
            
def reasoning(claim,initial_prompt, label, f, sub_prompt):
            
    engine="gpt-3.5-turbo-0125"         
    #engine = "gpt-4o-mini-2024-07-18"
    chatbot = OpenAIBot(engine, client)

    iter_limit=30
    gold_set =[]
    for i in range(iter_limit):
        
        # Get Prompt from User
        if i == 0:
            prompt = initial_prompt
        else:
            #prompt = input()
            
            prompt, result, triples = client_answer(claim,response, label, gold_set,f, sub_prompt)
            
            if len(triples) > 0:
                gold_set+=triples
        
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
        
        
def client_answer(claim,response, label, gold_set,f, sub_prompt):
    #prompt, result, triples
    result = None
    #called multi helper functions
    #if not response.startswith('getRelation', 11) or not response.startswith('exploreKG',11) or not response.startswith('Verify', 11):
    #    prompt = '[Server]\nYou gave wrong format. Call the helper function again follow the right format'
    #    return prompt, result

    helper_ftn_calls, prompt = split_functions(response)
    triples = []
    for helper_str in helper_ftn_calls:
        
        
        if 'getRelation' in helper_str:
    
            result = getRelations(helper_str)
            prompt +=  "\n" + result
            #return prompt, result, []
            
            
        elif 'exploreKG' in helper_str:
            result, result_prompt = exploreKGs(helper_str)
            prompt += "\n" + result_prompt
            triples += result
            #return prompt, triples, triples
        
            
        elif 'Verification' in helper_str:
            sub_answer, case, result = verification(claim,gold_set,f, sub_prompt)
            prompt += "\n" +sub_answer
            
            f.write(f"CASE COUNT:{case}")
            #return prompt, prediction, []
        else:
            prompt += '\nYou gave wrong format. Call the helper function again follow the right format'
            result =''
    
    return prompt, result, triples
    

def retrieval_relation_parse_answer(rel):
    
    post_rel = re.sub('[-=+,#/\?:^.@*\"※ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', '', rel)
    return post_rel 

def split_functions(response):
    helper_ftn_calls=[]
    prompt=''
    try:
        response = response.replace("[ChatGPT]\n",'')
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
    
    try:
        entity = helper_str.split("getRelation[")[1].split("]")[0].strip()[1:-1]
        relations += db.getRelationsFromEntity(entity)
        relations += db.getRelationsFromEntity('"' + entity + '"')
        if len(relations) ==0 :
            return f"Do not change the format of entity {entity} in helper function."
        else:
            return 'Relations_list["' + entity + '"] = ' + str(relations)
    except:
        return "You gave wrong format of getRelations() function. Follow the format of examples."


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
                

def verification(claim,gold_set,f, sub_prompt):
    
    sub_response, case, prediction =sa.feedback(claim,gold_set,f,sub_prompt)
    return sub_response, case, prediction
    
    
    
    

def score(predict, label,f):
    abs, correct, wrong =0,0,0
    f.write(f"predict:{predict.lower()}, lable:{label.lower()}")
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
    
    parser = argparse.ArgumentParser()
    parser.add_argument("type", type=str, default="existence")
    parser.add_argument("subagent", type=str, default="7shot")
    args = parser.parse_args()
    
    save_path = f"./result_{args.subagent}"
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
            


    total_correct, total_abs,total_wrong =0,0,0
    
    if args.type == 'existence': qid_list = sample_number.existence
    elif args.type =="num1" : qid_list = sample_number.num1
    elif args.type =='multi_claim' : qid_list = sample_number.multi_claim
    elif args.type =="multi_hop" : qid_list = sample_number.multi_hop
    else:
        print("Wrong argument")
    
    if args.subagent == '7shot' : sub_prompt = prompts.sub_agent_7shot
    if args.subagent == '2option' : sub_prompt = prompts.sub_agent_2option
    if args.subagent == '2option_V2' : sub_prompt = prompts.sub_agent_2option_v2
    else:
        print("Wrong argument")

    
    iter_num_list=[]
    answer_list= [['qid','prediction','gt_label']]
    with open(os.path.join(save_path, f"result_{args.type}.txt"),'a') as f:
        for qid in qid_list:
            print(f"Qid:{qid}")
            question = questions_dict[qid]
            label = label_set_dict[qid]
            entities = entity_set_dict[qid]
            
            f.write(f"\n\n\nQid:{qid}\nQuestion :{question}")
            f.write(f"GT entity:{entities}")
            print(f"GT entity:{entities}")
            
            prompt = prompts.main_agent.replace('<<<<CLAIM>>>>', question).replace('<<<<GT_ENTITY>>>', str(entities))
            
            prediction, iter_num = reasoning(question,prompt, label,f, sub_prompt)
            abs, correct, wrong= score(str(prediction), str(label[0]),f)
            total_correct += correct
            total_wrong += wrong
            total_abs += abs
            iter_num_list.append(iter_num)
            answer_list.append([qid, str(prediction), str(label[0])])


        
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
        
    f= open(os.path.join(save_path, f"only_result_{args.type}.csv"),'w')
    writer= csv.writer(f)
    writer.writerows(answer_list)
    f.close()