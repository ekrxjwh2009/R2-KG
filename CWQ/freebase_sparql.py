from SPARQLWrapper import SPARQLWrapper, JSON
import itertools
import re

DATABASE_PATH = "[SPARQL SERVER URL]"

prefix = "PREFIX ns: <http://rdf.freebase.com/ns/>\nPREFIX nsk: <http://rdf.freebase.com/key/>"
prefix_dict = {'ns': 'http://rdf.freebase.com/ns/',
               'nsk': 'http://rdf.freebase.com/key/'}

query_nf = """
    SELECT ?subject ?predicate ?object
    WHERE {
        ?subject ?predicate ?object .
    }
"""

query_rel = """
    SELECT DISTINCT ?predicate 
    WHERE {
        ?subject ?predicate ?object .
    }
"""

query_sub = """
    SELECT ?subject ?predicate ?object
    WHERE {
      ns:{entity_name} ?predicate ?object .
      BIND(ns:{entity_name} AS ?subject)
    }
    # LIMIT 10
"""
query_pred = """
    SELECT ?subject ?predicate ?object
    WHERE {
      ?subject ns:{entity_name} ?object .
      BIND(ns:{entity_name} AS ?predicate)
    }
    # LIMIT 10
"""
query_obj = """
    SELECT ?subject ?predicate ?object
    WHERE {
      ?subject ?predicate ns:{entity_name} .
      BIND(ns:{entity_name} AS ?object)
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

query_type_relation = """
    SELECT ?subject ?predicate ?object WHERE {
      dbpo:{type_left} ?predicate dbpo:{type_right} .
      BIND(dbpo:{type_left} AS ?subject)
      BIND(dbpo:{type_right} AS ?object)
    }
"""

query_getmidname = """
    SELECT DISTINCT ?name WHERE {
        ?mid <http://rdf.freebase.com/ns/type.object.name> ?name
    }
"""

query_exist = """
    ASK WHERE {
        ?subject ?predicate ?object .
    }
"""

def replace_unicode_sequences(s):
    return re.sub(r'\$([0-9A-Fa-f]{4})', lambda x: chr(int(x.group(1), 16)), s)

def uriToWord(uri):
    uri = uri.strip('<').strip('>')
    if "http" in uri:
        if prefix_dict['ns'] in uri:
            word = uri.split(prefix_dict['ns'])[-1]
        else:
            print('No freebase prefix in uri')
            raise NotImplementedError
    else:
        word = uri
    return word

def relToUri(rel):
    ns = query_exist.replace('?predicate', '<' + prefix_dict['ns'] + rel + '>')
    nsk = query_exist.replace('?predicate', '<' + prefix_dict['nsk'] + rel + '>')

    try:
        sparql = SPARQLWrapper(DATABASE_PATH)
        sparql.setQuery(prefix + ns)
        sparql.setReturnFormat(JSON)
        results_elem = sparql.query().convert()

        if results_elem['boolean']: return '<' + prefix_dict['ns'] + rel + '>'
        
        sparql = SPARQLWrapper(DATABASE_PATH)
        sparql.setQuery(prefix + nsk)
        sparql.setReturnFormat(JSON)
        results_elem = sparql.query().convert()

        if results_elem['boolean']: return '<' + prefix_dict['nsk'] + rel + '>'

        return False
    except:
        return False


def ismid(entity):
    entity = '<' + prefix_dict['ns'] + entity + '>'
    exist_sub = query_exist.replace('?subject', entity)
    exist_obj = query_exist.replace('?object', entity)
    try:
        sparql = SPARQLWrapper(DATABASE_PATH)
        sparql.setQuery(prefix + exist_sub)
        sparql.setReturnFormat(JSON)
        results_elem = sparql.query().convert()

        res_sub = results_elem['boolean']

        if res_sub: return True

        sparql = SPARQLWrapper(DATABASE_PATH)
        sparql.setQuery(prefix + exist_obj)
        sparql.setReturnFormat(JSON)
        results_elem = sparql.query().convert()

        res_obj = results_elem['boolean']

        if res_obj: return True

        return False
    
    except:
        return False

def isleaf(entity):
    exist = query_exist.replace('?object', '"' + entity + '"')
    sparql = SPARQLWrapper(DATABASE_PATH)
    sparql.setQuery(prefix + exist)
    sparql.setReturnFormat(JSON)
    results_elem = sparql.query().convert()

    res_sub = results_elem['boolean']

    if res_sub: return True

    exist = query_exist.replace('?object', '"' + entity + '"@en')
    sparql = SPARQLWrapper(DATABASE_PATH)
    sparql.setQuery(prefix + exist)
    sparql.setReturnFormat(JSON)
    results_elem = sparql.query().convert()

    res_sub = results_elem['boolean']

    if res_sub: return True

    return False

# Convert Freebase MID into name
def mid2name(mid):
    temp = mid
    if 'http://' in mid and '<' not in mid: mid = '<' + mid + '>'
    elif 'http://' not in mid: mid = '<http://rdf.freebase.com/ns/' + mid + '>'
    else: raise NotImplementedError

    query = query_getmidname.replace('?mid', mid)

    results = queryResponse(query)
    names = []

    for result in results["results"]["bindings"]:
        if result["name"]["xml:lang"] == "en":
            name = result["name"]["value"]
            names.append(name)
    
    # print(names)
    if len(names) != 1: return temp

    return names[0]
    


def queryResponse(query):
    results = {'head': {'vars': ['subject', 'predicate', 'object']}, 'results': {'bindings': []}}
    bindings = []

    sparql = SPARQLWrapper(DATABASE_PATH)
    sparql.setQuery(prefix + query)
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

def tripleToWord(triple):
    triple[0], triple[1], triple[2] = uriToWord(triple[0]), uriToWord(triple[1]), uriToWord(triple[2])
    return triple

def getRelationsFromTriples(triples):
    rel = []
    for trip in triples:
        rel.append(trip[1])
    return list(set(rel))

def nowiki(rels):
    res = []

    for r in rels:
        if 'wikipedia' in r or 'w3.org' in r: continue
        else: res.append(r)
    
    return res

def getRelationsFromEnt(entity):
    rels = []
    try:
        query = query_rel.replace("?subject", '<' + prefix_dict['ns'] + entity + '>')
        query = prefix + query
        # print(query)
        results = queryResponse(query)
        for result in results["results"]["bindings"]:
            pred = result["predicate"]["value"]
            rels.append(pred)
            # print(triple_elem)
        
    except:
        pass
    
    # Convert each inner list to a tuple and use a set to remove duplicates
    rels = list(set(rels))
    rels = nowiki(rels)

    # print(unique_list)
    return rels

def getRelationsFromLeaf(entity):
    rels = []
    # entity = escape_special_chars(entity)
    try:
        query = query_rel.replace("?object", '"' + entity + '"')
        query = prefix + query
        results = queryResponse(query)
        for result in results["results"]["bindings"]:
            pred = result["predicate"]["value"]
            rels.append(pred)
            # print(triple_elem)
        
        query = query_rel.replace("?object", '"' + entity + '"@en')
        query = prefix + query
        # print(query)
        results = queryResponse(query)
        for result in results["results"]["bindings"]:
            pred = result["predicate"]["value"]
            rels.append(pred)
    except:
        pass

    # Convert each inner list to a tuple and use a set to remove duplicates
    rels = list(set(rels))
    rels = nowiki(rels)

    # print(unique_list)
    return rels

def getRelationsFromEntity(entity):

    if ismid(entity):
        rels = getRelationsFromEnt(entity)
    elif isleaf(entity):
        rels = getRelationsFromLeaf(entity)
    else: rels = []

    return rels


# Input
# entity1 : written-style entity (ex. Alan_Bean)
# entity2 : written-style entity 
# Output
# triple : triple sets from entity1 and entity2 with written-style ([ ['Alan_Bean', 'nationality', 'United_States'] ])
def getTriplesFromEntities(entity1, entity2, dataset = "all"):
    triple = []

    if entity1[0] != '?' and entity1[0] != '"':
        entity1_candidates = ['<' + prefix_dict['ns'] + entity1 + '>']
    else:
        entity1_candidates = [entity1]
    if entity2[0] != '?' and entity2[0] != '"':
        entity2_candidates = ['<' + prefix_dict['ns'] + entity2 + '>']
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

def getTriplesFromLeafNode(leafNode):
    triples = []
    try:
        query = query_obj_leaf.replace("{entity_name}", leafNode)
        query = prefix + query
        results = queryResponse(query)
        for result in results["results"]["bindings"]:
            sub, pred, obj = result["subject"]["value"], result["predicate"]["value"], result["object"]["value"]
            triple_elem = [sub, pred, obj]

            temp = tripleToWord(triple_elem)
            temp[0], temp[1], temp[2] = temp[2], '~'+temp[1], temp[0]
            triple_elem = temp
            
            triples.append(triple_elem)
    except:
        pass
    
    # Convert each inner list to a tuple and use a set to remove duplicates
    unique_list = list(set(tuple(i) for i in triples))

    # Convert tuples back to lists
    unique_list = [list(i) for i in unique_list]

    # print(unique_list)
    return unique_list

# So far below function assume entity has prefix 'ns'.
def getTriplesFromEntity(entity):
    triples = []
    try:
        query = query_sub.replace("ns:{entity_name}", '<' + prefix_dict['ns'] + entity + '>')
        query = prefix + query
        results = queryResponse(query)
        for result in results["results"]["bindings"]:
            sub, pred, obj = result["subject"]["value"], result["predicate"]["value"], result["object"]["value"]
            triple_elem = [sub, pred, obj]
            triple_elem = tripleToWord(triple_elem)
            triples.append(triple_elem)
            # print(triple_elem)
        
        query = query_obj.replace("ns:{entity_name}", '<' + prefix_dict['ns'] + entity + '>')
        query = prefix + query
        results = queryResponse(query)
        for result in results["results"]["bindings"]:
            sub, pred, obj = result["subject"]["value"], result["predicate"]["value"], result["object"]["value"]
            triple_elem = [sub, pred, obj]
            temp = tripleToWord(triple_elem)
            temp[0], temp[1], temp[2] = temp[2], '~'+temp[1], temp[0]
            triple_elem = temp
            triples.append(triple_elem)
    except:
        pass
    
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
    if '~' in relation:
        relation = relation.split('~')[1]
        reverseflag = True
    
    if ismid(entity):
        ent = '<' + prefix_dict['ns'] + entity + '>'

    rel = 'ns:' + relation
    
    if not reverseflag:         
        query = prefix + query_nf.replace('?subject', ent).replace('?predicate', rel).replace('?object', '?object')
        try:
            results = queryResponse(query)
            for result in results["results"]["bindings"]:
                o = result["object"]["value"]
                o = uriToWord(o)
                o = replace_unicode_sequences(o)
                tails.append(o)
        except:
            pass
    else:
        query = prefix + query_nf.replace('?object', ent).replace('?predicate', rel).replace('?subject', '?subject')
        try:
            results = queryResponse(query)
            for result in results["results"]["bindings"]:
                s = result["subject"]["value"]
                s = uriToWord(s)
                s = replace_unicode_sequences(s)
                tails.append(s)
        except:
            pass
    return list(set(tails))


def tripleDirection(entity1, entity2, rel, dataset = "all"):
    triple = []

    if entity1[0] != '?' and entity1[0] != '"':
        entity1_candidates = ['<' + prefix_dict['ns'] + entity1 + '>']
    else:
        entity1_candidates = [entity1]
    if entity2[0] != '?' and entity2[0] != '"':
        entity2_candidates = ['<' + prefix_dict['ns'] + entity2 + '>']
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
    except:
        return None
    return None

# entity_set must be head, tail entity set
def addPrefix(entity_set):
    result = []
    prefix = ['ns']
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
    prefix = ['ns']
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
    pass