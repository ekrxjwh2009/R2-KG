# 06-25
"""Generate answers with GPT-3.5"""
# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import argparse
import json
import os
import time
import re
import openai
import tqdm
import shortuuid
import pickle
import ast
import dbpedia_sparql as db
import helper_function as helper
from tqdm import tqdm
from chatbot import Chatbot
from prompt.metaqa_prompt import prompt_fusion


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

def get_answer(qid: int, claim: str, gt_entity: str, KG: dict, top_k: int, max_tokens: int, iteration_trial):
    ans = {
        "answer_id": shortuuid.uuid(),
    }
    entities = re.findall(r'\[(.*?)\]', claim)

    rel_dict = {}
    ent_dict = {}
    labels = []

    # for gt_entity_elem in gt_entity:
    gt_entity_lower = gt_entity.strip('"').replace(' ', '_').lower()
    ent_dict[gt_entity_lower] = []
    rel_dict[gt_entity_lower] = db.getRelationsFromEntity(gt_entity_lower, noInverse = True)
    
    # print(gt_entity_lower)

    # Create Chatbot for GPT-User communication
    chatbot = Chatbot()

    pr = prompt_fusion.replace('<<<<CLAIM>>>>', claim).replace('<<<<GT_ENTITY>>>>', gt_entity)

    res = chatbot.chat_with_history2(pr)
    # print(res)

    chat_history = []
    chat_history.append(res)

    # Extracting helper function included string
    flag = False
    used_relation = []
    for trial in range(10):
        helper_str = ''
        for line in reversed(res.splitlines()):
            if 'Helper function: ' in line:
                helper_str = line
                break
        
        if 'Verification' in helper_str:
            flag = True
            labels = helper.helper_function_parser(helper_str, chat_history)
            labels = ast.literal_eval(labels.split('Execution result: ')[1])
            break
        # print(helper.helper_function_parser(helper_str, used_relation))
        if not 'confidenceCheck' in helper_str:
            chat_history.append(helper.helper_function_parser(helper_str, chat_history))
        res = chatbot.chat_with_history2(helper.helper_function_parser(helper_str, chat_history))
        # print(chatbot.chat_history)
        if not 'confidenceCheck' in res:
            chat_history.append(res)
        # print(res)
        
    
    if not flag:
        print("I Don't Know!")
    

    return list(set(labels))

def f1_score(label, pred):
    label_len = len(label)
    pred_len = len(pred)

    for i in range(pred_len): pred[i] = pred[i].replace(' ', '_').lower()

    tp = 0
    for lab in label:
        lab = lab.replace(' ', '_').lower()
        if lab in pred:
            tp += 1
    
    fn = label_len - tp
    fp = pred_len - tp

    try:
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
    except:
        return 0

    if (precision + recall) == 0:
        return 0
    
    f1 = (2 * precision * recall) / (precision + recall)

    return f1



if __name__ == "__main__":

    futures = []
    start_token = 0
    
    ####For new experiment, use it.
    result = {}
    questions_dict = {}
    entity_set_dict = {}
    label_set_dict = {}
    with open(os.path.expanduser(f"../data/twohop_test_set.jsonl")) as f:
        for line in f:
            if not line:
                continue
            q = json.loads(line)
            questions_dict[q["question_id"]] = q["question"]
            entity_set_dict[q["question_id"]] = q["entity_set"]
            label_set_dict[q["question_id"]] = q["Label"]

    Correct = []
    Wrong = []
    Error = []
    Another = []
    futures = []
    
    f1_score_total = 0
    qid_count = 0

    for qid, question in tqdm(questions_dict.items()):
        if qid > 10000:
            continue
        
        if qid % 20 != 0:
            continue

        f1_score_total = f1_score_total * qid_count
        qid_count += 1
        
        flag = 'Error'

        # try:
        future = get_answer(qid, question, entity_set_dict[qid][0], KG=metakg, top_k = 5, max_tokens=1024, iteration_trial = 3)
        is_correct = 0

        lower_label = []
        for lab in label_set_dict[qid]:
            lab = lab.replace(' ', '_').lower()
            for future_elem in future:
                if lab in future_elem.lower():
                    is_correct += 1
                    break

        f1 = f1_score(label_set_dict[qid], future)
        print('qid f1 score : ', f1)
        f1_score_total = (f1_score_total + f1) / qid_count

        if is_correct > 0:
            Correct.append(qid)
            # print(qid, ': Correct!')
            result[qid] = 'Correct'
            flag = 'Correct'
        else:
            Wrong.append(qid)
            # print(qid, ': Wrong...')
            result[qid] = 'Wrong'
            flag = 'Wrong'

        # except Exception as e:
        #     # print(e)
        #     Error.append(qid)
        #     # print(qid, ': Error...')
        #     result[qid] = 'Error'
        #     flag = 'Error'
        #     f1_score_total = f1_score_total / qid_count
        
        # print('current total hit@1 score : ', len(Correct), ' / ', qid_count)
        print('current total f1 score : ', f1_score_total)
        # with open(f'/nfs_edlab/jschoi/share_code/metaqa/twohop_result.pickle', 'wb') as f:
        #     pickle.dump(result, f)
    
        dict = {"question_id": qid, "question" : question, "prediction" : future, "gt_label" : label_set_dict[qid], "correctness": flag}
        with open("/nfs_edlab/jschoi/share_code/metaqa/unified/analysis/3helper_datasetintegrated_0912/onehop_fusion_gpt4omini.jsonl", 'a', encoding = 'utf-8') as outfile:
            json_str = json.dumps(dict, ensure_ascii=False)
            outfile.write(json_str + '\n')

    print('Correct: ', len(Correct), Correct)
    print('Wrong: ', len(Wrong), Wrong)
    print('Error: ', len(Error), Error)
    print('Result: ', len(Correct)/len(list(result)))
