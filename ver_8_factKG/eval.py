import argparse
import json

# Write Positive Number ( Write +10 to deduct 10 when it's wrong )
PENALTY = 0

def load_jsonl(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line.strip()))
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type = str,
                        default = "../../extracted_dev_set.jsonl", help = "given datset")
    parser.add_argument("--output_file", type = str,
                        default = "./abstention_20240920/existence_true_gpt35.jsonl", help = "output file")
    parser.add_argument("--penalty", type = int,
                        default = 0, help = 'integer value for penalty term')
    
    args = parser.parse_args()

    original_data = load_jsonl(args.dataset)
    experiment_data = load_jsonl(args.output_file)
    PENALTY = args.penalty

    # Number of questions LLM tried to answer (No Abstain)
    attend = 0
    total_score = 0

    for item in experiment_data:
        qid = item['question_id']
        prediction = item['prediction']

        if item['correctness'] not in ["Correct", "Wrong"]:
            continue
        else: attend += 1

        score = 0

        gt_item = original_data[qid - 1]
        if gt_item['question_id'] != qid:
            ind = qid - gt_item['question_id']
            gt_item = original_data[qid - 1 + ind]
        
        # print(item)
        # print(gt_item)
        # break
        # Error Check Code
        if gt_item['question_id'] != qid: raise NotImplementedError

        gt_label = gt_item['Label'][0]

        if gt_label == prediction:
            score += 1
        else:    
            if PENALTY == 0:
                pass
            else:
                # wrong_num = gt_label_num + prediction_label_num
                score -= PENALTY

        # print(score)
        # if score < 0: print(item)
        total_score += score
    
    print('total : ', len(experiment_data))
    print('attended : ', attend)
    print('score with penalty {0} : '.format(PENALTY), total_score)

    print()
    print('metric 1 : ', attend / len(experiment_data))
    print('metric 2 : ', total_score / attend)