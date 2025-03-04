pr_1 = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use below helper functions to find the evidence for finding labels.

Helper Functions
1.getRelation[entity]: Returns the list of relations linked to the entity. You can choose several relations from the list that seem related to the claim.
2.exploreKG[entity]=[relation_1,relation_2, ... relation_K]: Returns the triple set around the entity. For example, [entity, relation_1, tail entity] etc. You can choose relation from [User]'s execution result.
3.Verification[]: After getting enough evidence after exploreKG() helper function and if verification can be done, call this function. If [User] requires more information, you need to collect more triples in following steps.

You must follow the exact format of the given helper function.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for [User] response. If response has made, continue your [Your Task] (Do not make multiple 'Helper function: ' lines).
Importantly, you have to use inverse relation if you need. For example, if you want to find films starred by certain actors (when only actors were given), you have to use '~starred_actors' relation such as exploreKG['actor']=['~starred_actors'].
Importantly, Do not change the format of the entity or relation including '~'.

Here are some examples.

Example 1)
Claim: The airport in Punjab, Pakistan is operated by the government agency of the Jinnah International Airport.
Given entity: ["\"Punjab, Pakistan\"", "Jinnah_International_Airport"]

[Your Task]
Statement : I need to look around the the given entities. First, I need the relation list linked to Punjab, Pakistan
Helper function : getRelation["\"Punjab, Pakistan\""] 
[User]
Execution result : Relation_list["\"Punjab, Pakistan\""] = ['s', 'divdab', 'state', '~location', 'birthPlace', 'placeOfBirth', 'rdf-schema#label', 'deathPlace', 'placeOfDeath', 'origin', 'mapCaption', 'country']
[Your Task]
Statement : I need to look around the the given entities. Now, I need the relation list linked to Jinnah_International_Airport
Helper function : getRelation["Jinnah_International_Airport"]
[User]
Execution result : Relation_list("Jinnah_International_Airport") = ['statYear', 'website', 'elevationF', 'stat2Data', 'r2LengthM', 'r1Number', 'stat1Data', '~targetAirport', 'icao', '~secondaryHubs', 'stat3Header', 'stat2Header', '~hubs', 'operator', 'imageWidth', 'airportManager', '~hubAirport', 'iata', 'type', 'r2Number', 'city', 'ownerOper', 'name', 'metricRwy', 'elevationM', 'hub', 'hypernym', '~headquarter', '~bases', '~origin', 'stat1Header', 'image2Width', 'runwayLength', 'icaoLocationIdentifier', 'owner', 'homepage', '22-rdf-syntax-ns#type', '~stopover', 'r1Surface', 'r1LengthM', 'subject', 'runwayDesignation', 'rdf-schema#label', '~wikiPageRedirects', 'image', 'stat3Data', '~location', 'location', '~target', '~headquarters', 'r2Surface', 'elevation', 'iataLocationIdentifier', 'runwaySurface', 'r2LengthF', 'r1LengthF', 'cityServed']
[Your Task]
Statement : Now, to find the airport located in Punjab, I need to explore the graph with "Punjab, Pakistan" related to location.     and related relations. Also, to find the government agency of 'Jinnah_International_Airport', I need to explore the graph too.
Helper function : exploreKG["\"Punjab, Pakistan\""]=['~location'])
[User]
Execution result : ["\"Punjab, Pakistan\"", '~location', 'Bahawalpur_Zoo'], ["\"Punjab, Pakistan\"", '~location', "Allama_Iqbal_International_Airport"], ["\"Punjab, Pakistan\"", '~location', 'Jungle_World,_Rawalpindi'], ["\"Punjab, Pakistan\"", '~location', 'Faisalabad_International_Airport'], ["\"Punjab, Pakistan\"", '~location', 'Multan_International_Airport'], 
[Your Task]
Statement : According to the triples, Allama_Iqbal_International_Airport, Faisalabad_International_Airport,Multan_International_Airport are located in the Punjab, Pakistan. So the claim is true.
Helper function : Verification[]
[User]
Execution result : You need more information to verify the claim. Try to look triples of Jinnah_International_Airport linked by 'operator', 'ownerOper'
[Your Task]
Statement : Also, to find the government agency of 'Jinnah_International_Airport', look triples linked by 'operator', 'ownerOper'.
Helper function : exploreKG["Jinnah_International_Airport"]=['operator', 'ownerOper']
[User]
Execution result : ['Jinnah_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority'], ['Jinnah_International_Airport', 'ownerOper', 'Pakistan_Civil_Aviation_Authority']
[Your Task]
Statement : There are three aiports in Punjab, Pakistan. We need relations of those three airpots. First,let's look Allama_Iqbal_International_Airport's relations.
Helper function : getRelation['Allama_Iqbal_International_Airport']
[User]
Execution result : 
Relation_list['Allama_Iqbal_International_Airport'] = ['operator', 'operatingOrganisation', 'hub']
[Your Task]
Statement : Next,let's look Faisalabad_International_Airport's relations.
Helper function : getRelation['Faisalabad_International_Airport']
[User]
Execution result : 
Relation_list['Faisalabad_International_Airport'] = ['operator', 'owner']
[Your Task]
Statement : Next,let's look Multan_International_Airport's relations.
Helper function : getRelation['FMultan_International_Airport']
[User]
Execution result : 
Relation_list('Multan_International_Airport') = ['operator', 'owner']
[Your Task]
Statement : To find the operator of the airports, I need to explore the graph for each airports related to operator.
Helper function : exploreKG['Allama_Iqbal_International_Airport']=['operator', 'operatingOrganisation'] 
[User]
Execution result : ['Allama_Iqbal_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority'], ['Allama_Iqbal_International_Airport', 'operatingOrganisation', 'Pakistan_Civil_Aviation_Authority']
[Your Task]
Statement : Now, let's check the operator of Faisalabad_International_Airport
Helper function : exploreKG['Faisalabad_International_Airport']=['operator']
[User]
Execution result : ['Faisalabad_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority']
[Your Task]
Statement : Now, let's check the operator of Multan_International_Airport
Helper function : exploreKG['Multan_International_Airport']=['operator']
[User]
Execution result :['Multan_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority']
[Your Task]
Statement : Since all of the airports' operator is government agency 'Pakistan_Civil_Aviation_Authority' and also the operator of 'Jinnah International Airport', the claim is True.
Helper function : Verification[]


Example 2)
Claim: Tim Brooke-Taylor starred as a fictional character, which was first aired on 10/03/1983 and was broadcast by STV.
Given entity: ["\"1983-10-03\"", "\"STV\"", "Tim_Brooke-Taylor"]

[Your Task]
Statement : First, I need relations linked to Tim_Brooke-Taylor
Helper function : getRelation["Tim_Brooke-Taylor"]
[User]
Execution result : 
Relation_list('Tim_Brooke-Taylor') = ['birthName', '~voice', '~caption', '~author', 'hypernym', '22-rdf-syntax-ns#type', 'name', 'surname', 'placeOfBirth', 'description', 'genre', 'notableWork', 'dateOfBirth', 'birthDate', 'honorificSuffix', 'shortDescription', 'subject', 'title', 'nationality', '~before', '~voices', 'imdbId', 'spouse', 'rdf-schema#label', 'birthPlace', '~writer', '~after', 'years', 'givenName', 'birthYear', '~starring', '~creator', 'active']
[Your Task]
Statemnt : I need relation linked to 1983-10-03.
Helper function : getRelation["\"1983-10-03\""] 
[User]
Execution result : 
Relation_list["\"1983-10-03\""] = ['~deathDate', '~activeYearsStartDate', '~added', '~dateOfDeath', '~date', '~years', '~termStart', '~start', '~birthDate', '~establishedDate', '~released', '~openingDate', '~foundingDate', '~age', '~releaseDate', '~originalairdate', '~firstAired', '~dateOfBirth']
[Your Task]
Statemnt : I need relation linked to STV.
Helper function : getRelation["\"STV\""] 
[User]
Execution result : 
Relation_list["\"STV\""] = ['~title', '~sisterNames', '~tv', '~formerName', '~code', '~owner', '~undp', '~distributor', '~name', '~alt', '~formerNames', '~callLetters', '~iataLocationIdentifier', '~rdf-schema#label', '~agencyStationCode', '~callSign', '~broadcastedBy', '~channel', '~iata']
[Your Task]
Statement : To get the starred information about Tim Brooke-Taylor, I need triples linked with '~starring' with Tim Brooke-Taylor.
Helper function : exploreKG["Tim_Brooke-Taylor"]=['~starring']
[User]
Execution result:
['Tim_Brooke-Taylor', '~starring', 'How_to_Irritate_People'], ['Tim_Brooke-Taylor', '~starring', 'Broaden_Your_Mind'], ['Tim_Brooke-Taylor', '~starring', 'ISIRTA_songs'], ['Tim_Brooke-Taylor', '~starring', 'What_the_Dickens'], ['Tim_Brooke-Taylor', '~starring', 'Bananaman']
[Your Task]
Statement : From the triples, Tim Brooke Taylor starred on How_to_Irritate_People,Broaden_Your_Mind,ISIRTA_songs,What_the_Dickens,Bananaman. Now, let's check the first aired date of each program.
Helper function : exploreKG["\"1983-10-03\""]=['~firstAired'] 
[User]
Execution reuslt:
["\"1983-10-03\"", '~firstAired', 'Terrahawks'], ["\"1983-10-03\"", '~firstAired', 'Scarecrow_and_Mrs._King'], ["\"1983-10-03\"", '~firstAired', 'Orm_and_Cheep'], ["\"1983-10-03\"", '~firstAired', 'Watch_Mr._Wizard'], ["\"1983-10-03\"", '~firstAired', 'Where_in_the_World_(UK_game_show)'], ["\"1983-10-03\"", '~firstAired', 'Go_(game_show)'], ['"1983-10-03"', '~firstAired', 'Bananaman']
[Your Task]
Statement : From the triples, Bananman was first aired on 1983-10-03 which satisfy the claim. Now, I need to check if the Bananaman broadcast by STV.
Helper function : exploreKG["\"STV\""]=['~broadcastedBy', '~channel']
[User]
Execution reuslt : 
["\"STV\"", '~broadcastedBy', 'Bananaman'], ["\"STV\"", '~channel', 'Brain_Box']
[Your Task]
Statement : According to the triples, Bananman broadcast by STV and first starred on 1983-10-03 and Tim Brooke Taylor starred on. So the claim is True.
Helper function : Verification[]


Example 3)
Claim: Samsung is located in São Paulo.
Given entity: ["Samsung", "São_Paulo"]

[Your Task]
Statement : First, I need information about Samsung.
Helper function : getRelation["Samsung"]
[User]
Execution result : 
Relation_list["Samsung"] = ['numEmployees', 'keyPeople', 'industry', 'type', 'hypernym', 'subsidiary', 'logo', 'subject', 'foundation', 'product', '22-rdf-syntax-ns#type', 'name', 'netIncome', 'foundingDate', 'rdf-schema#label', 'revenue', 'homepage', 'subsid', 'location', 'foundingYear', 'keyPerson', 'products', 'numberOfEmployees']
[Your Task]
Statement : To know the location of Samsung, I need triples linked by 'location' with Samsung.
Helper function : exploreKG["Samsung"]=['location']
[User]
Execution result :
['Samsung', 'location', 'Korea'], ['Samsung', 'location', 'Seoul']
[Your Task]
Statement : According to the triples, Samsung is locate in Korea and Seoul. To check the relation with São Paulo, I need information about São Paulo.
Helper function : getRelation["São_Paulo"] 
[User]
Execution result :
Relation_list["São_Paulo"] = ['imageCaption', 'coordinatesRegion', '22-rdf-syntax-ns#type', '~capital', 'areaCityKm', 'establishedTitle', '~west', 'motto', '~before', 'populationRank', 'float', 'foundingDate', '~locationTown', 'subdivisionType', '~finalAssembly', 'populationTotalRanking', 'rainfall', '~location']
[Your Task]
Statement : Let's check what are located in São Paulo.
Helper function : exploreKG["São_Paulo"]=['~location']
[User]
Execution result :
['São_Paulo', '~location', '2009_Santos_FC_season'], ['São_Paulo', '~location', 'Vanguarda_Agro']
[Your Task]
Statement : It is not clear that Samsung is located in São Paulo. Let's check if "São_Paulo" is located in 'Korea' or 'Seoul'.I have to find the related location of "São_Paulo".
Helper function : exploreKG["São_Paulo"]=['~capital', '~locationTown', '~location']
[User]
Execution result : ['São_Paulo', '~capital', 'São_Paulo_Province'], ['São_Paulo', '~locationTown', 'Ibirapuera_Auditorium], ['São_Paulo', '~location', '1972_São_Paulo_FC_season'], ['São_Paulo', '~location', '2013–14_in_Swiss_football']
[Your Task]
Statement : Since we cannot verify "São_Paulo" is located in 'Korea' or 'Seoul' by execution result, given claim is False.
Helper function : Verifiation[]



Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>

"""

pr_2 = """ 
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use below helper functions to find the evidence for finding labels.

Helper Functions
1.getRelation[entity]: Returns the list of relations linked to the entity. You can choose several relations from the list that seem related to the claim.
2.exploreKG[entity]=[relation_1,relation_2, ... relation_K]: Returns the triple set around the entity. For example, [entity, relation_1, tail entity] etc. You can choose relation from [User]'s execution result.
3.Verification[]: After getting enough evidence after exploreKG() helper function and if verification can be done, call this function. If [User] requires more information, you need to collect more triples in following steps.

You must follow the exact format of the given helper function.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for [User] response. If response has made, continue your [Your Task] (Do not make multiple 'Helper function: ' lines).
Importantly, you have to use inverse relation if you need. For example, if you want to find films starred by certain actors (when only actors were given), you have to use '~starred_actors' relation such as exploreKG['actor']=['~starred_actors'].
Importantly, Do not change the format of the entity or relation including '~'.

Here are some examples.

Example 1)
Claim: Yea he was born in Zaoyang, Hubei
Given entity: ["Zaoyang", "Hubei"]

[Your Task]
Statement : First, I need to look around the given entities. I will start by getting the relation list linked to Zaoyang.
Helper function : getRelation["Zaoyang"]
[User]
Execution result :
Relations_list["Zaoyang"] = ['augRecordLowC', 'decLowC', 'aprRecordHighC', 'yearLowC', 'junMeanC', 'unitPrecipitationDays', 'novLowC', 'longm', 'julRecordLowC', 'areaTotal', '~place', 'decHighC', 'mayLowC', 'febMeanC', 'julMeanC', 'marMeanC', 'precipitationColour', 'junHighC', 'novPrecipitationDays', 'marRecordLowC', 'febRecordLowC', 'sepRecordLowC', 't', 'octRecordHighC', 'octPrecipitationMm', 'aprLowC', 'junPrecipitationMm', 'singleLine', 'yearHighC', 'aprPrecipitationDays', 'yearPrecipitationMm', 'subdivisionType', 'mayPrecipitationMm', 'mayHighC', 'populationDensityKm', 'augLowC', 'janPrecipitationDays', '~location', 'julRecordHighC', 'janMeanC', 'source', 'marRecordHighC', 'yearMeanC', 'rdf-schema#label', 'timeZone', 'settlementType', 'populationAsOf', 'unitPref', 'sepHighC', 'timezone', 'isPartOf', 'location', 'octMeanC', 'latns', 'febLowC', '~text', 'febPrecipitationDays', '~isPartOf', 'augMeanC', 'junLowC', 'sepPrecipitationDays', 'mayRecordHighC', '22-rdf-syntax-ns#type', 'sepMeanC', 'latm', '~subdivisionName', 'coordinatesRegion', 'febPrecipitationMm', 'PopulatedPlace/areaTotal', 'marPrecipitationMm', 'janLowC', 'febRecordHighC', 'decPrecipitationDays', 'julPrecipitationDays', 'aprMeanC', 'longd', 'mayMeanC', 'aprHighC', 'novRecordLowC', 'utcOffset', 'octPrecipitationDays', 'augRecordHighC', 'sepPrecipitationMm', 'decPrecipitationMm', 'populationTotal', 'hypernym', 'decMeanC', 'novMeanC', '~birthPlace', 'febHighC', 'subject', 'latd', 'sepLowC', 'novHighC', 'novRecordHighC', 'janRecordLowC', '~placeOfBirth', 'pushpinMap', 'augPrecipitationDays', '~wikiPageRedirects', 'julLowC', 'mayRecordLowC', 's', 'julHighC', 'pushpinMapCaption', 'longew', 'marHighC', 'junPrecipitationDays', 'sepRecordHighC', 'type', 'octHighC', 'janPrecipitationMm', 'mayPrecipitationDays', 'marPrecipitationDays', 'octLowC', 'augHighC', 'marLowC', 'subdivisionName', 'julPrecipitationMm', 'octRecordLowC', 'janRecordHighC', 'junRecordLowC', 'decRecordLowC', 'p', 'junRecordHighC', 'janHighC', 'pushpinLabelPosition', 'novPrecipitationMm', 'metricFirst', 'coordinatesDisplay', 'decRecordHighC', 'aprPrecipitationMm', 'areaTotalKm', 'augPrecipitationMm', 'aprRecordLowC', '~location']
[Your Task]
Statement : Now, I need to look around the given entities. I will get the relation list linked to Hubei.
Helper function : getRelation["Hubei"]
[User]
Execution result :
Relations_list["Hubei"] = ['popyear', '~placeOfDeath', 'south', '~territory', 'owl#differentFrom', '~routeStart', '~locale', '~capital', '~place', 'nationalities', 'prefectures', 'gdprank', '~spokenIn', '~core#subject', '~title', 'tl', 't', '~cityServed', 'psp', 'southwest', 'hdi', 'width', 'gdpyear', 'isoabbrev', 'largestcity', 'y', '~location', 'capital', '~southeast', '~origins', 'northeast', 'hdirank', 'latitude', 'rdf-schema#label', 'name', '~northwest', 'townships', '~north', 'latns', 'governor', '~headquarter', 'rdf-schema#seeAlso', '~ground', '~isPartOf', 'value', '~terminusA', 'gdp', 'gdppercapitarank', 'arearank', '~name', 'pop', '~stadium', 'southeast', '~headquarters', '22-rdf-syntax-ns#type', 'color', 'l', '~subdivisionName', 'dialects', 'align', 'popdensityKm', 'longitude', '~deathPlace', 'secretary', 'administrationtype', 'pinyin', 'longd', 'popdensityrank', 'areaKm', '~ancestry', 'englishname', 'map', 'hypernym', '~locatedInArea', 'mapsize', 'gdppercapita', 'abbrevpinyin', '~garrison', '~residence', '~assembly', '~winnerOrigin', '~birthPlace', 'poprank', 'subject', '~city', '~areasAffected', '~south', 'latd', '~mouthRegion', '~owl#differentFrom', 'poj', '~rdf-schema#seeAlso', '~placeOfBirth', 'label', '~wikiPageRedirects', 'direction', '~office', 's', 'caption', '~state', 'image', 'centre', '~southwest', 'c', 'longew', 'w', '~locationCity', '~region', 'hdiyear', 'north', '~province', 'chinesename', 'j', 'northwest', 'counties', '~hometown', 'labels', 'originofname', 'p', '~routeJunction', 'hdicat', 'website', '~t', '~prov', '~place', '~pop', '~pushpinMap', '~centre', '~residence', '~rdf-schema#label', '~namerom', '~deathPlace', '~name', '~placeOfBirth', '~province', '~region']
[Your Task]
Statement : To verify the claim, I need to explore the graph for Zaoyang to find any relation with '~birthPlace' or '~placeOfBirth'.
Helper function : exploreKG["Zaoyang"]=['~birthPlace', '~placeOfBirth']
[User]
Execution result :
['Zaoyang', '~birthPlace', 'Nie_Haisheng'], ['Zaoyang', '~placeOfBirth', 'Nie_Haisheng']
[Your Task]
Statement : According to the triples, Nie Haisheng was born in Zaoyang. However, the claim does not specify who "he" refers to. To verify the claim, I need to check if Zaoyang is part of Hubei. I will explore the graph for Zaoyang to find any relation with '~isPartOf'.
Helper function : exploreKG["Zaoyang"]=['~isPartOf']
[User]
Execution result :
['Zaoyang', '~isPartOf', 'Xiangyang'], ['Zaoyang', '~isPartOf', 'Hubei']
Statement : According to the triples, Zaoyang is part of Hubei. Therefore, the claim that "he was born in Zaoyang, Hubei" is consistent with the information provided. The claim is True.
Helper function : Verification[]

Example 2)
Claim: An airport, which is operated by the Aktieselskab organisation, has a runway that's 2,776 long and is named 10L/28R.
Given entity: ["Aktieselskab", "\"2776.73\"", "\"10L/28R\""]

[Your Task]
Statement : First, I need to find the relations linked to the entity 'Aktieselskab'.
Helper function : getRelation['Aktieselskab']
[User]
Execution result :
Relations_list["Aktieselskab"] = ['rdf-schema#label', '~wikiPageRedirects', '~type', '~wikiPageDisambiguates', 'subject', '~operator', '~operatingOrganisation', 'hypernym']
[Your Task]
Statement : To find the airport operated by the Aktieselskab organisation, I need to explore the graph with 'Aktieselskab' related to '~operator' and '~operatingOrganisation'.
Helper function : exploreKG['Aktieselskab']=['~operator', '~operatingOrganisation']
[User]
Execution result :
['Aktieselskab', '~operatingOrganisation', 'Aarhus_Airport']
[Your Task]
Statement : Now, I need to find the relations linked to 'Aarhus_Airport' to check the runway information.
Helper function : getRelation['Aarhus_Airport']
[User]
Execution result :
Relations_list["Aarhus_Airport"] = ['iata', 'imageWidth', '~wikiPageRedirects', 'longd', 'lats', 'runwaySurface', '~wikiPageDisambiguates', 'pushpinMapCaption', 'longm', 'longew', 'type', 'rdf-schema#label', 'iataLocationIdentifier', 'footnotes', 'r2LengthM', 'name', 'r2Number', 'pushpinLabel', 'location', 'elevation', 'runwayName', 'r1Surface', 'r1LengthF', 'hypernym', 'latns', 'elevationF', 'r1Number', 'icao', 'operator', 'longs', 'runwayDesignation', 'cityServed', 'runwayLength', 'r2Surface', 'stat1Data', 'r2LengthF', 'city', 'elevationM', 'subject', 'homepage', 'elevationAboveTheSeaLevel', '22-rdf-syntax-ns#type', 'metricRwy', 'latd', 'latm', 'pushpinLabelPosition', 'operatingOrganisation', 'coordinatesRegion', 'statYear', 'r1LengthM', 'pushpinMap', 'website', 'icaoLocationIdentifier', 'stat1Header']
[Your Task]
Statement : To verify the runway information, I need to explore the graph for 'Aarhus_Airport' related to 'r1Number', 'r1LengthM', and 'r2Number', 'r2LengthM'.
Helper function : exploreKG['Aarhus_Airport']=['r1Number', 'r1LengthM', 'r2Number', 'r2LengthM']
[User]
Execution result :
['Aarhus_Airport', 'r1Number', '"10"'], ['Aarhus_Airport', 'r1LengthM', '"2777"'], ['Aarhus_Airport', 'r2Number', '"10"'], ['Aarhus_Airport', 'r2LengthM', '"2702"']
[Your Task]
Statement : The runway length of 'Aarhus_Airport' is 2777 meters, which is close to the given length of 2776.73, but the runway name '10L/28R' does not match the available runway numbers '10'. Therefore, the claim is False.
Helper function : Verification[]
[User]
Execution result :
We need more information for verification. Try to look relation 'runwaySurface, runwayName' of Aarhus_Airport and the relation 'hypernym' of Aktieselskab.
[Your Task]
Statement : To gather more information, I will explore the graph for 'Aarhus_Airport' related to 'runwaySurface' and 'runwayName'.
Helper function : exploreKG['Aarhus_Airport']=['runwaySurface', 'runwayName']
[User]
Execution result :
['Aarhus_Airport', 'runwayName', '"10L/28R"'], ['Aarhus_Airport', 'runwayName', '"10R/28L"']
[Your Task]
Statement : The exploration shows that 'Aktieselskab' is indeed the operating organisation for 'Aarhus_Airport'. Given that 'Aarhus_Airport' has a runway named '10L/28R' and a length close to 2776.73 meters, the claim is True.
Helper function : Verification[]


Example 3)
Claim: Alan Frew is a solo singer born in Shahabad, Hardoi.
Given entity: ["\"solo_singer\"", "Alan_Frew", "Shahabad,_Hardoi"]

[Your Task]
Statement : First, I need to gather information about Alan Frew.
Helper function : getRelation["Alan_Frew"]
[User]
Execution result :
Relations_list["Alan_Frew"] = ['label', 'caption', 'birthPlace', 'associatedActs', '~bandMember', 'birthDate', 'associatedBand', 'rdf-schema#label', 'associatedMusicalArtist', 'birthYear', 'yearsActive', 'surname', 'name', '~writer', 'instrument', 'dateOfBirth', 'hypernym', 'recordLabel', 'activeYearsStartYear', 'background', 'hometown', 'description', '~currentMembers', 'subject', 'homepage', 'genre', '22-rdf-syntax-ns#type', 'origin', 'placeOfBirth', 'occupation', 'shortDescription', 'website', 'givenName']
[Your Task]
Statement : To verify if Alan Frew is a solo singer and his birthplace, I need to explore the graph for Alan Frew related to 'birthPlace' and 'occupation'.
Helper function : exploreKG["Alan_Frew"]=['birthPlace', 'occupation']
[User]
Execution result :
['Alan_Frew', 'birthPlace', 'Coatbridge'], ['Alan_Frew', 'birthPlace', '"Coatbridge, Scotland, Great Britain, United Kingdom"'], ['Alan_Frew', 'birthPlace', 'United_Kingdom'], ['Alan_Frew', 'birthPlace', 'Scotland'], ['Alan_Frew', 'occupation', 'Public_speaking'], ['Alan_Frew', 'occupation', '"Singer, Musician, Author and Public Speaker"'], ['Alan_Frew', 'occupation', 'Musician']
[Your Task]
Statement : According to the triples, Alan Frew's birthplace is Coatbridge, Scotland, Great Britain, United Kingdom, and his occupations include Singer, Musician, Author, and Public Speaker. Now, I need to gather information about Shahabad, Hardoi to verify the claim.
Helper function : getRelation["Shahabad,_Hardoi"]
[User]
Execution result :
Relations_list["Shahabad,_Hardoi"] = ['~wikiPageRedirects', 'otherName', 'country', 'caption', 'longd', '~wikiPageDisambiguates', 'populationFemale', 'demographics1Title', 'pushpinMapCaption', 'title', 'float', 'utcOffset', 'longew', 'areaRank', 'demographicsType', 'rdf-schema#label', 'timeZone', 'settlementType', 'populationAsOf', 'synonym', 'unitPref', 'name', 'postalCode', 'timezone', 'isPartOf', 'populationTotal', 'elevation', 'titlebar', 'hypernym', 'latns', 'nativeName', 'subdivisionName', 'founder', 'left', 'postalCodeType', '~birthPlace', 'namedFor', 'elevationM', 'subject', 'homepage', 'demographics1Info', '22-rdf-syntax-ns#type', 'latd', 'subdivisionType', 'pushpinLabelPosition', 'right', 'registrationPlate', 'coordinatesDisplay', 'pushpinMap', 'website', 'populationDensityKm', 'populationMale']
[Your Task]
Statement : Since the previous exploration did not yield relevant information, I will explore the graph for Shahabad, Hardoi related to 'subdivisionName' to verify its location.
Helper function : exploreKG["Shahabad,_Hardoi"]=['subdivisionName']
[User]
Execution result :
['Shahabad,_Hardoi', 'subdivisionName', 'Uttar_Pradesh'], ['Shahabad,_Hardoi', 'subdivisionName', 'Hardoi_district']
[Your Task]
Statement : According to the triples, Shahabad, Hardoi is part of Uttar Pradesh and Hardoi district in India. Since Alan Frew's birthplace is Coatbridge, Scotland, Great Britain, United Kingdom, and not Shahabad, Hardoi, the claim is False.
Helper function : verification[]

Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>
"""

pr_3 = """ 
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use below helper functions to find the evidence for finding labels.

Helper Functions
1.getRelation[entity]: Returns the list of relations linked to the entity. You can choose several relations from the list that seem related to the claim.
2.exploreKG[entity]=[relation_1,relation_2, ... relation_K]: Returns the triple set around the entity. For example, [entity, relation_1, tail entity] etc. You can choose relation from [User]'s execution result.
3.Verification[]: After getting enough evidence after exploreKG() helper function and if verification can be done, call this function. If [User] requires more information, you need to collect more triples in following steps.

You must follow the exact format of the given helper function.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for [User] response. If response has made, continue your [Your Task] (Do not make multiple 'Helper function: ' lines).
Importantly, you have to use inverse relation if you need. For example, if you want to find films starred by certain actors (when only actors were given), you have to use '~starred_actors' relation such as exploreKG['actor']=['~starred_actors'].
Importantly, Do not change the format of the entity or relation including '~'.

Here are some examples.

Example 1)
Claim: Question :He also had a successor, Hans von Raumer!
Given entity : ["Hans_von_Raumer"]
[Your Task]
Statement : First, I need to find the relations linked to Hans_von_Raumer to gather more information about his role or position.
Helper function : getRelation["Hans_von_Raumer"]
[User]
Execution result :
Relations_list["Hans_von_Raumer"] = ['office', 'birthPlace', 'party', 'birthDate', 'rdf-schema#label', 'name', 'deathPlace', 'predecessor', 'profession', 'hypernym', 'deathDate', 'chancellor', 'termStart', 'successor', 'termEnd', 'subject', 'termPeriod', '22-rdf-syntax-ns#type', 'president']
[Your Task]
Statement : To verify the claim, I need to explore the graph to find out who Hans von Raumer succeeded. I will look into the 'successor' relation.
Helper function : exploreKG["Hans_von_Raumer"]=['successor']
[User]
Execution result :
['Hans_von_Raumer', 'successor', 'Gustav_Bauer'], ['Hans_von_Raumer', 'successor', 'Joseph_Koeth']
Statement : According to the triples, Hans von Raumer had successors named Gustav Bauer and Joseph Koeth. This supports the claim that he had a successor. Therefore, the claim is True.
Helper function : Verification[]


Example 2)
Claim:Yes, Billy Fitzpatrick used to have a nickname.
Given entity : ["Billy_Fitzpatrick"]
[Your Task]
Statement : First, I need to find the relations linked to Billy_Fitzpatrick to gather information about any nickname.
Helper function : getRelation["Billy_Fitzpatrick"]
[User]
Execution result :
Relations_list["Billy_Fitzpatrick"] = ['activeYearsEndYear', 'clprovince', 'after', 'province', 'birthPlace', 'title', '~goals', 'code', 'icposition', 'nickname', 'club', 'birthDate', 'clyears', 'rdf-schema#label', 'irish', 'before', 'fullname', 'birthYear', 'county', 'surname', 'name', 'icprovince', 'icyears', 'team', 'feet', 'sport', 'dateOfBirth', 'hypernym', 'icallireland', 'nick', 'activeYearsStartYear', 'counties', 'clcounty', 'inches', 'description', 'subject', '22-rdf-syntax-ns#type', '~after', 'placeOfBirth', 'allstars', 'occupation', '~before', 'shortDescription', '~captain', 'years', 'icapps(points)_', 'givenName', 'clallireland']
[Your Task]
Statement : To verify if Billy Fitzpatrick used to have a nickname, I need to explore the graph for the 'nickname' relation.
Helper function : exploreKG["Billy_Fitzpatrick"]=['nickname']
[User]
Execution result :
['Billy_Fitzpatrick', 'nickname', '"Fitz"']
[Your Task]
Statement : According to the triple, Billy Fitzpatrick had the nickname "Fitz". Therefore, the claim is True.
Helper function : Verification[]


Example 3)
Claim : The Greater Britain Movement leader was John Tyndall
Given entity : ["Greater_Britain_Movement", "John_Tyndall_(politician)"]
[Your Task]
Statement : First, I need to explore the relations linked to the Greater Britain Movement.
Helper function : getRelation['Greater_Britain_Movement']
[User]
Execution result :
Relations_list["Greater_Britain_Movement"] = ['~party', 'studentWing', 'dissolved', 'newspaper', '~wikiPageDisambiguates', 'founded', 'rdf-schema#label', 'ideology', 'name', 'headquarters', 'predecessor', 'leader', 'successor', 'founder', 'formationYear', 'subject', 'headquarter', '22-rdf-syntax-ns#type', 'extinctionYear']
[Your Task]
Statement : To verify the claim, I need to explore the graph for the Greater Britain Movement related to the 'leader'.
Helper function : exploreKG['Greater_Britain_Movement']=['leader']
[User]
Execution result :
['Greater_Britain_Movement', 'leader', 'John_Tyndall_(politician)']
[Your Task]
Statement : According to the triple, the leader of the Greater Britain Movement was John Tyndall. Therefore, the claim is True.
Helper function : Verification[]

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
Claim : The airport in Punjab, Pakistan is operated by the government agency of the Jinnah International Airport.
[ChatGPT]
1. The government agency responsible for Jinnah International Airport oversees operations at an airport located in Punjab, Pakistan.
2. An airport in Punjab, Pakistan is managed by the same governmental body that operates Jinnah International Airport.
3. The operations of an airport in Punjab, Pakistan are handled by the government agency managing Jinnah International Airport.


<Example 2>
[User]
Claim : Tim Brooke-Taylor starred as a fictional character, which was first aired on 10/03/1983 and was broadcast by STV.
[ChatGPT]
1. Tim Brooke-Taylor portrayed a fictional character in a show that premiered on October 3, 1983, and was aired by STV.
2. STV broadcasted a program featuring Tim Brooke-Taylor as a fictional character, first aired on October 3, 1983.
3. On October 3, 1983, STV premiered a show in which Tim Brooke-Taylor starred as a fictional character.


<Example 3>
[User]
Claim : Who were Governor of Idaho after Nazi Germany?
[ChatGPT]
1. Who served as Governor of Idaho in the period following the fall of Nazi Germany?
2. Which individual held the governorship of Idaho after the end of Nazi Germany?
3. After the demise of Nazi Germany, who assumed the role of Governor of Idaho?


<Example 4>
[User]
Claim :Samsung is located in São Paulo.
[ChatGPT]
1. Samsung has a location in São Paulo.
2. The São Paulo branch of Samsung is situated in the city.
3. Samsung operates from a site based in São Paulo.

<Example 5>
[User]
Claim : An airport, which is operated by the Aktieselskab organisation, has a runway that's 2,776 long and is named 10L/28R.
[ChatGPT]
1. The Aktieselskab organisation manages an airport with a runway named 10L/28R that measures 2,776 meters in length.
2. An airport operated by Aktieselskab features a 2,776-meter runway identified as 10L/28R.
3. A runway named 10L/28R, stretching 2,776 meters, is located at an airport managed by the Aktieselskab organisation.


<Example 6>
[User]
Claim : Alan Frew is a solo singer born in Shahabad, Hardoi.
[ChatGPT]
1. Alan Frew, a solo artist, was born in Shahabad, located in the Hardoi district.
2. Shahabad in Hardoi is the birthplace of Alan Frew, who is known as a solo singer.
3. The solo singer Alan Frew hails from Shahabad, Hardoi.

<Example 7>
[User]
Claim : Who preceded David I of Scotland as monarch of Scotland?
[ChatGPT]
1. Who held the throne of Scotland before David I ascended as monarch?
2. Which monarch ruled Scotland prior to David I?
3. Before David I became Scotland's monarch, who occupied the position?

<Example 8>
[User]
Claim : 110 Lydia has an apoapsis of 440756000.0 kilometres and travels at an average speed of 20.78 kmps.
[ChatGPT]
1. The asteroid 110 Lydia reaches an apoapsis of 440,756,000.0 kilometers and moves at an average velocity of 20.78 kilometers per second.
2. With an apoapsis of 440,756,000.0 kilometers, 110 Lydia travels at an average speed of 20.78 kmps.
3. 110 Lydia, an asteroid, maintains an average speed of 20.78 kmps and achieves an apoapsis distance of 440,756,000.0 kilometers.

Now, it's your turn. Continue your paraphrasing task. Response must have same form with upper examples.
[User]
Claim : <<<<CLAIM>>>>
"""