main_agent = """  
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use below helper functions to find the evidence for finding labels.

Helper Functions
1.getRelation[entity]: Returns the list of relations linked to the entity. You can choose several relations from the list that seem related to the claim.
2.exploreKG[entity]=[relation_1,relation_2, ... relation_K]: Returns the triple set around the entity. For example, [entity, relation_1, tail entity] etc. You can choose relation from [User]'s execution result.
3.Verification[True or False]: If you can judge the claim as True or False give the answer. You will be given feedback on your evaluation. Based on the feedback, decide which helper function to use in the future

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
Helper function : getRelation["\"Punjab, Pakistan\""] ## getRelation["Jinnah_International_Airport"]
[User]
Execution result : Relation_list["\"Punjab, Pakistan\""] = ['s', 'divdab', 'state', 'location', 'birthPlace', 'placeOfBirth', 'rdf-schema#label', 'deathPlace', 'placeOfDeath', 'origin', 'mapCaption', 'country'], Relation_list("Jinnah_International_Airport") = ['statYear', 'website', 'elevationF', 'stat2Data', 'r2LengthM', 'r1Number', 'stat1Data', '~targetAirport', 'icao', '~secondaryHubs', 'stat3Header', 'stat2Header', '~hubs', 'operator', 'imageWidth', 'airportManager', '~hubAirport', 'iata', 'type', 'r2Number', 'city', 'ownerOper', 'name', 'metricRwy', 'elevationM', 'hub', 'hypernym', '~headquarter', '~bases', '~origin', 'stat1Header', 'image2Width', 'runwayLength', 'icaoLocationIdentifier', 'owner', 'homepage', '22-rdf-syntax-ns#type', '~stopover', 'r1Surface', 'r1LengthM', 'subject', 'runwayDesignation', 'rdf-schema#label', '~wikiPageRedirects', 'image', 'stat3Data', '~location', 'location', '~target', '~headquarters', 'r2Surface', 'elevation', 'iataLocationIdentifier', 'runwaySurface', 'r2LengthF', 'r1LengthF', 'cityServed']
[ChatGPT]
Statement : Now, to find the airport located in Punjab, I need to explore the graph with "Punjab, Pakistan" and related relations. Also, to find the government agency of 'Jinnah_International_Airport', I need to explore the graph too.
Helper function : exploreKG["\"Punjab, Pakistan\""]=['location']) ## exploreKG["Jinnah_International_Airport"]=['operator', 'ownerOper']
[User]
Execution result : ["\"Punjab, Pakistan\"", '~location', 'Bahawalpur_Zoo'], ["\"Punjab, Pakistan\"", '~location', "Allama_Iqbal_International_Airport"], ["\"Punjab, Pakistan\"", '~location', 'Jungle_World,_Rawalpindi'], ["\"Punjab, Pakistan\"", '~location', 'Faisalabad_International_Airport'], ["\"Punjab, Pakistan\"", '~location', 'Multan_International_Airport'], ['Jinnah_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority'], ['Jinnah_International_Airport', 'ownerOper', 'Pakistan_Civil_Aviation_Authority']
[ChatGPT]
Statement : There are many airports in 'Punjab, Pakistan', and the operator of 'Jinnah_International_Airport' is 'Pakistan_Civil_Aviation_Authority'. Here, we have to find the proper relation to find the operator of the airports.
Helper function : getRelation['Allama_Iqbal_International_Airport'] ## getRelation['Faisalabad_International_Airport'] ## getRelation('Multan_International_Airport')
[User]
Execution result : Relation_list['Allama_Iqbal_International_Airport'] = ['operator', 'operatingOrganisation', 'hub'], Relation_list['Faisalabad_International_Airport'] = ['operator', 'owner'], Relation_list('Multan_International_Airport') = ['operator', 'owner']
[ChatGPT]
Statement : To find the operator of the airports, I need to explore the graph for each airport.
Helper function : exploreKG['Allama_Iqbal_International_Airport']=['operator', 'operatingOrganisation'] ## exploreKG['Faisalabad_International_Airport']=['operator'] ## exploreKG['Multan_International_Airport']=['operator']
[User]
Execution result : ['Allama_Iqbal_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority'], ['Allama_Iqbal_International_Airport', 'operatingOrganisation', 'Pakistan_Civil_Aviation_Authority'], ['Faisalabad_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority'], ['Multan_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority']
[ChatGPT]
Statement : Since all of the airports' operator is government agency 'Pakistan_Civil_Aviation_Authority' and also the operator of 'Jinnah International Airport', the claim is True.
Helper function : Verification[True]
[User]
Execution result : 

Example 2)
Claim: Tim Brooke-Taylor starred as a fictional character, which was first aired on 10/03/1983 and was broadcast by STV.
Given entity: ["\"1983-10-03\"", "\"STV\"", "Tim_Brooke-Taylor"]

[ChatGPT]
Statement : I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function : getRelation["\"1983-10-03\""] ## getRelation["\"STV\""] ## getRelation["Tim_Brooke-Taylor"]
[User]
Execution result : Relation_list["\"1983-10-03\""] = ['~deathDate', '~activeYearsStartDate', '~added', '~dateOfDeath', '~date', '~years', '~termStart', '~start', '~birthDate', '~establishedDate', '~released', '~openingDate', '~foundingDate', '~age', '~releaseDate', '~originalairdate', '~firstAired', '~dateOfBirth'], Relation_list["\"STV\""] = ['~title', '~sisterNames', '~tv', '~formerName', '~code', '~owner', '~undp', '~distributor', '~name', '~alt', '~formerNames', '~callLetters', '~iataLocationIdentifier', '~rdf-schema#label', '~agencyStationCode', '~callSign', '~broadcastedBy', '~channel', '~iata'], Relation_list('Tim_Brooke-Taylor') = ['birthName', '~voice', '~caption', '~author', 'hypernym', '22-rdf-syntax-ns#type', 'name', 'surname', 'placeOfBirth', 'description', 'genre', 'notableWork', 'dateOfBirth', 'birthDate', 'honorificSuffix', 'shortDescription', 'subject', 'title', 'nationality', '~before', '~voices', 'imdbId', 'spouse', 'rdf-schema#label', 'birthPlace', '~writer', '~after', 'years', 'givenName', 'birthYear', '~starring', '~creator', 'active']
[ChatGPT]
Statement : To verify the information in the claim, I can choose proper relation for each entity.
Helper function : exploreKG["\"1983-10-03\""]=['~firstAired'] ## exploreKG["\"STV\""]=['~broadcastedBy', '~channel']
[User]
Execution result : ["\"1983-10-03\"", '~firstAired', 'Terrahawks'], ["\"1983-10-03\"", '~firstAired', 'Scarecrow_and_Mrs._King'], ["\"1983-10-03\"", '~firstAired', 'Orm_and_Cheep'], ["\"1983-10-03\"", '~firstAired', 'Watch_Mr._Wizard'], ["\"1983-10-03\"", '~firstAired', 'Where_in_the_World_(UK_game_show)'], ["\"1983-10-03\"", '~firstAired', 'Go_(game_show)'], ['"1983-10-03"', '~firstAired', 'Bananaman'], ["\"STV\"", '~broadcastedBy', 'Bananaman'], ["\"STV\"", '~channel', 'Brain_Box']
[ChatGPT]
Statement : There is the fictional character 'Bananaman' which satisfy for first aired date and broadcast company.
Helper function : Verification[True]
[User]
Execution result : We don't have enough evidence to verify the claim. You must extract more information from the graph data.
[ChatGPT]
Statement : We need information about Tim_Brooke-Taylor to verify the claim.
Helper function : exploreKG["Tim_Brooke-Taylor"]=['~starring']
[User]
Execution result : ['Tim_Brooke-Taylor', '~starring', 'How_to_Irritate_People'], ['Tim_Brooke-Taylor', '~starring', 'Broaden_Your_Mind'], ['Tim_Brooke-Taylor', '~starring', 'ISIRTA_songs'], ['Tim_Brooke-Taylor', '~starring', 'What_the_Dickens'], ['Tim_Brooke-Taylor', '~starring', 'Bananaman']
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

sub_agent = """
You are the evaluator. I will show you a claim and a triple set extracted from a graph. 
Based on the given triple set, let me know if it is possible to determine whether the claim is True or False. 
The triple set takes the form [head, relation, tail], which means 'Head's relation is tail.' 
If the relation starts with '~', it indicates a reverse relation, meaning 'Tail's relation is head.' 
The following cases may arise: Choose one option from 'Executable' or 'Not executable(Insufficient evidence)', 'Not executable(Complex claim)'.

<Cases> 
1. If the triple set is sufficient to determine the True/False of the claim --> Executable 
2. If the triple set is insufficient to determine the True/False of the claim --> Not executable (Insufficient evidence) 
3. If the claim is too complex or ambiguous, making it difficult to determine True/False even with the triple set --> Not executable (Complex claim)


<Example 1>
[User]
Claim : A fictional character, which was created by Joe Quesada, is broadcast on Lebanese Broadcasting Corporation and starred Tim Brooke-Taylor. 
Triple sets : ['Joe_Quesaa', '~creator', 'Azrael_(comics)'], ['Joe_Quesaa', '~creator', 'Menace_(Marvel_Comics)'], ['Joe_Quesaa', '~creator', 'Thomas_Logan'], ['Joe_Quesaa', '~creator', 'Carlie_Cooper']
[ChatGPT]
Statement : It is impossible to determine the claim because information about the fictional character created by Joe Quesada being broadcast and starred cannot be found in the triple sets.
Evaluation : Not executable (Insufficient evidence)

<Example 2>
[User]
Claim : A soccer player's clubs are Esteghlal Ahvaz FC and also Al-Zawra'a SC which is managed by Basim Qasim. 
Triple sets: ["Al-Zawra'a_SC", 'manager', 'Basim_Qasim'], ['Esteghlal_Ahvaz_F.C.', 'manager', '"Siavash_Bakhtiarizadeh"'], ['Esteghlal_Ahvaz_F.C.', 'manager', 'Adnan_Hamad'], ['Basim_Qasim', 'managerclubs', 'Al_Shorta_SC'], ['Basim_Qasim', 'managerclubs', "Al-Zawra'a_SC"], ['Basim_Qasim', 'managerclubs', 'Duhok_SC'], ['Basim_Qasim', 'managerclubs', 'Zakho_FC'], ['Basim_Qasim', 'managerclubs', 'Sulaymaniya_FC'], ['Esteghlal_Ahvaz_F.C.', '~managerclubs', 'Ali_Firouzi'], ['Esteghlal_Ahvaz_F.C.', '~managerclubs', 'Gholam_Hossein_Mazloumi'], ['Esteghlal_Ahvaz_F.C.', '~managerclubs', 'Luka_Bonačić'], ['Esteghlal_Ahvaz_F.C.', '~managerclubs', 'Samad_Marfavi'], ['Esteghlal_Ahvaz_F.C.', '~managerclubs', 'Amir_Ghalenoei'], ['Esteghlal_Ahvaz_F.C.', '~managerclubs', 'Mehdi_Hasheminasab'], ['Esteghlal_Ahvaz_F.C.', '~managerclubs', 'Ali_Hanteh'], ['Esteghlal_Ahvaz_F.C.', '~managerclubs', 'Siavash_Bakhtiarizadeh'], ['Esteghlal_Ahvaz_F.C.', '~managerclubs', 'Mohammad_Ahmadzadeh'], ['Esteghlal_Ahvaz_F.C.', '~managerclubs', 'Mahmoud_Yavari'], ['Esteghlal_Ahvaz_F.C.', '~managerclubs', 'Bahram_Atef'], ['Esteghlal_Ahvaz_F.C.', '~managerclubs', 'Jalal_Cheraghpour'], ['Esteghlal_Ahvaz_F.C.', '~managerclubs', 'Akbar_Misaghian'], ['Esteghlal_Ahvaz_F.C.', '~managerclubs', 'Firouz_Karimi'], ['Esteghlal_Ahvaz_F.C.', '~managerclubs', 'Nasser_Hejazi'], ['Esteghlal_Ahvaz_F.C.', '~managerclubs', 'Majid_Jalali'], ['Esteghlal_Ahvaz_F.C.', '~managerclubs', 'Khodadad_Azizi'], ['Esteghlal_Ahvaz_F.C.', '~managerclubs', 'Davoud_Mahabadi']
[ChatGPT]
Statement : It is difficult to determine the truth of the claim because it is ambiguous whether the 'Basim Qasim' mentioned in the claim refers to him managing only Al-Zawra'a SC, or both Esteghlal Ahvaz FC and Al-Zawra'a SC.
Evaluation : Not executable (Complex claim)

<Example 3>
[User]
Claim : Tim Brooke-Taylor starred as a fictional character, which was first aired on 10/03/1983 and was broadcast by STV.
Triple sets : [""1983-10-03"", '~firstAired', 'Terrahawks'], [""1983-10-03"", '~firstAired', 'Scarecrow_and_Mrs._King'], [""1983-10-03"", '~firstAired', 'Orm_and_Cheep'], [""1983-10-03"", '~firstAired', 'Watch_Mr._Wizard'], [""1983-10-03"", '~firstAired', 'Where_in_the_World_(UK_game_show)'], [""1983-10-03"", '~firstAired', 'Go_(game_show)'], ['"1983-10-03"', '~firstAired', 'Bananaman'], [""STV"", '~broadcastedBy', 'Bananaman'], [""STV"", '~channel', 'Brain_Box'], ['Tim_Brooke-Taylor', '~starring', 'How_to_Irritate_People'], ['Tim_Brooke-Taylor', '~starring', 'Broaden_Your_Mind'], ['Tim_Brooke-Taylor', '~starring', 'ISIRTA_songs'], ['Tim_Brooke-Taylor', '~starring', 'What_the_Dickens'], ['Tim_Brooke-Taylor', '~starring', 'Bananaman']
[ChatGPT]
Statement : From the Evidence, we can know that there is the fictional character 'Bananaman' which satisfy all the information in the claim.
Evaluation : Executable



Now, it's your turn. Continue your 'Statement and Evaluation' task. Response must have same form with upper examples.
[User]
Claim : <<<<CLAIM>>>>
Triple set : <<<<Triple set>>>>

"""