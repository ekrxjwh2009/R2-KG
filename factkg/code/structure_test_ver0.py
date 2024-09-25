"""Generate answers with GPT-3.5-turbo"""
# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import argparse
import json
import os
import re
import pickle
from collections import defaultdict
import helper_function as helper
import fair_qid as qid_test
from tqdm import tqdm
from chatbot import Chatbot
from prompt.factkg_prompt import prompt

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


def get_answer(qid: int, claim: str, gt_entities: list, top_k: int, max_tokens: int):
    #### 1. 
    chatbot = Chatbot()

    prom = prompt.replace('<<<<CLAIM>>>>', claim).replace('<<<<GT_ENTITY>>>>', str(gt_entities))
    res = chatbot.chat_with_history2(prom)
    print(res)

    # Extracting helper function included string
    flag = False
    label = ''
    chat_history = []
    chat_history.append(res)
    for trial in range(7):
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
        if 'Abstain' in helper_str:
            flag = False
            break
        print(helper.helper_function_parser(helper_str, chat_history))

        if not 'confidenceCheck' in helper_str:
            chat_history.append(helper.helper_function_parser(helper_str, chat_history))
        res = chatbot.chat_with_history2(helper.helper_function_parser(helper_str, chat_history))
        # print(chatbot.chat_history)
        if not 'confidenceCheck' in res:
            chat_history.append(res)
        print(res)
    
    if not flag:
        print("I Don't Know!")
        label = 'IDK'

    # print(chat_history)
    return label


if __name__ == "__main__":

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
    Error = []
    Dash = []
    Another = []

    question_types = {'num1' : 0, 'existence' : 0, 'multi claim' : 0, 'multi hop' : 0}

    for qid, question in tqdm(questions_dict.items()):

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
            elif qid in qid_test.multihop_false:
                qtype = 'multihop_false'
            question_types['multi hop'] += 1
        else:
            continue

        flag = 'Error'
        future = ''

        try:
            future = get_answer(qid, question, entity_set_dict[qid], top_k = 5, max_tokens=1024)
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
        with open("../result/3helper_20240903/wrong_cases_0913/{}.jsonl".format(qtype), 'a', encoding = 'utf-8') as outfile:
            json_str = json.dumps(dict, ensure_ascii=False)
            outfile.write(json_str + '\n')

        print(question_types)
        
    print('Correct: ', len(Correct), Correct)
    print('Wrong: ', len(Wrong), Wrong)
    print('IDK: ', len(IDK), IDK)
    print('Error: ', len(Error), Error)
    print('Result: ', len(Correct)/len(list(result)))
