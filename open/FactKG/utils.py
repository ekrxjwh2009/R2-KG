import os, sys
import pickle
import json
import csv
from collections import defaultdict

sys.path.append(os.path.dirname(__file__))
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import prompt_main, prompt_sub
from chatbot_2Agent_openai import reasoning


def main(args):
    if args.prompt =='pr_1': 
        main_prompt = prompt_main.pr_1
        save_path = f"./results_final/2Agent/{args.model}/sub_{args.subagent}/result_pr1/"
    elif args.prompt =='pr_2': 
        main_prompt = prompt_main.pr_2
        save_path = f"./results_final/2Agent/{args.model}/sub_{args.subagent}/result_pr2/"
    else : 
        main_prompt = prompt_main.pr_3
        save_path = f"./results_final/2Agent/{args.model}/sub_{args.subagent}/result_pr3/"
    
    sub_prompt = prompt_sub.sub_1

    if not os.path.exists(save_path):
        os.makedirs(save_path)


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
    
    qid_list = questions_dict.keys()
    
    for qid in qid_list:
        with open(os.path.join(save_path,'log.txt'),'a') as f:
            print(f"Qid:{qid}")
            question = questions_dict[qid]
            label = label_set_dict[qid]
            entities = entity_set_dict[qid]
            
            f.write(f"\n\n\nQid:{qid}\nQuestion :{question}")
            f.write(f"GT entity:{entities}")
            
            prompt = main_prompt.replace('<<<<CLAIM>>>>', question).replace('<<<<GT_ENTITY>>>', str(entities))

            prediction, _ = reasoning(args.model, args.subagent, question, args.iter_limit, prompt, sub_prompt, entities, f)
            tmp = [qid, str(prediction), str(label[0])]

            with open(os.path.join(save_path, f"{args.iter_limit}_only_result.csv"),'a') as ff:
                writer = csv.writer(ff)
                writer.writerow(tmp)
