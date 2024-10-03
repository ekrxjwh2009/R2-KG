## parser & helper function for extracting evidence
import ast
import re
import openai
import time
import dbpedia_sparql as db
from individual_claim_info import Information

helper_functions = ['getRelation', 'exploreKG', 'checkSufficiency', 'confidenceCheck', 'Verification']

def matching_parentheses(string):

    op= [] 
    dc = { 
        op.pop() if op else -1:i for i,c in enumerate(string) if 
        (c=='(' and op.append(i) and False) or (c==')' and op)
    }
    return False if dc.get(-1) or op else dc

def matching_big_parentheses(string):

    op= [] 
    dc = { 
        op.pop() if op else -1:i for i,c in enumerate(string) if 
        (c=='[' and op.append(i) and False) or (c==']' and op)
    }
    return False if dc.get(-1) or op else dc

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

# Input : 'Helper fuction : ' included string line
# Output : 
def helper_function_parser(helper_str, temp_param, information = Information(0, '', [])):
    try:
        helper_str = helper_str.split('Helper function: ')[1]
    except:
        return 'Execution result: '

    for ind in range(len(helper_functions)):
        if helper_functions[ind] in helper_str:
            break

    if ind == 0:
        # res = getRelations(helper_str)

        res = getRelations_integrate(helper_str)

    elif ind == 1:
        res = exploreKGs(helper_str, information)
        # res = exploreKGs_abstain(helper_str, information)

    elif ind == 2:
        res = checkSufficiency(helper_str)
    elif ind == 3:
        previous_chat = ''
        for chat in temp_param:
            previous_chat += chat + '\n'
        res = str(previous_chat)
        res = str(temp_param[-2:])
    else:
        res = verification(helper_str)
    pass

    
    return 'Execution result: ' + str(res)

def getRelations(helper_str):

    helpers = helper_str.split('getRelation')
    params = []
    for ind in range(len(helpers)):
        if ind == 0:
            continue
        paren = matching_parentheses(helpers[ind])
        start = min(paren.keys())
        end = paren[start]
        # print(helpers[ind][start + 1 : end])
        params.append(helpers[ind][start + 1 : end])

    res_string = []
    # print('params : ', params)

    for ent in params:
        ent_list = []
        try:
            ent_list = ast.literal_eval(ent)
        except:
            ent_list = [ent]
        rels = []

        # print('ent list : ', ent_list)

        for e in ent_list:
            e = e.replace(' ', '_').lower()
            rels += db.getRelationsFromEntity(e)
            rels += db.getRelationsFromEntity('"' + e + '"')

            for ind in range(len(rels)):
                if rels[ind][0] == '~':
                    rels[ind] = rels[ind].split('~')[1]
                
        rels = list(set(rels))
        s = 'Relations_list("' + str(ent_list) + '") = ' + str(rels)
        res_string.append(s)
    
    return ', '.join(res_string)


def getRelations_integrate(helper_str):

    helpers = helper_str.split('getRelation')
    params = []
    for ind in range(len(helpers)):
        if ind == 0:
            continue
        pattern_quote = r"'((?:\\'|[^'])*)'"
        pattern_doublequote = r'"((?:\\"|[^"])*)"'
        params = re.findall(pattern_quote, helpers[ind]) + re.findall(pattern_doublequote, helpers[ind])
        params = [match.replace("\\'", "'") for match in params]
        params = [match.replace('\\"', '"') for match in params]

    res_string = []
    # print(params)
    for ent in params:
        ent_list = []
        try:
            ent_list = ast.literal_eval(ent)
        except:
            ent_list = [ent]
        rels = []

        for e in ent_list:
            e = e.replace(' ', '_').lower()
            rels += db.getRelationsFromEntity(e)

            for ind in range(len(rels)):
                if rels[ind][0] == '~':
                    rels[ind] = rels[ind].split('~')[1]
                
        rels = list(set(rels))
        s = 'Relations_list("' + str(ent_list) + '") = ' + str(rels)
        res_string.append(s)
    
    return ', '.join(res_string)

def exploreKGs(helper_str, information):
    helpers_temp = helper_str.split('exploreKG')

    helpers = []
    for i in range(len(helpers_temp)):
        if i == 0:
            continue
        elif i == (len(helpers_temp) - 1):
            helpers.append('exploreKG' + helpers_temp[i])
        else:
            helpers.append('exploreKG' + helpers_temp[i][: -2])
    
    ent_rel_pair = []
    # For exploreKG with ':' splitter
    # try:
    for helper in helpers:
        paren = matching_parentheses(helper)
        start = min(paren.keys())
        end = paren[start]

        param = helper[start + 1 : end]
        ent_list = param.split(': ')[0]
        # ent_list = ast.literal_eval(ent_list)
        try:
            ent_list = ast.literal_eval(ent_list)
            if not type(ent_list) == type([]): ent_list = [ent_list]
        except:
            ent_list = [ent_list]
        rels = ast.literal_eval(param.split(': ')[1])
        ent_rel_pair.append((ent_list, rels))
        

    triples = []
    entire_tails = []
    # print(ent_rel_pair)
    for pair in ent_rel_pair:
        for ent in pair[0]:
            ent = ent.replace(' ', '_').lower()
            if len(db.getRelationsFromEntity(ent)) == 0 < len(db.getRelationsFromEntity('"' + ent + '"')):
                ent = '"' + ent + '"'
            rels = pair[1]
            # print(ent, rels)
            
            for rel in rels:
                tails = []
                if rel[0] == '~':
                    tails += db.getEntityFromEntRel(ent, rel)
                    tails += db.getEntityFromEntRel(ent, rel.split('~')[1])
                else:
                    tails += db.getEntityFromEntRel(ent, rel)
                    tails += db.getEntityFromEntRel(ent, '~' + rel)
                
                entire_tails += tails
                for tail in tails:
                    if tail == information.gt_entity: continue
                    triples.append([ent, rel, tail])
        
    
    # print(triples)
    return str(triples)
    # return str(entire_tails)

def exploreKGs_abstain(helper_str, information):
    helpers_temp = helper_str.split('exploreKG')
    # print(helpers_temp)

    helpers = []
    for i in range(len(helpers_temp)):
        if i == 0:
            continue
        elif i == (len(helpers_temp) - 1):
            helpers.append('exploreKG' + helpers_temp[i])
        else:
            helpers.append('exploreKG' + helpers_temp[i][: -2])
    
    # print(helpers)
    
    ent_rel_pair = []
    for helper in helpers:
        paren = matching_parentheses(helper)
        start = min(paren.keys())
        end = paren[start]

        param = helper[start + 1 : end]
        if ':' in param:
            ent_list = param.split(': ')[0]
        else:
            ent_list = param.split(', ')[0]
        # ent_list = ast.literal_eval(ent_list)
        try:
            ent_list = ast.literal_eval(ent_list)
            if not type(ent_list) == type([]): ent_list = [ent_list]
        except:
            ent_list = [ent_list]
        try:
            rels = ast.literal_eval(param.split(': ')[1])
        except:
            rels = ast.literal_eval(param.split(', ')[1])
        
        ent_rel_pair.append((ent_list, rels))
    

    triples = []
    for pair in ent_rel_pair:
        for ent in pair[0]:
            ent = ent.replace(' ', '_').lower()
            rels = pair[1]
            
            for rel in rels:
                if (ent, rel) in information.ent_rel_history:
                    print(information.ent_rel_history, pair)
                    information.set_abstain(-1)
                    return ''
                
                tails = []
                if rel[0] == '~':
                    tails += db.getEntityFromEntRel(ent, rel)
                    tails += db.getEntityFromEntRel(ent, rel.split('~')[1])
                else:
                    tails += db.getEntityFromEntRel(ent, rel)
                    tails += db.getEntityFromEntRel(ent, '~' + rel)
                
                for tail in tails:
                    if tail == information.gt_entity: continue # Line for metaqa property : don't take entity same with given entity
                    triples.append([ent, rel, tail])
                
                information.add_pair((ent, rel))
        
    
    # print(triples)
    if len(triples) == 0:
        information.set_abstain(-4)
        
    return str(triples)

def checkSufficiency():
    pass

def verification(helper_str):
    helpers_temp = helper_str.split('Verification')[1]
    paren = matching_big_parentheses(helpers_temp)
    start = min(paren.keys())
    end = paren[start]

    labels = helpers_temp[start : end + 1]
    labels = ast.literal_eval(labels)

    for ind in range(len(labels)):
        labels[ind] = str(labels[ind]).replace(' ', '_').lower()

    return labels


if __name__ == '__main__':
    a = "Helper function: exploreKG(\"United_States\": ['starring', '~firstAired', 'broadcastedBy']), exploreKG(\"1983-10-03\": ['~releaseDate', '~firstAired']), exploreKG(\"STV\": ['~broadcastedBy']), exploreKG(\"Tim_Brooke-Taylor\": ['~starring', '~firstAired'])"
    print(helper_function_parser(a))
    pass