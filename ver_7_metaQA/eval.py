import csv
import re
import argparse

def score(predict, label):
    per_score = len(label)
    abs, correct, wrong =0,0,0
    if 'abstain' in str(predict).lower():
        abs+=1

    else:
        new_pred_list, new_label_list = [],[]
        predict_list = predict.split(', ')
        for pred in predict_list:
            pred_tmp = re.sub(r"[^a-zA-Z0-9]", "", pred.lower())
            new_pred_list.append(pred_tmp)
        for lab in label:
            lab_tmp = re.sub(r"[^a-zA-Z0-9]", "", lab.lower())
            new_label_list.append(lab_tmp)

        for new_pred in new_pred_list:
            if new_pred in new_label_list:
                correct = 1
        
        if correct ==0:
            wrong =1
                    
    
    return abs, correct, wrong



parser = argparse.ArgumentParser()
parser.add_argument("--result_pth", type=str, default="two_hop")
args = parser.parse_args()
result_pth = f"./result_{args.result_pth}_gpt3.5_maxiter_15_multicalls_temp0/only_result.csv"

total_sample,at_least_correct,total_abs, at_least_wrong =0,0,0, 0
with open(result_pth, newline='') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        predict = row[3]
        label = row[4].split(', ')
        abs, correct, wrong = score(predict, label)
        total_sample += 1
        at_least_correct +=correct
        at_least_wrong += wrong
        total_abs+= abs
        
print(total_sample,at_least_correct,at_least_wrong, total_abs)
        