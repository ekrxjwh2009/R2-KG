# Test code from helper function prompt including abstention method
# both systemetic way and LLM-wise way
import argparse
import json
import os
import re
import pickle
from collections import defaultdict
import dbpedia_sparql as db
import chain_test as chain
import helper_function as helper
import fair_qid as qid_test
# import query_form as sparql
import query_form_with_rel as sparql
from tqdm import tqdm
from chatbot import Chatbot
from individual_claim_info import Information
from prompt.factkg_prompt import prompt
from prompt.factkg_prompt import prompt_wo_statement


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

        
def get_answer(qid: int, claim: str, gt_entities: list, top_k: int, max_tokens: int, max_iter: int):

    information = Information(qid, claim, gt_entities)

    #### 1. 
    chatbot = Chatbot()

    chat_iter = 0

    prom = prompt.replace('<<<<CLAIM>>>>', claim).replace('<<<<GT_ENTITY>>>>', str(gt_entities))
    res = chatbot.chat_with_history2(prom)
    chat_iter += 1
    
    print(res)

    # TODO : Add token error handling code here

    # Extracting helper function included string
    flag = False
    label = ''

    chat_history = []
    chat_history.append(res)

    while chat_iter <= max_iter:

        print('==============================================')
        helper_str = ''
        for line in reversed(res.splitlines()):
            if 'Helper function: ' in line:
                helper_str = line
                break
        
        if 'Verification' in helper_str:
            flag = True
            if 'True' in helper_str:
                label = True
            else:
                label = False
            break

        if 'getRelation' in helper_str:
            prev_history = chatbot.chat_history
            prev_res = res
        
        # prev_history = chatbot.chat_history
        # prev_res = res
        execution_result = helper.helper_function_parser(helper_str, chat_history, information)
        print(execution_result)

        if information.state == -1:
                flag = False
                break
        elif information.state == -4:
            res = prev_res
            chatbot.chat_history = prev_history
            information.set_abstain(1)
            continue

        res = chatbot.chat_with_history2(execution_result)
        print(res)
        chat_iter += 1
        
        
        chat_history.append(res)
    
    if not flag:
        if information.state == -1:
            print(str(qid), "Abstain - same pair of entrel")
            label = 'Abstain'

        else: 
            print(str(qid), "I Don't Know! - max iteration")
            label = 'IDK'

    return label


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max_iter", type = int,
                        default = 6, help = "max iteration (LLM-User communication) limit")

    args = parser.parse_args()
    
    futures = []
    start_token = 0
    
    ####For new experiment, use it.
    result = {}
    questions_dict = {}
    entity_set_dict = {}
    label_set_dict = {}
    types_dict = {}
    with open(os.path.expanduser(f"../data/extracted_dev_set.jsonl")) as f:
        for line in f:
            if not line:
                continue
            q = json.loads(line)
            questions_dict[q["question_id"]] = q["question"]
            entity_set_dict[q["question_id"]] = q["entity_set"]
            label_set_dict[q["question_id"]] = q["Label"]
            types_dict[q["question_id"]] = q["types"]

    Correct = []
    Wrong = []
    IDK = []
    Abstain = []
    Error = []
    Dash = []
    Another = []

    question_types = {'num1' : 0, 'existence' : 0, 'multi claim' : 0, 'multi hop' : 0}


    for qid, question in tqdm(questions_dict.items()):

        # if qid not in [194, 203]: continue

        question  = questions_dict[qid]
        question_type = types_dict[qid]

        qtype = ''

        # If you wanna check True / False seperately, uncomment the middle part of each statement.
        if qid in qid_test.existence_total:
            qtype = 'existence'
            if qid in qid_test.existence_true:
                qtype = 'existence_true'
            elif qid in qid_test.existence_false:
                qtype = 'existence_false'
            question_types['existence'] += 1

        elif qid in qid_test.num1_total:
            qtype = 'num1'
            if qid in qid_test.num1_true:
                qtype = 'num1_true'
            elif qid in qid_test.num1_false:
                qtype = 'num1_false'
            question_types['num1'] += 1

        elif qid in qid_test.multiclaim_total:
            qtype = 'multiclaim'
            if qid in qid_test.multiclaim_true:
                qtype = 'multiclaim_true'
            elif qid in qid_test.multiclaim_false:
                qtype = 'multiclaim_false'
            question_types['multi claim'] += 1

        elif qid in qid_test.multihop_total:
            qtype = 'multihop'
            if qid in qid_test.multihop_true:
                qtype = 'multihop_true'
                # continue
            elif qid in qid_test.multihop_false:
                qtype = 'multihop_false'
            question_types['multi hop'] += 1
        else:
            continue
        
        flag = 'Error'
        future = ''

        try:
            future = get_answer(qid, question, entity_set_dict[qid], top_k = 5, max_tokens=1024, max_iter = args.max_iter)
            futures.append(future)
            if future == 'Another Answer':
                # Another.append(qid)
                Error.append(qid)
                result[qid] = 'Error'
                flag = 'Error'
            elif future == 'IDK':
                IDK.append(qid)
                # print(qid, ': I Dont Know...')
                result[qid] = 'IDK'
                flag = 'IDK'
            elif future == 'Abstain':
                Abstain.append(qid)
                result[qid] = 'Abstain'
                flag = 'Abstain'
            elif future == label_set_dict[qid][0]:
                Correct.append(qid)
                # print(qid, ': Correct!')
                result[qid] = 'Correct'
                flag = 'Correct'
            else:
                Wrong.append(qid)
                # print(qid, ': Wrong...')
                result[qid] = 'Wrong'
                flag = 'Wrong'
        except:
            Error.append(qid)
            # print(qid, ': Error...')
            result[qid] = 'Error'
            flag = 'Error'
        
        dict = {"question_id": qid, "question" : question, "prediction" : future, "correctness": flag}
        with open("../result/abstention_ver5_20240928/test/{}.jsonl".format(qtype), 'a', encoding = 'utf-8') as outfile:
            json_str = json.dumps(dict, ensure_ascii=False)
            outfile.write(json_str + '\n')

        print(question_types)
        
    print('Correct: ', len(Correct), Correct)
    print('Wrong: ', len(Wrong), Wrong)
    print('Abstain: ', len(Abstain), Abstain)
    print('IDK: ', len(IDK), IDK)
    print('Error: ', len(Error), Error)
    print('Result: ', len(Correct)/len(list(result)))
