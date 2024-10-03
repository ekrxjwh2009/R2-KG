## parser & helper function for extracting evidence
import ast
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

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

# Input : 'Helper fuction : ' included string line
# Output : 
def helper_function_parser(helper_str, temp_param, information = Information(0, '', [])):
    helper_str = helper_str.split('Helper function: ')[1]

    for ind in range(len(helper_functions)):
        if helper_functions[ind] in helper_str:
            break

    # getRelation()
    if ind == 0:
        res = getRelations(helper_str)

    # exploreKG
    elif ind == 1:
        # res = exploreKGs(helper_str)
        res = exploreKGs_abstain(helper_str, information)

    # checkSufficiency
    elif ind == 2:
        res = str(list(set(temp_param)))

    # confidenceCheck
    elif ind == 3:
        previous_chat = ''
        for chat in temp_param:
            previous_chat += chat + '\n'
        res = str(previous_chat)
        res = str(temp_param[-2:])
    # Verification
    else:
        res = helper_str

    return 'Execution result: ' + res

def getRelations(helper_str):

    helpers = helper_str.split('getRelation')
    params = []
    for ind in range(len(helpers)):
        if ind == 0:
            continue
        paren = matching_parentheses(helpers[ind])
        start = min(paren.keys())
        end = paren[start]
        params.append(helpers[ind][start + 2 : end - 1])

    res_string = []

    for ent in params:
        rels = []
        rels += db.getRelationsFromEntity(ent)
        rels += db.getRelationsFromEntity('"' + ent + '"')

        for ind in range(len(rels)):
            if rels[ind][0] == '~':
                rels[ind] = rels[ind].split('~')[1]
            
        # topk_rels = relation_selection("The airport in Punjab, Pakistan is also operated by the government agency of Jinnah International Airport.", ent, rels)
        s = 'Relations_list("' + ent + '") = ' + str(rels)
        res_string.append(s)
    
    return ', '.join(res_string)

def exploreKGs(helper_str):
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
        ent = param.split(': ')[0][1 : -1]
        rels = ast.literal_eval(param.split(': ')[1])
        ent_rel_pair.append((ent, rels))
    
    # print(ent_rel_pair)

    triples = []
    for pair in ent_rel_pair:
        ent = pair[0]
        if len(db.getRelationsFromEntity(ent)) < len(db.getRelationsFromEntity('"' + ent + '"')):
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
            
            for tail in tails:
                triples.append([ent, rel, tail])
        
    
    # print(triples)
    return str(triples)

def checkSufficiency():
    pass

# Including Abstain - if ent-rel pair appears even if it was executed before, abstain and exit.
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
        ent = param.split(': ')[0][1 : -1]
        rels = ast.literal_eval(param.split(': ')[1])
        ent_rel_pair.append((ent, rels))
    
    # print(ent_rel_pair)

    triples = []
    for pair in ent_rel_pair:
        
        ent = pair[0]
        if len(db.getRelationsFromEntity(ent)) < len(db.getRelationsFromEntity('"' + ent + '"')):
            ent = '"' + ent + '"'
        rels = pair[1]
        # print(ent, rels)
        
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
                triples.append([ent, rel, tail])

            information.add_pair((ent, rel))
    
    # print(triples)
    if len(triples) == 0:
        information.set_abstain(-4)
        
    return str(triples)