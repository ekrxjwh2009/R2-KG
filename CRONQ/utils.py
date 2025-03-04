import os, sys
import pickle
import json
import csv
from collections import defaultdict

sys.path.append(os.path.dirname(__file__))
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import prompt_main, prompt_sub, prompt_single
from paraphraser import paraphrase
from r2kg_chatbot import reasoning

def make_data():
    print("Making dataset")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    gt_pth = os.path.join(script_dir, './data/wikidata_big')

    split = 'test'
    filename = os.path.join(gt_pth, 'questions/{split}.pickle'.format(split=split))
    questions = pickle.load(open(filename, 'rb'))
    
    KG_pth = os.path.join(gt_pth, 'kg/full.txt')
    entid_2_txt_pth = os.path.join(gt_pth, 'kg/wd_id2entity_text.txt')
    relid_2_txt_pth = os.path.join(gt_pth, 'kg/wd_id2relation_text.txt')
    kg_dataset = open(KG_pth, 'r').readlines()
    entid2txt = open(entid_2_txt_pth,'r').readlines()
    relid2txt = open(relid_2_txt_pth,'r').readlines()

    entid2txt_dict, relid2txt_dict = {},{}
    non_exist_ent, non_exist_rel = 0, 0
    for line in entid2txt:
        line = line.rstrip()
        try :
            id, ent = line.split('\t')
        except :
            non_exist_ent += 1
            continue
        entid2txt_dict[id] = ent
        
    for line in relid2txt:
        line = line.rstrip()
        try: 
            id, rel = line.split('\t')
        except :
            non_exist_rel += 1
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
            inverse_rel = '~' + rel
            tail = entid2txt_dict[tail_id]
        except:
            non_exist_graph += 1
            continue
        full_KG[head].append([head, rel, tail ,start_time, end_time])
        full_KG[tail].append([tail, inverse_rel, head, start_time, end_time])
    
    return full_KG, entid2txt_dict, relid2txt_dict

def parsing_question(question_path, entid2txt_dict, relid2txt_dict):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    gt_pth = os.path.join(script_dir, './data/wikidata_big')

    question_path = os.path.join(gt_pth, question_path)

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

def main(args):
    if args.prompt =='pr_1': 
        sub_prompt = prompt_sub.pr_1 
        main_prompt = prompt_main.pr_1 if not args.single_agent else prompt_single.pr_1
    elif args.prompt =='pr_2': 
        sub_prompt = prompt_sub.pr_2
        main_prompt = prompt_main.pr_2 if not args.single_agent else prompt_single.pr_2
    else : 
        sub_prompt = prompt_sub.pr_3
        main_prompt = prompt_main.pr_3 if not args.single_agent else prompt_single.pr_3
    
    if args.single_agent: save_path = f"./results/single_agent/"
    else: save_path = f"./results/dual_agent/"

    save_path = os.path.join(os.path.dirname(__file__), save_path)
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    full_KG, entid2txt_dict, relid2txt_dict = make_data()
    time_join_question_path = "./questions/time_join.json"
    simple_time_question_path = "./questions/simple_time.json"
    simple_entity_question_path = "./questions/simple_entity.json"
    time_join_qa_list = parsing_question(time_join_question_path, entid2txt_dict, relid2txt_dict)
    simple_time_qa_list = parsing_question(simple_time_question_path, entid2txt_dict, relid2txt_dict)
    simple_entity_qa_list = parsing_question(simple_entity_question_path, entid2txt_dict, relid2txt_dict)

    qa_list_dict = [time_join_qa_list,simple_time_qa_list,simple_entity_qa_list]
    qid_list_dict = {0:[i for i in range(len(time_join_qa_list))] , 1:[i for i in range(len(simple_time_qa_list))], 2:[i for i in range(len(simple_entity_qa_list))]}

    if args.paraphrase:
        for order, qa_list in enumerate(qa_list_dict):
            qid_list = qid_list_dict[order]

            for qid in qid_list:
                original_question = qa_list[qid]['question']
                paraphrase_list = paraphrase(original_question, prompt_main.paraphrase_prompt)

                for i in range(3):
                    question = paraphrase_list[i]

                    if args.single_agent:
                        result_filename = f"op_{args.operator}_iter_{args.iter_limit}_{args.prompt}_temp_{args.temperature}_topp_{args.top_p}_paraphrase_{i}"
                    else:
                        result_filename = f"op_{args.operator}_sup_{args.supervisor}_iter_{args.iter_limit}_{args.prompt}_temp_{args.temperature}_topp_{args.top_p}_paraphrase_{i}"

                    with open(os.path.join(save_path, f"{result_filename}.txt"),'a') as f:
                        print(f"Qid: {qid}\nQuestion: {question}")
                        label = qa_list[qid]['answers']
                        entities = qa_list[qid]['given_entities']
                        
                        f.write(f"\n\n\nQid: {qid}\nQuestion: {question}\n")
                        f.write(f"GT entity: {entities}")
                        
                        prompt = main_prompt.replace('<<<Question>>>', question).replace('<<<Entity set>>>', str(entities))
                        
                        prediction, _ = reasoning((args.operator, args.temperature, args.top_p), args.supervisor, question, args.iter_limit, prompt, sub_prompt, entities, f, KG=full_KG)
                        
                        with open(os.path.join(save_path, f"{result_filename}.csv"),'a') as ff:
                            writer= csv.writer(ff)
                            writer.writerow([qid, prediction, label])

    else:
        for order, qa_list in enumerate(qa_list_dict):
            qid_list = qid_list_dict[order]
            for qid in qid_list:
                if args.single_agent:
                    result_filename = f"op_{args.operator}_iter_{args.iter_limit}_{args.prompt}_temp_{args.temperature}_topp_{args.top_p}"
                else:
                    result_filename = f"op_{args.operator}_sup_{args.supervisor}_iter_{args.iter_limit}_{args.prompt}_temp_{args.temperature}_topp_{args.top_p}"

                with open(os.path.join(save_path, f"{result_filename}.txt"),'a') as f:
                    print(f"Qid: {qid}")
                    question = qa_list[qid]['question']
                    label = qa_list[qid]['answers']
                    entities = qa_list[qid]['given_entities']
                    
                    f.write(f"\n\n\nQid: {qid}\nQuestion: {question}\n")
                    f.write(f"GT entity: {entities}")
                    
                    prompt = main_prompt.replace('<<<Question>>>', question).replace('<<<Entity set>>>', str(entities))
                    
                    prediction, _ = reasoning((args.operator, args.temperature, args.top_p), args.supervisor, question, args.iter_limit, prompt, sub_prompt, entities, f, KG=full_KG)
                    
                    with open(os.path.join(save_path, f"{result_filename}.csv"),'a') as ff:
                        writer= csv.writer(ff)
                        writer.writerow([qid, prediction, label])
