
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
import sample_number

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

def reasoning(original_prompt):
            
    
    engine = "gpt-4o-mini-2024-07-18"
    chatbot = OpenAIBot(engine, client)
    response = chatbot.generate_response(prompt)

    return response


original_prompt = """
Your task is to verify the claim is True of False.
The format of claim can be explanatory sentence, reasoning sentence, riddle sentence, request sentence..etc.
You must pick 'true' or 'false'. 
Sometimes, some pronouns appeared in the claim, then use your knowledge to deduce what the pronoun in the sentence is.

For example)
Claim : Were you aware that Richard Hatfield had a successor.
Your answer : 'true'

Claim : I heard that James T. McIntyre had a successor.
Your answer : 'true'

Question : His name is Andrew Mwesigwa. He had a youthclub.
Your answer : 'false'

Now, it's your turn.
Question : <<<<CLAIM>>>>
Your answer : 

"""


if __name__ == "__main__":
    
    #python original_reasoning.py --type num1 --data test --model gpt-4o-mini
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", type=str, default="existence")
    parser.add_argument("--model", type = str, default='gpt-4o-mini')
    parser.add_argument("--data", type =str, default="test")
    args = parser.parse_args()
    
    if args.type == 'existence': qid_list = sample_number.existence
    elif args.type =="num1" : qid_list = sample_number.num1
    elif args.type =='multi_claim' : qid_list = sample_number.multi_claim
    elif args.type =="multi_hop" : qid_list = sample_number.multi_hop
    else:
        print("Wrong argument")
    
    save_path = f"results_{args.data}/Baseline/{args.model}/{args.type}"
    question_path = f"/home/smjo/KG-gpt2_cronKG/CronQA_data/wikidata_big/questions/{args.type}.json"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        
    
    
    result = {}
    questions_dict = {}
    entity_set_dict = {}
    label_set_dict = {}
    types_dict ={}
    if args.data =='dev':
        f= open("/home/smjo/share_code/factkg/data/extracted_train_set.jsonl")
    elif args.data =='test':
        f= open("/home/smjo/share_code/factkg/data/extracted_test_set.jsonl")
    else : 
        print('Wrong argument')
    for line in f:
        if not line:
            continue
        q = json.loads(line)

        questions_dict[q["question_id"]] = q["question"]
        entity_set_dict[q["question_id"]] = q["entity_set"]
        label_set_dict[q["question_id"]] = q["Label"]
        types_dict[q['question_id']] = q["types"] 
    f.close()
    
    
    answer_list= [['qid','prediction','gt_label']]
    for qid in qid_list:
        print(f"Qid:{qid}")
        question = questions_dict[qid]
        label = label_set_dict[qid]
        entities = entity_set_dict[qid]
        

        prompt = original_prompt.replace('<<<<CLAIM>>>>', question)

        prediction= reasoning(prompt)
        ff= open(os.path.join(save_path, f"only_answer.csv"), 'a')
        writer= csv.writer(ff)
        writer.writerow([qid, prediction, label])
        ff.close()    