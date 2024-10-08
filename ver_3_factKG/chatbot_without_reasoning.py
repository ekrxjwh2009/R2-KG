import openai
import sys, os
from openai import OpenAI
import json
import ast
import csv
import argparse
import sample_number
import numpy as np
import re
import dbpedia_sparql as db




initial_prompt = """  
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use below helper functions to find the evidence for finding labels.

Helper Functions
1.getRelation[entity]: Returns the list of relations linked to the entity. You can choose several relations from the list that seem related to the claim.
2.exploreKG[entity]=[relation_1,relation_2, ... relation_K]: Returns the triple set around the entity. For example, [entity, relation_1, tail entity] etc. You can choose relation from [User]'s execution result.
3.Verification[True or False]: If you can judge the claim as True or False give the answer.

You must follow the exact format of the given helper function.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for my response. If response has made, continue your 'Statement and Helper function' task.
Importantly, Do not change the format of the entity including quotation mark of slash mark.
Do not change the format of relation including '~'.

Example 1)
Claim: The airport in Punjab, Pakistan is operated by the government agency of the Jinnah International Airport.
Given entity: ["\"Punjab, Pakistan\"", "Jinnah_International_Airport"]

[ChatGPT]
Statement : I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function : getRelation["\"Punjab, Pakistan\""] ## getRelation["Jinnah_International_Airport"]
[User]
Execution result : Relation_list["\"Punjab, Pakistan\""] = ['s', 'divdab', 'state', 'location', 'birthPlace', 'placeOfBirth', 'rdf-schema#label', 'deathPlace', 'placeOfDeath', 'origin', 'mapCaption', 'country'], Relation_list["Jinnah_International_Airport"] = ['statYear', 'website', 'elevationF', 'stat2Data', 'r2LengthM', 'r1Number', 'stat1Data', '~targetAirport', 'icao', '~secondaryHubs', 'stat3Header', 'stat2Header', '~hubs', 'operator', 'imageWidth', 'airportManager', '~hubAirport', 'iata', 'type', 'r2Number', 'city', 'ownerOper', 'name', 'metricRwy', 'elevationM', 'hub', 'hypernym', '~headquarter', '~bases', '~origin', 'stat1Header', 'image2Width', 'runwayLength', 'icaoLocationIdentifier', 'owner', 'homepage', '22-rdf-syntax-ns#type', '~stopover', 'r1Surface', 'r1LengthM', 'subject', 'runwayDesignation', 'rdf-schema#label', '~wikiPageRedirects', 'image', 'stat3Data', '~location', 'location', '~target', '~headquarters', 'r2Surface', 'elevation', 'iataLocationIdentifier', 'runwaySurface', 'r2LengthF', 'r1LengthF', 'cityServed']
[ChatGPT]
Statement : Now, to find the airport located in Punjab, I need to explore the graph with "Punjab, Pakistan" and related relations. Also, to find the government agency of 'Jinnah_International_Airport', I need to explore the graph too.
Helper function : exploreKG["\"Punjab, Pakistan\""]=['location'] ## exploreKG["Jinnah_International_Airport"]=['operator', 'ownerOper']
[User]
Execution result : ["\"Punjab, Pakistan\"", '~location', 'Bahawalpur_Zoo'], ["\"Punjab, Pakistan\"", '~location', "Allama_Iqbal_International_Airport"], ["\"Punjab, Pakistan\"", '~location', 'Jungle_World,_Rawalpindi'], ["\"Punjab, Pakistan\"", '~location', 'Faisalabad_International_Airport'], ["\"Punjab, Pakistan\"", '~location', 'Multan_International_Airport'], ['Jinnah_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority'], ['Jinnah_International_Airport', 'ownerOper', 'Pakistan_Civil_Aviation_Authority']
[ChatGPT]
Statement : There are many airports in 'Punjab, Pakistan', and the operator of 'Jinnah_International_Airport' is 'Pakistan_Civil_Aviation_Authority'. Here, we have to find the proper relation to find the operator of the airports.
Helper function : getRelation['Allama_Iqbal_International_Airport'] ## getRelation['Faisalabad_International_Airport'] ## getRelation['Multan_International_Airport']
[User]
Execution result : Relation_list['Allama_Iqbal_International_Airport'] = ['operator', 'operatingOrganisation', 'hub'], Relation_list['Faisalabad_International_Airport'] = ['operator', 'owner'], Relation_list['Multan_International_Airport'] = ['operator', 'owner']
[ChatGPT]
Statement : To find the operator of the airports, I need to explore the graph for each airport.
Helper function : exploreKG['Allama_Iqbal_International_Airport']=['operator', 'operatingOrganisation'] ## exploreKG['Faisalabad_International_Airport']=['operator'] ## exploreKG['Multan_International_Airport']=['operator']
[User]
Execution result : ['Allama_Iqbal_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority'], ['Allama_Iqbal_International_Airport', 'operatingOrganisation', 'Pakistan_Civil_Aviation_Authority'], ['Faisalabad_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority'], ['Multan_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority']
[ChatGPT]
Statement : Since all of the airports' operator is government agency 'Pakistan_Civil_Aviation_Authority' and also the operator of 'Jinnah International Airport', the claim is True.
Helper function : Verification[True]

Example 2)
Claim: Tim Brooke-Taylor starred as a fictional character, which was first aired on 10/03/1983 and was broadcast by STV.
Given entity: ["\"1983-10-03\"", "\"STV\"", "Tim_Brooke-Taylor"]

[ChatGPT]
Statement : I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function : getRelation["\"1983-10-03\""] ## getRelation["\"STV\""] ## getRelation["Tim_Brooke-Taylor"]
[User]
Execution result : Relation_list["\"1983-10-03\""] = ['~deathDate', '~activeYearsStartDate', '~added', '~dateOfDeath', '~date', '~years', '~termStart', '~start', '~birthDate', '~establishedDate', '~released', '~openingDate', '~foundingDate', '~age', '~releaseDate', '~originalairdate', '~firstAired', '~dateOfBirth'], Relation_list["\"STV\""] = ['~title', '~sisterNames', '~tv', '~formerName', '~code', '~owner', '~undp', '~distributor', '~name', '~alt', '~formerNames', '~callLetters', '~iataLocationIdentifier', '~rdf-schema#label', '~agencyStationCode', '~callSign', '~broadcastedBy', '~channel', '~iata'], Relation_list['Tim_Brooke-Taylor'] = ['birthName', '~voice', '~caption', '~author', 'hypernym', '22-rdf-syntax-ns#type', 'name', 'surname', 'placeOfBirth', 'description', 'genre', 'notableWork', 'dateOfBirth', 'birthDate', 'honorificSuffix', 'shortDescription', 'subject', 'title', 'nationality', '~before', '~voices', 'imdbId', 'spouse', 'rdf-schema#label', 'birthPlace', '~writer', '~after', 'years', 'givenName', 'birthYear', '~starring', '~creator', 'active']
[ChatGPT]
Statement : To verify the information in the claim, I can choose proper relation for each entity.
Helper function : exploreKG["\"1983-10-03\""]=['~firstAired'] ## exploreKG["\"STV\""]=['~broadcastedBy', '~channel'] ## exploreKG["Tim_Brooke-Taylor"]=['~starring']
[User]
Execution result : ["\"1983-10-03\"", '~firstAired', 'Terrahawks'], ["\"1983-10-03\"", '~firstAired', 'Scarecrow_and_Mrs._King'], ["\"1983-10-03\"", '~firstAired', 'Orm_and_Cheep'], ["\"1983-10-03\"", '~firstAired', 'Watch_Mr._Wizard'], ["\"1983-10-03\"", '~firstAired', 'Where_in_the_World_(UK_game_show)'], ["\"1983-10-03\"", '~firstAired', 'Go_(game_show)'], ['"1983-10-03"', '~firstAired', 'Bananaman'], ["\"STV\"", '~broadcastedBy', 'Bananaman'], ["\"STV\"", '~channel', 'Brain_Box'], ['Tim_Brooke-Taylor', '~starring', 'How_to_Irritate_People'], ['Tim_Brooke-Taylor', '~starring', 'Broaden_Your_Mind'], ['Tim_Brooke-Taylor', '~starring', 'ISIRTA_songs'], ['Tim_Brooke-Taylor', '~starring', 'What_the_Dickens'], ['Tim_Brooke-Taylor', '~starring', 'Bananaman']
[ChatGPT]
Statement : There is the fictional character 'Bananaman' which satisfy all the information in the claim.
Helper function : Verification[True]

Example 3)
Claim: Samsung is located in São Paulo.
Given entity: ["Samsung", "São_Paulo"]

[ChatGPT]
Statement : I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function : getRelation["Samsung"] ## getRelation["São_Paulo"]
[User]
Execution result : Relation_list["Samsung"] = ['numEmployees', 'keyPeople', 'industry', 'type', 'hypernym', 'subsidiary', 'logo', 'subject', 'foundation', 'product', '22-rdf-syntax-ns#type', 'name', 'netIncome', 'foundingDate', 'rdf-schema#label', 'revenue', 'homepage', 'subsid', 'location', 'foundingYear', 'keyPerson', 'products', 'numberOfEmployees'], Relation_list["São_Paulo"] = ['imageCaption', 'coordinatesRegion', '22-rdf-syntax-ns#type', '~capital', 'areaCityKm', 'establishedTitle', '~west', 'motto', '~before', 'populationRank', 'float', 'foundingDate', '~locationTown', 'subdivisionType', '~finalAssembly', 'populationTotalRanking', 'rainfall', '~location']
[ChatGPT]
Statement : To verify the information in the claim, I have to find the location of 'Samsung' or place located in 'São_Paulo'.
Helper function : exploreKG["Samsung"]=['location'] ## exploreKG["São_Paulo"]=['~location']
[User]
Execution result : ['Samsung', 'location', 'Korea'], ['Samsung', 'location', 'Seoul'], ['São_Paulo', '~location', '2009_Santos_FC_season'], ['São_Paulo', '~location', 'Vanguarda_Agro']
[ChatGPT]
Statement : I need to check "São_Paulo" is located in 'Korea' or 'Seoul'. I need to explore the graph from "São_Paulo".
Helper function : getRelation["São_Paulo"] 
[User]
Execution result : Relation_list["São_Paulo"] = ['imageCaption', 'coordinatesRegion', '22-rdf-syntax-ns#type', '~capital', 'areaCityKm', 'establishedTitle', '~west', 'motto', '~before', 'populationRank', 'float', 'foundingDate', '~locationTown', 'subdivisionType', '~finalAssembly', 'populationTotalRanking', 'rainfall', '~location']
[ChatGPT]
Statement : To verify "São_Paulo" is located in 'Korea' or 'Seoul', I have to find the related location of "São_Paulo".
Helper function : exploreKG["São_Paulo"]=['~capital', '~locationTown', '~location']
[User]
Execution result : ['São_Paulo', '~capital', 'São_Paulo_Province'], ['São_Paulo', '~locationTown', 'Ibirapuera_Auditorium], ['São_Paulo', '~location', '1972_São_Paulo_FC_season'], ['São_Paulo', '~location', '2013–14_in_Swiss_football']
[ChatGPT]
Statement : Since we cannot verify "São_Paulo" is located in 'Korea' or 'Seoul' by execution result, given claim is False.
Helper function : Verifiation[False]


Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>
"""



openai.api_key = "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"
client = OpenAI(api_key=openai.api_key)

class OpenAIBot:
    def __init__(self,engine, client):
        # Initialize conversation with a system message
        self.conversation = [{"role": "system", "content": "You are a helpful assistant."}]
        self.engine = engine
        self.client = client
    def add_message(self, role, content):
        # Adds a message to the conversation.

        self.conversation.append({"role": role, "content": content})
    def generate_response(self, prompt):
        # Add user prompt to conversation
        self.add_message("user", prompt)

        try:
            # Make a request to the API using the chat-based endpoint with conversation context
            response = self.client.chat.completions.create( model=self.engine, messages=self.conversation, temperature= 0.3, top_p = 0.1)
            # Extract the response
            #print(response)
            assistant_response = response.choices[0].message.content.strip()

            
            # Add assistant response to conversation
            self.add_message("assistant", assistant_response)
            # Return the response
            return assistant_response
        #except:
        #    print('Error Generating Response!')
        except openai.APIError as e:
            #Handle API error here, e.g. retry or log
            print(f"OpenAI API returned an API Error: {e}")
            return f"OpenAI API returned an API Error: {e}"
            
def reasoning(initial_prompt, label, f):
            
    #engine="gpt-3.5-turbo-0125"         
    engine = "gpt-4o-mini-2024-07-18"
    chatbot = OpenAIBot(engine, client)

    iter_limit=15

    for i in range(iter_limit):
        
        # Get Prompt from User
        if i == 0:
            prompt = initial_prompt
        else:
            #prompt = input()
            
            prompt, result = client_answer(response, label)
            
        f.write(prompt)
        # User can stop the chat by sending 'End Chat' as a Prompt
        if 'Done!!' in prompt:
        
            break

        # Generate and Print the Response from ChatBot
        response = chatbot.generate_response(prompt)
        f.write(f"\n************************************Iteration:{i}***********************************")
        f.write("\n"+response)
    
    if i==iter_limit-1:
        result = 'Abstain'   
        
    return result, i
        
        
def client_answer(response, label):
    result = None
    #called multi helper functions
    #if not response.startswith('getRelation', 11) or not response.startswith('exploreKG',11) or not response.startswith('Verify', 11):
    #    prompt = '[Server]\nYou gave wrong format. Call the helper function again follow the right format'
    #    return prompt, result

    helper_ftn_calls = split_functions(response)
    prompt = '\n[User]\nExecution result : '
    for ftn in helper_ftn_calls:
        
        
        if 'getRelation' in ftn:
        
            result = get_relation(ftn)
            prompt += "\n" + result
                
    
        elif 'exploreKG' in ftn:
            result = exploreKGs(ftn)
            prompt += "\n" +result
            
        elif 'Verification' in ftn:
            try:
                result = ftn.split("Verification(")[1].split(")")[0]
                prompt += f"\nDone!!Prediction:{result}\nReal label:{label}"
            except:
                prompt += '\nYou gave wrong format. Call the helper function again follow the right format'
        else:
            prompt += '\nYou gave wrong format. Call the helper function again follow the right format'
    
    return prompt, result
    
def retrieval_relation_parse_answer(rel):
    
    post_rel = re.sub('[-=+,#/\?:^.@*\"※ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', '', rel)
    return post_rel 

def split_functions(response):
    helper_ftn_calls=[]
    response = response.replace("[ChatGPT]\n",'')
    statement = response.split("Statement : ")[0].split("Helper function : ")[0]
    functions = response.split("Helper function : ")[1]
    if '##' in functions:
        helper_ftn_calls = functions.split(' ## ')
    else :
        helper_ftn_calls = [functions]
    return helper_ftn_calls

def get_relation(entity):

    relation_list = db.getRelationsFromEntity(entity)
    #print(f"reltaion list of called fucntion:{relation_list}")
    return relation_list

def matching_parentheses(string):

    op= [] 
    dc = { 
        op.pop() if op else -1:i for i,c in enumerate(string) if 
        (c=='[' and op.append(i) and False) or (c==']' and op)
    }
    return False if dc.get(-1) or op else dc

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
        if len(rels)==0:
            return f"\nDo not change the format of entity {ent} in helper function."

        else:
            for ind in range(len(rels)):
                if rels[ind][0] == '~':
                    rels[ind] = rels[ind].split('~')[1]
                
            # topk_rels = relation_selection("The airport in Punjab, Pakistan is also operated by the government agency of Jinnah International Airport.", ent, rels)
            s = 'Relation_list["' + ent + '"] = ' + str(rels)
            res_string.append(s)
    
    return ', '.join(res_string)

def explore_kg(entity, relations):
    triple_sets= []
    if len(db.getRelationsFromEntity(entity)) ==0 :
        return triple_sets
    else:
        for rel in relations:
            rel = retrieval_relation_parse_answer(rel)
            #print(f"Entity:{entity}, Relation:{rel}")
            tails = db.getEntityFromEntRel(entity, rel)
            for tail in tails:
                tmp = [entity,rel,tail]
                triple_sets.append(tmp)
        #print(f'triple sets:{triple_sets}')
    return triple_sets

def exploreKGs(helper_str):
    helpers_temp = helper_str.split('exploreKG')
    print(f"Helper temp:{helpers_temp}")

    helpers = []
    for i in range(len(helpers_temp)):
        if i == 0:
            continue
        elif i == (len(helpers_temp) - 1):
            helpers.append('exploreKG' + helpers_temp[i])
        else:
            helpers.append('exploreKG' + helpers_temp[i][: -2])
    
    print(f"Helpers:{helpers}")
    ent_rel_pair = []
    for helper in helpers:
        paren = matching_parentheses(helper)
        start = min(paren.keys())
        end = paren[start]

        param = helper[start + 1 : end]
        print(f"Param:{param}")
        ent = param.split('=')[0][1 : -1]
        print(f"Ent:{ent}")
        rels = ast.literal_eval(param.split('=')[1])
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

def score(predict, label,f):
    abs, correct, wrong =0,0,0
    f.write(f"predict:{predict.lower()}, lable:{label.lower()}")
    print(f"predict:{predict.lower()}, lable:{label.lower()}")
    if 'abstain' in predict.lower():
        abs+=1
    elif predict.lower() == label.lower():
        correct+=1
    else:
        wrong +=1
    #LLM abs개수, correct 개수
    return abs, correct, wrong
    
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("type", type=str, default="existence")
    args = parser.parse_args()
    
    save_path = f"./with_reasoning_result"
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    
    result = {}
    questions_dict = {}
    entity_set_dict = {}
    label_set_dict = {}
    types_dict ={}
    
    with open("/home/smjo/share_code/factkg/data/extracted_dev_set.jsonl") as f:
        for line in f:
            if not line:
                continue
            q = json.loads(line)

            questions_dict[q["question_id"]] = q["question"]
            entity_set_dict[q["question_id"]] = q["entity_set"]
            label_set_dict[q["question_id"]] = q["Label"]
            types_dict[q['question_id']] = q["types"] 
            


    total_correct, total_abs,total_wrong =0,0,0
    
    if args.type == 'existence': qid_list = sample_number.existence
    elif args.type =="num1" : qid_list = sample_number.num1
    elif args.type =='multi_claim' : qid_list = sample_number.multi_claim
    elif args.type =="multi_hop" : qid_list = sample_number.multi_hop
    else:
        print("Wrong argument")

    
    iter_num_list=[]
    answer_list= [['qid','prediction','gt_label']]
    with open(os.path.join(save_path, f"result_{args.type}.txt"),'a') as f:
        for qid in qid_list:
            print(f"Qid:{qid}")
            question = questions_dict[qid]
            label = label_set_dict[qid]
            entities = entity_set_dict[qid]
            
            f.write(f"\n\n\nQid:{qid}\nQuestion :{question}")
            f.write(f"GT entity:{entities}")
            
            prompt = initial_prompt.replace('<<<<CLAIM>>>>', question).replace('<<<<GT_ENTITY>>>', str(entities))
            
            prediction, iter_num = reasoning(prompt, label,f)
            abs, correct, wrong= score(str(prediction), str(label[0]),f)
            total_correct += correct
            total_wrong += wrong
            total_abs += abs
            iter_num_list.append(iter_num)
            answer_list.append([qid, str(prediction), str(label[0])])


        
        if (len(qid_list) - total_abs ) ==0 :
            metric1=0
        else:
            metric1 = (len(qid_list) - total_abs ) /  len(qid_list)
        if total_correct==0:
            metric2 =0
        else :
            metric2 = total_correct/  (len(qid_list) - total_abs)
            
        if (total_correct-total_wrong)==0 :
            metric3 =0
        else:
            metric3 = (total_correct-total_wrong) / (len(qid_list) - total_abs)
        
            
        
        

        f.write(f"\n\n\nTotal sample:{len(qid_list)}, Total_Correct:{total_correct}, Total_Wrong:{total_wrong}, Total_abstain:{total_abs}\n")
        f.write(f"mrtric1:{metric1}\n mertric2:{metric2}\n metric3:{metric3}")
        f.write(f"avg iter:{np.average(iter_num_list)}\n max_iter:{np.max(iter_num_list)}\n min_iter:{np.min(iter_num_list)}")
        
    f= open(f"./with_reasoning_result/only_answer_{args.type}.csv",'w')
    writer= csv.writer(f)
    writer.writerows(answer_list)
    f.close()