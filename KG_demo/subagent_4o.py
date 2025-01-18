import openai
from openai import OpenAI


openai.api_key = "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"
client = OpenAI(api_key=openai.api_key)


sub_agent_2option_beta = """
You are the evaluator. I will show you a claim and a triple set extracted from a graph. 
Based on the given triple set and relation list of each entity, determine whether the claim is True or False. 
If given triple sets are lack of information to verify the claim, give the the combination of entity and relation you need. You can refer the given relations list and choosed what relation information is more needed.
The triple set takes the form [Head, Relation, Tail], which means 'Head's Relation is Tail.' 
If the relation starts with '~', it indicates a reverse relation, meaning 'Tail's relation is head.' 
The following cases may arise: Choose one option from 'Executable (True or False)' or 'Not executable(Insufficient evidence)'.
If you choose 'Not executable(Insufficient evidence)', You must specify in the statement which additional relation information is needed for a particular entity. However, the relation can only be selected from the given Relation_list and cannot be created arbitrarily.
Refer to the explanations of the two options below to answer the Statement and Evaluation.

<Cases> 
1. If the triple sets are sufficient to determine the True/False of the claim --> Executable (True or False)
2. If the triple set is insufficient or ambiguos to determine the True/False of the claim --> Not executable (Insufficient evidence) 

<Example 1>
[User]
Claim : A fictional character, which was created by Joe Quesada, is broadcast on Lebanese Broadcasting Corporation and starred Tim Brooke-Taylor. 
Triple sets : [['Joe_Quesaa', '~creator', 'Azrael_(comics)'], ['Joe_Quesaa', '~creator', 'Menace_(Marvel_Comics)'], ['Joe_Quesaa', '~creator', 'Thomas_Logan'], ['Joe_Quesaa', '~creator', 'Carlie_Cooper']]
Relations of Entity : 
Relations_list["Tim_Brooke-Taylor"] = ['birthPlace', 'honorificSuffix', '~after', 'notableWork', 'genre', 'years', 'spouse', 'title', 'givenName', 'shortDescription', 'surname', '~author', 'birthName', '~writer', '~creator', 'placeOfBirth', '~caption', 'active', 'hypernym', '~starring', '~voices', 'birthYear', 'dateOfBirth', 'rdf-schema#label', 'subject', 'birthDate', '22-rdf-syntax-ns#type', '~wikiPageRedirects', 'nationality', 'imdbId', 'description', '~before', '~voice', 'name']
Relations_list["Joe_Quesada"] = ['influences', 'birthPlace', '~after', '~keyPeople', '~artists', 'write', 'years', 'title', '~executiveProducer', 'givenName', '~wikiPageDisambiguates', 'shortDescription', 'surname', 'birthName', '~writer', '~creator', 'placeOfBirth', '~writers', '~pencillers', 'type', '~keypeople', 'hypernym', '~foundedBy', 'birthYear', 'edit', 'caption', 'dateOfBirth', '~creators', 'rdf-schema#label', 'birthDate', 'subject', '~keyPerson', '22-rdf-syntax-ns#type', '~wikiPageRedirects', 'nationality', 'pencil', 'subcat', 'after', 'description', '~aux', '~before', 'before', '~editors', 'awards', 'id', 'name']
Relations_list["Lebanese_Broadcasting_Corporation"] = ['networkLogo', 'broadcastArea', 'homepage', 'networkName', '~owningCompany', 'country', '~wikiPageDisambiguates', 'networkType', '~channel', '~network', '~employer', 'launchDate', 'slogan', '~distributor', 'owner', 'hypernym', '~tv', 'locationCountry', 'firstAirDate', 'rdf-schema#label', 'subject', '22-rdf-syntax-ns#type', '~sisterNames', '~wikiPageRedirects', 'owningCompany', 'logocaption', 'available', '~sisterStation']
[ChatGPT]
Statement : We need more information for verification. Try to look relation '~starring' linked with Tim_Brooke-Taylor and relation 'broadcastArea, ~channel,~tv' linked with Lebanese_Broadcasting_Corporation.
Evaluation : Not executable (Insufficient evidence)


<Example 2>
[User]
Claim : Allama Iqbal International airport is located in Pakistan, the leader of the country is Gil Snider.
Triple sets : [['Allama_Iqbal_International_Airport', 'location', 'Punjab,_Pakistan'], ['Allama_Iqbal_International_Airport', 'location', 'Pakistan'], ['Allama_Iqbal_International_Airport', 'location', '"Punjab, Pakistan"'], ['Pakistan', 'leader', 'Anwar_Zaheer_Jamali'], ['Pakistan', 'leader', 'Mamnoon_Hussain'], ['Pakistan', 'leader', 'Nawaz_Sharif'], ['Pakistan', 'leader', 'Sardar_Ayaz_Sadiq'], ['"Gil Snider"', '~leaderName', 'Conroe,_Texas']]
Relations of Entity :
Relations_list["Allama_Iqbal_International_Airport"] = ['city', '~wikiPageRedirects', 'r2Surface', 'icaoLocationIdentifier', 'stat2Header', 'homepage', 'pushpinMapCaption', 'stat3Header', 'hub', '~hubAirport', 'longs', '~secondaryHubs', 'runwayDesignation', '~rdf-schema#seeAlso', 'runwayLength', 'longd', 'pushpinLabel', 'operatingOrganisation', 'stat2Data', 'r1LengthM', 'image2Width', 'r2LengthF', 'footnotes', 'coordinatesRegion', 'rdf-schema#label', '~targetAirport', 'subject', '22-rdf-syntax-ns#type', 'website', 'elevation', 'r2LengthM', 'elevationF', 'r1Number', 'pushpinMapsize', 'longm', 'latns', 'icao', 'imageMapCaption', 'image', 'imageMap', 'longew', 'lats', 'cityServed', 'stat3Data', 'r1LengthF', '~wikiPageDisambiguates', 'latd', 'operator', 'hypernym', 'name', 'runwaySurface', 'latm', 'pushpinMap', 'r1Surface', '~core#subject', 'type', 'pushpinLabelPosition', 'location', 'iata', 'imageWidth', 'stat1Data', 'runwayName', 'iataLocationIdentifier', 'imageMapsize', 'r2Number', '~focusCities', 'statYear', 'stat1Header', 'elevationM']
Relations_list["Pakistan"] = ['flag', '~body', '~allegiance', '~broadcastArea', '~coach', 'longName', '~origins', '~basedAt', '~availability', '~fightingOutOf', '~markets', '~available', '~parent', '~influenced', '~locatedInArea', '~placeOfArrest', '~foundation', '~mouthCountry', '~terminusB', '~awardedBy', '~basinCountries', '~education', '~restingplace', '~sourceCountry', 'gdpPppRank', 'governmentType', 'caption', 'language', 'latns', 'longm', '~usingCountry', '~cityOrRegion', '~owner', '~hometown', '~stateParty', '~nearestCity', '~knownFor', 'latd', 'name', '~armiger', '~ethnicity', 'symbolType', '~team2Name', '~team', '~withdraws', '~observedby', '~subdivisionType', '~homeTown', '~placeOfDeath', '~hqLocation', 'title', '~populationPlace', '~presenter', '~residencePlace', 'float', 'demonym', 'nationalAnthem', '~governmentName', '~wikiPageRedirects', '~label', '~occupation', '~bankOf', '~publisher', '~address', 'rdf-schema#seeAlso', '~presentlyLivingIn', '~locationMap', 'religion', '~foundedPlace', '~birthDate', 'populationDensitySqMi', 'cctld', 'largestCity', 'areaRank', 'percentWater', '~commandStructure', '~distribution', 'gdpNominalYear', '~runnersUp', 'officialLanguage', 'voy', 'gdpNominalPerCapita', 'hdiChange', '~spokenIn', 'capital', '22-rdf-syntax-ns#type', 'text', '~country', 'languagesType', '~lived', '~manufacturer', '~site', '~returns', '~stadium', '~rd2t2Loc', '~cableServ', 'd', 'legislature', 'image', '~isPartOf', '~placeOfBirth', 'establishedDate', '~locationSigned', '~recordLabel', '~debuts', 'mapCaption', '~mouthMountain', '~hypernym', '~cityServed', '~notableWork', 'lowerHouse', 'latm', 'establishedEvent', '~rd0t1Loc', '~nationality', 'currencyCode', 'align', '~literaryGenre', '~countryOfOrigin', '~opponents', 'footnoteA', '~areas', '~seat', '~nonFictionSubject', 'areaTotal', '~firstAired', 'hdi', '~office', '~rd3t1Loc', '~host', 'mapWidth', '~countriesAffected', '~international', '~shipCountry', '~overviewbody', '~commands', 'hdiRank', 'utcOffsetDst', '~subdivisionName', '~headquarters', '~worldHeadquarters', 'imageFlag', '~designation1Free1value', 'gdpNominalPerCapitaRank', '~county', '~blankNameSec', '~data', '~foundationPlace', '~area', '~2rpt1Loc', 'populationEstimateRank', '~award', '~subject', '~legaljuris', 'sovereigntyType', '~citizenship', '~rd1t4Loc', 'longd', 'footnoteB', '~countries', 'currency', '~rd2t1Loc', '~campus', '~headOffice', '~ground', '~commander', '~nationalOrigin', '~locationCountry', '~deathPlace', '~owl#differentFrom', '~billed', '~nation', 'subject', '~founded', 'rdf-schema#label', '~mausoleum', '~firstRun', '~mouthPlace', 'PopulatedPlace/populationDensity', '~almaMater', '~placeOfBurial', '~venue', 'sovereigntyNote', '~origin', '~stateOfOrigin', 'areaSqMi', '~territory', 'imageCoat', '~affected', '~musicOrigin', '~wikiPageDisambiguates', '~sportCountry', '~nationalTeam', 'officialLanguages', 'gdpPppPerCapitaRank', 'gdpPppPerCapita', '~rd1t1Loc', '~originalSignatories', '~city', 'percentageOfAreaWater', 'leaderTitle', '~borders', '~aux', '~assembly', 'gdpNominalRank', '~governmentType', '~culturalOrigins', 'gdpPpp', 'leader', 'populationDensityRank', '~routeStart', 'populationEstimateYear', '~perps', '~nationalteam', '~caption', '~routeEnd', '~countryWithFirstSatellite', '~satServ', '~residence', '~language', '~type', 'right', 'PopulatedPlace/areaTotal', '~state', '~today', '~states', '~rd1t2Loc', '~regionServed', '~arrestPlace', '~burialPlace', '~countryOrigin', 'gdpPppYear', '~rdf-schema#seeAlso', '~religion', '~locale', '~combatant', '~location', '~locationCity', 'populationDensity', '~recordedIn', '~restingPlace', '~notableIdea', 'languages', 'foundingDate', '~workInstitution', '~finish', 'conventionalLongName', '~moreUsers', '~mainInterest', '~testSite', 'callingCode', '~headquarter', '~place', 'timeZone', '~hqLocationCountry', 'gdpNominal', '~jurisdiction', 'width', '~countryName', 'left', '~producers', '~locmapin', '~garrison', 'longew', 'upperHouse', 'commonName', '~channel', 'imageMap', '~regions', 'hdiYear', '~birthPlace', '~popplace', '~presentlyLiving', 'leaderName', '~hostCity', 'populationDensityKm', '~areasAffected', 'hypernym', '~affiliation', 'populationEstimate', 'gini', '~stopover', 'author', '~nota', '~core#subject', '~rd1t3Loc', '~club', '~region', '~workplaces', 'utcOffset', 'drivesOn', 'areaKm', 'populationTotal', 'giniYear', '~areaServed', 'titlebar', '~usedBy', '~second', '~rdf-schema#label', '~body', '~party', '~allegiance', '~broadcastArea', '~origins', '~casualties', '~west', '~odidebutfor', '~winningTeam', '~flagName', '~placeOfArrest', '~onlytestaway', '~rcmNat', '~basinCountries', '~teamName', '~northwest', '~service', '~nat', '~owner', '~lastt20ihome', '~stateParty', '~largestvictory', '~keypoints', '~lasttesthome', '~team1Name', '~causalties', '~odidebutagainst', '~stateSenate', '~team2Name', '~team', '~lastodihome', '~observedby', '~subdivisionType', '~placeOfDeath', '~firsttestaway', '~locations', '~gauge', '~t20idebutagainst', '~label', '~t20idebutfor', '~address', '~locationMap', '~foundedPlace', '~rcbNat', '~relegated', '~participants', '~rd3Team', '~runnersUp', '~linesman1association', '~country', '~lasttestfor', '~onlyodihome', '~placeOfBirth', '~strength', '~firstt20iaway', '~lastodiaway', '~battingSecond', '~shipRegistry', '~rd1Team', '~observances', '~nationality', '~opponents', '~promteam', '~testdebutagainst', '~office', '~host', '~countriesAffected', '~debutagainst', '~southwest', '~shipCountry', '~battingFirst', '~title', '~subdivisionName', '~headquarters', '~designation1Free1value', '~lastodifor', '~county', '~it20debutagainst', '~countryflag', '~data', '~area', '~firsttesthome', '~mapType', '~citizenship', '~firstodihome', '~ambassadorFrom', '~mostWins', '~runnerUp', '~third', '~commander', '~locationCountry', '~deathPlace', '~locationHeader', '~teamsInvolved', '~rd2Team', '~lasttestaway', '~champions', '~firstRun', '~firstt20ihome', '~mapCaption', '~s', '~origin', '~north', '~motmCountry', '~relteam', '~pushpinMap', '~rd4Team', '~allies', '~flag', '~testdebutfor', '~t20debutagainst', '~lastt20iaway', '~governmentType', '~assembly', '~placeOfRelease', '~nationalteam', '~map', '~residence', '~parties', '~plannedBy', '~state', '~countryLink', '~states', '~regionServed', '~arrestPlace', '~pushpinMapCaption', "~men'sMostRecentChampion(s)_", '~combatant', '~location', '~thirdPlace', '~divname', '~place', '~jurisdiction', '~voy', '~locmapin', '~firstodiaway', '~champion', '~lastt20iagainst', '~birthPlace', '~popplace', '~lasttestagainst', '~areasAffected', '~lastodiagainst', '~employer', '~twin7Country', '~umpire1Country', '~name', '~club', '~region', '~commonName', '~detainedAt', '~south', '~areaServed', '~usedBy', '~clubnat']
Relations_list["Gil Snider"] = ['~leaderName']
[ChatGPT]
Statement : The 'Allama Iqbal International Airport' is located in 'Punjab, Pakistan', which confirms the first part of the claim. However, the leaders of Pakistan are 'Anwar Zaheer Jamali', 'Mamnoon Hussain', and 'Nawaz Sharif', among others, but 'Gil Snider' is not listed as a leader of Pakistan. Therefore, the second part of the claim is not supported.
Evaluation : Executable (False)


<Example 3>
[User]
Claim : Michele Marcolini played for Tokat Plevne Belediyesi and manages A.C. Lumezzane.
Triple sets : [['Michele_Marcolini', 'managerclubs', 'Real_Vicenza_V.S.'], ['Michele_Marcolini', 'managerclubs', 'A.C._Lumezzane'], ['Michele_Marcolini', 'currentclub', 'Real_Vicenza_V.S.'], ['A.C._Lumezzane', 'manager', 'Michele_Marcolini'], ['"Tokat Plevne Belediyesi"', '~clubs', 'Emre_Batur']]
Relations of Entity :
Relations_list["Michele_Marcolini"] = ['caps', 'position', '~currentMember', 'birthDate', 'team', 'youthclub', 'description', 'currentclub', 'youthclubs', 'goals', 'Person/height', 'birthPlace', 'rdf-schema#label', 'clubs', 'subject', '22-rdf-syntax-ns#type', '~manager', 'height', 'manageryears', 'givenName', 'shortDescription', '~wikiPageDisambiguates', 'placeOfBirth', 'hypernym', 'name', 'years', 'managerclubs', 'birthYear', 'club', '~name', 'dateOfBirth', 'surname', 'managerClub', 'careerStation']
Relations_list["A.C._Lumezzane"] = ['~wikiPageRedirects', 'nat', 'season', 'position', 'capacity', 'patternB', 'socks', '~managerClub', 'leftarm', 'rdf-schema#label', '22-rdf-syntax-ns#type', 'subject', '~rd2Team', 'league', 'clubname', '~clubs', 'founded', '~youthclubs', 'nick', 'fullName', 'shorts', 'fullname', 'manager', 'ground', 'other', 'hypernym', 'name', 'chrtitle', 'pos', '~rd1Team', 'chairman', 'rightarm', '~managerclubs', '~team', '~core#subject', '~club', '~currentclub', 'nickname', 'body', 'numberOfMembers', 'chairmanTitle']
Relations_list["Tokat Plevne Belediyesi"] = ['~clubs']
[ChatGPT]
Statement : From the evidence, we can know that Michele_Marcolini manages A.C._Lumezzane, however there are no evidence that he played for Tokat Plevne Belediyesi. There for Michele_Marcolini is played for Tokat Plevne Belediyesi is not supported.
Evaluation : Executable (False)


<Example 4>
[User]
Claim : A food is part of Colombian cuisine, one of its ingredients is another food, that is found in the Andalusia region.
Triple sets : [['Colombian_cuisine', '~foodType', 'Pueblito_Viejo'], ['Andalusia', '~location', 'Sierra_de_la_Alfaguara'], ['Andalusia', '~location', 'Sierra_de_Los_Filabres'], ['Andalusia', '~location', 'Open_de_Andalucía'], ['Andalusia', '~location', 'Sierra_de_Cogollos'], ['Andalusia', '~location', 'Carteia'], ['Andalusia', '~location', '2012–13_Getafe_CF_season'], ['Andalusia', '~location', 'Bombing_of_Jaén'], ['Andalusia', '~location', 'Cabo_de_Gata-Níjar_Natural_Park'], ['Andalusia', '~location', 'CB_Sevilla'], ['Andalusia', '~location', 'Sierra_Norte_de_Sevilla'], ['Andalusia', '~location', 'Sierra_de_Aracena'], ['Andalusia', '~location', 'Pico_Mágina'], ['Andalusia', '~location', 'Bahía_de_Cádiz_Natural_Park'], ['Andalusia', '~location', 'Alcazaba_(Sierra_Nevada)'], ['Andalusia', '~location', 'Mosque–Cathedral_of_Córdoba'], ['Andalusia', '~location', '2004–05_Real_Madrid_C.F._season'], ['Andalusia', '~location', 'La_Maroma'], ['Andalusia', '~location', 'CB_Villa_de_Los_Barrios'], ['Andalusia', '~location', 'Alcazaba_of_Almería'], ['Andalusia', '~location', 'Ciudad_Deportiva_Rafael_Gómez'], ['Andalusia', '~location', 'Hotel_París_(Huelva)'], ['Andalusia', '~location', '2012–13_Recreativo_de_Huelva_season'], ['Andalusia', '~location', 'Sierra_Arana'], ['Andalusia', '~location', 'Sierra_de_Cazorla'], ['Andalusia', '~location', 'Despeñaperros'], ['Andalusia', '~location', 'CB_Ciudad_de_Huelva'], ['Andalusia', '~location', 'Seville_Cathedral'], ['Andalusia', '~location', 'Jabalcón'], ['Andalusia', '~location', 'Hotel_Anglo-Hispano'], ['Andalusia', '~location', 'Monastery_of_Santa_Maria_de_las_Cuevas'], ['Andalusia', '~location', '2014–15_CA_Osasuna_season'], ['Andalusia', '~location', 'La_Cala_Resort'], ['Andalusia', '~location', 'Palacio_de_Campo_Real'], ['Andalusia', '~location', 'Los_Millares'], ['Andalusia', '~location', '2014–15_Granada_CF_season'], ['Andalusia', '~location', 'Baloncesto_Málaga'], ['Andalusia', '~location', 'PS10_solar_power_plant'], ['Andalusia', '~location', 'IRAM_30m_telescope'], ['Andalusia', '~location', 'Sierra_de_Huétor'], ['Andalusia', '~location', 'Generalife'], ['Andalusia', '~location', 'Ciudad_Deportiva_José_Ramón_Cisneros_Palacios'], ['Andalusia', '~location', '2011_Volvo_World_Match_Play_Championship'], ['Andalusia', '~location', 'Montes_de_Málaga'], ['Andalusia', '~location', 'Ciudad_Deportiva_del_Granada_CF'], ['Andalusia', '~location', 'Los_Alcornocales_Natural_Park'], ['Andalusia', '~location', '2009_Volvo_World_Match_Play_Championship'], ['Andalusia', '~location', 'Sierra_Blanca_(Andalusia)'], ['Andalusia', '~location', 'Ciudad_Deportiva_de_El_Viso'], ['Andalusia', '~location', 'Sea_Life_Benalmádena'], ['Andalusia', '~location', '2013–14_CA_Osasuna_season'], ['Andalusia', '~location', 'El_Fraile_(Sierra_del_Cabo_de_Gata)'], ['Andalusia', '~location', 'Sierra_de_las_Nieves'], ['Andalusia', '~location', '2011–12_RCD_Mallorca_season'], ['Andalusia', '~location', 'Hotel_Pez_Espada'], ['Andalusia', '~location', 'Ramón_Sánchez_Pizjuán_Stadium'], ['Andalusia', '~location', 'Veleta_(Sierra_Nevada)'], ['Andalusia', '~location', 'Penibaetic_System'], ['Andalusia', '~location', 'CB_Granada'], ['Andalusia', '~location', '2014–15_Middlesbrough_F.C._season'], ['Andalusia', '~location', '2012_Volvo_World_Match_Play_Championship'], ['Andalusia', '~location', '2001–02_Real_Madrid_C.F._season'], ['Andalusia', '~location', 'Circuito_de_Jerez'], ['Andalusia', '~location', 'Sierra_de_Baza'], ['Andalusia', '~location', 'CB_Ciudad_de_Algeciras'], ['Andalusia', '~location', 'Baelo_Claudia'], ['Andalusia', '~location', 'Subbaetic_System'], ['Andalusia', '~location', 'Museum_of_Almería'], ['Andalusia', '~location', 'General_Archive_of_the_Indies'], ['Andalusia', '~location', 'Ciudad_Deportiva_Luis_del_Sol'], ['Andalusia', '~location', 'Peña_de_los_Enamorados'], ['Andalusia', '~location', 'Caminito_del_Rey'], ['Andalusia', '~location', 'Sierra_Sur_de_Jaén'], ['Andalusia', '~location', 'CD_Huelva_Baloncesto'], ['Andalusia', '~location', 'San_Roque_Club'], ['Andalusia', '~location', 'CD_Oximesa'], ['Andalusia', '~location', 'CB_Morón'], ['Andalusia', '~location', 'Pico_del_Caballo'], ['Andalusia', '~location', 'Sierra_de_Mijas'], ['Andalusia', '~location', '2012–13_RCD_Espanyol_season'], ['Pueblito_Viejo', 'foodType', 'Colombian_cuisine']]
Relations of Entity :
Relations_list["Colombian_cuisine"] = ['22-rdf-syntax-ns#type', '~wikiPageRedirects', '~core#subject', '~country', '~foodType', '~rdf-schema#seeAlso', 'rdf-schema#label', 'subject']
Relations_list["Andalusia"] = ['imageFlag', 'direction', 'areaTotalKm', 'country', 'populationAsOf', '~ground', 'type', '~jurisdiction', 'hypernym', '~sourceRegion', 'longew', 'coordinatesDisplay', 'imageShield', 'subdivisionType', 'areaRank', 'caption', 'latm', 'blank2InfoSec', 'rdf-schema#label', '~stylisticOrigins', '~title', '22-rdf-syntax-ns#type', '~placeOfDeath', 'demographics1Name', '~province', 'longm', 'latns', '~deathPlace', 'width', 'flagAlt', 'PopulatedPlace/areaTotal', 'alt', '~location', 'leaderParty', 'flagSize', '~state', '~significantProject', '~origin', '~stylisticOrigin', 'blankInfoSec', '~regionServed', '~place', 'image', 'settlementType', '~seats1Title', 'leader', '~genre', 'populationRank', 'longd', 'imageMap', 'populationTotal', '~capital', 'coordinatesType', 'shieldSize', 'coordinatesRegion', '~region', '~isPartOf', 'seat', '~other', 'align', 'mapCaption', 'leaderName', 'populationTotalRanking', 'blankNameSec', '~headquarter', '~autonomousCommunity', '~wikiPageDisambiguates', '~populationPlace', 'leaderTitle', '~popplace', 'postalCode', '~restingPlace', '~rdf-schema#seeAlso', '~hometown', 'motto', 'governingBody', 'postalCodeType', '~locationCountry', '~headquarters', '~available', 'areaTotal', 'subject', 'blank1InfoSec', '~wikiPageRedirects', 'anthem', 'populationDensityKm', 'name', '~shipNamesake', 'homepage', '~broadcastArea', '~mouthRegion', '~subdivisionName', '~armiger', 'shieldAlt', '~placeOfBirth', 'populationBlank', '~birthPlace', '~core#subject', '~locatedInArea', '~country', 'populationDemonym', '~locale', 'populationBlank1Title', 'seatType', '~residence', 'blank1NameSec', 'latd', 'blank2NameSec', '~body', '~location', '~otherName', '~largestCityWl', '~subdivisionName', '~autonomousCommunity', '~origin', '~centre', '~seatWl', '~commonscat', '~rdf-schema#label', '~highschool', '~seat', '~country', '~territory', '~name', '~article', '~synonym', '~title', '~region', '~team']
Relation_list(Pueblito_Viejo) = ['telephone', 'seatingCapacity', 'established', 'country', 'zip', 'hypernym', 'subject', 'cuisine', 'name', '22-rdf-syntax-ns#type', 'streetAddress', 'address', 'state', 'currentOwner', 'city', 'foodType', 'rdf-schema#label']
[ChatGPT]
Statement : We need more information for verification. Try to look relations 'country, zip, subject, cuisine' of Pueblito_Viejo.
Evaluation : Not executable (Insufficient evidence)


<Example 5>
[User]
Claim : Raúl Gibb Guerrero attended university.
Triple sets : [['Raúl_Gibb_Guerrero', 'university', '"University of Southern Indiana"']]
Relations of Entity : 
Relations_list["Raúl_Gibb_Guerrero"] = ['residence', 'surname', 'name', 'nationality', 'organization', '22-rdf-syntax-ns#type', 'width', 'knownFor', 'rdf-schema#label', 'float', 'nativeNameLang', '~wikiPageRedirects', 'deathCause', 'alternativemap', 'occupation', 'shortDescription', 'term', 'deathPlace', 'awards', 'nativeName', 'deathDate', 'birthYear', 'dateOfBirth', 'caption', 'university', 'dateOfDeath', 'birthDate', 'alt', 'hypernym', 'description', 'placeOfDeath', 'homepage', 'project', 'course', 'subject', 'deathYear', 'givenName']
[ChatGPT]
Statement : According to the triple sets, we can know that Raúl_Gibb_Guerrero's universitiy is University of Southern Indiana. So the claim that Raúl Gibb Guerrero attended university is supported.
Evaluation : Executable (True)


Now, it's your turn. Continue your 'Statement and Evaluation' task. Response must have same form with upper examples.
[User]
Claim : <<<<CLAIM>>>>
Triple set : <<<<Triple set>>>>
Relations of Entity : <<<<GOLD RELATIONS>>>>


"""

sub_agent_2option_beta_concentrate_relation = """
You are the evaluator. I will show you a claim and a triple set extracted from a graph. 
Based on the given triple set and relation list of each entity, determine whether the claim is True or False. 
If given triple sets are lack of information to verify the claim, give the the combination of entity and relation you need. You can refer the given relations list and choosed what relation information is more needed.
The triple set takes the form [Head, Relation, Tail], which means 'Head's Relation is Tail.' 
If the relation starts with '~', it indicates a reverse relation, meaning 'Tail's relation is head.' 
The following cases may arise: Choose one option from 'Executable (True or False)' or 'Not executable(Insufficient evidence)'.
If you choose 'Not executable(Insufficient evidence)', You must specify in the statement which additional relation information is needed for a particular entity. However, the relation can only be selected from the given Relation_list and cannot be created arbitrarily.
Refer to the explanations of the two options below to answer the Statement and Evaluation.

<Cases> 
1. If the triple sets are sufficient to determine the True/False of the claim --> Executable (True or False)
2. If the triple set is insufficient or ambiguos to determine the True/False of the claim --> Not executable (Insufficient evidence) 

<Example 1>
[User]
Claim : A fictional character, which was created by Joe Quesada, is broadcast on Lebanese Broadcasting Corporation and starred Tim Brooke-Taylor. 
Triple sets : [['Joe_Quesaa', '~creator', 'Azrael_(comics)'], ['Joe_Quesaa', '~creator', 'Menace_(Marvel_Comics)'], ['Joe_Quesaa', '~creator', 'Thomas_Logan'], ['Joe_Quesaa', '~creator', 'Carlie_Cooper']]
Relations of Entity : 
Relations_list["Tim_Brooke-Taylor"] = ['birthPlace', 'honorificSuffix', '~after', 'notableWork', 'genre', 'years', 'spouse', 'title', 'givenName', 'shortDescription', 'surname', '~author', 'birthName', '~writer', '~creator', 'placeOfBirth', '~caption', 'active', 'hypernym', '~starring', '~voices', 'birthYear', 'dateOfBirth', 'rdf-schema#label', 'subject', 'birthDate', '22-rdf-syntax-ns#type', '~wikiPageRedirects', 'nationality', 'imdbId', 'description', '~before', '~voice', 'name']
Relations_list["Joe_Quesada"] = ['influences', 'birthPlace', '~after', '~keyPeople', '~artists', 'write', 'years', 'title', '~executiveProducer', 'givenName', '~wikiPageDisambiguates', 'shortDescription', 'surname', 'birthName', '~writer', '~creator', 'placeOfBirth', '~writers', '~pencillers', 'type', '~keypeople', 'hypernym', '~foundedBy', 'birthYear', 'edit', 'caption', 'dateOfBirth', '~creators', 'rdf-schema#label', 'birthDate', 'subject', '~keyPerson', '22-rdf-syntax-ns#type', '~wikiPageRedirects', 'nationality', 'pencil', 'subcat', 'after', 'description', '~aux', '~before', 'before', '~editors', 'awards', 'id', 'name']
Relations_list["Lebanese_Broadcasting_Corporation"] = ['networkLogo', 'broadcastArea', 'homepage', 'networkName', '~owningCompany', 'country', '~wikiPageDisambiguates', 'networkType', '~channel', '~network', '~employer', 'launchDate', 'slogan', '~distributor', 'owner', 'hypernym', '~tv', 'locationCountry', 'firstAirDate', 'rdf-schema#label', 'subject', '22-rdf-syntax-ns#type', '~sisterNames', '~wikiPageRedirects', 'owningCompany', 'logocaption', 'available', '~sisterStation']
[ChatGPT]
Statement : We need more information for verification. Try to look relation '~starring' linked with Tim_Brooke-Taylor and relation 'broadcastArea, ~channel,~tv' linked with Lebanese_Broadcasting_Corporation.
Evaluation : Not executable (Insufficient evidence)

<Example 2>
[User]
Claim : A soccer player, whose birthdate is 1 July 1976, plays for Al-Naft and his club is Steel Azin FC.
Triple sets : [['"1976-07-01"', '~dateOfBirth', 'Matt_Grindley'], ['"1976-07-01"', '~dateOfBirth', 'Richard_Piakura'], ['"1976-07-01"', '~dateOfBirth', 'Patrick_Kluivert'], ['"1976-07-01"', '~dateOfBirth', 'Aaron_Cassidy'], ['"1976-07-01"', '~dateOfBirth', 'Hannu_Tihinen'], ['"1976-07-01"', '~dateOfBirth', 'Ahmad_Kadhim_Assad'], ['Al-Naft', '~currentclub', 'Samer_Saeed'], ['Al-Naft', '~currentclub', 'Ahmad_Kadhim_Assad'], ['Al-Naft', '~currentclub', 'Hussam_Kadhim'], ['Al-Naft', '~currentclub', 'Hassan_Turki_Attiya'], ['Steel_Azin_F.C.', '~currentclub', 'Arash_Gholizadeh']]
Relations of Entity :
Relations_list["Al-Naft"] = ['no', '~managerClub', 'patternB', 'pos', 'leftarm', 'hypernym', 'chairman', '~club', '~youthclubs', 'name', '~t', 'body', 'season', 'league', 'socks', 'nickname', 'ground', 'patternRa', 'rightarm', 'nick', 'capacity', '~text', 'nat', '~team', 'patternLa', 'manager', 'fullname', 'shorts', 'subject', '~clubs', '~currentclub', 'position', '~managerclubs', 'clubname', '~t', '~text', '~rdf-schema#label', '~rd1Team', '~team']
Relations_list["Steel_Azin_F.C."] = ['no', '~managerClub', 'patternB', '~tenant', 'pos', 'leftarm', '~promoted', 'hypernym', '~rd1Team', 'chairman', 'founded', '~tenants', '~club', '~youthclubs', '~rd3Team', 'name', 'owner', 'body', 'league', '~operator', 'socks', 'ground', 'gender', 'patternRa', 'rightarm', 'capacity', '22-rdf-syntax-ns#type', 'nat', 'pattern', '~team', 'manager', 'fullname', 'patternLa', 'shorts', 'subject', '~relegated', '~occupation', '~wikiPageDisambiguates', '~clubs', '~currentclub', '~other', '~managerclubs', 'clubname']
Relations_list[""1976-07-01""] = ['~dateOpened', '~openingDate', '~firstdate', '~launch', '~released', '~dateOfDeath', '~originalairdate', '~lastAired', '~termEnd', '~releaseDate', '~firstAirDate', '~dateOfBirth', '~birthDate', '~deathDate', '~completionDate', '~founded', '~shipStruck', '~first', '~recorded', '~session4End', '~decommissioningDate', '~recordDate', '~foundingDate', '~established', '~activeYearsEndDate', '~dateOfRet', '~airdate', '~age', '~opened', '~designation1Date', '~added', '~activeYearsStartDate', '~shipDecommissioned', '~date', '~termStart']
[ChatGPT]
Statement : 'Ahmad_Kadhim_Assad' was born 1 July 1976, and played for Al-Naft. However, we cannot verify the information about 'Steel Azin FC'. Only '~currentClub' relation was used in triple sets, but also we can use '~club', '~team', '~clubs' to find such information. Therefore, use those relation and collect more evidences.
Evaluation : Not executable (Insufficient evidence)

<Example 3>
[User]
Claim : Michele Marcolini played for Tokat Plevne Belediyesi and manages A.C. Lumezzane.
Triple sets : [['Michele_Marcolini', 'managerclubs', 'Real_Vicenza_V.S.'], ['Michele_Marcolini', 'managerclubs', 'A.C._Lumezzane'], ['Michele_Marcolini', 'currentclub', 'Real_Vicenza_V.S.'], ['A.C._Lumezzane', 'manager', 'Michele_Marcolini'], ['"Tokat Plevne Belediyesi"', '~clubs', 'Emre_Batur']]
Relations of Entity :
Relations_list["Michele_Marcolini"] = ['caps', 'position', '~currentMember', 'birthDate', 'team', 'youthclub', 'description', 'currentclub', 'youthclubs', 'goals', 'Person/height', 'birthPlace', 'rdf-schema#label', 'clubs', 'subject', '22-rdf-syntax-ns#type', '~manager', 'height', 'manageryears', 'givenName', 'shortDescription', '~wikiPageDisambiguates', 'placeOfBirth', 'hypernym', 'name', 'years', 'managerclubs', 'birthYear', 'club', '~name', 'dateOfBirth', 'surname', 'managerClub', 'careerStation']
Relations_list["A.C._Lumezzane"] = ['~wikiPageRedirects', 'nat', 'season', 'position', 'capacity', 'patternB', 'socks', '~managerClub', 'leftarm', 'rdf-schema#label', '22-rdf-syntax-ns#type', 'subject', '~rd2Team', 'league', 'clubname', '~clubs', 'founded', '~youthclubs', 'nick', 'fullName', 'shorts', 'fullname', 'manager', 'ground', 'other', 'hypernym', 'name', 'chrtitle', 'pos', '~rd1Team', 'chairman', 'rightarm', '~managerclubs', '~team', '~core#subject', '~club', '~currentclub', 'nickname', 'body', 'numberOfMembers', 'chairmanTitle']
Relations_list["Tokat Plevne Belediyesi"] = ['~clubs']
[ChatGPT]
Statement : From the evidence, we can know that Michele_Marcolini manages A.C._Lumezzane, however there are no evidence that he played for Tokat Plevne Belediyesi. There for Michele_Marcolini is played for Tokat Plevne Belediyesi is not supported.
Evaluation : Executable (False)

<Example 4>
[User]
Claim : There is a building with 45 floors in Public Square, Cleveland.
Triple sets : [['Public_Square,_Cleveland', '~location', 'Park_Building_(Cleveland,_Ohio)'], ['Public_Square,_Cleveland', '~location', 'Key_Tower'], ['Public_Square,_Cleveland', '~location', '200_Public_Square'], ['"45"', '~floors', 'Sheraton_Kansas_City_Hotel_at_Crown_Center'], ['"45"', '~floors', 'Four_Seasons_Hotel_Hong_Kong'], ['"45"', '~topFloor', 'Sun_Towers']]
Relations of Entity :
Relations_list['"45"'] = ['~currentRecord', '~usnwrLaw', '~valid', '~plantLatS', '~medlineplus', '~lengthMi', '~carNumber', '~rangeLongM', '~quellhöhe', '~traffic', '~attend', '~shipLength', '~event', '~ranking', '~stagewins', '~totalCupRaces', '~floorArea', '~topFloor', '~visitorTotal', '~floorCount', '~fifaMax', '~areakm']
Relations_list['Public_Square,_Cleveland'] = ['caption', 'latDirection', 'name', 'added', 'yearOfConstruction', 'latMinutes', 'latSeconds', '~routeStart', 'refnum', 'designatedOther1Color', 'longMinutes', '~location', '~start', 'location', 'longDegrees', 'longSeconds', 'built', 'locmapin', 'governingBody', 'designatedOther1Link', 'coordDisplay']
[ChatGPT]
Statement : From the evidence, we cannot find the building having 45 floors and located in Public Square, Cleveland. However, we can find more building that has 45 floors using '~floorCount' relation in '"45"' entity (since triple sets used '~floors' and '~topFloor' for finding evidences). Therefore, use those relation and collect more evidences.
Evaluation : Not executable (Insufficient evidence)

<Example 5>
[User]
Claim : Raúl Gibb Guerrero attended university.
Triple sets : [['Raúl_Gibb_Guerrero', 'university', '"University of Southern Indiana"']]
Relations of Entity : 
Relations_list["Raúl_Gibb_Guerrero"] = ['residence', 'surname', 'name', 'nationality', 'organization', '22-rdf-syntax-ns#type', 'width', 'knownFor', 'rdf-schema#label', 'float', 'nativeNameLang', '~wikiPageRedirects', 'deathCause', 'alternativemap', 'occupation', 'shortDescription', 'term', 'deathPlace', 'awards', 'nativeName', 'deathDate', 'birthYear', 'dateOfBirth', 'caption', 'university', 'dateOfDeath', 'birthDate', 'alt', 'hypernym', 'description', 'placeOfDeath', 'homepage', 'project', 'course', 'subject', 'deathYear', 'givenName']
[ChatGPT]
Statement : According to the triple sets, we can know that Raúl_Gibb_Guerrero's universitiy is University of Southern Indiana. So the claim that Raúl Gibb Guerrero attended university is supported.
Evaluation : Executable (True)


Now, it's your turn. Continue your 'Statement and Evaluation' task. Response must have same form with upper examples.
[User]
Claim : <<<<CLAIM>>>>
Triple set : <<<<Triple set>>>>
Relations of Entity : <<<<GOLD RELATIONS>>>>

"""

def feedback(claim,gold_set,gold_relations,f):
    
    #engine="gpt-3.5-turbo-0125"
    #engine = "gpt-4o-mini-2024-07-18"
    engine = "gpt-4o-2024-08-06"
    
    f.write("\n\n------------------------------")
    f.write("\nSub Agent Verification Process\n")
    f.write("------------------------------\n")
    print("\n------------------------------")
    print("Sub Agent Verification Process")
    print("------------------------------\n")
    f.write(f"Connected Relations with Entities:{gold_relations}\n\n")    
    print(f"Connected Relations with Entities:{gold_relations}\n")
    final_evidence=[]
    
    
    for tri in gold_set:
        if tri not in final_evidence:
            final_evidence.append(tri)
      
    f.write(f"Collected Evidences:\n{gold_set}\n") 
    print(f"Collected Evidences:\n{gold_set}\n")
       
    
    conversation = [{"role": "system", "content": "You are a helpful assistant."}]
    prompt = sub_agent_2option_beta.replace('<<<<CLAIM>>>>', claim).replace('<<<<Triple set>>>>', str(final_evidence)).replace('<<<<GOLD RELATIONS>>>>', gold_relations)
    conversation.append({"role": "user", "content": prompt})
    
    # Initialize variables
    sub_response = None
    case = None
    prediction = None
    
    
    for i in range(5):

        
        try :  
            response = client.chat.completions.create( model=engine, messages=conversation, temperature= 0.3, top_p = 0.1)
            assistant_response = response.choices[0].message.content.strip()
            print(assistant_response)
            
            try:
                sub_statement = assistant_response.split("Statement")[1].split("Evaluation")[0].strip()
                sub_result = assistant_response.split("Evaluation")[1].strip()
                print(f"Sub result: {sub_result}")
                f.write(f"Sub result: {sub_result}")
                
                if "(Insufficient evidence)" in sub_result:
                    #sub_response = "We don't have enough evidence to verify the claim. You must extract more information from the graph data."
                    sub_response = sub_statement
                    case =1
                    prediction = None
                    break
                elif "(Complex claim)" in sub_result:
                    sub_response = "Done!! Abstain"
                    case=2
                    prediction = "Abstain"
                    break
                else: 
                    if 'True' in sub_result or 'true' in sub_result:
                        sub_response = "Done!! True"
                        prediction = 'True'
                        case = 3
                        break  # Ensure the loop exits
                    elif 'False' in sub_result or 'false' in sub_result:
                        sub_response = "Done!! False"
                        prediction = 'False'
                        case = 3
                        break  # Ensure the loop exits
            except Exception as e:
                print(f"Error parsing assistant response: {e}")
                continue


        

        except openai.APIError as e:
                #Handle API error here, e.g. retry or log
                print(f"OpenAI API returned an API Error: {e}")
                continue
    
    # Ensure sub_response has a value before returning
    if sub_response is None:
        sub_response = "There is problem in server. Please call Verification[] one more time/"
        case = -1
        prediction = None
    
    
    return sub_response, case, prediction