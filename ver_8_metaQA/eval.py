import csv
import re
import argparse

def score(predict, label):
    per_score = len(label)
    abs, correct, wrong =0,0,0

    new_pred_list, new_label_list = [],[]
    
    predict = predict.split(',')
    label = label.split(',')
    for pred in predict:
        pred_tmp = re.sub(r"[^a-zA-Z0-9]", "", pred.lower())
        new_pred_list.append(pred_tmp)
    for lab in label:
        lab_tmp = re.sub(r"[^a-zA-Z0-9]", "", lab.lower())
        new_label_list.append(lab_tmp)

    
    if 'abstain' in new_pred_list:
        abs+=1
    
    else:   
        for new_pred in new_pred_list:
            if new_pred in new_label_list:
                correct = 1
        
        if correct ==0:
            wrong =1
                    
    
    return abs, correct, wrong


#[['qid','ensemble prediction(=common elements)','gt_label']]


parser = argparse.ArgumentParser()
parser.add_argument("--result_pth", type=str, default="two_hop")
args = parser.parse_args()
#result_pth = f"/home/smjo/KG-gpt2/ver_8_metaQA/result_{args.result_pth}_gpt3.5_maxiter_30_multicalls_temp0/only_result.csv"
result_pth = "/home/smjo/KG-gpt2/ver_8_metaQA/result_three_hop_gpt4mini_maxiter_20_multicalls_temp0/only_result.csv"
total_sample,at_least_correct,total_abs, at_least_wrong =0,0,0, 0
with open(result_pth, newline='') as csvfile:
    spamreader = csv.reader(csvfile)
    for i,row in enumerate(spamreader):
        if i==0: 
            continue
        predict = row[1]
        label = row[2]
        abs, correct, wrong = score(predict, label)
        total_sample += 1
        at_least_correct +=correct
        at_least_wrong += wrong
        total_abs+= abs

print(total_sample,at_least_correct,at_least_wrong, total_abs)
        