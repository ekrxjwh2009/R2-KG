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
import paraphraser
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(root_dir)
load_dotenv()

# GITIGNORE WHEN MAKING REPO PUBLIC
openai.api_key = os.getenv('OPENAI_KEY')

client = OpenAI(
    api_key = os.getenv('OPENAI_KEY')
)


initial_prompt = """  
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use below helper functions to find the evidence for finding labels.

Helper Functions
1.getRelation(entity): Returns the list of relations linked to the entity. You can choose several relations from the list that seem related to the claim.
2.exploreKG(entity)=[relation_1,relation_2, ... relation_K]: Returns the triple set around the entity. For example, [entity, relation_1, tail entity] etc. You can choose relation from [User]'s execution result.
3.Verification('true' or 'false'): If you can judge the claim as True or False give the answer.

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
Statement : I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function : getRelation("\"Punjab, Pakistan\"") ## getRelation("Jinnah_International_Airport")
[User]
Execution result : Relation_list("\"Punjab, Pakistan\"") = ['s', 'divdab', 'state', 'location', 'birthPlace', 'placeOfBirth', 'rdf-schema#label', 'deathPlace', 'placeOfDeath', 'origin', 'mapCaption', 'country'], Relation_list("Jinnah_International_Airport") = ['statYear', 'website', 'elevationF', 'stat2Data', 'r2LengthM', 'r1Number', 'stat1Data', '~targetAirport', 'icao', '~secondaryHubs', 'stat3Header', 'stat2Header', '~hubs', 'operator', 'imageWidth', 'airportManager', '~hubAirport', 'iata', 'type', 'r2Number', 'city', 'ownerOper', 'name', 'metricRwy', 'elevationM', 'hub', 'hypernym', '~headquarter', '~bases', '~origin', 'stat1Header', 'image2Width', 'runwayLength', 'icaoLocationIdentifier', 'owner', 'homepage', '22-rdf-syntax-ns#type', '~stopover', 'r1Surface', 'r1LengthM', 'subject', 'runwayDesignation', 'rdf-schema#label', '~wikiPageRedirects', 'image', 'stat3Data', '~location', 'location', '~target', '~headquarters', 'r2Surface', 'elevation', 'iataLocationIdentifier', 'runwaySurface', 'r2LengthF', 'r1LengthF', 'cityServed']
[ChatGPT]
Statement : Now, to find the airport located in Punjab, I need to explore the graph with "Punjab, Pakistan" and related relations. Also, to find the government agency of 'Jinnah_International_Airport', I need to explore the graph too.
Helper function : exploreKG("\"Punjab, Pakistan\"")=['location']) ## exploreKG("Jinnah_International_Airport")=['operator', 'ownerOper']
[User]
Execution result : ["\"Punjab, Pakistan\"", '~location', 'Bahawalpur_Zoo'], ["\"Punjab, Pakistan\"", '~location', "Allama_Iqbal_International_Airport"], ["\"Punjab, Pakistan\"", '~location', 'Jungle_World,_Rawalpindi'], ["\"Punjab, Pakistan\"", '~location', 'Faisalabad_International_Airport'], ["\"Punjab, Pakistan\"", '~location', 'Multan_International_Airport'], ['Jinnah_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority'], ['Jinnah_International_Airport', 'ownerOper', 'Pakistan_Civil_Aviation_Authority']
[ChatGPT]
Statement : There are many airports in 'Punjab, Pakistan', and the operator of 'Jinnah_International_Airport' is 'Pakistan_Civil_Aviation_Authority'. Here, we have to find the proper relation to find the operator of the airports.
Helper function : getRelation('Allama_Iqbal_International_Airport') ## getRelation('Faisalabad_International_Airport') ## getRelation('Multan_International_Airport')
[User]
Execution result : Relation_list('Allama_Iqbal_International_Airport') = ['operator', 'operatingOrganisation', 'hub'], Relation_list('Faisalabad_International_Airport') = ['operator', 'owner'], Relation_list('Multan_International_Airport') = ['operator', 'owner']
[ChatGPT]
Statement : To find the operator of the airports, I need to explore the graph for each airport.
Helper function : exploreKG('Allama_Iqbal_International_Airport')=['operator', 'operatingOrganisation'] ## exploreKG('Faisalabad_International_Airport')=['operator'] ## exploreKG('Multan_International_Airport')=['operator']
[User]
Execution result : ['Allama_Iqbal_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority'], ['Allama_Iqbal_International_Airport', 'operatingOrganisation', 'Pakistan_Civil_Aviation_Authority'], ['Faisalabad_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority'], ['Multan_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority']
[ChatGPT]
Statement : Since all of the airports' operator is government agency 'Pakistan_Civil_Aviation_Authority' and also the operator of 'Jinnah International Airport', the claim is True.
Helper function : Verification('True')

Example 2)
Claim: Tim Brooke-Taylor starred as a fictional character, which was first aired on 10/03/1983 and was broadcast by STV.
Given entity: ["\"1983-10-03\"", "\"STV\"", "Tim_Brooke-Taylor"]

[ChatGPT]
Statement : I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function : getRelation("\"1983-10-03\"") ## getRelation("\"STV\"") ## getRelation("Tim_Brooke-Taylor")
[User]
Execution result : Relation_list("\"1983-10-03\"") = ['~deathDate', '~activeYearsStartDate', '~added', '~dateOfDeath', '~date', '~years', '~termStart', '~start', '~birthDate', '~establishedDate', '~released', '~openingDate', '~foundingDate', '~age', '~releaseDate', '~originalairdate', '~firstAired', '~dateOfBirth'], Relation_list("\"STV\"") = ['~title', '~sisterNames', '~tv', '~formerName', '~code', '~owner', '~undp', '~distributor', '~name', '~alt', '~formerNames', '~callLetters', '~iataLocationIdentifier', '~rdf-schema#label', '~agencyStationCode', '~callSign', '~broadcastedBy', '~channel', '~iata'], Relation_list('Tim_Brooke-Taylor') = ['birthName', '~voice', '~caption', '~author', 'hypernym', '22-rdf-syntax-ns#type', 'name', 'surname', 'placeOfBirth', 'description', 'genre', 'notableWork', 'dateOfBirth', 'birthDate', 'honorificSuffix', 'shortDescription', 'subject', 'title', 'nationality', '~before', '~voices', 'imdbId', 'spouse', 'rdf-schema#label', 'birthPlace', '~writer', '~after', 'years', 'givenName', 'birthYear', '~starring', '~creator', 'active']
[ChatGPT]
Statement : To verify the information in the claim, I can choose proper relation for each entity.
Helper function : exploreKG("\"1983-10-03\"")=['~firstAired'] ## exploreKG("\"STV\"")=['~broadcastedBy', '~channel'] ## exploreKG("Tim_Brooke-Taylor")=['~starring']
[User]
Execution result : ["\"1983-10-03\"", '~firstAired', 'Terrahawks'], ["\"1983-10-03\"", '~firstAired', 'Scarecrow_and_Mrs._King'], ["\"1983-10-03\"", '~firstAired', 'Orm_and_Cheep'], ["\"1983-10-03\"", '~firstAired', 'Watch_Mr._Wizard'], ["\"1983-10-03\"", '~firstAired', 'Where_in_the_World_(UK_game_show)'], ["\"1983-10-03\"", '~firstAired', 'Go_(game_show)'], ['"1983-10-03"', '~firstAired', 'Bananaman'], ["\"STV\"", '~broadcastedBy', 'Bananaman'], ["\"STV\"", '~channel', 'Brain_Box'], ['Tim_Brooke-Taylor', '~starring', 'How_to_Irritate_People'], ['Tim_Brooke-Taylor', '~starring', 'Broaden_Your_Mind'], ['Tim_Brooke-Taylor', '~starring', 'ISIRTA_songs'], ['Tim_Brooke-Taylor', '~starring', 'What_the_Dickens'], ['Tim_Brooke-Taylor', '~starring', 'Bananaman']
[ChatGPT]
Statement : There is the fictional character 'Bananaman' which satisfy all the information in the claim.
Helper function : Verification('True')

Example 3)
Claim: Samsung is located in São Paulo.
Given entity: ["Samsung", "São_Paulo"]

[ChatGPT]
Statement : I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function : getRelation("Samsung") ## getRelation("São_Paulo")
[User]
Execution result : Relation_list("Samsung") = ['numEmployees', 'keyPeople', 'industry', 'type', 'hypernym', 'subsidiary', 'logo', 'subject', 'foundation', 'product', '22-rdf-syntax-ns#type', 'name', 'netIncome', 'foundingDate', 'rdf-schema#label', 'revenue', 'homepage', 'subsid', 'location', 'foundingYear', 'keyPerson', 'products', 'numberOfEmployees'], Relation_list("São_Paulo") = ['imageCaption', 'coordinatesRegion', '22-rdf-syntax-ns#type', '~capital', 'areaCityKm', 'establishedTitle', '~west', 'motto', '~before', 'populationRank', 'float', 'foundingDate', '~locationTown', 'subdivisionType', '~finalAssembly', 'populationTotalRanking', 'rainfall', '~location']
[ChatGPT]
Statement : To verify the information in the claim, I have to find the location of 'Samsung' or place located in 'São_Paulo'.
Helper function : exploreKG("Samsung")=['location'] ## exploreKG("São_Paulo")=['~location']
[User]
Execution result : ['Samsung', 'location', 'Korea'], ['Samsung', 'location', 'Seoul'], ['São_Paulo', '~location', '2009_Santos_FC_season'], ['São_Paulo', '~location', 'Vanguarda_Agro']
[ChatGPT]
Statement : I need to check "São_Paulo" is located in 'Korea' or 'Seoul'. I need to explore the graph from "São_Paulo".
Helper function : getRelation("São_Paulo") 
[User]
Execution result : Relation_list("São_Paulo") = ['imageCaption', 'coordinatesRegion', '22-rdf-syntax-ns#type', '~capital', 'areaCityKm', 'establishedTitle', '~west', 'motto', '~before', 'populationRank', 'float', 'foundingDate', '~locationTown', 'subdivisionType', '~finalAssembly', 'populationTotalRanking', 'rainfall', '~location']
[ChatGPT]
Statement : To verify "São_Paulo" is located in 'Korea' or 'Seoul', I have to find the related location of "São_Paulo".
Helper function : exploreKG("São_Paulo")=['~capital', '~locationTown', '~location']
[User]
Execution result : ['São_Paulo', '~capital', 'São_Paulo_Province'], ['São_Paulo', '~locationTown', 'Ibirapuera_Auditorium], ['São_Paulo', '~location', '1972_São_Paulo_FC_season'], ['São_Paulo', '~location', '2013–14_in_Swiss_football']
[ChatGPT]
Statement : Since we cannot verify "São_Paulo" is located in 'Korea' or 'Seoul' by execution result, given claim is False.
Helper function : Verifiation('False')


Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>
"""
initial_prompt2 = """  
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use below helper functions to find the evidence for finding labels.

Helper Functions
1. getRelation[entity]: Returns the list of relations linked to the entity. You can choose several relations from the list that seem related to the claim.
2. exploreKG[entity]=[relation_1,relation_2, ... relation_K]: Returns the triple set around the entity. For example, [entity, relation_1, tail entity] etc. You can choose relation from [User]'s execution result.
3. Verification['true' or 'false']: If you can judge the claim as True or False give the answer.

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
Statement: I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function: getRelation["\"Punjab, Pakistan\""] ## getRelation["Jinnah_International_Airport"]
<Wait For User Response>

[User]
Execution result: Relation_list['"Punjab, Pakistan"'] = ['s', 'divdab', 'state', 'location', 'birthPlace', 'placeOfBirth', 'rdf-schema#label', 'deathPlace', 'placeOfDeath', 'origin', 'mapCaption', 'country'], Relation_list["Jinnah_International_Airport"] = ['statYear', 'website', 'elevationF', 'stat2Data', 'r2LengthM', 'r1Number', 'stat1Data', '~targetAirport', 'icao', '~secondaryHubs', 'stat3Header', 'stat2Header', '~hubs', 'operator', 'imageWidth', 'airportManager', '~hubAirport', 'iata', 'type', 'r2Number', 'city', 'ownerOper', 'name', 'metricRwy', 'elevationM', 'hub', 'hypernym', '~headquarter', '~bases', '~origin', 'stat1Header', 'image2Width', 'runwayLength', 'icaoLocationIdentifier', 'owner', 'homepage', '22-rdf-syntax-ns#type', '~stopover', 'r1Surface', 'r1LengthM', 'subject', 'runwayDesignation', 'rdf-schema#label', '~wikiPageRedirects', 'image', 'stat3Data', '~location', 'location', '~target', '~headquarters', 'r2Surface', 'elevation', 'iataLocationIdentifier', 'runwaySurface', 'r2LengthF', 'r1LengthF', 'cityServed']
[ChatGPT]
Statement: Now, to find the airport located in Punjab, I need to explore the graph with "Punjab, Pakistan" and related relations. Also, to find the government agency of 'Jinnah_International_Airport', I need to explore the graph too.
Helper function: exploreKG['"Punjab, Pakistan"']=['location'] ## exploreKG["Jinnah_International_Airport"]=['operator', 'ownerOper']
<Wait For User Response>

[User]
Execution result: ['"Punjab, Pakistan"', '~location', 'Bahawalpur_Zoo'], ['"Punjab, Pakistan"', '~location', "Allama_Iqbal_International_Airport"], ['"Punjab, Pakistan"', '~location', 'Jungle_World,_Rawalpindi'], ['"Punjab, Pakistan"', '~location', 'Faisalabad_International_Airport'], ['"Punjab, Pakistan"', '~location', 'Multan_International_Airport'], ['Jinnah_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority'], ['Jinnah_International_Airport', 'ownerOper', 'Pakistan_Civil_Aviation_Authority']
[ChatGPT]
Statement: There are many airports in 'Punjab, Pakistan', and the operator of 'Jinnah_International_Airport' is 'Pakistan_Civil_Aviation_Authority'. Here, we have to find the proper relation to find the operator of the airports.
Helper function: getRelation['Allama_Iqbal_International_Airport'] ## getRelation['Faisalabad_International_Airport'] ## getRelation['Multan_International_Airport']
<Wait For User Response>

[User]
Execution result: Relation_list['Allama_Iqbal_International_Airport'] = ['operator', 'operatingOrganisation', 'hub'], Relation_list['Faisalabad_International_Airport'] = ['operator', 'owner'], Relation_list['Multan_International_Airport'] = ['operator', 'owner']
[ChatGPT]
Statement: To find the operator of the airports, I need to explore the graph for each airport.
Helper function: exploreKG['Allama_Iqbal_International_Airport']=['operator', 'operatingOrganisation'] ## exploreKG['Faisalabad_International_Airport']=['operator'] ## exploreKG['Multan_International_Airport']=['operator']
<Wait For User Response>

[User]
Execution result: ['Allama_Iqbal_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority'], ['Allama_Iqbal_International_Airport', 'operatingOrganisation', 'Pakistan_Civil_Aviation_Authority'], ['Faisalabad_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority'], ['Multan_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority']
[ChatGPT]
Statement: Since all of the airports' operator is government agency 'Pakistan_Civil_Aviation_Authority' and also the operator of 'Jinnah International Airport', the claim is True.
Helper function: Verification['True']

Example 2)
Claim: Tim Brooke-Taylor starred as a fictional character, which was first aired on 10/03/1983 and was broadcast by STV.
Given entity: ["\"1983-10-03\"", "\"STV\"", "Tim_Brooke-Taylor"]

[ChatGPT]
Statement: I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function: getRelation['"1983-10-03"'] ## getRelation['"STV"'] ## getRelation["Tim_Brooke-Taylor"]
<Wait For User Response>

[User]
Execution result: Relation_list['"1983-10-03"'] = ['~deathDate', '~activeYearsStartDate', '~added', '~dateOfDeath', '~date', '~years', '~termStart', '~start', '~birthDate', '~establishedDate', '~released', '~openingDate', '~foundingDate', '~age', '~releaseDate', '~originalairdate', '~firstAired', '~dateOfBirth'], Relation_list['"STV"'] = ['~title', '~sisterNames', '~tv', '~formerName', '~code', '~owner', '~undp', '~distributor', '~name', '~alt', '~formerNames', '~callLetters', '~iataLocationIdentifier', '~rdf-schema#label', '~agencyStationCode', '~callSign', '~broadcastedBy', '~channel', '~iata'], Relation_list['Tim_Brooke-Taylor'] = ['birthName', '~voice', '~caption', '~author', 'hypernym', '22-rdf-syntax-ns#type', 'name', 'surname', 'placeOfBirth', 'description', 'genre', 'notableWork', 'dateOfBirth', 'birthDate', 'honorificSuffix', 'shortDescription', 'subject', 'title', 'nationality', '~before', '~voices', 'imdbId', 'spouse', 'rdf-schema#label', 'birthPlace', '~writer', '~after', 'years', 'givenName', 'birthYear', '~starring', '~creator', 'active']
[ChatGPT]
Statement: To verify the information in the claim, I can choose proper relation for each entity.
Helper function: exploreKG['"1983-10-03"']=['~firstAired'] ## exploreKG['"STV"']=['~broadcastedBy', '~channel'] ## exploreKG["Tim_Brooke-Taylor"]=['~starring']
<Wait For User Response>

[User]
Execution result: ['"1983-10-03"', '~firstAired', 'Terrahawks'], ['"1983-10-03"', '~firstAired', 'Scarecrow_and_Mrs._King'], ['"1983-10-03"', '~firstAired', 'Orm_and_Cheep'], ['"1983-10-03"', '~firstAired', 'Watch_Mr._Wizard'], ['"1983-10-03"', '~firstAired', 'Where_in_the_World_(UK_game_show)'], ['"1983-10-03"', '~firstAired', 'Go_(game_show)'], ['"1983-10-03"', '~firstAired', 'Bananaman'], ['"STV"', '~broadcastedBy', 'Bananaman'], ['"STV"', '~channel', 'Brain_Box'], ['Tim_Brooke-Taylor', '~starring', 'How_to_Irritate_People'], ['Tim_Brooke-Taylor', '~starring', 'Broaden_Your_Mind'], ['Tim_Brooke-Taylor', '~starring', 'ISIRTA_songs'], ['Tim_Brooke-Taylor', '~starring', 'What_the_Dickens'], ['Tim_Brooke-Taylor', '~starring', 'Bananaman']
[ChatGPT]
Statement: There is the fictional character 'Bananaman' which satisfy all the information in the claim.
Helper function: Verification['True']

Example 3)
Claim: Samsung is located in São Paulo.
Given entity: ["Samsung", "São_Paulo"]

[ChatGPT]
Statement: I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function: getRelation["Samsung"] ## getRelation["São_Paulo"]
<Wait For User Response>

[User]
Execution result: Relation_list["Samsung"] = ['numEmployees', 'keyPeople', 'industry', 'type', 'hypernym', 'subsidiary', 'logo', 'subject', 'foundation', 'product', '22-rdf-syntax-ns#type', 'name', 'netIncome', 'foundingDate', 'rdf-schema#label', 'revenue', 'homepage', 'subsid', 'location', 'foundingYear', 'keyPerson', 'products', 'numberOfEmployees'], Relation_list["São_Paulo"] = ['imageCaption', 'coordinatesRegion', '22-rdf-syntax-ns#type', '~capital', 'areaCityKm', 'establishedTitle', '~west', 'motto', '~before', 'populationRank', 'float', 'foundingDate', '~locationTown', 'subdivisionType', '~finalAssembly', 'populationTotalRanking', 'rainfall', '~location']
[ChatGPT]
Statement: To verify the information in the claim, I have to find the location of 'Samsung' or place located in 'São_Paulo'.
Helper function: exploreKG["Samsung"]=['location'] ## exploreKG["São_Paulo"]=['~location']
<Wait For User Response>

[User]
Execution result: ['Samsung', 'location', 'Korea'], ['Samsung', 'location', 'Seoul'], ['São_Paulo', '~location', '2009_Santos_FC_season'], ['São_Paulo', '~location', 'Vanguarda_Agro']
[ChatGPT]
Statement: I need to check "São_Paulo" is located in 'Korea' or 'Seoul'. I need to explore the graph from "São_Paulo".
Helper function: getRelation["São_Paulo"] 
<Wait For User Response>

[User]
Execution result: Relation_list["São_Paulo"] = ['imageCaption', 'coordinatesRegion', '22-rdf-syntax-ns#type', '~capital', 'areaCityKm', 'establishedTitle', '~west', 'motto', '~before', 'populationRank', 'float', 'foundingDate', '~locationTown', 'subdivisionType', '~finalAssembly', 'populationTotalRanking', 'rainfall', '~location']
[ChatGPT]
Statement: To verify "São_Paulo" is located in 'Korea' or 'Seoul', I have to find the related location of "São_Paulo".
Helper function: exploreKG["São_Paulo"]=['~capital', '~locationTown', '~location']
<Wait For User Response>

[User]
Execution result: ['São_Paulo', '~capital', 'São_Paulo_Province'], ['São_Paulo', '~locationTown', 'Ibirapuera_Auditorium], ['São_Paulo', '~location', '1972_São_Paulo_FC_season'], ['São_Paulo', '~location', '2013–14_in_Swiss_football']
[ChatGPT]
Statement: Since we cannot verify "São_Paulo" is located in 'Korea' or 'Seoul' by execution result, given claim is False.
Helper function: Verifiation['False']


Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>
"""

main_agent = """  
Your task is to extract proper evidences from knowledge graph to verify the claim.
You can use below helper functions to find the evidence for finding labels.

Helper Functions
1.getRelation[entity]: Returns the list of relations linked to the entity. You can choose several relations from the list that seem related to the claim.
2.exploreKG[entity]=[relation_1,relation_2, ... relation_K]: Returns the triple set around the entity. For example, [entity, relation_1, tail entity] etc. You can choose relation from [User]'s execution result.
3.Verification[]: Call you think you collected enough evidence to judge the claim as True or False. 
Based on the evidence gathered so far, [User] will determine whether it is True or False. If [User] think the evidence is insufficient, [User] will ask you to collect more evidence. If [User] say the evidence is insufficient, continue the evidence collection process using a different helper function.

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
Statement: I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function: getRelation["\"Punjab, Pakistan\""] ## getRelation["Jinnah_International_Airport"]
[User]
Execution result: Relation_list["\"Punjab, Pakistan\""] = ['s', 'divdab', 'state', 'location', 'birthPlace', 'placeOfBirth', 'rdf-schema#label', 'deathPlace', 'placeOfDeath', 'origin', 'mapCaption', 'country'], Relation_list("Jinnah_International_Airport") = ['statYear', 'website', 'elevationF', 'stat2Data', 'r2LengthM', 'r1Number', 'stat1Data', '~targetAirport', 'icao', '~secondaryHubs', 'stat3Header', 'stat2Header', '~hubs', 'operator', 'imageWidth', 'airportManager', '~hubAirport', 'iata', 'type', 'r2Number', 'city', 'ownerOper', 'name', 'metricRwy', 'elevationM', 'hub', 'hypernym', '~headquarter', '~bases', '~origin', 'stat1Header', 'image2Width', 'runwayLength', 'icaoLocationIdentifier', 'owner', 'homepage', '22-rdf-syntax-ns#type', '~stopover', 'r1Surface', 'r1LengthM', 'subject', 'runwayDesignation', 'rdf-schema#label', '~wikiPageRedirects', 'image', 'stat3Data', '~location', 'location', '~target', '~headquarters', 'r2Surface', 'elevation', 'iataLocationIdentifier', 'runwaySurface', 'r2LengthF', 'r1LengthF', 'cityServed']
[ChatGPT]
Statement: Now, to find the airport located in Punjab, I need to explore the graph with "Punjab, Pakistan" and related relations. Also, to find the government agency of 'Jinnah_International_Airport', I need to explore the graph too.
Helper function: exploreKG["\"Punjab, Pakistan\""]=['location']) ## exploreKG["Jinnah_International_Airport"]=['operator', 'ownerOper']
[User]
Execution result: ["\"Punjab, Pakistan\"", '~location', 'Bahawalpur_Zoo'], ["\"Punjab, Pakistan\"", '~location', "Allama_Iqbal_International_Airport"], ["\"Punjab, Pakistan\"", '~location', 'Jungle_World,_Rawalpindi'], ["\"Punjab, Pakistan\"", '~location', 'Faisalabad_International_Airport'], ["\"Punjab, Pakistan\"", '~location', 'Multan_International_Airport'], ['Jinnah_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority'], ['Jinnah_International_Airport', 'ownerOper', 'Pakistan_Civil_Aviation_Authority']
[ChatGPT]
Statement: There are many airports in 'Punjab, Pakistan', and the operator of 'Jinnah_International_Airport' is 'Pakistan_Civil_Aviation_Authority'. Here, we have to find the proper relation to find the operator of the airports.
Helper function: getRelation['Allama_Iqbal_International_Airport'] ## getRelation['Faisalabad_International_Airport'] ## getRelation('Multan_International_Airport')
[User]
Execution result: Relation_list['Allama_Iqbal_International_Airport'] = ['operator', 'operatingOrganisation', 'hub'], Relation_list['Faisalabad_International_Airport'] = ['operator', 'owner'], Relation_list('Multan_International_Airport') = ['operator', 'owner']
[ChatGPT]
Statement: To find the operator of the airports, I need to explore the graph for each airport.
Helper function: exploreKG['Allama_Iqbal_International_Airport']=['operator', 'operatingOrganisation'] ## exploreKG['Faisalabad_International_Airport']=['operator'] ## exploreKG['Multan_International_Airport']=['operator']
[User]
Execution result: ['Allama_Iqbal_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority'], ['Allama_Iqbal_International_Airport', 'operatingOrganisation', 'Pakistan_Civil_Aviation_Authority'], ['Faisalabad_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority'], ['Multan_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority']
[ChatGPT]
Statement: Since all of the airports' operator is government agency 'Pakistan_Civil_Aviation_Authority' and also the operator of 'Jinnah International Airport', the claim is True.
Helper function: Verification['True']
[User]
Execution result: True

Example 2)
Claim: Tim Brooke-Taylor starred as a fictional character, which was first aired on 10/03/1983 and was broadcast by STV.
Given entity: ["\"1983-10-03\"", "\"STV\"", "Tim_Brooke-Taylor"]

[ChatGPT]
Statement: I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function: getRelation['"1983-10-03"'] ## getRelation['"STV"'] ## getRelation["Tim_Brooke-Taylor"]
[User]
Execution result: Relation_list['"1983-10-03"'] = ['~deathDate', '~activeYearsStartDate', '~added', '~dateOfDeath', '~date', '~years', '~termStart', '~start', '~birthDate', '~establishedDate', '~released', '~openingDate', '~foundingDate', '~age', '~releaseDate', '~originalairdate', '~firstAired', '~dateOfBirth'], Relation_list['"STV"'] = ['~title', '~sisterNames', '~tv', '~formerName', '~code', '~owner', '~undp', '~distributor', '~name', '~alt', '~formerNames', '~callLetters', '~iataLocationIdentifier', '~rdf-schema#label', '~agencyStationCode', '~callSign', '~broadcastedBy', '~channel', '~iata'], Relation_list('Tim_Brooke-Taylor') = ['birthName', '~voice', '~caption', '~author', 'hypernym', '22-rdf-syntax-ns#type', 'name', 'surname', 'placeOfBirth', 'description', 'genre', 'notableWork', 'dateOfBirth', 'birthDate', 'honorificSuffix', 'shortDescription', 'subject', 'title', 'nationality', '~before', '~voices', 'imdbId', 'spouse', 'rdf-schema#label', 'birthPlace', '~writer', '~after', 'years', 'givenName', 'birthYear', '~starring', '~creator', 'active']
[ChatGPT]
Statement: To verify the information in the claim, I can choose proper relation for each entity.
Helper function: exploreKG['"1983-10-03"']=['~firstAired'] ## exploreKG['"STV"']=['~broadcastedBy', '~channel']
[User]
Execution result: ['"1983-10-03"', '~firstAired', 'Terrahawks'], ['"1983-10-03"', '~firstAired', 'Scarecrow_and_Mrs._King'], ['"1983-10-03"', '~firstAired', 'Orm_and_Cheep'], ['"1983-10-03"', '~firstAired', 'Watch_Mr._Wizard'], ['"1983-10-03"', '~firstAired', 'Where_in_the_World_(UK_game_show)'], ['"1983-10-03"', '~firstAired', 'Go_(game_show)'], ['"1983-10-03"', '~firstAired', 'Bananaman'], ['"STV"', '~broadcastedBy', 'Bananaman'], ['"STV"', '~channel', 'Brain_Box']
[ChatGPT]
Statement: There is the fictional character 'Bananaman' which satisfy for first aired date and broadcast company.
Helper function: Verification['True']
[User]
Execution result: We don't have enough evidence to verify the claim. You must extract more information from the graph data.
[ChatGPT]
Statement: Alright. We need information about Tim_Brooke-Taylor to verify the claim.
Helper function: exploreKG["Tim_Brooke-Taylor"]=['~starring']
[User]
Execution result: ['Tim_Brooke-Taylor', '~starring', 'How_to_Irritate_People'], ['Tim_Brooke-Taylor', '~starring', 'Broaden_Your_Mind'], ['Tim_Brooke-Taylor', '~starring', 'ISIRTA_songs'], ['Tim_Brooke-Taylor', '~starring', 'What_the_Dickens'], ['Tim_Brooke-Taylor', '~starring', 'Bananaman']
[ChatGPT]
Statement: There is the fictional character 'Bananaman' which satisfy all the information in the claim.
Helper function: Verification['True']
[User]
Execution result: True

Example 3)
Claim: Samsung is located in São Paulo.
Given entity: ["Samsung", "São_Paulo"]

[ChatGPT]
Statement: I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function: getRelation["Samsung"] ## getRelation["São_Paulo"]
[User]
Execution result: Relation_list["Samsung"] = ['numEmployees', 'keyPeople', 'industry', 'type', 'hypernym', 'subsidiary', 'logo', 'subject', 'foundation', 'product', '22-rdf-syntax-ns#type', 'name', 'netIncome', 'foundingDate', 'rdf-schema#label', 'revenue', 'homepage', 'subsid', 'location', 'foundingYear', 'keyPerson', 'products', 'numberOfEmployees'], Relation_list["São_Paulo"] = ['imageCaption', 'coordinatesRegion', '22-rdf-syntax-ns#type', '~capital', 'areaCityKm', 'establishedTitle', '~west', 'motto', '~before', 'populationRank', 'float', 'foundingDate', '~locationTown', 'subdivisionType', '~finalAssembly', 'populationTotalRanking', 'rainfall', '~location']
[ChatGPT]
Statement: To verify the information in the claim, I have to find the location of 'Samsung' or place located in 'São_Paulo'.
Helper function: exploreKG["Samsung"]=['location'] ## exploreKG["São_Paulo"]=['~location']
[User]
Execution result: ['Samsung', 'location', 'Korea'], ['Samsung', 'location', 'Seoul'], ['São_Paulo', '~location', '2009_Santos_FC_season'], ['São_Paulo', '~location', 'Vanguarda_Agro']
[ChatGPT]
Statement: I need to check "São_Paulo" is located in 'Korea' or 'Seoul'. I need to explore the graph from "São_Paulo".
Helper function: getRelation["São_Paulo"] 
[User]
Execution result: Relation_list["São_Paulo"] = ['imageCaption', 'coordinatesRegion', '22-rdf-syntax-ns#type', '~capital', 'areaCityKm', 'establishedTitle', '~west', 'motto', '~before', 'populationRank', 'float', 'foundingDate', '~locationTown', 'subdivisionType', '~finalAssembly', 'populationTotalRanking', 'rainfall', '~location']
[ChatGPT]
Statement: To verify "São_Paulo" is located in 'Korea' or 'Seoul', I have to find the related location of "São_Paulo".
Helper function: exploreKG["São_Paulo"]=['~capital', '~locationTown', '~location']
[User]
Execution result: ['São_Paulo', '~capital', 'São_Paulo_Province'], ['São_Paulo', '~locationTown', 'Ibirapuera_Auditorium], ['São_Paulo', '~location', '1972_São_Paulo_FC_season'], ['São_Paulo', '~location', '2013–14_in_Swiss_football']
[ChatGPT]
Statement: Since we cannot verify "São_Paulo" is located in 'Korea' or 'Seoul' by execution result, given claim is False.
Helper function: Verifiation['False']
[User]
Execution result: False


Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>
"""


class OpenAIBot:
    def __init__(self, engine, client):
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
            response = self.client.chat.completions.create( model=self.engine, messages=self.conversation, temperature= 0, top_p = 0.1)
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
            
def reasoning(claim, initial_prompt, label, max_iter, model, f):
            
    # engine= "gpt-3.5-turbo"
    # engine = "gpt-4o-mini"
    engine = model
    chatbot = OpenAIBot(engine, client)
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
            if info.state == -1:
                f.write(f"\nDuplicated Entity-Relation pair!")
                break
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
                result = helper_str.split("Verification[")[1].split("]")[0][1:-1]
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
        functions = response.split("Helper function: ")[1].split("\n<Wait For User Response>")[0]
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


def score(predict, label,f):
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
    parser.add_argument("--num_iter", type = int, default = "10")
    parser.add_argument("--model", type = str, default= "gpt-3.5-turbo")
    args = parser.parse_args()
    
    save_path = f"../result/paraphrase_ensemble_20241023"
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    
    result = {}
    questions_dict = {}
    entity_set_dict = {}
    label_set_dict = {}
    types_dict ={}
    
    with open("../data/extracted_dev_set.jsonl") as f:
        for line in f:
            if not line:
                continue
            q = json.loads(line)

            questions_dict[q["question_id"]] = q["question"]
            entity_set_dict[q["question_id"]] = q["entity_set"]
            label_set_dict[q["question_id"]] = q["Label"]
            types_dict[q['question_id']] = q["types"] 
            


    # total_correct, total_abs, total_wrong = 0, 0, 0
    total_correct = [0, 0, 0]
    total_abs = [0, 0, 0]
    total_wrong = [0, 0, 0]
    
    if args.type == 'existence': qid_list = fair_qid.existence
    elif args.type == "num1" : qid_list = fair_qid.num1
    elif args.type == 'multi_claim' : qid_list = fair_qid.multi_claim
    elif args.type == "multi_hop" : qid_list = fair_qid.multi_hop
    else:
        print("Wrong argument")

    
    # iter_num_list = []
    answer_list = {0: [['qid','prediction','gt_label']], 1: [['qid','prediction','gt_label']], 2: [['qid','prediction','gt_label']]}

    for qid in qid_list:
        # with open(os.path.join(save_path, f"result_{args.type}_4omini.txt"),'a') as f:
        print(f"Qid:{qid}")
        question = questions_dict[qid]
        label = label_set_dict[qid]
        entities = entity_set_dict[qid]

        paraphrase_claims = paraphraser.paraphrase(question)
        
        for p in range(len(paraphrase_claims)):
            q = paraphrase_claims[p]
            with open(os.path.join(save_path, f"result_{args.type}_{args.model}_maxiter_{args.num_iter}_paraphrase_{p}.txt"), 'a') as f:
                f.write(f"\n\n\nQid:{qid}\nQuestion :{q}\n")
                f.write(f"GT entity:{entities}")
                prompt = initial_prompt2.replace('<<<<CLAIM>>>>', q).replace('<<<<GT_ENTITY>>>', str(entities))

                prediction, iter_num = reasoning(q, prompt, label, args.num_iter, args.model, f)
                abs, correct, wrong= score(str(prediction), str(label[0]),f)
                total_correct[p] += correct
                total_wrong[p] += wrong
                total_abs[p] += abs
                # iter_num_list.append(iter_num)
                answer_list[p].append([qid, str(prediction), str(label[0])])

                f.close()

    
    # if (len(qid_list) - total_abs) == 0 :
    #     metric1 = 0
    # else:
    #     metric1 = (len(qid_list) - total_abs) / len(qid_list)
    # if total_correct == 0:
    #     metric2 = 0
    # else :
    #     metric2 = total_correct / (len(qid_list) - total_abs)
        
    # if (total_correct - total_wrong) == 0 :
    #     metric3 = 0
    # else:
    #     metric3 = (total_correct-total_wrong) / (len(qid_list) - total_abs)
            
    for i in range(3):
        with open(os.path.join(save_path, f"result_{args.type}_{args.model}_maxiter_{args.num_iter}_paraphrase_{i}.txt"),'a') as f:
        # with open(os.path.join(save_path, f"result_{args.type}_4omini.txt"),'a') as f:
            f.write(f"\n\n\nTotal sample:{len(qid_list)}, Total_Correct:{total_correct[i]}, Total_Wrong:{total_wrong[i]}, Total_abstain:{total_abs[i]}\n")
            # f.write(f"metric1:{metric1}\n mertric2:{metric2}\n metric3:{metric3}")
            # f.write(f"avg iter:{np.average(iter_num_list)}\n max_iter:{np.max(iter_num_list)}\n min_iter:{np.min(iter_num_list)}")
        
        f= open(f"../result/paraphrase_ensemble_20241023/only_answer_{args.type}_{args.model}_maxiter_{args.num_iter}_paraphrase_{i}.csv",'w')
        # f= open(f"./with_reasoning_result/only_answer_{args.type}_4omini.csv",'w')

        writer= csv.writer(f)
        writer.writerows(answer_list[i])
        f.close()