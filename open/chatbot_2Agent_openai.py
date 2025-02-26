import sys, os
import openai
from openai import OpenAI
import argparse
import utils
import config
# from prompt import initial_prompt, pr1_singlecall
from dotenv import load_dotenv
from difflib import get_close_matches


current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)
load_dotenv()

# GITIGNORE WHEN MAKING REPO PUBLIC
openai.api_key = os.getenv('OPENAI_KEY')

client = OpenAI(
    api_key = os.getenv('OPENAI_KEY')
)


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
            response = self.client.chat.completions.create( model=self.engine, messages=self.conversation, temperature= 0.95, top_p = 0.95)
            # Extract the response
            assistant_response = response.choices[0].message.content.strip()
            # Add assistant response to conversation
            self.add_message("assistant", assistant_response)
            # Return the response
            return assistant_response
        
        except openai.APIError as e:
            #Handle API error here, e.g. retry or log
            print(f"OpenAI API returned an API Error: {e}")
            return f"OpenAI API returned an API Error: {e}"
        

def reasoning(model, subagent, claim, iter_limit, initial_prompt, sub_prompt, entities, f, KG=[]):
    if model =='gpt-4o-mini': engine = "gpt-4o-mini-2024-07-18"
    elif model == 'gpt-4o': engine = "gpt-4o-2024-08-06"
    chatbot = OpenAIBot(engine, client)

    gold_set =[]
    gold_relations =''
    gold_entities =[]

    for i in range(iter_limit):
        # Get Prompt from User
        if i == 0:
            prompt = initial_prompt
            gold_entities += entities

        else:
            prompt, result, triples, relations, get_rel_state, new_entites = client_answer(claim, subagent, response, gold_set, gold_relations, sub_prompt, gold_entities, KG)
            
            if len(triples) > 0:
                gold_set += triples
            if get_rel_state == 1:
                gold_relations += relations
            if len(new_entites) > 0:
                gold_entities += new_entites  
        
        # User can stop the chat by sending 'End Chat' as a Prompt
        if 'Done!!' in prompt:
            break
        
        if i > 0:    
            f.write(prompt)

        # Generate and Print the Response from ChatBot
        response = chatbot.generate_response(prompt)
        f.write(f"\n************************************Iteration:{i}************************************")
        f.write("\n"+response)
    
    if i == iter_limit - 1:
        result = 'Abstain'   
        
    return result, i

def split_functions(response):
    helper_ftn_calls = []
    prompt = ''
    try:
        response = response.replace("[Your Task]\n", '')
        functions = response.split("Helper function:")[1]

        if '##' in functions:
            helper_ftn_calls = functions.split(' ## ')
        else:
            helper_ftn_calls = [functions]

        prompt = '\n[User]\nExecution result :'
        return helper_ftn_calls, prompt
        
    except:
        # print("Wrong format of call function")
        pass
        
    try: 
        response = response.replace("[Your Task]\n",'')
        functions = response.split("Helper function :")[1]

        if '##' in functions:
            helper_ftn_calls = functions.split(' ## ')
        else:
            helper_ftn_calls = [functions]

        prompt = '\n[User]\nExecution result :'
        return helper_ftn_calls, prompt
    
    except:
        # print("Wrong format of call functions")
        prompt = "\n[User]\nYou gave wrong format of Statement and Helper function."
        
    return helper_ftn_calls, prompt


def client_answer(claim, subagent, response, gold_set, gold_relations, sub_prompt, gold_entities, KG=[]):
    result = None

    helper_ftn_calls, prompt = split_functions(response)
    triples = []
    new_entities = []
    relations = ""
    get_rel_state = 0

    for helper_str in helper_ftn_calls:
        if 'getRelation' in helper_str:
            get_rel_state, result = getRelations(helper_str, gold_entities, KG)
            prompt +=  "\n" + result
            if get_rel_state == 1:
                relations += "\n" + result
            
        elif 'exploreKG' in helper_str:
            result, result_prompt = exploreKGs(helper_str, gold_entities, KG)
            prompt += "\n" + result_prompt
            triples += result
            
            #For matching entities
            new_entities += find_new_entity(triples)
            
        elif 'Verification' in helper_str:
            sub_answer, case, result = verification(subagent, claim, gold_set, gold_relations, sub_prompt)
            prompt += "\n" +sub_answer
            print(prompt)
            
        else:
            prompt += '\nYou gave wrong format. Call the helper function again follow the right format'
            result =''
    
    return prompt, result, triples, relations, get_rel_state, new_entities

def find_new_entity(triples):
    new_entities = []
    for triple_set in triples:
        head, rel, tail = triple_set[0], triple_set[1], triple_set[2]

        if head not in new_entities:
            new_entities.append(head)

        if tail not in new_entities:
            new_entities.append(tail)
    
    return new_entities

def match_and_replace_single(parsed_entity, gold_entities):

    # Find the closest match from gold_entities
    matches = get_close_matches(parsed_entity, gold_entities, n=1, cutoff=0.6)  # Adjust cutoff as needed
    if matches:
        return matches[0]  # Return the closest match
    return parsed_entity  # Return the original if no match is found

def getRelations(helper_str, gold_entities, KG):
    relations = []
    state = 0

    try:
        entity = helper_str.split("getRelation[")[1].split("]")[0].strip()[1:-1]
        #Entity matching
        matched_entity = match_and_replace_single(entity, gold_entities)
        print(f"Before :{entity}, matched:{matched_entity}")

        if config.DATASET == 'CRONQUESTIONS':
            subgraphs = KG[matched_entity]
            for graph in subgraphs:
                rel = graph[1]
                if rel not in relations:
                    relations.append(rel)
        
        elif config.DATASET == 'FactKG':
            import FactKG.dbpedia_sparql as db
            relations += db.getRelationsFromEntity(matched_entity)
            relations += db.getRelationsFromEntity('"' + matched_entity + '"')
        
        elif config.DATASET == 'WebQSP':
            relations += db.getRelationsFromEntity(matched_entity)

        if len(relations) == 0:
            state = 0
            return state, f"Do not change the format of entity {entity} in helper function."
        else:
            state = 1
            return state, 'Relations_list["' + matched_entity + '"] = ' + str(relations)
        
    except:
        return state,"You gave wrong format of getRelations() function. Follow the format of examples."
    
def exploreKGs(helper_str, gold_entities, KG):
    triples= []
    result_prompt = ''
    try: 
        ent = helper_str.split("exploreKG[")[1].split("]=")[0].strip()[1:-1]
        relations = helper_str.split('=[')[1].split(']')[0].strip().split(', ')
        #Entity matching
        matched_entity = match_and_replace_single(ent, gold_entities)
        print(f"Before :{ent}, matched:{matched_entity}")


        if config.DATASET == 'CRONQUESTIONS':
            subgraphs = KG[matched_entity]
            existing_relations = []
            for graph in subgraphs:
                exist_rel = graph[1]
                if exist_rel not in existing_relations:
                    existing_relations.append(exist_rel) 
            
            for rel in relations:
                rel = rel[1:-1]
                print(f"Relation :{rel}")
                if (rel not in existing_relations) and ('~' + rel) not in existing_relations:
                    result_prompt += f"'The relation you chose '{rel}' does not exist.Choose from the following list."
                    result_prompt += 'Relations_list["' + matched_entity + '"] = ' + str(existing_relations)
                
                for sub_graph in KG[matched_entity]:
                    if rel == sub_graph[1]:
                        triples.append(sub_graph)

        elif config.DATASET == 'FactKG':
            import FactKG.dbpedia_sparql as db
            if len(db.getRelationsFromEntity(matched_entity)) < len(db.getRelationsFromEntity('"' + matched_entity + '"')):
                matched_entity = '"' + matched_entity + '"'
                
            for rel in relations:
                rel = utils.retrieval_relation_parse_answer(rel)
                ###check if the LLM required non-existing relations
                existing_relations = db.getRelationsFromEntity(matched_entity)
                if (rel not in existing_relations) and ('~' + rel) not in existing_relations:
                    #result_prompt += f"""The relation you chose '{rel}' does not exist. Choose from the following list. Relations_list["' + {ent} + '"] = ' + {str(existing_relations)}"""
                    result_prompt += f"'The relation you chose '{rel}' does not exist.Choose from the following list."
                    result_prompt += 'Relations_list["' + matched_entity + '"] = ' + str(existing_relations)
                
                
                tails = []
                if rel[0] == '~':
                    tails += db.getEntityFromEntRel(matched_entity, rel)
                    tails += db.getEntityFromEntRel(matched_entity, rel.split('~')[1])
                else:
                    tails += db.getEntityFromEntRel(matched_entity, rel)
                    tails += db.getEntityFromEntRel(matched_entity, '~' + rel)
                
                for tail in tails:
                    triples.append([matched_entity, rel, tail])





        if len(triples) >= 50:
            triples = triples[:50]
        if len(triples)==0:
            result_prompt += f"Choose other relations based refer to the Relations_list Or follow the format of Entity {ent} and Relations"
        
        else:
            result_prompt += ', '.join(str(sublist) for sublist in triples)
        
    except:
        result_prompt += "You gave wrong format of exploreKGs() function. Follow the format of examples."


    return triples, result_prompt

def verification(subagent, claim, gold_set, gold_relations, sub_prompt):
    if config.DATASET == 'CRONQUESTIONS':
        import CRONQ.subagent as sa
    elif config.DATASET == 'FactKG':
        import FactKG.subagent as sa
    elif config.DATASET == 'WebQSP':
        import WebQSP.subagent as sa
    elif config.DATASET == 'MetaQA':
        import MetaQA.subagent as sa
    sub_response, case, prediction = sa.feedback(subagent, claim, gold_set, gold_relations, sub_prompt)
    return sub_response, case, prediction




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, default='WebQSP', help='Dataset name')
    parser.add_argument('--model', type=str, default='gpt-4o-mini', help='Operator model name')
    parser.add_argument('--subagent', type=str, default='gpt-4o', help='Supervisor model name')
    parser.add_argument('--prompt', type=str, default='initial_prompt', help='Prompt for Opearator')
    parser.add_argument('--iter_limit', type=int, default=10, help='Iteration limit')
    args = parser.parse_args()

    config.DATASET = args.dataset

    if args.dataset == 'CRONQUESTIONS':
        import CRONQ.utils as cronq
        cronq.main(args)
    
    elif args.dataset == 'FactKG':
        import FactKG.utils as factkg
        factkg.main(args)

    pass