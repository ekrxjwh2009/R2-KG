from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, Literal, RDF, URIRef
from collections import OrderedDict
from tqdm import tqdm
import itertools

database_path = "http://143.248.157.135:3030/"

datasets = ["article_categories",
            "category_labels_clean",
            "disambiguations",
            "genders",
            "infobox_properties_clean",
            "instance_types",
            "labels",
            "mappingbased_clean",
            "persondata",
            "redirects",
            "skos_categories",
            "template_parameters",
            "topical_concepts",
            "web_nlg"]  


prefix = ("""PREFIX dbpr: <http://dbpedia.org/resource/>\nPREFIX dbpo: <http://dbpedia.org/ontology/>\nPREFIX dbp: <http://dbpedia.org/property/>\nPREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\nPREFIX rdftype: <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>\nPREFIX dct: <http://purl.org/dc/terms/>\nPREFIX rdfslabel: <http://www.w3.org/2000/01/rdf-schema#label>\nPREFIX xmlns: <http://xmlns.com/foaf/0.1/>\nPREFIX gold: <http://purl.org/linguistics/gold/>\nPREFIX dc: <http://purl.org/dc/elements/1.1/>""")
prefix_dict = {'http': 'http://www.w3.org/2011/http#/',
            'dbp' : 'http://dbpedia.org/property/',
            'rdf' : 'http://www.w3.org/1999/02/22-rdf-syntax-ns#/',
            'rdfs' : 'http://www.w3.org/2000/01/rdf-schema#/',
            'rdftype' : 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type/',
            'dbpr' : 'http://dbpedia.org/resource/',
            'dbpo' : 'http://dbpedia.org/ontology/',
            'dct' : 'http://purl.org/dc/terms/',
            'rdfslabel' : 'http://www.w3.org/2000/01/rdf-schema#label/',
            'xmlns' : 'http://xmlns.com/foaf/0.1/',
            'gold' : 'http://purl.org/linguistics/gold/',
            'dc' : 'http://purl.org/dc/elements/1.1/'}

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
      dbpr:{entity_name} ?predicate ?object .
      BIND(dbpr:{entity_name} AS ?subject)
    }
    # LIMIT 10
"""
query_pred = """
    SELECT ?subject ?predicate ?object
    WHERE {
      ?subject dbpr:{entity_name} ?object .
      BIND(dbpr:{entity_name} AS ?predicate)
    }
    # LIMIT 10
"""
query_obj = """
    SELECT ?subject ?predicate ?object
    WHERE {
      ?subject ?predicate dbpr:{entity_name} .
      BIND(dbpr:{entity_name} AS ?object)
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
      ?subject <http://dbpedia.org/property/22-rdf-syntax-ns#type> dbpr:{type_name} .
      BIND(dbpr:{type_name} AS ?object)
    }
    LIMIT 10
"""

query_type_relation = """
    SELECT ?subject ?predicate ?object WHERE {
      dbpo:{type_left} ?predicate dbpo:{type_right} .
      BIND(dbpo:{type_left} AS ?subject)
      BIND(dbpo:{type_right} AS ?object)
    }
"""
query_type_relation_leftonly = """
    SELECT ?subject ?predicate ?object WHERE {
      dbpo:{type_left} ?predicate ?object .
      BIND(dbpo:{type_left} AS ?subject)
    }
"""
query_gettypes = """
    SELECT DISTINCT ?object WHERE {
      ?subject <http://dbpedia.org/property/22-rdf-syntax-ns#type> ?object .
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

# Fuseki 서버의 SPARQL 엔드포인트 설정
# 143.248.157.135
# sparql = SPARQLWrapper("http://localhost:3030/article_categories/query")

def queryResponse(query, dataset_elem="all"):
    results = {'head': {'vars': ['subject', 'predicate', 'object']}, 'results': {'bindings': []}}
    bindings = []
    if dataset_elem == "all":
        for ds in datasets:
            # print(database_path + f"{ds}/query")
            sparql = SPARQLWrapper(database_path + f"{ds}/query")
            sparql.setQuery(query)
            sparql.setReturnFormat(JSON)
            results_elem = sparql.query().convert()
            bindings += results_elem["results"]["bindings"]
    else:
        sparql = SPARQLWrapper(database_path + f"{dataset_elem}/query")
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results_elem = sparql.query().convert()
        bindings += results_elem["results"]["bindings"]
    
    results["results"]["bindings"] = bindings

    return results

### Temporal Error Solver!
# To avoid error from '-' included in entity.
# Can be solved in much clever way, but below function is for temporal error solver.
# def dash_solver(query_form, entity):
#     query = query_obj.replace("{entity_name}", entity)
#     query = query_sub.replace("{entity_name}", entity)
#     query = query_obj_leaf.replace("{entity_name}", leafNode)
#     query = query_type.replace("{type_name}", type)
#     query_template = [query_sub, query_obj, query_obj_leaf, query_type, query_nf]

#     if query_form == query_sub:
#         if '-' in entity:
#             ent = '<' + prefix_dict['dbpr'] + entity + '>'
#             query = query_sub.replace("dbpr:{entity_name}", ent)
    
#     if query_form == query_obj_leaf:




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
    uri = uri.strip('<').strip('>')
    if "http" in uri:
        if prefix_dict['dbpr'] in uri:
            word = uri.split(prefix_dict['dbpr'])[-1]
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

def getRelationsFromEntity(entity, dataset = "all"):
    rel = []
    if '"' not in entity:
        triples = getTriplesFromEntity(entity, dataset)
    else:
        triples = getTriplesFromLeafNode(entity, dataset)

    for trip in triples:
        rel.append(trip[1])

    return list(set(rel))

def getRelationsFromEntities(entity1, entity2, dataset = "all"):
    rel = []

    if entity1[0] != '?' and entity1[0] != '"':
        entity1_candidates = ['<' + prefix_dict['dbpr'] + entity1 + '>']
    else:
        entity1_candidates = [entity1]
    if entity2[0] != '?' and entity2[0] != '"':
        entity2_candidates = ['<' + prefix_dict['dbpr'] + entity2 + '>']
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
        entity1_candidates = ['<' + prefix_dict['dbpr'] + entity1 + '>']
    else:
        entity1_candidates = [entity1]
    if entity2[0] != '?' and entity2[0] != '"':
        entity2_candidates = ['<' + prefix_dict['dbpr'] + entity2 + '>']
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
        # print(query)
        # exit(0)
    
    # Convert each inner list to a tuple and use a set to remove duplicates
    unique_list = list(set(tuple(i) for i in triples))

    # Convert tuples back to lists
    unique_list = [list(i) for i in unique_list]

    # print(unique_list)
    return unique_list

# So far below function assume entity has prefix 'dbpr'.
def getTriplesFromEntity(entity, dataset = "all"):
    triples = []
    # entity = escape_special_chars(entity)
    try:
        # query = query_sub.replace("{entity_name}", entity)
        query = query_sub.replace("dbpr:{entity_name}", '<' + prefix_dict['dbpr'] + entity + '>')
        query = prefix + query
        results = queryResponse(query, dataset)
        for result in results["results"]["bindings"]:
            sub, pred, obj = result["subject"]["value"], result["predicate"]["value"], result["object"]["value"]
            triple_elem = [sub, pred, obj]
            tiple_elem = tripleToWord(triple_elem)
            triples.append(triple_elem)
            # print(triple_elem)
        
        # query = query_obj.replace("{entity_name}", entity)
        query = query_obj.replace("dbpr:{entity_name}", '<' + prefix_dict['dbpr'] + entity + '>')
        query = prefix + query
        results = queryResponse(query, dataset)
        for result in results["results"]["bindings"]:
            sub, pred, obj = result["subject"]["value"], result["predicate"]["value"], result["object"]["value"]
            triple_elem = [sub, pred, obj]
            temp = tripleToWord(triple_elem)
            temp[0], temp[1], temp[2] = temp[2], '~'+temp[1], temp[0]
            triple_elem = temp
            triples.append(triple_elem)
            # print(triple_elem)
    except:
        print(entity)
        # print(query)
        # exit(0)
    
    # Convert each inner list to a tuple and use a set to remove duplicates
    unique_list = list(set(tuple(i) for i in triples))

    # Convert tuples back to lists
    unique_list = [list(i) for i in unique_list]

    # print(unique_list)
    return unique_list


def getTriplesFromEntityandLeaf(entity, dataset = 'all'):
    triples = []
    if '"' not in entity:
        triples = getTriplesFromEntity(entity, dataset)
    else:
        triples = getTriplesFromLeafNode(entity, dataset)

    for trip in triples:
        triples.append(trip)

    return list(set(triples))


def getEntityFromEntRel(entity, relation, dataset = "all"):
    tails = []
    reverseflag = False
    ent = entity
    if '"' not in entity:
        ent = escape_special_chars(entity)
    if '~' in relation:
        relation = relation.split('~')[1]
        reverseflag = True
    sub = ['dbpr:' + ent, entity]
    obj = ['dbpr:' + ent, entity]
    rel = ['dbp:' + relation]

    if not reverseflag:
        for s in sub:
            for r in rel:
                pref_ent = s.split(':')[0]
                if 'dbpr' in pref_ent:
                    if '–' in s:
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
                if 'dbpr' in pref_ent:
                    if '–' in o:
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

    if entity1[0] != '?' and entity1[0] != '"':
        entity1_candidates = ['<' + prefix_dict['dbpr'] + entity1 + '>']
    else:
        entity1_candidates = [entity1]
    if entity2[0] != '?' and entity2[0] != '"':
        entity2_candidates = ['<' + prefix_dict['dbpr'] + entity2 + '>']
    else:
        entity2_candidates = [entity2]
    
    relation = '<' + prefix_dict['dbp'] + rel + '>'

    try:
        for ent1 in entity1_candidates:
            for ent2 in entity2_candidates:
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
        return 
    return 

def getTypes():
    types = []
    query = prefix + query_gettypes
    try:
        results = queryResponse(query, "instance_types")
        for result in results["results"]["bindings"]:
            s = result["object"]["value"]
            types.append(uriToWord(s))
    except:
        pass
    types = list(set(types))
    return types

# entity_set must be head, tail entity set
def addPrefix(entity_set):
    result = []
    prefix = ['dbpr']
    head = entity_set[0]
    head_pref = []
    tail = entity_set[1]
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
    
    return result

# entity_set must be head, tail entity set
def addPrefix_withrel(entity_set):
    result = []
    prefix = ['dbpr']
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
        temp.insert(1, '<' + prefix_dict['dbp'] + entity_set[1] + '>')
    return result



if __name__ == '__main__':
    graph = testSPARQL(['article_categories_en_1.ttl', 'article_categories_en_2.ttl'])

    query = """
    SELECT ?subject ?predicate ?object
    WHERE {
      ?subject ?predicate ?object .
      #BIND(dbpr:{entity_name} AS ?predicate)
    }
    LIMIT 10
    """
    qres = graph.query(query)
    print(qres)