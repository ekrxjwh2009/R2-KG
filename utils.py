import re
from difflib import get_close_matches

class Model:
    def __init__(self, model_name, temperature, top_p, max_tokens=None):
        self.model_name = model_name
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens

def retrieval_relation_parse_answer(rel):
    post_rel = re.sub('[-=+,#/\?:^@*\"※ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', '', rel)
    return post_rel 

def preprocess_ent(ent):
    ent = ent.replace('\\', '')
    if (ent[0]=='"' and ent[-1]=='"') or (ent[0]=="'" and ent[-1]=="'"):
        return ent[1:-1].replace(' ', '_').lower()
    else:
        return ent.replace(' ', '_').lower()
    
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