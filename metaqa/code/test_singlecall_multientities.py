import openai
import sys, os
from openai import OpenAI
import json
import csv
import argparse
import re
import ast
import dbpedia_sparql as db
import numpy as np
from prompt.various_prompt import initial_prompt, pr1_singlecall, pr1_singlecall_with_multiple_entities
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(root_dir)
load_dotenv()

# GITIGNORE WHEN MAKING REPO PUBLIC
openai.api_key = os.getenv('OPENAI_KEY')

client = OpenAI(
    api_key = os.getenv('OPENAI_KEY')
)

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
            response = self.client.chat.completions.create( model=self.engine, messages=self.conversation, temperature= 0.2)
            # Extract the response
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
    def __init__(self, gt_entity):
        self.entrel = []
        self.gt_entity = gt_entity
        self.state = 0

    def setState(self, state):
        self.state = state


def reasoning(initial_prompt, label, entities, max_iter, model, f):
            
    # engine= "gpt-3.5-turbo"
    # engine = "gpt-4o-mini"
    engine = model
    chatbot = OpenAIBot(engine, client)
    gt_entity = preprocess_ent(entities[0])
    info = Information(gt_entity)

    iter_limit=max_iter
    flag = False

    for i in range(iter_limit + 1):
        
        # Get Prompt from User
        if i == 0:
            prompt = initial_prompt
        else:
            #prompt = input()
            
            prompt, result = client_answer(response, label, info)
            if info.state == -1:
                break
            f.write(prompt)

        # f.write(prompt)
        # User can stop the chat by sending 'End Chat' as a Prompt
        if 'Done!!' in prompt:
            flag = True
            break

        # Generate and Print the Response from ChatBot
        f.write(f"\n************************************Iteration:{i}***********************************")

        response = chatbot.generate_response(prompt)

        if 'Error' in response:
            return 'Error', i
        
        f.write("\n"+response)
    
    if flag == False:
        result = 'Abstain' 
        
    return result, i
        
        
def client_answer(response, label, info):
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
    
    for ftn in helper_ftn_calls:
        if 'getRelation' in ftn:
            try :
                entity_list = ftn.split("getRelation(")[1].split(")")[0]
                entity_list = ast.literal_eval(entity_list)
                print(f"entity_list:{entity_list}")
                result = get_relations(entity_list)
                if len(result) == 0:
                    prompt += "\nDo not change the format of entity in helper function."
                else:
                    for entity in entity_list:
                        entity = preprocess_ent(entity)
                        prompt += f"\nRelation_list('{entity}') = {result[entity]}"
            except :
                prompt += '\nYou gave wrong format. Call the helper function again follow the right format'
        elif 'exploreKG' in ftn:
            try:
                entity_list = ftn.split("exploreKG(")[1].split(")=")[0]
                entity_list = ast.literal_eval(entity_list)
                relations = ftn.split("=[")[1].split("]")[0].strip().split(', ')
                for entity in entity_list:
                    entity = preprocess_ent(entity)
                    result = explore_kg(entity, relations, info)      #entity, string of relation list
                    if len(result) == 0:
                        continue
                    else:
                        prompt += f"\n{', '.join([str(triple) for triple in result])}"
            except:
                prompt = '\nYou gave wrong format. Call the helper function again follow the right format'
        elif 'Verification' in ftn:
            try:
                result = ftn.split("Verification(")[1].split(")")[0]
                result = ast.literal_eval(result)
                result = list(set(result))
                # result = ftn.split("Verification(")[1].split(")")[0][1:-1]

                prompt += f"\nDone!!Prediction:{result}\nReal label:{label}"
            except:
                prompt += '\nYou gave wrong format. Call the helper function again follow the right format'
        else:
            prompt += '\nYou gave wrong format. Call the helper function again follow the right format'
    return prompt, result


def split_functions(response):
    helper_ftn_calls=[]
    response = response.replace("[ChatGPT]\n",'')
    statement = response.split("Statement: ")[0].split("Helper function: ")[0]
    functions = response.split("Helper function: ")[1]
    if '##' in functions:
        helper_ftn_calls = functions.split(' ## ')
    else :
        helper_ftn_calls = [functions]
    return helper_ftn_calls

def preprocess_ent(ent):
    if (ent[0]=='"' and ent[-1]=='"') or (ent[0]=="'" and ent[-1]=="'"):
        return ent[1:-1].replace(' ', '_').lower()
    else:
        return ent.replace(' ', '_').lower()

def get_relations(entity_list):
    #print(f"befor enetity:{entity}")
    entity_list = [preprocess_ent(entity) for entity in entity_list]
    #print(f"after entity:{entity}")
    relation_list = {}
    for entity in entity_list:
        relation_list[entity] = db.getRelationsFromEntity(entity)
    print(f"reltaion list of called fucntion:{relation_list}")
    return relation_list

def explore_kg(entity, relations, info):
    #print(f"entity:{entity}, relations:{relations}")
    entity = preprocess_ent(entity)
    triple_sets= []
    for rel in relations:
        rel = rel[1:-1]
        # if (entity, rel) in info.entrel:
        #     info.setState(-1)
        #     return []
        # else: info.entrel.append((entity, rel))
        #print(f"looking entity:{entity}, relation:{rel}")
        tails = db.getEntityFromEntRel(entity, rel)
        for tail in tails:
            if tail == info.gt_entity: continue
            tmp = [entity,rel,tail]
            triple_sets.append(tmp)
    #print(f'triple sets:{triple_sets}')
    return triple_sets

def score(predict, label,f):
    per_score = len(label)
    abs, correct, wrong = 0, 0, 0
    print(f"predict:{predict}\nlabel:{label}")
    if 'abstain' in str(predict).lower():
        abs+=1
        f.write('\nabstain!')

    else:
        new_pred_list, new_label_list = [],[]
        # predict_list = predict.split(', ')
        predict_list = predict

        for pred in predict_list:
            new_pred_list.append(preprocess_ent(pred))
        for lab in label:
            # lab_tmp = re.sub(r"[^a-zA-Z0-9]", "", lab.lower())
            new_label_list.append(preprocess_ent(lab))
        
        # print(new_pred_list, new_label_list)

        for new_pred in new_pred_list:
            if new_pred in new_label_list:
                correct += 1/per_score
            else:
                wrong += 1/per_score

        if correct > 0: f.write('\nCorrect!')
        else: f.write('\nWrong')        
    
    f.write(f'\nscore: {correct}, {wrong}')

    return abs, correct, wrong
    
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", type=str, default="three_hop")
    parser.add_argument("--num_iter", type = int, default = "10")
    parser.add_argument("--model", type = str, default= "gpt-4o-mini")
    parser.add_argument("--prompt", type = str, default= "initial_prompt")
    args = parser.parse_args()
    
    
    save_path = f"./prompt_variant_result_20241107"
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    
    # Load proper dataset
    if args.type=='one_hop':
        file_pth = "../data/onehop_test_set.jsonl"
    elif args.type =='two_hop':
        file_pth = "../data/twohop_test_set.jsonl"
    elif args.type == 'three_hop':
        file_pth = "../data/threehop_test_set.jsonl"
    else:
        print("wrong argument")

    # Load prompt
    if args.prompt == "initial_prompt":
        prompt_template = initial_prompt
    elif args.prompt == "pr1_singlecall":
        prompt_template = pr1_singlecall
    elif args.prompt == "pr1_singlecall_with_multiple_entities":
        prompt_template = pr1_singlecall_with_multiple_entities
    
    result = {}
    questions_dict = {}
    entity_set_dict = {}
    label_set_dict = {}
    types_dict ={}
    answer_list = []
    
    with open(os.path.expanduser(file_pth)) as f:
        for line in f:
            if not line:
                continue
            q = json.loads(line)
            questions_dict[q["question_id"]] = q["question"]
            entity_set_dict[q["question_id"]] = q["entity_set"]
            label_set_dict[q["question_id"]] = q["Label"]
    
            
    iter_num_list=[]
    total_correct, total_abs,total_wrong, total_sample =0,0,0,0
    answer_list= [['qid','correct','wrong','prediction','gt_label']]
    # with open(os.path.join(save_path,f"{args.type}.txt"),'a') as f:
    #     for qid, question in questions_dict.items():
    for qid, question in questions_dict.items():
        with open(os.path.join(save_path, f"result_{args.type}_{args.model}_maxiter_{args.num_iter}_prompt_{args.prompt}.txt"),'a') as f:
            if qid > 1000:
                break
            if qid % 20 != 0:
                continue
            print(f"Qid:{qid}")
            question = questions_dict[qid]
            label = label_set_dict[qid]
            entities = entity_set_dict[qid]
            
            f.write(f"\n\n\nQid:{qid}\nQuestion :{question}")
            f.write(f"GT entity:{entities}")
            
            prompt = prompt_template.replace('<<<<CLAIM>>>>', question).replace('<<<<GT_ENTITY>>>>', str(entities))
            
            prediction, iter_num = reasoning(prompt, label, entities, args.num_iter, args.model, f)
            abs, correct, wrong= score(prediction, label, f)
            total_correct += correct
            total_wrong += wrong
            total_abs += abs
            total_sample +=1
            iter_num_list.append(iter_num)
            answer_list.append([qid,correct,wrong,str(prediction), str(label)])

            f.close()
        
        if (total_sample - total_abs) ==0 :
            metric1 = 0
        else:
            metric1 = (total_sample - total_abs ) /  total_sample
        if total_correct==0:
            metric2 = 0
        else:
            metric2 = total_correct / (total_sample - total_abs)
        if (total_correct-total_wrong)==0 :
            metric3 = 0
        else:
            metric3 = (total_correct-total_wrong) / (total_sample - total_abs)

        with open(os.path.join(save_path, f"result_{args.type}_{args.model}_maxiter_{args.num_iter}_prompt_{args.prompt}.txt"),'a') as f:
            f.write(f"\n\nTotal sample:{total_sample}, Total_Correct:{total_correct}, Total_Wrong:{total_wrong}, Total_abstain:{total_abs}")
            f.write(f"metric1:{metric1}, metric2:{metric2}, metric3 :{metric3}")
            f.write(f"avg iter:{np.average(iter_num_list)}\n max_iter:{np.max(iter_num_list)}\n min_iter:{np.min(iter_num_list)}")
        
    f= open(f"./prompt_variant_result_20241107/only_answer_{args.type}_{args.model}_maxiter_{args.num_iter}_prompt_{args.prompt}.csv",'w')
    writer= csv.writer(f)
    writer.writerows(answer_list)
    f.close()