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
Helper function: getRelation["\"1983-10-03\""] ## getRelation["\"STV\""] ## getRelation["Tim_Brooke-Taylor"]
[User]
Execution result: Relation_list["\"1983-10-03\""] = ['~deathDate', '~activeYearsStartDate', '~added', '~dateOfDeath', '~date', '~years', '~termStart', '~start', '~birthDate', '~establishedDate', '~released', '~openingDate', '~foundingDate', '~age', '~releaseDate', '~originalairdate', '~firstAired', '~dateOfBirth'], Relation_list["\"STV\""] = ['~title', '~sisterNames', '~tv', '~formerName', '~code', '~owner', '~undp', '~distributor', '~name', '~alt', '~formerNames', '~callLetters', '~iataLocationIdentifier', '~rdf-schema#label', '~agencyStationCode', '~callSign', '~broadcastedBy', '~channel', '~iata'], Relation_list('Tim_Brooke-Taylor') = ['birthName', '~voice', '~caption', '~author', 'hypernym', '22-rdf-syntax-ns#type', 'name', 'surname', 'placeOfBirth', 'description', 'genre', 'notableWork', 'dateOfBirth', 'birthDate', 'honorificSuffix', 'shortDescription', 'subject', 'title', 'nationality', '~before', '~voices', 'imdbId', 'spouse', 'rdf-schema#label', 'birthPlace', '~writer', '~after', 'years', 'givenName', 'birthYear', '~starring', '~creator', 'active']
[ChatGPT]
Statement: To verify the information in the claim, I can choose proper relation for each entity.
Helper function: exploreKG["\"1983-10-03\""]=['~firstAired'] ## exploreKG["\"STV\""]=['~broadcastedBy', '~channel']
[User]
Execution result: ["\"1983-10-03\"", '~firstAired', 'Terrahawks'], ["\"1983-10-03\"", '~firstAired', 'Scarecrow_and_Mrs._King'], ["\"1983-10-03\"", '~firstAired', 'Orm_and_Cheep'], ["\"1983-10-03\"", '~firstAired', 'Watch_Mr._Wizard'], ["\"1983-10-03\"", '~firstAired', 'Where_in_the_World_(UK_game_show)'], ["\"1983-10-03\"", '~firstAired', 'Go_(game_show)'], ['"1983-10-03"', '~firstAired', 'Bananaman'], ["\"STV\"", '~broadcastedBy', 'Bananaman'], ["\"STV\"", '~channel', 'Brain_Box']
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

main_agent2 = """  
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
Claim: Chicharrón is a dish from Spain and is an ingredient found in a food which is a traditional food from the Paisa region.
Given entity: ["Spain", "Paisa_Region", "Chicharrón"]

[ChatGPT]
Statement: I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function: getRelation["Spain"] ## getRelation["Paisa_Region"] ## getRelation["Chicharrón"]
[User]
Execution result: Relation_list["Spain"] = ['areaRank', '~railwayRollingStock', '~foundationPlace', 'languages2Type', 'nationalAnthem', 'flag', '~deathPlace', '~nationalOrigin', 'lowerHouse', '~regions', '~countries', '~education', '~builder', '~patronage', '~spokenIn', '~states', 'hdi', '~citizenship', '~hostCity', '~knownFor', '~controlledby', '~recordedIn', '~buried', 'gdpPppYear', 'establishedDate', '~restingPlace', '~largestDistillery', '~site', '~populationPlace', 'languages', '~finish', '~country'], Relation_list("Chicharrón") = ['subject', '~ingredient', 'region', 'country', 'rdf-schema#label', 'mainIngredient', 'servingTemperature', 'other', 'ingredient', 'hypernym', '22-rdf-syntax-ns#type', 'ingredientName', 'caption', 'notes', 'served', 'course', 'type', 'name'], Relation_list("Paisa_Region") = ['subject', '~wikiPageDisambiguates', 'hypernym', '22-rdf-syntax-ns#type', '~region']
[ChatGPT]
Statement: Now, to find whether Chicharrón is a dish from Spain, I need to explore the graph with "Chicharrón" and related relations. Also, to find the food from 'Paisa Region', we have to find the proper relation to find the food from Paisa Region.
Helper function: exploreKG["Chicharrón"]=['country']) ## exploreKG["Paisa_Region"]=['~region']
[User]
Execution result: ['Chicharrón', 'country', 'Spain'], ['Paisa_Region', '~region', 'Bandeja_paisa']
[ChatGPT]
Statement: Now, we have to find the ingredient of 'Bandeja_paisa' is 'Chicharrón'. Here, we have to find proper relation to find the ingredient of 'Bandeja_paisa'.
Helper function: getRelation['Bandeja_paisa']
[User]
Execution result: Relation_list['Bandeja_paisa'] = ['variations', 'subject', 'country', 'region', 'mainIngredient', 'rdf-schema#label', 'name', 'ingredient', 'hypernym', '22-rdf-syntax-ns#type', 'ingredientName', 'caption', 'course', 'type', 'hasVariant']
[ChatGPT]
Statement: To find the ingredient of the 'Bandeja_paisa', I need to explore the graph for each airport.
Helper function: exploreKG['Bandeja_paisa']=['ingredient', 'mainIngredient']
[User]
Execution result: ['Bandeja_paisa', 'ingredient', 'Pork_belly'], ['Bandeja_paisa', 'ingredient', 'Chorizo'], ['Bandeja_paisa', 'ingredient', 'Lemon'], ['Bandeja_paisa', 'ingredient', 'Chicharrón'], ['Bandeja_paisa', 'ingredient', 'Arepa'], ['Bandeja_paisa', 'mainIngredient', '"red beans, pork belly, white rice, ground meat, chicharon, fried egg, plantain (patacones), chorizo, arepa, hogao sauce, black pudding (morcilla), avocado and lemon"']
[ChatGPT]
Statement: Since Chicharrón is from Spain, and Chicharrón is the ingredient of Bandeja_paisa, which is from Paisa region, the given claim is true.
Helper function: Verification['True']
[User]
Execution result: True

Example 2)
Claim: A building, in Cleveland, Ohio 44114 and completed in 1985, has 45 floors.
Given entity: ["\"45\"", "\"1985\"", "\"Cleveland, Ohio 44114\""]

[ChatGPT]
Statement: I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function: getRelation['"45"'] ## getRelation['"1985"'] ## getRelation['"Cleveland, Ohio 44114"']
[User]
Execution result: Relation_list['"45"'] = ['~floorCount', '~designatedOther1Number', '~rd1Score18Agg', '~highestsinglesranking', '~schoolnumber', '~itfRank', '~quellhöhe', '~peak19a', '~heightMetric', '~ruPointsa', '~h', '~shipAircraft', '~parishes', '~set', '~numEmployees', '~6.0−6._', '~arearank', '~diameterMetric', '~c3m', '~demographics1Info', '~currentAwards', '~areakm', '~fifaMin', '~us', '~draftpick', '~team1overs', '~seasonNumber', '~highestLatS', '~topFloor', '~floors', '~blankInfo'], Relation_list['"1985"'] = ['~buildingEndDate, '~completionDate'], Relation_list['"Cleveland, Ohio 44114"'] = ['~address', '~location']
[ChatGPT]
Statement: To verify the information in the claim, I can choose proper relation for each entity.
Helper function: exploreKG['"45"']=['~floorCount', '~floors'] ## exploreKG['"1985"']=['~buildingEndDate', '~completionDate'] ## exploreKG['"Cleveland, Ohio 44114"']=['~location']
[User]
Execution result: ['"45"', '~floorCount', 'Al_Boraq_Tower'], ['"45"', '~floorCount', 'Petron_Megaplaza'], ['"45"', '~floorCount', 'Canterra_Tower'], ['"45"', '~floorCount', '200_Public_Square'], ['"45"', '~floorCount', 'Act_Tower'], ['"1985"', '~buildingEndDate', 'Raymond_James_Tower'], ['"1985"', '~buildingEndDate', '88_on_Field'], ['"1985"', '~buildingEndDate', '200_Public_Square'], ['"Cleveland, Ohio 44114"', '~location', 'Public_Auditorium'], ['"Cleveland, Ohio 44114"', '~location', '200_Public_Square']
[ChatGPT]
Statement: There is the building '200_Public_Square' which satisfy having 45 floors, completed in 1985, and located in Cleveland, Ohio 44114.
Helper function: Verification['True']
[User]
Execution result: True

Example 3)
Claim: 2003–04 Gretna F.C. season leader's name is Niels Henry Sonne.
Given entity: ["2003–04_Gretna_F.C._season", "Niels_Henry_Sonne"]

[ChatGPT]
Statement: I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function: getRelation["2003–04_Gretna_F.C._season"] ## getRelation["Niels_Henry_Sonne"]
[User]
Execution result: Relation_list["2003–04_Gretna_F.C._season"] = ['club', '~predecessor', 'predecessor', 'nextseason', 'cup2Result', 'prevseason', 'successor', 'league', 'cup1Result', 'subject', 'season', 'manager', 'cup3Result', 'mgrtitle', 'team', 'cup', 'managerTitle', 'leagueResult'], Relation_list["Niels_Henry_Sonne"] = ['22-rdf-syntax-ns#type', 'description', 'birthPlace', 'birthName', 'surname', 'birthYear', 'birthDate', 'placeOfBirth', 'dateOfDeath', 'relatives', 'placeOfDeath', 'name', 'knownFor', 'subject', 'nationality', 'occupation', 'hypernym', 'shortDescription', 'deathPlace', 'relative', 'givenName', 'deathDate', 'dateOfBirth', 'rdf-schema#label', 'deathYear', 'spouse']
[ChatGPT]
Statement: To verify the information in the claim, I have to find the leader of '2003–04_Gretna_F.C._season' is 'Niels_Henry_Sonne'.
Helper function: exploreKG["2003–04_Gretna_F.C._season"]=['manager']
[User]
Execution result: ['2003–04_Gretna_F.C._season', 'manager', 'Rowan_Alexander']
[ChatGPT]
Statement: Since we cannot verify "Niels_Henry_Sonne" is not a leader of '2003–04_Gretna_F.C._season' by execution result, given claim is False.
Helper function: Verifiation['False']
[User]
Execution result: False


Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>
"""

main_agent3 = """  
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
Claim: Located in Pakistan, an airport has a runway length of 2900 metres and a runway name, 18L/36R.
Given entity: ["\"18L/36R\"", "Pakistan", "\"2900.0\""]

[ChatGPT]
Statement: I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function: getRelation['"18L/36R"'] ## getRelation["Pakistan"] ## getRelation['"2900.0"']
[User]
Execution result: Relation_list['"18L/36R"'] = ['~runwayName', '~runwayDesignation'], Relation_list["Pakistan"] = ['~location', '~lived', '~combatant', '~locationCountry', 'languagesType', 'currencyCode', '~areaServed', '~caption', 'populationEstimateRank', '~perps', 'utcOffsetDst', '~countriesAffected', 'populationEstimateYear', 'officialLanguages', '~language', '~manufacturer', 'sovereigntyType', '~channel', '~host'], Relation_list['"2900.0"'] = ['~frontCabHeight', '~maxTakeoffWeightAlt', '~loadedWeightAlt', '~weight', '~runwayLength', '~tuition', '~catchment', '~rangeMain', '~payloadAlt', '~emptyWeightMain', '~effectiveRadiatedPower', '~distLy', '~gdpPppPerCapita', '~goals', '~climbRateMain']
[ChatGPT]
Statement: Now, to find the airport located in Pakistan, I need to explore the graph with "Pakistan" and related relations. Also, we have to check the airport has a runway length of 2900 and name of runway is '18L/36R'. We have to find the information using proper relation.
Helper function: exploreKG['"18L/36R"']=['~runwayName']) ## exploreKG["Pakistan"]=['~location'] ## exploreKG['"2900.0"']=['~runwayLength']
[User]
Execution result: ['"18L/36R"', '~runwayName', 'Allama_Iqbal_International_Airport'], ['"18L/36R"', '~runwayName', 'Adolfo_Suárez_Madrid–Barajas_Airport'], ["Pakistan", '~location', 'Allama_Iqbal_International_Airport'], ["Pakistan", '~location', 'Pakistan_Science_Foundation'], ["Pakistan", '~location', 'Myers_College'], ["Pakistan", '~location', 'Kot_Diji'], ["Pakistan", '~location', '2014_Rawalpindi_suicide_bombing'], ['"2900.0"', '~runwayLength', 'Allama_Iqbal_International_Airport'], ['"2900.0"', '~runwayLength', 'Teniente_General_Benjamín_Matienzo_International_Airport'], ['"2900.0"', '~runwayLength', 'Federico_García_Lorca_Airport']
[ChatGPT]
Statement: Since 'Allama_Iqbal_International_Airport' is located in Pakistan, has runway length of 2900, and 18L/36R as a runway name, the claim is True.
Helper function: Verification['True']
[User]
Execution result: True

Example 2)
Claim: A company, the parent group of Mantecorp, was founded on January 1, 2001 in São Paulo.
Given entity: ["\"2001-01-01\"", "Mantecorp", "São_Paulo"]

[ChatGPT]
Statement: I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function: getRelation['"2001-01-01"'] ## getRelation["Mantecorp"] ## getRelation["São_Paulo"]
[User]
Execution result: Relation_list['"2001-01-01"'] = ['~foundingDate', '~closingDate', '~orderDate', '~openingDate', '~launch', '~populationAsOf', '~founded', '~extinctionDate', '~firstPublicationDate', '~formationDate', '~deathDate'], Relation_list["Mantecorp"] = ['~subsidiary', '22-rdf-syntax-ns#type', '~subsid'], Relation_list["São_Paulo"] = ['~location', 'imageCaption', '~locationCountry', 'populationMacrometro', '~areaServed', 'subdivisionName', '~caption', '~space', 'utcOffsetDst', '~subsidiary', 'areaMagnitude', 'elevationM', '~beatifiedPlace', '~canonizedPlace', 'officialName']
[ChatGPT]
Statement: Now, to find the parent group of Mantecorp, we have to find proper relation from 'Mantecorp'. Also, we have to find the parent group of Mantecorp was founded on January 1, 2001 and located in São_Paulo.
Helper function: exploreKG['"2001-01-01"']=['~foundingDate'] ## exploreKG["Mantecorp"]=['~subsidiary', '~subsid']  ## exploreKG["São_Paulo"]=['~location']
[User]
Execution result: ['"2001-01-01"', '~foundingDate', 'Hypermarcas'], ['Mantecorp', '~subsidiary', 'Hypermarcas'], ['Mantecorp', '~subsid', 'Hypermarcas'], ['São_Paulo', '~location', 'Brigadeiro_Faria_Lima_Avenue'], ['São_Paulo', '~location', 'Martinelli_Building'], ['São_Paulo', '~location', 'Votorantim_Siderurgia'], ['São_Paulo', '~location', '2015_São_Paulo_World_Cup'], ['São_Paulo', '~location', 'Banco_Votorantim'], ['São_Paulo', '~location', 'Hypermarcas']
[ChatGPT]
Statement: Since 'Hypermarcas' has a subsidiary company 'Mantecorp', which is founded on January 1, 2001 and located in São_Paulo, all of the information is satisfied.
Helper function: Verification['True']
[User]
Execution result: True

Example 3)
Claim: Am Harazé is located in the Pacific Daylight time zone and has a UTC offset of -6.
Given entity: ["Pacific_Daylight_Time", "\"−6\"", "Am_Harazé"]

[ChatGPT]
Statement: I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function: getRelation["Pacific_Daylight_Time"] ## getRelation['"−6"'] ## getRelation["Am_Harazé"]
[User]
Execution result: Relation_list["Pacific_Daylight_Time"] = ['rdf-schema#label', '~timeZone'], Relation_list['"−6"'] = ['~utcOffsetDst', '~decRecordLowC', '~decisionClock', '~sports', '~c5g', '~row12Shift', '~sepRecordLowC', '~julRecordLowC', '~synonyms', '~gd', '~longd', '~yearLowC', '~sepChill', '~janRecordHighC', '~mayRecordLowMaximumC', '~marRecordLowC', '~decLowC', '~nationalgoals', '~sepLowC', '~novLowC', '~systematicname'], Relation_list["Am_Harazé"] = ['timeZone', 'isPartOf', 'latd', 'longd', 'longm', 'coordinatesDisplay', 'subdivisionType', 'timezone', 'longew', 'coordinatesRegion', 'latm', 'pushpinMapsize', 'pushpinMapCaption', 'name', 'subject', 'hypernym', 'unitPref', 'longs', 'country', 'rdf-schema#label', 'subdivisionName', 'pushpinLabelPosition', 'utcOffset']
[ChatGPT]
Statement: To verify the information in the claim, I have to find 'Am_Harazé' is located in Pacific Daylight time zone and has UTC offset -6.
Helper function: exploreKG["Am_Harazé"]=['utcOffset', 'timezone'] ## exploreKG["Pacific_Daylight_Time"]=['~timeZone'] ## exploreKG['"-6"']=['~utcOffset']
[User]
Execution result: ['Am_Harazé', 'utcOffset', '"+1"'], ['Am_Harazé', 'timezone', 'West_Africa_Time'], ['Pacific_Daylight_Time', '~timeZone', 'Ciudad_Ayala'], ['"-6"', '~utcOffset', 'Bryce,_Utah'], ['"-6"', '~utcOffset', 'Mathews,_Alabama'], ['"-6"', '~utcOffset', 'Kanwaka,_Kansas'], ['"-6"', '~utcOffset', 'Ingersoll,_Oklahoma']
[ChatGPT]
Statement: By execution result, Am_Harazé is located in West Africa Time zone, and has utcOffset +1. Therefore, given claim is False.
Helper function: Verifiation['False']
[User]
Execution result: False


Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>
"""