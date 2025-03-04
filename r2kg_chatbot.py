import sys, os
import openai
from openai import OpenAI
import argparse
import utils
import config
from dotenv import load_dotenv
from model import LLMBot


current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)
load_dotenv()

openai.api_key = os.getenv('OPENAI_KEY')

client = OpenAI(
    api_key = os.getenv('OPENAI_KEY')
)


class OpenAIBot:
    def __init__(self, engine, client, temp, top_p):
        # Initialize conversation with a system message
        self.conversation = [{"role": "system", "content": "You are a helpful assistant."}]
        self.engine = engine
        self.client = client
        self.temperature = temp
        self.top_p = top_p

    def add_message(self, role, content):
        # Adds a message to the conversation.
        self.conversation.append({"role": role, "content": content})

    def generate_response(self, prompt):
        # Add user prompt to conversation
        self.add_message("user", prompt)

        try:
            # Make a request to the API using the chat-based endpoint with conversation context
            response = self.client.chat.completions.create(model=self.engine, messages=self.conversation, temperature=self.temperature, top_p=self.top_p)
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
        

def reasoning(operator, supervisor, claim, iter_limit, initial_prompt, sub_prompt, entities, f, KG=[], info=None):
    if operator[0] =='gpt-4o-mini': 
        engine = "gpt-4o-mini-2024-07-18"
        chatbot = OpenAIBot(engine, client, operator[1], operator[2])

    elif operator[0] == 'gpt-4o': 
        engine = "gpt-4o-2024-08-06"
        chatbot = OpenAIBot(engine, client, operator[1], operator[2])
    
    else:
        chatbot = LLMBot(operator[0], operator[1], operator[2], 2000)


    gold_set =[]
    gold_relations =''
    gold_entities =[]

    for i in range(iter_limit):
        # Get Prompt from User
        if i == 0:
            prompt = initial_prompt
            gold_entities += entities

        else:
            prompt, result, triples, relations, get_rel_state, new_entites = client_answer(claim, supervisor, response, gold_set, gold_relations, sub_prompt, gold_entities, KG, info)
            
            if len(triples) > 0:
                gold_set += triples
            if get_rel_state == 1:
                gold_relations += relations
            if len(new_entites) > 0:
                gold_entities += new_entites  
        
        if 'Done!!' in prompt:
            print(f"Prediction : {result}")
            break
        
        if i > 0:    
            f.write(prompt)

        # Generate and Print the Response from ChatBot
        response = chatbot.generate_response(prompt)
        if response == None or 'Error' in response:
            return 'Abstain', i
        
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
        prompt = "\n[User]\nYou gave wrong format of Statement and Helper function."
        
    return helper_ftn_calls, prompt


def client_answer(claim, supervisor, response, gold_set, gold_relations, sub_prompt, gold_entities, KG=[], info=None):
    result = None

    helper_ftn_calls, prompt = split_functions(response)
    triples = []
    new_entities = []
    relations = ""
    get_rel_state = 0

    for helper_str in helper_ftn_calls:
        if 'getRelation' in helper_str:
            get_rel_state, result = getRelations(helper_str, gold_entities, KG, info)
            prompt +=  "\n" + result
            if get_rel_state == 1:
                relations += "\n" + result
            
        elif 'exploreKG' in helper_str:
            result, result_prompt = exploreKGs(helper_str, gold_entities, KG, info)
            prompt += "\n" + result_prompt
            triples += result
            
            #For matching entities
            new_entities += utils.find_new_entity(triples)
            
        elif 'Verification' in helper_str:
            sub_answer, result = verification(helper_str, supervisor, claim, gold_set, gold_relations, sub_prompt)
            prompt += "\n" +sub_answer
            
        else:
            prompt += '\nYou gave wrong format. Call the helper function again follow the right format'
            result =''
    
    return prompt, result, triples, relations, get_rel_state, new_entities



def getRelations(helper_str, gold_entities, KG, info):
    relations = []
    state = 0

    try:
        entity = helper_str.split("getRelation[")[1].split("]")[0].strip()[1:-1]
        #Entity matching
        matched_entity = utils.match_and_replace_single(entity, gold_entities)
        # print(f"Before :{entity}, matched:{matched_entity}")

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
            import WebQSP.freebase_sparql as db
            if entity in info.mid_dict.keys(): mid = info.mid_dict[entity]
            else: raise NotImplementedError

            relations += db.getRelationsFromEntity(mid)
            rels = []
            for rel in relations:
                rel_keyword = rel.split('/')[-1]
                rels.append(rel_keyword)
                if rel_keyword in info.rel_dict.keys():
                    continue
                else:
                    info.rel_dict[rel_keyword] = rel
            relations = rels
        
        elif config.DATASET == 'MetaQA':
            import MetaQA.movie_sparql as db
            entity = utils.preprocess_ent(entity)

            relations += db.getRelationsFromEntity(entity)

        if len(relations) == 0:
            state = 0
            return state, f"Do not change the format of entity {entity} in helper function."
        else:
            state = 1
            return state, 'Relations_list["' + matched_entity + '"] = ' + str(relations)
        
    except:
        return state,"You gave wrong format of getRelations() function. Follow the format of examples."
    
def exploreKGs(helper_str, gold_entities, KG, info):
    triples= []
    result_prompt = ''
    try: 
        ent = helper_str.split("exploreKG[")[1].split("]=")[0].strip()[1:-1]
        relations = helper_str.split('=[')[1].split(']')[0].strip().split(', ')
        #Entity matching
        matched_entity = utils.match_and_replace_single(ent, gold_entities)

        if config.DATASET == 'CRONQUESTIONS':
            subgraphs = KG[matched_entity]
            existing_relations = []
            for graph in subgraphs:
                exist_rel = graph[1]
                if exist_rel not in existing_relations:
                    existing_relations.append(exist_rel) 
            
            for rel in relations:
                rel = rel[1:-1]
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
                existing_relations = db.getRelationsFromEntity(matched_entity)
                if (rel not in existing_relations) and ('~' + rel) not in existing_relations:
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

        elif config.DATASET == 'WebQSP':
            import WebQSP.freebase_sparql as db
            ent_mid = info.mid_dict[ent]

            for rel in relations:
                rel = utils.retrieval_relation_parse_answer(rel)
                tails = []
                tails += db.getEntityFromEntRel(ent_mid, rel)
                for tail in tails:
                    name = db.mid2name(tail)
                    if name in list(info.gt_entity): continue
                    # CVT node or Name converted entity
                    info.mid_dict[name] = tail
                    triples.append([ent, rel, name])

        elif config.DATASET == 'MetaQA':
            import MetaQA.movie_sparql as db
            ent = utils.preprocess_ent(ent)
            for rel in relations:
                rel = utils.retrieval_relation_parse_answer(rel)
                existing_relations = db.getRelationsFromEntity(ent)
                if (rel not in existing_relations) and ('~' + rel) not in existing_relations:
                    result_prompt += f"The relation you chose '{rel}' does not exist."
                    continue

                tails = []

                if rel[0] == '~':
                    tails += db.getEntityFromEntRel(ent, rel)
                    tails += db.getEntityFromEntRel(ent, rel.split('~')[1])
                else:
                    tails += db.getEntityFromEntRel(ent, rel)
                    tails += db.getEntityFromEntRel(ent, '~' + rel)
                
                for tail in tails:
                    if tail == info.gt_entity: continue # MetaQA dataset doesn't contain gt_entity while the hop goes by.
                    triples.append([ent, rel, tail])


        if len(triples) >= 50:
            triples = triples[:50]
        if len(triples) == 0:
            result_prompt += f"Choose other relations based refer to the Relations_list Or follow the format of Entity {ent} and Relations"
        
        else:
            result_prompt += ', '.join(str(sublist) for sublist in triples)
        
    except:
        result_prompt += "You gave wrong format of exploreKGs() function. Follow the format of examples."


    return triples, result_prompt

def verification(helper_str, supervisor, claim, gold_set, gold_relations, sub_prompt):
    if config.SINGLE_AGENT: # For Single-Agent mode
        if ' ## ' in helper_str:
            helper_str = helper_str.split(' ## ')[0]
        
        try: 
            prediction = helper_str.split("Verification[")[1].split("]")[0]
            sub_response = f"\nDone!!\nPrediction:{prediction}"
        except:
            sub_response = '\nYou gave wrong format. Call the verification function again follow the right format'

    else: # For Dual-Agent mode
        if config.DATASET == 'CRONQUESTIONS':
            import CRONQ.supervisor as sa
        elif config.DATASET == 'FactKG':
            import FactKG.supervisor as sa
        elif config.DATASET == 'WebQSP':
            import WebQSP.supervisor as sa
        elif config.DATASET == 'MetaQA':
            import MetaQA.supervisor as sa
        sub_response, prediction = sa.feedback(supervisor, claim, gold_set, gold_relations, sub_prompt)

    if prediction != None:
        if config.DATASET == 'WebQSP' or config.DATASET == 'MetaQA':
            prediction = '[' + prediction + ']' if not str(prediction).startswith("[") else prediction
        
    return sub_response, prediction




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, default='WebQSP', help='Dataset name')
    parser.add_argument('--operator', type=str, default='gpt-4o-mini', help='Operator model name')
    parser.add_argument('--supervisor', type=str, default='gpt-4o', help='Supervisor model name')
    parser.add_argument('--prompt', type=str, default='pr_1', help='Prompt for Opearator')
    parser.add_argument('--iter_limit', type=int, default=15, help='Iteration limit')
    parser.add_argument('--temperature', type=float, default=0.95, help='Temperature for Operator')
    parser.add_argument('--top_p', type=float, default=0.95, help='Top p for Operator')
    parser.add_argument('-paraphrase', action='store_true', help='Paraphrase the claim')
    parser.add_argument('-single_agent', action='store_true', help='Single mode')
    args = parser.parse_args()

    config.DATASET = args.dataset
    config.SINGLE_AGENT = True if args.single_agent else False

    if args.dataset == 'CRONQUESTIONS':
        import CRONQ.utils as cronq
        cronq.main(args)
    
    elif args.dataset == 'FactKG':
        import FactKG.utils as factkg
        factkg.main(args)
    
    elif args.dataset == 'WebQSP':
        import WebQSP.utils as webqsp
        webqsp.main(args)
    
    elif args.dataset == 'MetaQA':
        import MetaQA.utils as metaqa
        metaqa.main(args)
