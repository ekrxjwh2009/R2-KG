import csv
import sys
import os

def getWrong(filename):
    result = []
    result_dict = {'Correct': [], 'Wrong': [], 'Abstain': []}

    with open(filename, 'r') as file:
        reader = csv.reader(file)
        count = 0

        for row in reader:
            if count == 0:
                count += 1
                continue
            
            temp = row
            if temp[1] == 'Abstain' or temp[1] == 'Error':
                result.append((temp[0], 'Abstain'))
                result_dict['Abstain'].append(temp[0])
            elif temp[1].lower() == temp[2].lower():
                result.append((temp[0], 'Correct'))
                result_dict['Correct'].append(temp[0])
            elif temp[1].lower() != temp[2].lower():
                result.append((temp[0], 'Wrong'))
                result_dict['Wrong'].append(temp[0])

    return result, result_dict

def ensemble_k(filelist):
    file_num = len(filelist)
    # assert file_num % 2 != 0, 'Number of file should be odd'

    vote_num = (file_num + 1) / 2 # Previous ensemble (Majority voting)

    res = []
    for f in filelist:
        _, res_dict_temp = getWrong(f)
        res.append(res_dict_temp)
    
    qids = res[0]['Correct'] + res[0]['Wrong'] + res[0]['Abstain']

    ensemble_res = []
    for qid in qids:
        cor = 0
        wro = 0
        abs = 0
        for d in res:
            if qid in d['Correct']: cor += 1
            elif qid in d['Wrong']: wro += 1
            elif qid in d['Abstain']: abs += 1
            else: raise NotImplementedError
        
        # if cor >= vote_num: ans = 'c'
        # elif wro >= vote_num: ans = 'w'
        # elif abs >= vote_num: ans = 'a'
        # else: ans = 'a'

        if cor == file_num: ans = 'c'
        elif wro == file_num: ans = 'w'
        else: ans = 'a'

        ensemble_res.append([qid, cor, wro, abs, ans])
    
    return ensemble_res


def res_to_csv(filepath, res):
    f = open(fp, 'w')

    writer = csv.writer(f)
    writer.writerows(res)

    f.close()

def getWrongFromEnsemble(filename):
    f = open(filename, 'r')

    data = csv.reader(f)
    wrong_qids = []
    for row in data:
        if 'w' in row:
            wrong_qids.append(int(row[0]))

    wrong_qids.sort()
    return wrong_qids

if __name__ == '__main__':
    filelist = sys.argv[1 : -1]
    outputpath = sys.argv[-1]

    for f in filelist:
        assert os.path.isfile(f), 'File not exist : {0}'.format(f)

    print(sys.argv[1:-1])
    
    if '.csv' not in outputpath: fp = outputpath + ".csv"
    else: fp = outputpath

    res = ensemble_k(filelist)
    res_to_csv(fp, res)

    print('output csv file generated to ', fp)