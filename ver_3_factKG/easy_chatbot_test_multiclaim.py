import openai
import sys, os
from openai import OpenAI
import json
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import dbpedia_sparql as db

initial_prompt = """
Your role is to verify whether the claim is True or False based on the graph data. 
You must call helper functions to find the sub-graph used as evidence for verification.
If you decide to answer because there's enough evidence, you can choose either True or False.
I will give you a claim and a set of Given_entities for reference. However, some entities in the claim may not be included in the Given_entities. You can explore the graph and infer entities using helper functions.
When you answer, you must only call helper functions following the format like example. 
Important: You must follow the format when you call helper functions. Do not change the format of the entity or relation, including '~'.

Helper Functions
1.getRelation(entity): Returns the list of relations linked to the entity. You can choose several relations from the list that seem related to the claim.
2.exploreKG(entity: [relation_1,relation_2, ... relation_K]): Returns the triple set around the entity. For example, [entity, relation_1, tail entity], [entity, relation_2, tail entity], etc.
3.Verify('true' or 'false'): If you can judge the claim as True or False give the answer.

Here is an example. [ChatGPT] is your answer and [Server] is my answer. You and I take turns answering.

Example )
Claim :  The theater was operated by the company located in Newyork has 200 employess.
Given entity : ['NewYork', '200']

[ChatGPT]
getRelation('NewYork') ## getRelation('200')
[Server]
Relation_list('NewYork') = ['countryName','~location','Citizenship','headQuarters'], Relation_list('200') = ['MountHeight','~countOf','~employeeNumber']
[ChatGPT]
exploreKG('NewYork': ['~location' , 'headQuarters' , 'Citizenship']) ## exploreKG('200': ['MountHeight'])
[Server]
['NewYork','~location','Central Park'], ['NewYork','headQuarters','Dominic Corporation'], ['NewYork','Citizenship','permanent resident'], ['200', 'MountHeight', 'Mt.SaintRoie'] 
[ChatGPT]
exploreKG('200': ['~countOf' , '~employeeNumber'])
[Server]
['NewYork','~location','Central Park'], ['NewYork','headQuarters','Dominic Corporation'], ['200','~countOf','quoted ratio'], ['200','~employeeNumber','Barrymore Theatre']
[ChatGPT]
getRelation('Barrymore Theatre') ## getRelation('Dominic Coporation')
[Server]
Relation_list('Barrymore Theatre') = ['openDate','GoogleRate','employeeNumber','owner','operatedBy','~Operator'],  Relation_list('Dominic Corporation') = ['Operator','item','location','startDate']
[ChatGPT]
exploreKG('Barrymore Theatre': ['operatedBy' , '~Operator']) ## exploreKG('Dominic Corporation': ['Operator'])
[Server]
['Berrymore Theatre','operatedBy','Dominic Corporation'], ['Barrymore Theatre','~Operator','Dominic Corporation'], ['Dominic Corporation','Operator','Berrymore Theatre']
[ChatGPT]
Verify('true')


Now, it's your turn.
Claim : <<<Question>>>
Given entity: <<<Entity set>>>

Let's start the process.
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
            response = self.client.chat.completions.create( model=self.engine, messages=self.conversation, temperature= 0.2)
            # Extract the response
            assistant_response = "[ChatGPT]\n"+response.choices[0].message.content.strip()
            
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
    engine = "gpt-4o"
    chatbot = OpenAIBot(engine, client)

    iter_limit=30

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
        f.write(response)
    
    if i==iter_limit-1:
        result = 'Abstain'   
        
    return result
        
        
def client_answer(response, label):
    result = None
    #called multi helper functions
    #if not response.startswith('getRelation', 11) or not response.startswith('exploreKG',11) or not response.startswith('Verify', 11):
    #    prompt = '[Server]\nYou gave wrong format. Call the helper function again follow the right format'
    #    return prompt, result
    if '##' in response:
        helper_ftn_calls = response.split(' ## ')
    #calle on helper function
    else:
        helper_ftn_calls = [response]
    
    for ftn in helper_ftn_calls:
        if 'getRelation' in ftn:
            try :
                entity = ftn.split("getRelation(")[1].split(")")[0][1:-1]
                result = get_relation(entity)
                prompt = f"[Server]\nRelation_list({entity}) = {result}"
            except :
                prompt = '[Server]\nYou gave wrong format. Call the helper function again follow the right format'
        elif 'exploreKG' in ftn:
            try:
                entity = ftn.split("exploreKG(")[1].split(": ")[0][1:-1]
                relations = ftn.split(": [")[1].split("])")[0].strip().split(', ')
                result = explore_kg(entity, relations)      #entity, string of relation list
                prompt = f"[Server]\n{', '.join([str(triple) for triple in result])}"
            except:
                prompt = '[Server]\nYou gave wrong format. Call the helper function again follow the right format'
        elif 'Verify' in ftn:
            try:
                result = ftn.split("Verify('")[1].split("')")[0]
                prompt = f"Done!!Prediction:{result}, Real label:{label}"
            except:
                prompt = '[Server]\nYou gave wrong format. Call the helper function again follow the right format'
        else:
            prompt = '[Server]\nYou gave wrong format. Call the helper function again follow the right format'
    return prompt, result
    
def get_relation(entity):

    relation_list = db.getRelationsFromEntity(entity)
    #print(f"reltaion list of called fucntion:{relation_list}")
    return relation_list

def explore_kg(entity, relations):
    #print(f"entity:{entity}, relations:{relations}")
    triple_sets= []
    for rel in relations:
        rel = rel[1:-1]
        tails = db.getEntityFromEntRel(entity, rel)
        for tail in tails:
            tmp = [entity,rel,tail]
            triple_sets.append(tmp)
    #print(f'triple sets:{triple_sets}')
    return triple_sets

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
            
    qid_list = [1595, 1607, 1631, 1640, 1696, 1743, 1770, 1787, 1890, 1978, 2094, 2134, 2184, 2197, 2351, 2361, 2384, 2391, 2406, 2414, 2980, 3039, 3110, 3127, 3145, 3219, 3351, 3386, 3392, 3452, 3461, 3504, 3564, 3566, 3578, 3619, 3625, 3656, 3744, 3759, 3804, 3816, 3835, 3839, 3896, 3907, 8256, 8268, 8271, 8311, 8313, 8353, 8433, 8440, 8607, 8662, 8725, 8740, 8756, 8763, 8815, 8862, 8988, 9078, 9094, 9099, 9112, 9147, 9161, 9299, 9321, 9388, 9443, 9476, 9498, 9583, 9595, 9599, 9657, 9659, 9681, 9701, 9713, 9799, 9809, 9822, 9848, 9900, 9909, 9950, 9990, 10004, 10059, 10074, 10108, 11541, 11611, 12029, 12046, 12117]

    total_correct, total_abs,total_wrong =0,0,0
    
    with open("/home/smjo/share_code/factkg/unified/ver_0/result_multiclaim.txt",'a') as f:
        for qid in qid_list:
            question = questions_dict[qid]
            label = label_set_dict[qid]
            entities = entity_set_dict[qid]
            
            f.write(f"\n\n\nQid:{qid}\nQuestion :{question}")
            f.write(f"GT entity:{entities}")
            
            prompt = initial_prompt.replace('<<<Question>>>', question).replace('<<<Entity set>>>', str(entities))
            
            prediction = reasoning(prompt, label,f)
            abs, correct, wrong= score(str(prediction), str(label[0]),f)
            total_correct += correct
            total_wrong += wrong
            total_abs += abs

        
        if (len(qid_list) - total_abs ) ==0 :
            metric1=0
        else:
            metric1 = (len(qid_list) - total_abs ) /  len(qid_list)
        if (total_correct-total_wrong)==0 :
            metric2 =0
        else:
            metric2 = (total_correct-total_wrong) / (len(qid_list) - total_abs)
        f.write("\n\n\nmultihop")
        f.write(f"Total sample:{len(qid_list)}, Total_Correct:{total_correct}, Total_Wrong:{total_wrong}, Total_abstain:{total_abs}")
        f.write(f"mrtric1:{metric1}, mertric2:{metric2}")