import argparse
import re

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--output_file', type = str,
                        default="./multihop.txt", help="the output file name.")
    args = parser.parse_args()


    res = []

    qid_pattern = r"qid:(?P<qid>[0-9]+),\s*"
    labels = ['Correct!', 'Wrong', 'Error']

    we = []

    with open(args.output_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        flag = False
        for line in lines:
            if 'qid' in line:
                flag = True
                qid = int(re.match(qid_pattern, line).group('qid'))
            if flag:
                if any(label in line for label in ['Wrong', 'Error']):
                    we.append(qid)
    
    print(we)