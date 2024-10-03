import argparse
import json
import os
import re
import tqdm
import ast
import dbpedia_sparql as db
import helper_function as helper
from tqdm import tqdm
from chatbot import Chatbot
from individual_claim_info import Information
from prompt.metaqa_prompt import prompt_fusion


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

def get_answer(qid: int, claim: str, gt_entity: str, top_k: int, max_tokens: int, max_iter: int):

    gt_entity_lower = gt_entity.strip('"').replace(' ', '_').lower()

    information = Information(qid, claim, gt_entity_lower)

    labels = []
    chat_iter = 0

    # Create Chatbot for GPT-User communication
    chatbot = Chatbot()

    pr = prompt_fusion.replace('<<<<CLAIM>>>>', claim).replace('<<<<GT_ENTITY>>>>', gt_entity)
    res = chatbot.chat_with_history2(pr)
    chat_iter += 1

    print(res)

    # Have to be used in confidenceCheck, but not using in this version
    chat_history = []
    chat_history.append(res)

    # Extracting helper function included string
    flag = False

    while chat_iter <= max_iter: # 3
        helper_str = ''
        for line in reversed(res.splitlines()):
            if 'Helper function: ' in line:
                helper_str = line
                break
        
        if 'Verification' in helper_str:
            flag = True
            labels = helper.helper_function_parser(helper_str, chat_history, information)
            labels = ast.literal_eval(labels.split('Execution result: ')[1])
            break

        prev_history = chatbot.chat_history
        prev_res = res
        execution_result = helper.helper_function_parser(helper_str, chat_history, information)
        res = chatbot.chat_with_history2(execution_result)
        print(res)
        chat_iter += 1

        if 'exploreKG' in helper_str:
            if information.state == -1:
                flag = False
                break
            elif information.state == -4:
                res = prev_res
                chatbot.chat_history = prev_history
                continue

        chat_history.append(res)
        # print(res)
        
    if not flag:
        if information.state == -1:
            print(str(qid), "Abstain - same pair of entrel")
            labels = ['Abstain'] # Temporal form for abstained result (Have to be changed)

        else: 
            print(str(qid), "I Don't Know! - max iteration")
            labels = ['IDK']
    

    return list(set(labels))



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max_iter", type = int,
                        default = 7, help = "max iteration (LLM-User communication) limit")
    
    args = parser.parse_args()
    
    futures = []
    start_token = 0
    
    ####For new experiment, use it.
    result = {}
    questions_dict = {}
    entity_set_dict = {}
    label_set_dict = {}
    with open(os.path.expanduser(f"../data/threehop_test_set.jsonl")) as f:
        for line in f:
            if not line:
                continue
            q = json.loads(line)
            questions_dict[q["question_id"]] = q["question"]
            entity_set_dict[q["question_id"]] = q["entity_set"]
            label_set_dict[q["question_id"]] = q["Label"]

    #with open(f'./twohop_result.pickle', 'rb') as f:
    #    result = pickle.load(f)
    
    Correct = []
    Wrong = []
    IDK = []
    Abstain = []
    Error = []
    Another = []
    futures = []
    
    qid_count = 0

    for qid, question in tqdm(questions_dict.items()):
        if qid > 2000:
            continue

        if qid % 20 != 0:
            continue
            
        qid_count += 1
        
        flag = 'Error'
        future = ''

        try:
            future = get_answer(qid, question, entity_set_dict[qid][0], top_k = 5, max_tokens=1024, max_iter = args.max_iter)
            is_correct = 0

            lower_label = []
            for lab in label_set_dict[qid]:
                lab = lab.replace(' ', '_').lower()
                for future_elem in future:
                    if lab in future_elem.lower():
                        is_correct += 1
                        break

            if len(future) == 1 and future[0] == 'IDK':
                IDK.append(qid)
                result[qid] = 'IDK'
                flag = 'IDK'
                is_correct = -1
            elif len(future) == 1 and future[0] == 'Abstain':
                Abstain.append(qid)
                result[qid] = 'Abstain'
                flag = 'Abstain'
                is_correct = -1

            if is_correct > 0:
                Correct.append(qid)
                result[qid] = 'Correct'
                flag = 'Correct'
            elif is_correct == 0:
                Wrong.append(qid)
                result[qid] = 'Wrong'
                flag = 'Wrong'

        except Exception as e:
            # print(e)
            Error.append(qid)
            result[qid] = 'Error'
            flag = 'Error'
        
    
        dict = {"question_id": qid, "question" : question, "prediction" : future, "gt_label" : label_set_dict[qid], "correctness": flag}
        with open("../result/abstention_ver5_20240925/threehop_35turbo_gtignore_trial2.jsonl", 'a', encoding = 'utf-8') as outfile:
            json_str = json.dumps(dict, ensure_ascii=False)
            outfile.write(json_str + '\n')

    print('Correct: ', len(Correct), Correct)
    print('Wrong: ', len(Wrong), Wrong)
    print('Abstain: ', len(Abstain), Abstain)
    print('IDK: ', len(IDK), IDK)
    print('Error: ', len(Error), Error)
    print('Result: ', len(Correct)/len(list(result)))

