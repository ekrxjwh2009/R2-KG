import ast
import csv
import argparse



abs = 0
cor = 0
wro = 0
total_lab_wrong = 0

parser = argparse.ArgumentParser()
parser.add_argument("--output_file", type = str,
                    default = "./webqsp/only_answer_train_gpt-4o-mini_maxiter_15_temp_2.0_topp_0.1.csv", help = "output file")
parser.add_argument("--penalty", type = int,
                    default = 0, help = 'integer value for penalty term')

args = parser.parse_args()


def check_ensemble_res(ensemble_res_dict, label_dict):
    res = []
    cor, wro, abs = 0, 0, 0
    total_label_num = 0
    total_pred_num = 0
    total_wrong_num_in_pred = 0
    total_wrong_num_in_label = 0
    total_correct_num = 0

    for qid in ensemble_res_dict:
        # total_label_num += len(label_dict[qid])
        # total_pred_num += len(ensemble_res_dict[qid])

        if len(ensemble_res_dict[qid]) == 0:
            abs += 1
            # total_wrong_num_in_label += len(label_dict[qid])
            continue
        
        print(qid, len(label_dict[qid]), len(ensemble_res_dict[qid]))
        total_label_num += len(label_dict[qid])
        total_pred_num += len(ensemble_res_dict[qid])

        flag = False
        for p in ensemble_res_dict[qid]:
            if p in label_dict[qid]:
                total_correct_num += 1
                flag = True
            else:
                total_wrong_num_in_pred += 1

        for l in label_dict[qid]:
            if l not in ensemble_res_dict[qid]:
                total_wrong_num_in_label += 1

        cor += 1 if flag else 0
        wro += 1 if not flag else 0

    result_str = 'Correct : {0}, Wrong : {1}, Abstain : {2}\n'.format(cor, wro, abs)
    result_str += 'Total label num : {0}, Total pred num : {1}\n'.format(total_label_num, total_pred_num)
    result_str += 'Total correct num : {0}, Total wrong num in pred : {1}, Total wrong num in label : {2}\n'.format(total_correct_num, total_wrong_num_in_pred, total_wrong_num_in_label)
    # result_str += 'Ratio of wrong num in pred : {0}, Ratio of wrong num in label : {1}\n'.format(total_wrong_num_in_pred / total_pred_num, total_wrong_num_in_label / total_label_num)
    return result_str

def f1_score(tp, fp, fn):
    try:
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f1 = 2 * precision * recall / (precision + recall)
    except ZeroDivisionError:
        f1 = 0
    return f1

PENALTY = args.penalty

attend = 0
correct = 0
wrong = 0

total_label_entities = 0
total_pred_entities = 0
total_correct_entities = 0
wrong_qids = 0

total_score = 0

predict_num = 0
answer_num = 0
total_error = 0

wrong_in_pred = 0

with open(args.output_file, 'r') as f:
    csvfile = csv.reader(f)
    l = 0
    for line in csvfile:
        if l == 0:
            l += 1  
            continue
        qid = line[0]
        attend += 1
        try:
            prediction = ast.literal_eval(line[1])
        except:
            abs += 1
            continue
        
        gt_label = ast.literal_eval(line[2])

        lab_wrong = 0
        lab_cor = 0

        for a in gt_label:
            if a in prediction:
                lab_cor += 1
         
        lab_wrong += len(prediction) + len(gt_label) - (2 * lab_cor)

        if lab_cor > 0: cor += 1
        elif lab_cor == 0: wro += 1

        total_lab_wrong += lab_wrong


        

        score = 0
        error = 0

        gt_label_num = len(gt_label)
        total_label_entities += gt_label_num
        prediction_label_num = len(prediction)
        total_pred_entities += prediction_label_num
        # if gt_label_num != prediction_label_num: print(qid)

        predict_num += prediction_label_num
        answer_num += gt_label_num

        for pred in prediction:
            if pred not in gt_label:
                wrong_in_pred += 1

        for label in gt_label:
            if label in prediction:
                total_correct_entities += 1
                score += (1 / len(gt_label))
                
                gt_label_num -= 1
                prediction_label_num -= 1
        if score < 0.9999:
            print('asdfasdf', qid, score)
        if any(ent in gt_label for ent in prediction): correct += 1
        else:
            print('no', qid)
            print(gt_label, prediction)
        
        if prediction_label_num > 0:
            print(qid, prediction, gt_label)

        error += (gt_label_num + prediction_label_num)
        wrong += error
        error /= len(gt_label)
        if error != 0: 
            print(qid, error, gt_label_num + prediction_label_num)
            wrong_qids += 1

        if PENALTY == 0:
            pass
        elif PENALTY == -1:
            wrong_num = gt_label_num + prediction_label_num
            if wrong_num > 0:
                print('decreased : ', wrong_num / len(gt_label))
            score -= (wrong_num / len(gt_label))
        else:
            wrong_num = gt_label_num + prediction_label_num
            score -= (wrong_num * PENALTY / len(gt_label)) 

        # print(score)
        # if score < 0: print(item)
        total_score += score
        total_error += error
        print("# Wrong : ", qid, wrong, gt_label, prediction)






print(cor, wro, abs)
print(total_lab_wrong)

print('attended : ', attend)
print('abstain : ', abs)
print('correct : ', correct)
print('hit@1 : ', correct / (attend - abs))
print('total label entities : ', total_label_entities)
print('total prediction entities : ', total_pred_entities)
print('correct entities : ', total_correct_entities)
print('wrong in prediction : ', wrong_in_pred)
print('wrong entities : ', wrong)
print('wrong entity qids : ', wrong_qids)
print('score with penalty {0} : '.format(PENALTY), total_score)

print()
print('metric 1 : ', (attend - abs) / attend)
print('metric 2 : ', total_score / (attend - abs))
print('metric 3 : ', total_error / (attend - abs))
print('metric 4 : ', (total_correct_entities - wrong_in_pred) / total_label_entities)
print('f1_score : ', f1_score(total_correct_entities, wrong_in_pred, wrong - wrong_in_pred))
