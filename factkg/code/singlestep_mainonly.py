import openai
import sys, os
from openai import OpenAI
import json
import csv
import argparse
import fair_qid
import numpy as np
import re
import dbpedia_sparql as db
import subagent as sa
from unified_prompts.accurate_prompt.factkg_prompt import main_agent2
from unified_prompts.accurate_prompt.factkg_prompt import main_agent3

main_agent_singlestep = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use one of the helper functions below to find the evidence for finding labels.

Helper Functions
1.getRelation[entity]: Returns the list of relations linked to the entity. You can choose several relations from the list that seem related to the claim.
2.exploreKG[entity]=[relation_1,relation_2, ... relation_K]: Returns the triple set around the entity. For example, [entity, relation_1, tail entity] etc. You can choose relation from [User]'s execution result.
3.Verification[True/False]: If you can judge the claim as True or False give the answer.

You must follow the exact format of the given helper function.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for my response. If response has made, continue your 'Statement and Helper function' task.
Importantly, Do not change the format of the entity or relation including '~'.

Example 1)
Claim: The airport in Punjab, Pakistan is operated by the government agency of the Jinnah International Airport.
Given entity: ["\"Punjab, Pakistan\"", "Jinnah_International_Airport"]

[ChatGPT]
Statement: I need to look around the the given entities. First, I need the relation list linked to Punjab, Pakistan
Helper function: getRelation["\"Punjab, Pakistan\""] 
[User]
Execution result: 
Relation_list["\"Punjab, Pakistan\""] = ['s', 'divdab', 'state', '~location', 'birthPlace', 'placeOfBirth', 'rdf-schema#label', 'deathPlace', 'placeOfDeath', 'origin', 'mapCaption', 'country']
[ChatGPT]
Statement: I need to look around the the given entities. Now, I need the relation list linked to the Jinnah_International_Airport.
Helper function: getRelation["Jinnah_International_Airport"]
[User]
Execution result: 
Relation_list("Jinnah_International_Airport") = ['statYear', 'website', 'elevationF', 'stat2Data', 'r2LengthM', 'r1Number', 'stat1Data', '~targetAirport', 'icao', '~secondaryHubs', 'stat3Header', 'stat2Header', '~hubs', 'operator', 'imageWidth', 'airportManager', '~hubAirport', 'iata', 'type', 'r2Number', 'city', 'ownerOper', 'name', 'metricRwy', 'elevationM', 'hub', 'hypernym', '~headquarter', '~bases', '~origin', 'stat1Header', 'image2Width', 'runwayLength', 'icaoLocationIdentifier', 'owner', 'homepage', '22-rdf-syntax-ns#type', '~stopover', 'r1Surface', 'r1LengthM', 'subject', 'runwayDesignation', 'rdf-schema#label', '~wikiPageRedirects', 'image', 'stat3Data', '~location', 'location', '~target', '~headquarters', 'r2Surface', 'elevation', 'iataLocationIdentifier', 'runwaySurface', 'r2LengthF', 'r1LengthF', 'cityServed']
[ChatGPT]
Statement: Now, to find the airport located in Punjab, I need to explore the graph with "Punjab, Pakistan" related to location.
Helper function: exploreKG["\"Punjab, Pakistan\""]=['~location'])
[User]
Execution result: 
["\"Punjab, Pakistan\"", '~location', 'Bahawalpur_Zoo'], ["\"Punjab, Pakistan\"", '~location', "Allama_Iqbal_International_Airport"], ["\"Punjab, Pakistan\"", '~location', 'Jungle_World,_Rawalpindi'], ["\"Punjab, Pakistan\"", '~location', 'Faisalabad_International_Airport'], ["\"Punjab, Pakistan\"", '~location', 'Multan_International_Airport'], 
[ChatGPT]
Statement: Also, to find the government agency of 'Jinnah_International_Airport', look triples linked by 'operator', 'ownerOper'.
Helper function: exploreKG["Jinnah_International_Airport"]=['operator', 'ownerOper']
[User]
Execution result: 
['Jinnah_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority'], ['Jinnah_International_Airport', 'ownerOper', 'Pakistan_Civil_Aviation_Authority']
[ChatGPT]
Statement: There are three aiports in Punjab, Pakistan. We need relations of those three airports. First, let's look Allama_Iqbal_International_Airport's relations.
Helper function: getRelation['Allama_Iqbal_International_Airport']
[User]
Execution result: 
Relation_list['Allama_Iqbal_International_Airport'] = ['operator', 'operatingOrganisation', 'hub']
[ChatGPT]
Statement: Next, let's look Faisalabad_International_Airport's relations.
Helper function: getRelation['Faisalabad_International_Airport']
[User]
Execution result: 
Relation_list['Faisalabad_International_Airport'] = ['operator', 'owner']
[ChatGPT]
Statement: Next, let's look Multan_International_Airport's relations.
Helper function: getRelation['FMultan_International_Airport']
[User]
Execution result: 
Relation_list('Multan_International_Airport') = ['operator', 'owner']
[ChatGPT]
Statement: To find the operator of the airports, I need to explore the graph for each airports related to operator.
Helper function: exploreKG['Allama_Iqbal_International_Airport']=['operator', 'operatingOrganisation'] 
[User]
Execution result: 
['Allama_Iqbal_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority'], ['Allama_Iqbal_International_Airport', 'operatingOrganisation', 'Pakistan_Civil_Aviation_Authority']
[ChatGPT]
Statement: Now, let's check the operator of Faisalabad_International_Airport.
Helper function: exploreKG['Faisalabad_International_Airport']=['operator']
[User]
Execution result: 
['Faisalabad_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority']
[ChatGPT]
Statement: Now, let's check the operator of Multan_International_Airport.
Helper function: exploreKG['Multan_International_Airport']=['operator']
[User]
Execution result: 
['Multan_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority']
[ChatGPT]
Statement: Since all of the airports' operator is government agency 'Pakistan_Civil_Aviation_Authority' and also the operator of 'Jinnah International Airport', the claim is True.
Helper function: Verification[True]


Example 2)
Claim: Tim Brooke-Taylor starred as a fictional character, which was first aired on 10/03/1983 and was broadcast by STV.
Given entity: ["\"1983-10-03\"", "\"STV\"", "Tim_Brooke-Taylor"]

[ChatGPT]
Statement: First, I need relations linked to Tim_Brooke-Taylor.
Helper function: getRelation["Tim_Brooke-Taylor"]
[User]
Execution result: 
Relation_list('Tim_Brooke-Taylor') = ['birthName', '~voice', '~caption', '~author', 'hypernym', '22-rdf-syntax-ns#type', 'name', 'surname', 'placeOfBirth', 'description', 'genre', 'notableWork', 'dateOfBirth', 'birthDate', 'honorificSuffix', 'shortDescription', 'subject', 'title', 'nationality', '~before', '~voices', 'imdbId', 'spouse', 'rdf-schema#label', 'birthPlace', '~writer', '~after', 'years', 'givenName', 'birthYear', '~starring', '~creator', 'active']
[ChatGPT]
Statemnt: I need relation linked to 1983-10-03.
Helper function: getRelation["\"1983-10-03\""] 
[User]
Execution result: 
Relation_list["\"1983-10-03\""] = ['~deathDate', '~activeYearsStartDate', '~added', '~dateOfDeath', '~date', '~years', '~termStart', '~start', '~birthDate', '~establishedDate', '~released', '~openingDate', '~foundingDate', '~age', '~releaseDate', '~originalairdate', '~firstAired', '~dateOfBirth']
[ChatGPT]
Statemn : I need relation linked to STV.
Helper function: getRelation["\"STV\""] 
[User]
Execution result: 
Relation_list["\"STV\""] = ['~title', '~sisterNames', '~tv', '~formerName', '~code', '~owner', '~undp', '~distributor', '~name', '~alt', '~formerNames', '~callLetters', '~iataLocationIdentifier', '~rdf-schema#label', '~agencyStationCode', '~callSign', '~broadcastedBy', '~channel', '~iata']
[ChatGPT]
Statement: To get the starred information about Tim Brooke-Taylor, I need triples linked with '~starring' with Tim Brooke-Taylor.
Helper function: exploreKG["Tim_Brooke-Taylor"]=['~starring']
[User]
Execution result:
['Tim_Brooke-Taylor', '~starring', 'How_to_Irritate_People'], ['Tim_Brooke-Taylor', '~starring', 'Broaden_Your_Mind'], ['Tim_Brooke-Taylor', '~starring', 'ISIRTA_songs'], ['Tim_Brooke-Taylor', '~starring', 'What_the_Dickens'], ['Tim_Brooke-Taylor', '~starring', 'Bananaman']
[ChatGPT]
Statement: From the triples, Tim Brooke Taylor starred on How_to_Irritate_People, Broaden_Your_Mind, ISIRTA_songs, What_the_Dickens, Bananaman. Now, let's check the first aired date of each program.
Helper function: exploreKG["\"1983-10-03\""]=['~firstAired'] 
[User]
Execution reuslt:
["\"1983-10-03\"", '~firstAired', 'Terrahawks'], ["\"1983-10-03\"", '~firstAired', 'Scarecrow_and_Mrs._King'], ["\"1983-10-03\"", '~firstAired', 'Orm_and_Cheep'], ["\"1983-10-03\"", '~firstAired', 'Watch_Mr._Wizard'], ["\"1983-10-03\"", '~firstAired', 'Where_in_the_World_(UK_game_show)'], ["\"1983-10-03\"", '~firstAired', 'Go_(game_show)'], ['"1983-10-03"', '~firstAired', 'Bananaman']
[ChatGPT]
Statement: From the triples, Bananman was first aired on 1983-10-03 which satisfy the claim. Now, I need to check if the Bananaman broadcast by STV.
Helper function: exploreKG["\"STV\""]=['~broadcastedBy', '~channel']
[User]
Execution reuslt: 
["\"STV\"", '~broadcastedBy', 'Bananaman'], ["\"STV\"", '~channel', 'Brain_Box']
[ChatGPT]
Statement: According to the triples, Bananman broadcast by STV and first starred on 1983-10-03 and Tim Brooke Taylor starred on. So the claim is True.
Helper function: Verification[True]


Example 3)
Claim: Samsung is located in São Paulo.
Given entity: ["Samsung", "São_Paulo"]

[ChatGPT]
Statement: First, I need information about Samsung.
Helper function: getRelation["Samsung"]
[User]
Execution result: 
Relation_list["Samsung"] = ['numEmployees', 'keyPeople', 'industry', 'type', 'hypernym', 'subsidiary', 'logo', 'subject', 'foundation', 'product', '22-rdf-syntax-ns#type', 'name', 'netIncome', 'foundingDate', 'rdf-schema#label', 'revenue', 'homepage', 'subsid', 'location', 'foundingYear', 'keyPerson', 'products', 'numberOfEmployees']
[ChatGPT]
Statement: To know the location of Samsung, I need triples linked by 'location' with Samsung.
Helper function: exploreKG["Samsung"]=['location']
[User]
Execution result:
['Samsung', 'location', 'Korea'], ['Samsung', 'location', 'Seoul']
[ChatGPT]
Statement: According to the triples, Samsung is locate in Korea and Seoul. To check the relation with São Paulo, I need information about São Paulo.
Helper function: getRelation["São_Paulo"] 
[User]
Execution result:
Relation_list["São_Paulo"] = ['imageCaption', 'coordinatesRegion', '22-rdf-syntax-ns#type', '~capital', 'areaCityKm', 'establishedTitle', '~west', 'motto', '~before', 'populationRank', 'float', 'foundingDate', '~locationTown', 'subdivisionType', '~finalAssembly', 'populationTotalRanking', 'rainfall', '~location']
[ChatGPT]
Statement: Let's check what are located in São Paulo.
Helper function: exploreKG["São_Paulo"]=['~location']
[User]
Execution result:
['São_Paulo', '~location', '2009_Santos_FC_season'], ['São_Paulo', '~location', 'Vanguarda_Agro']
[ChatGPT]
Statement: It is not clear that Samsung is located in São Paulo. Let's check if "São_Paulo" is located in 'Korea' or 'Seoul'. I have to find the related location of "São_Paulo".
Helper function: exploreKG["São_Paulo"]=['~capital', '~locationTown', '~location']
[User]
Execution result: 
['São_Paulo', '~capital', 'São_Paulo_Province'], ['São_Paulo', '~locationTown', 'Ibirapuera_Auditorium], ['São_Paulo', '~location', '1972_São_Paulo_FC_season'], ['São_Paulo', '~location', '2013–14_in_Swiss_football']
[ChatGPT]
Statement: Since we cannot verify "São_Paulo" is located in 'Korea' or 'Seoul' by execution result, given claim is False.
Helper function: Verifiation[False]



Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>

"""


openai.api_key = "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"
client = OpenAI(api_key=openai.api_key)

class OpenAIBot:
    def __init__(self, engine, client, temperature, top_p):
        # Initialize conversation with a system message
        self.conversation = [{"role": "system", "content": "You are a helpful assistant."}]
        self.engine = engine
        self.client = client
        self.temperature = temperature
        self.top_p = top_p

    def add_message(self, role, content):
        # Adds a message to the conversation.
        self.conversation.append({"role": role, "content": content})

    def generate_response(self, prompt):
        # Add user prompt to conversation
        self.add_message("user", prompt)

        try:
            # Make a request to the API using the chat-based endpoint with conversation context
            response = self.client.chat.completions.create(model = self.engine, messages = self.conversation, temperature = self.temperature, top_p = self.top_p)
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

class Information:
    def __init__(self):
        self.entrel = []
        self.state = 0
        self.gold_set = []

    def setState(self, state):
        self.state = state
    
    def addEvidence(self, triples):
        self.gold_set += triples
            
def reasoning(claim, initial_prompt, label, max_iter, model, temperature, top_p, f):
            
    # engine= "gpt-3.5-turbo"
    # engine = "gpt-4o-mini"
    engine = model
    chatbot = OpenAIBot(engine, client, temperature, top_p)
    info = Information()

    iter_limit = max_iter
    flag = False

    for i in range(iter_limit + 1):
        
        # Get Prompt from User
        if i == 0:
            prompt = initial_prompt
        else:
            #prompt = input()
            
            prompt, result = client_answer(claim, response, label, info, f)
            # if info.state == -1:
            #     f.write(f"\nDuplicated Entity-Relation pair!")
            #     break
            f.write(prompt)
            
        # f.write(prompt)
        # User can stop the chat by sending 'End Chat' as a Prompt
        if 'Done!!' in prompt:
            flag = True
            break

        # Generate and Print the Response from ChatBot
        f.write(f"\n************************************Iteration:{i}************************************")

        response = chatbot.generate_response(prompt)

        if 'Error' in response:
            return 'Error', i

        f.write("\n"+response)
        f.write(f"---")

    
    if flag == False:
        result = 'Abstain'
        
    return result, i
        
        
def client_answer(claim, response, label, info, f):
    if response.count('[ChatGPT]') > 1:
        prompt = '\n[User]\nExecution result: ' + '\nYou should wait for the [User] response after calling helper function.'
        return prompt, []

    result = None
    #called multi helper functions
    #if not response.startswith('getRelation', 11) or not response.startswith('exploreKG',11) or not response.startswith('Verify', 11):
    #    prompt = '[Server]\nYou gave wrong format. Call the helper function again follow the right format'
    #    return prompt, result

    helper_ftn_calls = []
    helper_ftn_calls = split_functions(response)
    prompt = '\n[User]\nExecution result: '

    if len(helper_ftn_calls) == 0:
        prompt += '\nYou gave wrong format. Call the helper function again follow the right format'

    for helper_str in helper_ftn_calls:
        if 'getRelation' in helper_str:
    
            result = getRelations(helper_str)
            prompt +=  "\n" + result
            #return prompt, result, []

        elif 'exploreKG' in helper_str:
            result, result_prompt = exploreKGs(helper_str, info)
            prompt += "\n" + result_prompt
            # triples += result
            info.addEvidence(result)
            #return prompt, triples, triples
                
        elif 'Verification' in helper_str:
            try:
                result = helper_str.split("Verification[")[1].split("]")[0]#[1:-1]
                prompt += f"\nDone!!Prediction:{result}\nReal label:{label}"
            except:
                prompt += '\nYou gave wrong format. Call the helper function again follow the right format'


            # sub_answer, case, result = verification(claim, info.gold_set, f)
            # prompt += "\n" +sub_answer
            
            # f.write(f"CASE COUNT:{case}")

            #return prompt, prediction, []
        else:
            prompt += '\nYou gave wrong format. Call the helper function again follow the right format'
    
    return prompt, result
    
def retrieval_relation_parse_answer(rel):
    
    post_rel = re.sub('[-=+,#/\?:^.@*\"※ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', '', rel)
    return post_rel 

def retrieval_relation_parse_answer2(rel):
    for r in range(len(rel)):
        post_rel = re.sub('[-=+,#/\?:^.@*\"※ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', '', rel[r])
        rel[r] = post_rel
    return rel

def split_functions(response):
    helper_ftn_calls=[]
    response = response.replace("[ChatGPT]\n",'')
    # statement = response.split("Statement : ")[0].split("Helper function : ")[0]
    try:
        functions = response.split("Helper function: ")[1]#.split("\n<Wait For User Response>")[0]
        if '##' in functions:
            helper_ftn_calls = functions.split(' ## ')
        else :
            helper_ftn_calls = [functions]
        return helper_ftn_calls
    except:
        return helper_ftn_calls

def getRelations(helper_str):
    relations = []
    try:
        entity = helper_str.split("getRelation[")[1].split("]")[0].strip()[1:-1]
        relations += db.getRelationsFromEntity(entity)
        relations += db.getRelationsFromEntity('"' + entity + '"')
        if len(relations) ==0 :
            return f"Do not change the format of entity {entity} in helper function."
        else:
            return 'Relations_list["' + entity + '"] = ' + str(relations)
    except:
        return "You gave wrong format of getRelations[] function. Follow the format of examples."
    

def exploreKGs(helper_str, info):
    triples= []
    result_prompt = ''
    try: 
        ent = helper_str.split("exploreKG[")[1].split("]=")[0].strip()[1:-1]
        relations = helper_str.split('=[')[1].split(']')[0].strip().split(', ')
    
        if len(db.getRelationsFromEntity(ent)) < len(db.getRelationsFromEntity('"' + ent + '"')):
            ent = '"' + ent + '"'
            
        for rel in relations:
            rel = retrieval_relation_parse_answer(rel)

            if (ent, rel) in info.entrel:
                info.setState(-1)
                return [], result_prompt
            else: info.entrel.append((ent, rel))

            tails = []
            if rel[0] == '~':
                tails += db.getEntityFromEntRel(ent, rel)
                tails += db.getEntityFromEntRel(ent, rel.split('~')[1])
            else:
                tails += db.getEntityFromEntRel(ent, rel)
                tails += db.getEntityFromEntRel(ent, '~' + rel)
            
            for tail in tails:
                triples.append([ent, rel, tail])
                
        if len(triples) == 0:
            result_prompt += f"Choose other relations based refer to the Relations_list Or follow the format of Entity {ent} and Relations"
        
        else:
            result_prompt += ', '.join(str(sublist) for sublist in triples)
        
    except:
        result_prompt += "You gave wrong format of exploreKG[] function. Follow the format of examples."

    

    return triples, result_prompt


def verification(claim, gold_set, f):
    
    sub_response, case, prediction = sa.feedback(claim, gold_set, f)
    return sub_response, case, prediction


def score(predict, label, f):
    abs, correct, wrong = 0, 0, 0
    f.write(f"predict:{predict.lower()}, label:{label.lower()}")
    print(f"predict:{predict.lower()}, label:{label.lower()}")
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
    parser.add_argument("--type", type=str, default="multi_hop")
    parser.add_argument("--num_iter", type = int, default = "15")
    parser.add_argument("--model", type = str, default= "gpt-4o-mini")
    parser.add_argument("--temp", type = float, default = 0.0)
    parser.add_argument("--top_p", type = float, default = 0.0)
    args = parser.parse_args()
    
    save_path = f"./temperature_differ_singlecall"
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    
    result = {}
    questions_dict = {}
    entity_set_dict = {}
    label_set_dict = {}
    types_dict ={}
    
    with open("../extracted_dev_set.jsonl") as f:
        for line in f:
            if not line:
                continue
            q = json.loads(line)

            questions_dict[q["question_id"]] = q["question"]
            entity_set_dict[q["question_id"]] = q["entity_set"]
            label_set_dict[q["question_id"]] = q["Label"]
            types_dict[q['question_id']] = q["types"] 
            


    total_correct, total_abs, total_wrong = 0, 0, 0
    
    if args.type == 'existence': qid_list = fair_qid.existence
    elif args.type == "num1" : qid_list = fair_qid.num1
    elif args.type == 'multi_claim' : qid_list = fair_qid.multi_claim
    elif args.type == "multi_hop" : qid_list = fair_qid.multi_hop
    else:
        print("Wrong argument")

    
    iter_num_list=[]
    answer_list= [['qid','prediction','gt_label']]
    for qid in qid_list:
        with open(os.path.join(save_path, f"result_{args.type}_{args.model}_maxiter_{args.num_iter}_temp_{args.temp}_topp_{args.top_p}_trial5.txt"), 'a') as f:
        # with open(os.path.join(save_path, f"result_{args.type}_4omini.txt"),'a') as f:
            print(f"Qid:{qid}")
            question = questions_dict[qid]
            label = label_set_dict[qid]
            entities = entity_set_dict[qid]
            
            f.write(f"\n\n\nQid:{qid}\nQuestion :{question}\n")
            f.write(f"GT entity:{entities}")
            
            prompt = main_agent_singlestep.replace('<<<<CLAIM>>>>', question).replace('<<<<GT_ENTITY>>>', str(entities))
            
            prediction, iter_num = reasoning(question, prompt, label, args.num_iter, args.model, args.temp, args.top_p, f)
            abs, correct, wrong= score(str(prediction), str(label[0]),f)
            total_correct += correct
            total_wrong += wrong
            total_abs += abs
            iter_num_list.append(iter_num)
            answer_list.append([qid, str(prediction), str(label[0])])

            f.close()

    
    if (len(qid_list) - total_abs) == 0 :
        metric1 = 0
    else:
        metric1 = (len(qid_list) - total_abs) / len(qid_list)
    if total_correct == 0:
        metric2 = 0
    else:
        metric2 = total_correct / (len(qid_list) - total_abs)
        
    if (total_correct-total_wrong) == 0 :
        metric3 = 0
    else:
        metric3 = (total_correct-total_wrong) / (len(qid_list) - total_abs)
            
        
    with open(os.path.join(save_path, f"result_{args.type}_{args.model}_maxiter_{args.num_iter}_temp_{args.temp}_topp_{args.top_p}_trial5.txt"), 'a') as f:
        f.write(f"\n\n\nTotal sample:{len(qid_list)}, Total_Correct:{total_correct}, Total_Wrong:{total_wrong}, Total_abstain:{total_abs}\n")
        f.write(f"metric1:{metric1}\n mertric2:{metric2}\n metric3:{metric3}")
        f.write(f"avg iter:{np.average(iter_num_list)}\n max_iter:{np.max(iter_num_list)}\n min_iter:{np.min(iter_num_list)}")
        
    f= open(f"./temperature_differ_singlecall/only_answer_{args.type}_{args.model}_maxiter_{args.num_iter}_temp_{args.temp}_topp_{args.top_p}_trial5.csv", 'w')

    writer= csv.writer(f)
    writer.writerows(answer_list)
    f.close()