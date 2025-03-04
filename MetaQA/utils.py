import os, sys
import json
import csv

sys.path.append(os.path.dirname(__file__))
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import prompt_main, prompt_sub, prompt_single
from paraphraser import paraphrase
from r2kg_chatbot import reasoning

# For MetaQA to ignore gt_entity in final prediction (even if makes sense, author of MetaQA has not used it)
class Information:
    def __init__(self, gt_entity):
        self.gt_entity = gt_entity

def main(args):
    if args.prompt =='pr_1':
        main_prompt = prompt_main.pr_1 if not args.single_agent else prompt_single.pr_1
    elif args.prompt =='pr_2': 
        main_prompt = prompt_main.pr_2 if not args.single_agent else prompt_single.pr_2
    else: 
        main_prompt = prompt_main.pr_3 if not args.single_agent else prompt_single.pr_3
    
    sub_prompt = prompt_sub.sub_prompt

    if args.single_agent: save_path = f"./results/single_agent/"
    else: save_path = f"./results/dual_agent/"

    save_path = os.path.join(os.path.dirname(__file__), save_path)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    questions_dict = {}
    entity_set_dict = {}
    label_set_dict = {}

    with open(os.path.join(os.path.dirname(__file__), "./data/threehop_test_set.jsonl"), 'r') as f:
        for line in f:
            if not line:
                continue
            q = json.loads(line)
            questions_dict[q["question_id"]] = q["question"]
            entity_set_dict[q["question_id"]] = q["entity_set"]
            label_set_dict[q["question_id"]] = q["Label"]
    
    if args.paraphrase:
        for qid, question in questions_dict.items():
            paraphrase_list = paraphrase(question, prompt_main.paraphrase_prompt)

            for i in range(3):
                question = paraphrase_list[i]

                if args.single_agent:
                    result_filename = f"op_{args.operator}_iter_{args.iter_limit}_{args.prompt}_temp_{args.temperature}_topp_{args.top_p}_paraphrase_{i}"
                else:
                    result_filename = f"op_{args.operator}_sup_{args.supervisor}_iter_{args.iter_limit}_{args.prompt}_temp_{args.temperature}_topp_{args.top_p}_paraphrase_{i}"

                with open(os.path.join(save_path, f"{result_filename}.txt"),'a') as f:
                    print(f"Qid: {qid}\nQuestion: {question}")
                    label = label_set_dict[qid]
                    entities = entity_set_dict[qid]

                    info = Information(entities[0])

                    f.write(f"\n\n\nQid: {qid}\nQuestion: {question}\n")
                    f.write(f"GT entity: {entities}")

                    prompt = main_prompt.replace('<<<<CLAIM>>>>', question).replace('<<<<GT_ENTITY>>>>', str(entities))

                    prediction, _ = reasoning((args.operator, args.temperature, args.top_p), args.supervisor, question, args.iter_limit, prompt, sub_prompt, entities, f, info=info)
                    tmp = [qid, str(prediction), str(label)]

                    with open(os.path.join(save_path, f"{result_filename}.csv"),'a') as ff:
                        writer = csv.writer(ff)
                        writer.writerow(tmp)

    else:
        for qid, question in questions_dict.items():
            if args.single_agent:
                result_filename = f"op_{args.operator}_iter_{args.iter_limit}_{args.prompt}_temp_{args.temperature}_topp_{args.top_p}"
            else:
                result_filename = f"op_{args.operator}_sup_{args.supervisor}_iter_{args.iter_limit}_{args.prompt}_temp_{args.temperature}_topp_{args.top_p}"

            with open(os.path.join(save_path, f"{result_filename}.txt"), 'a') as f:
                print(f"Qid: {qid}")
                question = questions_dict[qid]
                label = label_set_dict[qid]
                entities = entity_set_dict[qid]

                info = Information(entities[0])

                f.write(f"\n\n\nQid: {qid}\nQuestion: {question}\n")
                f.write(f"GT entity: {entities}")

                prompt = main_prompt.replace('<<<<CLAIM>>>>', question).replace('<<<<GT_ENTITY>>>>', str(entities))

                prediction, _ = reasoning((args.operator, args.temperature, args.top_p), args.supervisor, question, args.iter_limit, prompt, sub_prompt, entities, f, info=info)
                tmp = [qid, str(prediction), str(label)]

                with open(os.path.join(save_path, f"{result_filename}.csv"),'a') as ff:
                    writer = csv.writer(ff)
                    writer.writerow(tmp)
