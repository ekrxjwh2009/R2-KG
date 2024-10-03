import argparse
import json

# Write Positive Number ( Write +10 to deduct 10 when it's wrong )
PENALTY = 0
# -1 Only for multi label ( 1/n deduction )

def load_jsonl(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line.strip()))
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type = str,
                        default = "../data/onehop_test_set.jsonl", help = "given datset")
    parser.add_argument("--output_file", type = str,
                        default = "./abstention_20240923/onehop_35turbo.jsonl", help = "output file")
    parser.add_argument("--penalty", type = int,
                        default = 0, help = 'integer value for penalty term')
    
    args = parser.parse_args()

    original_data = load_jsonl(args.dataset)
    experiment_data = load_jsonl(args.output_file)
    PENALTY = args.penalty

    # Number of questions LLM tried to answer (No Abstain)
    attend = 0
    total_score = 0

    predict_num = 0
    answer_num = 0
    total_error = 0

    for item in experiment_data:
        qid = item['question_id']
        prediction = item['prediction']

        if item['correctness'] not in ["Correct", "Wrong"]:
            continue
        else: attend += 1

        score = 0
        error = 0

        gt_item = original_data[qid - 1]
        if gt_item['question_id'] != qid:
            ind = qid - gt_item['question_id']
            gt_item = original_data[qid - 1 + ind]
        
        # print(item)
        # print(gt_item)
        # break
        # Error Check Code
        if gt_item['question_id'] != qid: raise NotImplementedError

        gt_label = gt_item['Label']
        gt_label_num = len(gt_label)
        prediction_label_num = len(prediction)
        # if gt_label_num != prediction_label_num: print(qid)

        predict_num += prediction_label_num
        answer_num += gt_label_num

        for label in gt_label:
            if label.replace(' ', '_').lower() in prediction:
                score += (1 / len(gt_label))
                gt_label_num -= 1
                prediction_label_num -= 1

        error += (gt_label_num + prediction_label_num)
        error /= len(gt_label)
        if error != 0: print(qid, error)

        if PENALTY == 0:
            pass
        elif PENALTY == -1:
            wrong_num = gt_label_num + prediction_label_num
            score -= (wrong_num / len(gt_label))
        else:
            wrong_num = gt_label_num + prediction_label_num
            score -= (wrong_num * PENALTY / len(gt_label)) 

        # print(score)
        # if score < 0: print(item)
        total_score += score
        total_error += error
    
    print('total : ', len(experiment_data))
    print('attended : ', attend)
    print('score with penalty {0} : '.format(PENALTY), total_score)

    print()
    print('metric 1 : ', attend / len(experiment_data))
    print('metric 2 : ', total_score / attend)
    print('metric 3 : ', total_error / attend)

    print(predict_num, answer_num)



