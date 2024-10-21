prompt = """
Your task is to determine the given claim is whether true or false based on the graph data without your base knowledge.
You can use below helper functions to find the evidence in knowledge graph data to find answer.

<Helper functions>
1. getRelation(entity): Returns the list of relations connected to the entity.
2. exploreKG(entity: [relations]): Returns the corresponding tail entities in graph data starts from single entity and given relations.
3. Verification(True/False): Once verification is done, call this function with labels.

You must follow the exact format of the given helper functions.

Now, I will give you a claim and Given Entity that you can refer to.
Your task is to use proper helper functions to explore and obtain proper triple information from the knowledge graph dataset.
Stop for my response after calling the helper function and continue your Statement task after getting a response from [User].
Importantly, the relation with the '~' symbol indicates the reverse direction of the relation.

Here are some examples.

Example 1)
Claim: The airport in Punjab, Pakistan is operated by the government agency of the Jinnah International Airport.
Given entity: ["Punjab, Pakistan", "Jinnah_International_Airport"]

[ChatGPT]
Statement: I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function: getRelation("Punjab, Pakistan"), getRelation("Jinnah_International_Airport")
[User]
Execution result: Relation_list("Punjab, Pakistan") = ['s', 'divdab', 'state', 'location', 'birthPlace', 'placeOfBirth', 'rdf-schema#label', 'deathPlace', 'placeOfDeath', 'origin', 'mapCaption', 'country'], Relation_list("Jinnah_International_Airport") = ['statYear', 'website', 'elevationF', 'stat2Data', 'r2LengthM', 'r1Number', 'stat1Data', '~targetAirport', 'icao', '~secondaryHubs', 'stat3Header', 'stat2Header', '~hubs', 'operator', 'imageWidth', 'airportManager', '~hubAirport', 'iata', 'type', 'r2Number', 'city', 'ownerOper', 'name', 'metricRwy', 'elevationM', 'hub', 'hypernym', '~headquarter', '~bases', '~origin', 'stat1Header', 'image2Width', 'runwayLength', 'icaoLocationIdentifier', 'owner', 'homepage', '22-rdf-syntax-ns#type', '~stopover', 'r1Surface', 'r1LengthM', 'subject', 'runwayDesignation', 'rdf-schema#label', '~wikiPageRedirects', 'image', 'stat3Data', '~location', 'location', '~target', '~headquarters', 'r2Surface', 'elevation', 'iataLocationIdentifier', 'runwaySurface', 'r2LengthF', 'r1LengthF', 'cityServed']
[ChatGPT]
Statement: Now, to find the airport located in Punjab, I need to explore the graph with "Punjab, Pakistan" and related relations. Also, to find the government agency of 'Jinnah_International_Airport', I need to explore the graph too.
Helper function: exploreKG('Punjab, Pakistan': ['location']), exploreKG("Jinnah_International_Airport": ['operator', 'ownerOper'])
[User]
Execution result: ['Punjab, Pakistan', '~location', 'Bahawalpur_Zoo'], ['Punjab, Pakistan', '~location', 'Allama_Iqbal_International_Airport'], ['Punjab, Pakistan', '~location', 'Jungle_World,_Rawalpindi'], ['Punjab, Pakistan', '~location', 'Faisalabad_International_Airport'], ['Punjab, Pakistan', '~location', 'Multan_International_Airport'], ['Jinnah_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority'], ['Jinnah_International_Airport', 'ownerOper', 'Pakistan_Civil_Aviation_Authority']
[ChatGPT]
Statement: There are many airports in 'Punjab, Pakistan', and the operator of 'Jinnah_International_Airport' is 'Pakistan_Civil_Aviation_Authority'. Here, we have to find the proper relation to find the operator of the airports.
Helper function: getRelation('Allama_Iqbal_International_Airport'), getRelation('Faisalabad_International_Airport'), getRelation('Multan_International_Airport')
[User]
Execution result: Relation_list('Allama_Iqbal_International_Airport') = ['operator', 'operatingOrganisation', 'hub'], Relation_list('Faisalabad_International_Airport') = ['operator', 'owner'], Relation_list('Multan_International_Airport') = ['operator', 'owner']
[ChatGPT]
Statement: To find the operator of the airports, I need to explore the graph for each airport.
Helper function: exploreKG('Allama_Iqbal_International_Airport': ['operator', 'operatingOrganisation']), exploreKG('Faisalabad_International_Airport': ['operator']), exploreKG('Multan_International_Airport': ['operator'])
[User]
Execution result: ['Allama_Iqbal_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority'], ['Allama_Iqbal_International_Airport', 'operatingOrganisation', 'Pakistan_Civil_Aviation_Authority'], ['Faisalabad_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority'], ['Multan_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority']
[ChatGPT]
Statement: Since all of the airports' operator is government agency 'Pakistan_Civil_Aviation_Authority' and also the operator of 'Jinnah International Airport', the claim is True.
Helper function: Verification('True')

Example 2)
Claim: Tim Brooke-Taylor starred as a fictional character, which was first aired on 10/03/1983 and was broadcast by STV.
Given entity: ["1983-10-03", "STV", "Tim_Brooke-Taylor"]

[ChatGPT]
Statement: I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function: getRelation("1983-10-03"), getRelation("STV"), getRelation("Tim_Brooke-Taylor")
[User]
Execution result: Relation_list("1983-10-03") = ['~deathDate', '~activeYearsStartDate', '~added', '~dateOfDeath', '~date', '~years', '~termStart', '~start', '~birthDate', '~establishedDate', '~released', '~openingDate', '~foundingDate', '~age', '~releaseDate', '~originalairdate', '~firstAired', '~dateOfBirth'], Relation_list("STV") = ['~title', '~sisterNames', '~tv', '~formerName', '~code', '~owner', '~undp', '~distributor', '~name', '~alt', '~formerNames', '~callLetters', '~iataLocationIdentifier', '~rdf-schema#label', '~agencyStationCode', '~callSign', '~broadcastedBy', '~channel', '~iata'], Relation_list('Tim_Brooke-Taylor') = ['birthName', '~voice', '~caption', '~author', 'hypernym', '22-rdf-syntax-ns#type', 'name', 'surname', 'placeOfBirth', 'description', 'genre', 'notableWork', 'dateOfBirth', 'birthDate', 'honorificSuffix', 'shortDescription', 'subject', 'title', 'nationality', '~before', '~voices', 'imdbId', 'spouse', 'rdf-schema#label', 'birthPlace', '~writer', '~after', 'years', 'givenName', 'birthYear', '~starring', '~creator', 'active']
[ChatGPT]
Statement: To verify the information in the claim, I can choose proper relation for each entity.
Helper function: exploreKG("1983-10-03": ['~firstAired']), exploreKG("STV": ['~broadcastedBy', '~channel']), exploreKG("Tim_Brooke-Taylor": ['~starring'])
[User]
Execution result: ['"1983-10-03"', '~firstAired', 'Terrahawks'], ['"1983-10-03"', '~firstAired', 'Scarecrow_and_Mrs._King'], ['"1983-10-03"', '~firstAired', 'Orm_and_Cheep'], ['"1983-10-03"', '~firstAired', 'Watch_Mr._Wizard'], ['"1983-10-03"', '~firstAired', 'Where_in_the_World_(UK_game_show)'], ['"1983-10-03"', '~firstAired', 'Go_(game_show)'], ['"1983-10-03"', '~firstAired', 'Bananaman'], ['"STV"', '~broadcastedBy', 'Bananaman'], ['"STV"', '~channel', 'Brain_Box'], ['Tim_Brooke-Taylor', '~starring', 'How_to_Irritate_People'], ['Tim_Brooke-Taylor', '~starring', 'Broaden_Your_Mind'], ['Tim_Brooke-Taylor', '~starring', 'ISIRTA_songs'], ['Tim_Brooke-Taylor', '~starring', 'What_the_Dickens'], ['Tim_Brooke-Taylor', '~starring', 'Bananaman']
[ChatGPT]
Statement: There is the fictional character 'Bananaman' which satisfy all the information in the claim.
Helper function: Verification('True')

Example 3)
Claim: Samsung is located in São Paulo.
Given entity: ["Samsung", "São_Paulo"]

[ChatGPT]
Statement: I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function: getRelation("Samsung"), getRelation("São_Paulo")
[User]
Execution result: Relation_list("Samsung") = ['numEmployees', 'keyPeople', 'industry', 'type', 'hypernym', 'subsidiary', 'logo', 'subject', 'foundation', 'product', '22-rdf-syntax-ns#type', 'name', 'netIncome', 'foundingDate', 'rdf-schema#label', 'revenue', 'homepage', 'subsid', 'location', 'foundingYear', 'keyPerson', 'products', 'numberOfEmployees'], Relation_list("São_Paulo") = ['imageCaption', 'coordinatesRegion', '22-rdf-syntax-ns#type', '~capital', 'areaCityKm', 'establishedTitle', '~west', 'motto', '~before', 'populationRank', 'float', 'foundingDate', '~locationTown', 'subdivisionType', '~finalAssembly', 'populationTotalRanking', 'rainfall', '~location']
[ChatGPT]
Statement: To verify the information in the claim, I have to find the location of 'Samsung' or place located in 'São_Paulo'.
Helper function: exploreKG("Samsung": ['location']), exploreKG("São_Paulo": ['~location'])
[User]
Execution result: ['Samsung', 'location', 'Korea'], ['Samsung', 'location', 'Seoul'], ['São_Paulo', '~location', '2009_Santos_FC_season'], ['São_Paulo', '~location', 'Vanguarda_Agro']
[ChatGPT]
Statement: I need to check "São_Paulo" is located in 'Korea' or 'Seoul'. I need to explore the graph from "São_Paulo".
Helper function: getRelation("São_Paulo") 
[User]
Execution result: Relation_list("São_Paulo") = ['imageCaption', 'coordinatesRegion', '22-rdf-syntax-ns#type', '~capital', 'areaCityKm', 'establishedTitle', '~west', 'motto', '~before', 'populationRank', 'float', 'foundingDate', '~locationTown', 'subdivisionType', '~finalAssembly', 'populationTotalRanking', 'rainfall', '~location']
[ChatGPT]
Statement: To verify "São_Paulo" is located in 'Korea' or 'Seoul', I have to find the related location of "São_Paulo".
Helper function: exploreKG("São_Paulo": ['~capital', '~locationTown', '~location'])
[User]
Execution result: ['São_Paulo', '~capital', 'São_Paulo_Province'], ['São_Paulo', '~locationTown', 'Ibirapuera_Auditorium], ['São_Paulo', '~location', '1972_São_Paulo_FC_season'], ['São_Paulo', '~location', '2013–14_in_Swiss_football']
[ChatGPT]
Statement: Since we cannot verify "São_Paulo" is located in 'Korea' or 'Seoul' by execution result, given claim is False.
Helper function: Verifiation('False')


Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>
"""

prompt_abstain = """
Your task is to determine the given claim is whether true or false based on the graph data without your base knowledge.
You can use below helper functions to find the evidence in graph data to find answer.

<Helper functions>
1. getRelation(entity): Returns the list of relations connected to the entity.
2. exploreKG(entity: [relations]): Returns the corresponding tail entities in graph data starts from single entity and given relations.
3. Abstain(): Abstain the claim if same helper function call is repeated in process. Otherwise don't use this helper function.
4. Verification(True/False): Once verification is done, call this function with labels.

You must follow the exact format of the given helper function.

Now, I will give you a claim and Given Entity that you can refer to.
Your task is to use proper helper functions to explore and obtain proper triple information from the knowledge graph datset.
Stop for my response after calling helper function and continue your Statement task after getting response from [User].
Importantly, relation with '~' symbol indicates the reverse direction of the relation.

Here are some examples.

Example 1)
Claim: The airport in Punjab, Pakistan is operated by the government agency of the Jinnah International Airport.
Given entity: ["Punjab, Pakistan", "Jinnah_International_Airport"]

[ChatGPT]
Statement: I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function: getRelation("Punjab, Pakistan"), getRelation("Jinnah_International_Airport")
[User]
Execution result: Relation_list("Punjab, Pakistan") = ['s', 'divdab', 'state', 'location', 'birthPlace', 'placeOfBirth', 'rdf-schema#label', 'deathPlace', 'placeOfDeath', 'origin', 'mapCaption', 'country'], Relation_list("Jinnah_International_Airport") = ['statYear', 'website', 'elevationF', 'stat2Data', 'r2LengthM', 'r1Number', 'stat1Data', '~targetAirport', 'icao', '~secondaryHubs', 'stat3Header', 'stat2Header', '~hubs', 'operator', 'imageWidth', 'airportManager', '~hubAirport', 'iata', 'type', 'r2Number', 'city', 'ownerOper', 'name', 'metricRwy', 'elevationM', 'hub', 'hypernym', '~headquarter', '~bases', '~origin', 'stat1Header', 'image2Width', 'runwayLength', 'icaoLocationIdentifier', 'owner', 'homepage', '22-rdf-syntax-ns#type', '~stopover', 'r1Surface', 'r1LengthM', 'subject', 'runwayDesignation', 'rdf-schema#label', '~wikiPageRedirects', 'image', 'stat3Data', '~location', 'location', '~target', '~headquarters', 'r2Surface', 'elevation', 'iataLocationIdentifier', 'runwaySurface', 'r2LengthF', 'r1LengthF', 'cityServed']
[ChatGPT]
Statement: Now, to find the airport located in Punjab, I need to explore the graph with "Punjab, Pakistan" and related relations. Also, to find the government agency of 'Jinnah_International_Airport', I need to explore the graph too.
Helper function: exploreKG('Punjab, Pakistan': ['location']), exploreKG("Jinnah_International_Airport": ['operator', 'ownerOper'])
[User]
Execution result: ['Punjab, Pakistan', '~location', 'Bahawalpur_Zoo'], ['Punjab, Pakistan', '~location', 'Allama_Iqbal_International_Airport'], ['Punjab, Pakistan', '~location', 'Jungle_World,_Rawalpindi'], ['Punjab, Pakistan', '~location', 'Faisalabad_International_Airport'], ['Punjab, Pakistan', '~location', 'Multan_International_Airport'], ['Jinnah_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority'], ['Jinnah_International_Airport', 'ownerOper', 'Pakistan_Civil_Aviation_Authority']
[ChatGPT]
Statement: There are many airports in 'Punjab, Pakistan', and the operator of 'Jinnah_International_Airport' is 'Pakistan_Civil_Aviation_Authority'. Here, we have to find the proper relation to find the operator of the airports.
Helper function: getRelation('Allama_Iqbal_International_Airport'), getRelation('Faisalabad_International_Airport'), getRelation('Multan_International_Airport')
[User]
Execution result: Relation_list('Allama_Iqbal_International_Airport') = ['operator', 'operatingOrganisation', 'hub'], Relation_list('Faisalabad_International_Airport') = ['operator', 'owner'], Relation_list('Multan_International_Airport') = ['operator', 'owner']
[ChatGPT]
Statement: To find the operator of the airports, I need to explore the graph for each airport.
Helper function: exploreKG('Allama_Iqbal_International_Airport': ['operator', 'operatingOrganisation']), exploreKG('Faisalabad_International_Airport': ['operator']), exploreKG('Multan_International_Airport': ['operator'])
[User]
Execution result: ['Allama_Iqbal_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority'], ['Allama_Iqbal_International_Airport', 'operatingOrganisation', 'Pakistan_Civil_Aviation_Authority'], ['Faisalabad_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority'], ['Multan_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority']
[ChatGPT]
Statement: Since all of the airports' operator is government agency 'Pakistan_Civil_Aviation_Authority' and also the operator of 'Jinnah International Airport', the claim is True.
Helper function: Verification('True')

Example 2)
Claim: Tim Brooke-Taylor starred as a fictional character, which was first aired on 10/03/1983 and was broadcast by STV.
Given entity: ["1983-10-03", "STV", "Tim_Brooke-Taylor"]

[ChatGPT]
Statement: I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function: getRelation("1983-10-03"), getRelation("STV"), getRelation("Tim_Brooke-Taylor")
[User]
Execution result: Relation_list("1983-10-03") = ['~deathDate', '~activeYearsStartDate', '~added', '~dateOfDeath', '~date', '~years', '~termStart', '~start', '~birthDate', '~establishedDate', '~released', '~openingDate', '~foundingDate', '~age', '~releaseDate', '~originalairdate', '~firstAired', '~dateOfBirth'], Relation_list("STV") = ['~title', '~sisterNames', '~tv', '~formerName', '~code', '~owner', '~undp', '~distributor', '~name', '~alt', '~formerNames', '~callLetters', '~iataLocationIdentifier', '~rdf-schema#label', '~agencyStationCode', '~callSign', '~broadcastedBy', '~channel', '~iata'], Relation_list('Tim_Brooke-Taylor') = ['birthName', '~voice', '~caption', '~author', 'hypernym', '22-rdf-syntax-ns#type', 'name', 'surname', 'placeOfBirth', 'description', 'genre', 'notableWork', 'dateOfBirth', 'birthDate', 'honorificSuffix', 'shortDescription', 'subject', 'title', 'nationality', '~before', '~voices', 'imdbId', 'spouse', 'rdf-schema#label', 'birthPlace', '~writer', '~after', 'years', 'givenName', 'birthYear', '~starring', '~creator', 'active']
[ChatGPT]
Statement: To verify the information in the claim, I can choose proper relation for each entity.
Helper function: exploreKG("1983-10-03": ['~firstAired']), exploreKG("STV": ['~broadcastedBy', '~channel']), exploreKG("Tim_Brooke-Taylor": ['~starring'])
[User]
Execution result: ['"1983-10-03"', '~firstAired', 'Terrahawks'], ['"1983-10-03"', '~firstAired', 'Scarecrow_and_Mrs._King'], ['"1983-10-03"', '~firstAired', 'Orm_and_Cheep'], ['"1983-10-03"', '~firstAired', 'Watch_Mr._Wizard'], ['"1983-10-03"', '~firstAired', 'Where_in_the_World_(UK_game_show)'], ['"1983-10-03"', '~firstAired', 'Go_(game_show)'], ['"1983-10-03"', '~firstAired', 'Bananaman'], ['"STV"', '~broadcastedBy', 'Bananaman'], ['"STV"', '~channel', 'Brain_Box'], ['Tim_Brooke-Taylor', '~starring', 'How_to_Irritate_People'], ['Tim_Brooke-Taylor', '~starring', 'Broaden_Your_Mind'], ['Tim_Brooke-Taylor', '~starring', 'ISIRTA_songs'], ['Tim_Brooke-Taylor', '~starring', 'What_the_Dickens'], ['Tim_Brooke-Taylor', '~starring', 'Bananaman']
[ChatGPT]
Statement: There is the fictional character 'Bananaman' which satisfy all the information in the claim.
Helper function: Verification('True')

Example 3)
Claim: Samsung is located in São Paulo.
Given entity: ["Samsung", "São_Paulo"]

[ChatGPT]
Statement: I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function: getRelation("Samsung"), getRelation("São_Paulo")
[User]
Execution result: Relation_list("Samsung") = ['numEmployees', 'keyPeople', 'industry', 'type', 'hypernym', 'subsidiary', 'logo', 'subject', 'foundation', 'product', '22-rdf-syntax-ns#type', 'name', 'netIncome', 'foundingDate', 'rdf-schema#label', 'revenue', 'homepage', 'subsid', 'location', 'foundingYear', 'keyPerson', 'products', 'numberOfEmployees'], Relation_list("São_Paulo") = ['imageCaption', 'coordinatesRegion', '22-rdf-syntax-ns#type', '~capital', 'areaCityKm', 'establishedTitle', '~west', 'motto', '~before', 'populationRank', 'float', 'foundingDate', '~locationTown', 'subdivisionType', '~finalAssembly', 'populationTotalRanking', 'rainfall', '~location']
[ChatGPT]
Statement: To verify the information in the claim, I have to find the location of 'Hypermarcas' or place located in 'São_Paulo'.
Helper function: exploreKG("Samsung": ['location']), exploreKG("São_Paulo": ['~location'])
[User]
Execution result: ['Samsung', 'location', 'Korea'], ['Samsung', 'location', 'Seoul'], ['São_Paulo', '~location', '2009_Santos_FC_season'], ['São_Paulo', '~location', 'Vanguarda_Agro']
[ChatGPT]
Statement: To verify 'Samsung' is located in 'São Paulo', I need the relation list of 'Samsung'.
Helper function: getRelation("Samsung"), getRelation("São_Paulo")
[User]
Execution result: Relation_list("Samsung") = ['numEmployees', 'keyPeople', 'industry', 'type', 'hypernym', 'subsidiary', 'logo', 'subject', 'foundation', 'product', '22-rdf-syntax-ns#type', 'name', 'netIncome', 'foundingDate', 'rdf-schema#label', 'revenue', 'homepage', 'subsid', 'location', 'foundingYear', 'keyPerson', 'products', 'numberOfEmployees'], Relation_list("São_Paulo") = ['imageCaption', 'coordinatesRegion', '22-rdf-syntax-ns#type', '~capital', 'areaCityKm', 'establishedTitle', '~west', 'motto', '~before', 'populationRank', 'float', 'foundingDate', '~locationTown', 'subdivisionType', '~finalAssembly', 'populationTotalRanking', 'rainfall', '~location']
[ChatGPT]
Statement: I repeated calling 'getRelation' for same entity "Samsung" and "São_Paulo". Therefore, we abstain the claim.
Helper function: Abstain()


Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>
"""

prompt_confidence = """
Your task is to determine the given claim is whether true or false based on the graph data without your base knowledge.
You can use below helper functions to find the evidence in knowledge graph data to find answer.

<Helper functions>
1. getRelation(entity): Returns the list of relations connected to the entity.
2. exploreKG(entity: [relations]): Returns the corresponding tail entities in graph data starts from single entity and given relations.
3. confidenceCheck(): Please review the previous conversation between the you and the user. If the reasoning is going in the right direction, say ‘Alright’. If the process is incorrect at any point, say ‘Wrong’.
4. Verification(True/False): Once verification is done, call this function with labels.

You must follow the exact format of the given helper functions.

Now, I will give you a claim and Given Entity that you can refer to.
Your task is to use proper helper functions to explore and obtain proper triple information from the knowledge graph dataset.
Stop for my response after calling the helper function and continue your Statement task after getting a response from [User].
Importantly, the relation with the '~' symbol indicates the reverse direction of the relation.

Here are some examples.

Example 1)
Claim: The airport in Punjab, Pakistan is operated by the government agency of the Jinnah International Airport.
Given entity: ["Punjab, Pakistan", "Jinnah_International_Airport"]

[ChatGPT]
Statement: I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function: getRelation("Punjab, Pakistan"), getRelation("Jinnah_International_Airport")
[User]
Execution result: Relation_list("Punjab, Pakistan") = ['s', 'divdab', 'state', 'location', 'birthPlace', 'placeOfBirth', 'rdf-schema#label', 'deathPlace', 'placeOfDeath', 'origin', 'mapCaption', 'country'], Relation_list("Jinnah_International_Airport") = ['statYear', 'website', 'elevationF', 'stat2Data', 'r2LengthM', 'r1Number', 'stat1Data', '~targetAirport', 'icao', '~secondaryHubs', 'stat3Header', 'stat2Header', '~hubs', 'operator', 'imageWidth', 'airportManager', '~hubAirport', 'iata', 'type', 'r2Number', 'city', 'ownerOper', 'name', 'metricRwy', 'elevationM', 'hub', 'hypernym', '~headquarter', '~bases', '~origin', 'stat1Header', 'image2Width', 'runwayLength', 'icaoLocationIdentifier', 'owner', 'homepage', '22-rdf-syntax-ns#type', '~stopover', 'r1Surface', 'r1LengthM', 'subject', 'runwayDesignation', 'rdf-schema#label', '~wikiPageRedirects', 'image', 'stat3Data', '~location', 'location', '~target', '~headquarters', 'r2Surface', 'elevation', 'iataLocationIdentifier', 'runwaySurface', 'r2LengthF', 'r1LengthF', 'cityServed']
[ChatGPT]
Statement: I need to check the process is going well.
Helper function: confidenceCheck()
[User]
Execution result: <Previous chat history>
[ChatGPT]
Statement: Everything is on track. Now, to find the airport located in Punjab, I need to explore the graph with "Punjab, Pakistan" and related relations. Also, to find the government agency of 'Jinnah_International_Airport', I need to explore the graph too.
Helper function: exploreKG('Punjab, Pakistan': ['location']), exploreKG("Jinnah_International_Airport": ['operator', 'ownerOper'])
[User]
Execution result: ['Punjab, Pakistan', '~location', 'Bahawalpur_Zoo'], ['Punjab, Pakistan', '~location', 'Allama_Iqbal_International_Airport'], ['Punjab, Pakistan', '~location', 'Jungle_World,_Rawalpindi'], ['Punjab, Pakistan', '~location', 'Faisalabad_International_Airport'], ['Punjab, Pakistan', '~location', 'Multan_International_Airport'], ['Jinnah_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority'], ['Jinnah_International_Airport', 'ownerOper', 'Pakistan_Civil_Aviation_Authority']
[ChatGPT]
Statement: I need to check the process is going well.
Helper function: confidenceCheck()
[User]
Execution result: <Previous chat history>
[ChatGPT]
Statement: Everything is on track. There are many airports in 'Punjab, Pakistan', and the operator of 'Jinnah_International_Airport' is 'Pakistan_Civil_Aviation_Authority'. Here, we have to find the proper relation to find the operator of the airports.
Helper function: getRelation('Allama_Iqbal_International_Airport'), getRelation('Faisalabad_International_Airport'), getRelation('Multan_International_Airport')
[User]
Execution result: Relation_list('Allama_Iqbal_International_Airport') = ['operator', 'operatingOrganisation', 'hub'], Relation_list('Faisalabad_International_Airport') = ['operator', 'owner'], Relation_list('Multan_International_Airport') = ['operator', 'owner']
[ChatGPT]
Statement: I need to check the process is going well.
Helper function: confidenceCheck()
[User]
Execution result: <Previous chat history>
[ChatGPT]
Statement: Everything is on track. To find the operator of the airports, I need to explore the graph for each airport.
Helper function: exploreKG('Allama_Iqbal_International_Airport': ['operator', 'operatingOrganisation']), exploreKG('Faisalabad_International_Airport': ['operator']), exploreKG('Multan_International_Airport': ['operator'])
[User]
Execution result: ['Allama_Iqbal_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority'], ['Allama_Iqbal_International_Airport', 'operatingOrganisation', 'Pakistan_Civil_Aviation_Authority'], ['Faisalabad_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority'], ['Multan_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority']
[ChatGPT]
Statement: I need to check the process is going well.
Helper function: confidenceCheck()
[User]
Execution result: <Previous chat history>
[ChatGPT]
Statement: Everything is on track. Since all of the airports' operator is government agency 'Pakistan_Civil_Aviation_Authority' and also the operator of 'Jinnah International Airport', the claim is True.
Helper function: Verification('True')
[User]
Execution result: Verification('True')
[ChatGPT]
Statement: I need to check the process is going well.
Helper function: confidenceCheck()
[User]
Execution result: <Previous chat history>
[ChatGPT]
Statement: Everything is on track. Finish the process since verification is done.

Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>
"""

paraphrase_prompt = """
You are the paraphraser. Rewrite the following claim in a more formal tone, keeping the core idea intact.
If the given claim has a colloquial style format, paraphrase it into written style format.
Give three paraphrased sentences for given claim.

<Example 1>
[User]
Claim : Sure. He was born in England on 1st January 1942.
[ChatGPT]
1. He was born in England on January 1, 1942.
2. His place of birth is England, and he was born on 1st January 1942.
3. The person was born in England on the 1st of January, 1942.


<Example 2>
[User]
Claim : Hypermarcas is a type of S.A. (corporation) that has a subsidiary called Mantecorp and employs 10252 employees.
[ChatGPT]
1. Hypermarcas operates as a type of S.A. (corporation) and possesses a subsidiary called Mantecorp, which has a workforce of 10,252 employees.
2. Hypermarcas is categorized as a type of S.A. (corporation) and has a subsidiary named Mantecorp, employing 10,252 workers.
3. Hypermarcas operates under the structure of an S.A. (corporation) and manages a subsidiary, Mantecorp, with a total of 10,252 employees.


<Example 3>
[User]
Claim : Albert B White was born in Cleveland on 22nd September 1856.
[ChatGPT]
1. Albert B. White was born in Cleveland on the 22nd of September, 1856.
2. The birth of Albert B. White took place in Cleveland on September 22, 1856.
3. On September 22, 1856, Albert B. White was born in Cleveland.


<Example 4>
[User]
Claim : The Baku Turkish Martyrs' Memorial, designed by Huseyin Butuner and Hilmi Guner, is located in Azerbaijan, where the leader is Artur Rasizade.
[ChatGPT]
1. The Baku Turkish Martyrs' Memorial, created by architects Huseyin Butuner and Hilmi Guner, is located in Azerbaijan, where Artur Rasizade serves as the leader.
2. Designed by Huseyin Butuner and Hilmi Guner, the Baku Turkish Martyrs' Memorial is located in Azerbaijan, where Artur Rasizade is the leader.
3. The Baku Turkish Martyrs' Memorial, created by Huseyin Butuner and Hilmi Guner, is found in Azerbaijan, the country led by Artur Rasizade.


<Example 5>
[User]
Claim : Anatole de Grunwald was the producer of 'English Without Tears', with Harold French, the director and Bernard Knowles, the cinematographer.
[ChatGPT]
1. "English Without Tears" was produced by Anatole de Grunwald, with Harold French as the director and Bernard Knowles serving as the cinematographer.
2. Anatole de Grunwald served as the producer of "English Without Tears," collaborating with director Harold French and cinematographer Bernard Knowles.
3. "English Without Tears" was produced by Anatole de Grunwald, with direction by Harold French and cinematography by Bernard Knowles.


<Example 6>
[User]
Claim : It can be found in Italy where Pietro Grasso the leader and the Italian language is spoken.
[ChatGPT]
1. It is located in Italy, where Pietro Grasso serves as the leader and the Italian language is spoken.
2. It can be found in Italy, a country where the Italian language is spoken and Pietro Grasso holds a leadership position.
3. This site can be found in Italy, where the Italian language is spoken and leadership is provided by Pietro Grasso.


<Example 7>
[User]
Claim : Yes Bill Oddie from Lancashire starred in Bananaman.
[ChatGPT]
1. Bill Oddie, a native of Lancashire, featured in "Bananaman."
2. Bill Oddie, originally from Lancashire, was a star in "Bananaman."
3. Bill Oddie, who comes from Lancashire, participated in the show "Bananaman."


<Example 8>
[User]
Claim : Well, lemon is an ingredient in Bandeja paisa.
[ChatGPT]
1. Lemon is an ingredient in Bandeja paisa.
2. Lemon is included as an ingredient in Bandeja paisa.
3. Lemon is a component of Bandeja paisa.



Now, it's your turn. Continue your 'Statement and Evaluation' task. Response must have same form with upper examples.
[User]
Claim : <<<<CLAIM>>>>
"""