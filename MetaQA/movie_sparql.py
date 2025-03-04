from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, Literal, URIRef
from tqdm import tqdm
import itertools
import re

DATABASE_PATH = "[SPARQL SERVER URL]"

## Store the dataset with the name: "metaqa"
datasets = ["metaqa"]  


prefix = ("""PREFIX metaent: <http://movie.com/resource/>\nPREFIX metarel: <http://movie.com/property/>\n""")
prefix_dict = {'metaent': 'http://movie.com/resource/',
            'metarel' : 'http://movie.com/property/',
            }

query_nf = """
    SELECT ?subject ?predicate ?object
    WHERE {
        {?subject} {?predicate} {?object} .
    }
"""

query_rel = """
    SELECT ?predicate 
    WHERE {
        {?subject} ?predicate {?object} .
    }
"""

query_sub = """
    SELECT ?subject ?predicate ?object
    WHERE {
      metaent:{entity_name} ?predicate ?object .
      BIND(metaent:{entity_name} AS ?subject)
    }
    # LIMIT 10
"""
query_pred = """
    SELECT ?subject ?predicate ?object
    WHERE {
      ?subject metaent:{entity_name} ?object .
      BIND(metaent:{entity_name} AS ?predicate)
    }
    # LIMIT 10
"""
query_obj = """
    SELECT ?subject ?predicate ?object
    WHERE {
      ?subject ?predicate metaent:{entity_name} .
      BIND(metaent:{entity_name} AS ?object)
    }
    # LIMIT 10
"""

query_obj_leaf = """
    SELECT ?subject ?predicate ?object
    WHERE {
      ?subject ?predicate {entity_name} .
      BIND({entity_name} AS ?object)
    }
    # LIMIT 10
"""

query_type = """
    SELECT ?subject ?predicate ?object WHERE {
      ?subject ?predicate metaent:{type_name} .
      BIND(metaent:{type_name} AS ?object)
    }
    LIMIT 10
"""

query_type_relation = """
    SELECT ?subject ?predicate ?object WHERE {
      metaent:{type_left} ?predicate metaent:{type_right} .
      BIND(metaent:{type_left} AS ?subject)
      BIND(metaent:{type_right} AS ?object)
    }
"""
query_type_relation_leftonly = """
    SELECT ?subject ?predicate ?object WHERE {
      metaent:{type_left} ?predicate ?object .
      BIND(metaent:{type_left} AS ?subject)
    }
"""
query_gettypes = """
    SELECT DISTINCT ?subject WHERE {
      ?subject ?predicate ?object .
    }
"""


def testSPARQL(filelist):
    graph = Graph()
    for f in tqdm(filelist):
        with open(f, 'r') as ff:
            lines = ff.readlines()
            for line in lines:
                temp = line.split(' ')
                head = temp[0]
                rel = temp[1]
                tail = ' '.join(temp[2:]).strip()
                # print(tail[-5:])
                if tail[-2:] == ' .':
                    tail = tail[:-2]
                else:
                    tail = tail[:-1]
                temp = [head, rel, tail]
                for i in range(3):
                    if temp[i][0] == '<' and temp[i][-1] == '>':
                        temp[i] = temp[i][1 : -1]
                
                if temp[2][0] == '"':
                    graph.add((URIRef(temp[0]), URIRef(temp[1]), Literal(temp[2])))
                else:
                    graph.add((URIRef(temp[0]), URIRef(temp[1]), URIRef(temp[2])))
                # print([head, rel, tail])
                
    return graph

def queryResponse(query, dataset_elem="all"):
    if prefix not in query:
        query = prefix + query
    # print(query)
    results = {'head': {'vars': ['subject', 'predicate', 'object']}, 'results': {'bindings': []}}
    bindings = []
    if dataset_elem == "all":
        for ds in datasets:
            # print(DATABASE_PATH + f"{ds}/query")
            sparql = SPARQLWrapper(DATABASE_PATH + f"{ds}/query")
            sparql.setQuery(query)
            sparql.setReturnFormat(JSON)
            results_elem = sparql.query().convert()
            bindings += results_elem["results"]["bindings"]
    else:
        sparql = SPARQLWrapper(DATABASE_PATH + f"{dataset_elem}/query")
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results_elem = sparql.query().convert()
        bindings += results_elem["results"]["bindings"]
    
    results["results"]["bindings"] = bindings

    return results


def escape_special_chars(s):
    special_chars = [
        ' ', '\t', '\n', '{', '}', '(', ')', '[', ']', ';', ',', '.', "'", '"',
        "'''", '"""', '#', '^^', '@', '<', '>', '*', '+', '?', '$'
    ]

    # First, escape any existing backslashes
    s = s.replace('\\', '\\\\')

    # Then replace each special character (except backslash) with a backslash followed by the character
    for char in special_chars:
        if char != '\\':  # Already handled backslashes
            s = s.replace(char, '\\' + char)

    return s

def uriToWord(uri):
    if "http" in uri:
        if prefix_dict['metaent'] in uri:
            word = uri.split(prefix_dict['metaent'])[-1]
        elif 'ontology' in uri and len(uri.split('/')) == 6:
            word = uri.split('/')[-2] + '/' + uri.split('/')[-1]
        else:
            word = uri.split('/')[-1]
    else:
        word = '"' + uri + '"'
    return word

def tripleToWord(triple):
    triple[0], triple[1], triple[2] = uriToWord(triple[0]), uriToWord(triple[1]), uriToWord(triple[2])
    return triple

def isType(type):
    if type[0] == '"':
        return False
    if "–" in type:
        return False
    type = escape_special_chars(type)
    query = query_type.replace("{type_name}", type)
    query = prefix + query
    results = queryResponse(query, 'instance_types')
    result = results["results"]["bindings"]
    if len(result) == 0:
        return False
    else:
        return True

def getRelationsFromTriples(triples):
    rel = []
    for trip in triples:
        rel.append(trip[1])
    return list(set(rel))

def getRelationsFromEntity(entity, dataset = "all", noInverse = False):
    rel = []
    if '"' not in entity:
        triples = getTriplesFromEntity(entity, dataset)
    else:
        triples = getTriplesFromLeafNode(entity, dataset)

    for trip in triples:
        if not noInverse:
            rel.append(trip[1])
        else:
            if trip[1][0] == '~':
                rel.append(trip[1].split('~')[1])
            else:
                rel.append(trip[1])

    return list(set(rel))

def getRelationsFromEntities(entity1, entity2, dataset = "all"):
    rel = []

    if entity1[0] != '?' and entity1[0] != '"':
        entity1_candidates = ['<' + prefix_dict['metaent'] + entity1 + '>']
    else:
        entity1_candidates = [entity1]
    if entity2[0] != '?' and entity2[0] != '"':
        entity2_candidates = ['<' + prefix_dict['metaent'] + entity2 + '>']
    else:
        entity2_candidates = [entity2]

    try:
        for ent1 in entity1_candidates:
            for ent2 in entity2_candidates:
                query = query_rel.replace("{?subject}", ent1).replace("{?object}", ent2)
                query = prefix + query
                results = queryResponse(query, dataset)
                for result in results["results"]["bindings"]:
                    pred = result["predicate"]["value"]
                    rel.append(pred)
                
                query = query_rel.replace("{?subject}", ent2).replace("{?object}", ent1)
                query = prefix + query
                results = queryResponse(query, dataset)
                for result in results["results"]["bindings"]:
                    pred = result["predicate"]["value"]
                    rel.append(pred)
        # print(rel)
    except:
        pass
    return list(set(rel))


# Input
# entity1 : written-style entity (ex. Alan_Bean)
# entity2 : written-style entity 
# Output
# triple : triple sets from entity1 and entity2 with written-style ([ ['Alan_Bean', 'nationality', 'United_States'] ])
def getTriplesFromEntities(entity1, entity2, dataset = "all"):
    triple = []

    if entity1[0] != '?' and entity1[0] != '"':
        entity1_candidates = ['<' + prefix_dict['metaent'] + entity1 + '>']
    else:
        entity1_candidates = [entity1]
    if entity2[0] != '?' and entity2[0] != '"':
        entity2_candidates = ['<' + prefix_dict['metaent'] + entity2 + '>']
    else:
        entity2_candidates = [entity2]

    try:
        for ent1 in entity1_candidates:
            for ent2 in entity2_candidates:
                query = query_rel.replace("{?subject}", ent1).replace("{?object}", ent2)
                query = prefix + query
                results = queryResponse(query, dataset)
                for result in results["results"]["bindings"]:
                    pred = result["predicate"]["value"]
                    if [ent1, pred, ent2] not in triple:
                        triple.append(tripleToWord([ent1, pred, ent2]))
                
                query = query_rel.replace("{?subject}", ent2).replace("{?object}", ent1)
                query = prefix + query
                results = queryResponse(query, dataset)
                for result in results["results"]["bindings"]:
                    pred = result["predicate"]["value"]
                    if [ent2, pred, ent1] not in triple:
                        triple.append(tripleToWord([ent2, pred, ent1]))
        # print(rel)
    except:
        pass
    return triple

def getTriplesFromLeafNode(leafNode, dataset = "all"):
    triples = []
    try:
        query = query_obj_leaf.replace("{entity_name}", leafNode)
        query = prefix + query
        results = queryResponse(query, dataset)
        for result in results["results"]["bindings"]:
            sub, pred, obj = result["subject"]["value"], result["predicate"]["value"], result["object"]["value"]
            triple_elem = [sub, pred, obj]
            # tiple_elem = tripleToWord(triple_elem)

            temp = tripleToWord(triple_elem)
            temp[0], temp[1], temp[2] = temp[2], '~'+temp[1], temp[0]
            triple_elem = temp
            
            triples.append(triple_elem)
    except:
        print(leafNode)
    
    # Convert each inner list to a tuple and use a set to remove duplicates
    unique_list = list(set(tuple(i) for i in triples))

    # Convert tuples back to lists
    unique_list = [list(i) for i in unique_list]

    return unique_list

# So far below function assume entity has prefix 'metaent'.
def getTriplesFromEntity(entity, dataset = "all"):
    triples = []
    query = query_sub.replace("metaent:{entity_name}", '<' + prefix_dict['metaent'] + entity + '>')
    query = prefix + query
    results = queryResponse(query, dataset)
    for result in results["results"]["bindings"]:
        sub, pred, obj = result["subject"]["value"], result["predicate"]["value"], result["object"]["value"]
        triple_elem = [sub, pred, obj]
        triple_elem = tripleToWord(triple_elem)
        triples.append(triple_elem)
        # print(triple_elem)
    
    # query = query_obj.replace("{entity_name}", entity)
    query = query_obj.replace("metaent:{entity_name}", '<' + prefix_dict['metaent'] + entity + '>')
    query = prefix + query
    results = queryResponse(query, dataset)
    for result in results["results"]["bindings"]:
        sub, pred, obj = result["subject"]["value"], result["predicate"]["value"], result["object"]["value"]
        triple_elem = [sub, pred, obj]
        temp = tripleToWord(triple_elem)
        temp[0], temp[1], temp[2] = temp[2], '~'+temp[1], temp[0]
        triple_elem = temp
        triples.append(triple_elem)
    
    # Convert each inner list to a tuple and use a set to remove duplicates
    unique_list = list(set(tuple(i) for i in triples))

    # Convert tuples back to lists
    unique_list = [list(i) for i in unique_list]

    # print(unique_list)
    return unique_list


def getEntityFromEntRel(entity, relation, dataset = "all"):
    tails = []
    reverseflag = False
    ent = entity
    if '"' not in entity:
        ent = escape_special_chars(entity)
    if '~' in relation:
        relation = relation.split('~')[1]
        reverseflag = True
    sub = ['metaent:' + ent, entity]
    obj = ['metaent:' + ent, entity]
    rel = ['metarel:' + relation]

    if not reverseflag:
        for s in sub:
            for r in rel:
                pref_ent = s.split(':')[0]
                if 'metaent' in pref_ent:
                    # if '–' in s:
                    s = '<' + prefix_dict[pref_ent] + entity + '>'
                        
                query = prefix + query_nf.replace('{?subject}', s).replace('{?predicate}', r).replace('{?object}', '?object')

                try:
                    results = queryResponse(query, dataset)
                    for result in results["results"]["bindings"]:
                        o = result["object"]["value"]
                        o = uriToWord(o)
                        tails.append(o)
                except:
                    continue
    else:
        for o in obj:
            for r in rel:
                pref_ent = o.split(':')[0]
                if 'metaent' in pref_ent:
                    # if '–' in o:
                    o = '<' + prefix_dict[pref_ent] + entity + '>'

                query = prefix + query_nf.replace('{?object}', o).replace('{?predicate}', r).replace('{?subject}', '?subject')
                
                try:
                    results = queryResponse(query, dataset)
                    for result in results["results"]["bindings"]:
                        s = result["subject"]["value"]
                        s = uriToWord(s)
                        tails.append(s)
                except:
                    continue
    return list(set(tails))


def getRelationsFromTypes(type_left, type_right = ''):
    rel = []
    if type_right == '':
        query = prefix + query_type_relation_leftonly.replace('{type_left}', type_left)
        try:
            results = queryResponse(query, "type_dict")
            # print(results)
            for result in results["results"]["bindings"]:
                s = result["predicate"]["value"]
                rel.append(uriToWord(s))
        except:
            pass
    else:
        query = prefix + query_type_relation.replace('{type_left}', type_left).replace('{type_right}', type_right)
        try:
            results = queryResponse(query, "type_dict")
            # print(results)
            for result in results["results"]["bindings"]:
                s = result["predicate"]["value"]
                rel.append(uriToWord(s))
        except:
            pass
    rel = list(set(rel))
    
    return rel

def tripleDirection(entity1, entity2, rel, dataset = "all"):
    triple = []

    if entity1[0] != '?':# and entity1[0] != '"':
        entity1_candidates = ['<' + prefix_dict['metaent'] + entity1 + '>']
    else:
        entity1_candidates = [entity1]
    if entity2[0] != '?':# and entity2[0] != '"':
        entity2_candidates = ['<' + prefix_dict['metaent'] + entity2 + '>']
    else:
        entity2_candidates = [entity2]
    
    relation = '<' + prefix_dict['metarel'] + rel + '>'

    try:
        for ent1 in entity1_candidates:
            for ent2 in entity2_candidates:
                if ent1[0] == '<':
                    ent1 = re.sub(r'\\(.)', r'\1', ent1.replace('"', ''))
                if ent2[0] == '<':
                    ent2 = re.sub(r'\\(.)', r'\1', ent2.replace('"', ''))
                query = query_nf.replace("{?subject}", ent1).replace("{?predicate}", relation).replace("{?object}", ent2)
                query = prefix + query
                results = queryResponse(query, dataset)
                for result in results["results"]["bindings"]:
                    if [entity1, rel ,entity2] not in triple:
                        return [entity1, rel, entity2]
                
                query = query_nf.replace("{?subject}", ent2).replace("{?predicate}", relation).replace("{?object}", ent1)
                query = prefix + query
                results = queryResponse(query, dataset)
                for result in results["results"]["bindings"]:
                    if [entity2, rel, entity1] not in triple:
                        return [entity2, rel, entity1]
        # print(rel)
    except:
        return None
    return None

def getTypes():
    types = []
    query = prefix + query_gettypes
    try:
        results = queryResponse(query, "type_dict")
        for result in results["results"]["bindings"]:
            s = result["subject"]["value"]
            types.append(uriToWord(s))
    except:
        pass
    types = list(set(types))
    return types

# entity_set must be head, tail entity set
def addPrefix(entity_set):
    result = []
    prefix = ['metaent']
    head = entity_set[0]
    head_pref = []
    tail = entity_set[2]
    tail_pref = []
    
    if head[0] != '"':
        for pref in prefix:
            head_pref.append('<' + prefix_dict[pref] + head + '>')
    else:
        head_pref.append(head)
    if tail[0] != '"':
        for pref in prefix:
            tail_pref.append('<' + prefix_dict[pref] + tail + '>')
    else:
        tail_pref.append(tail)
    
    head_tail = [head_pref, tail_pref]
    tail_head = [tail_pref, head_pref]
    for combination in itertools.product(*head_tail):
        result.append(list(combination))
    for combination in itertools.product(*tail_head):
        result.append(list(combination))
    
    for temp in result:
        temp.insert(1, '<' + prefix_dict['metarel'] + entity_set[1] + '>')
    return result


def existEntity(ent):
    ent = re.sub(r'\\(.)', r'\1', ent.replace(' ', '_').lower())
    triple = getTriplesFromEntity(ent)
    if len(triple) > 0:
        return True
    else:
        return False
