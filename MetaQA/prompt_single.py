pr_1 = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use below helper functions to find the evidence for finding labels.

<Helper functions>
1. getRelation[entity]: Returns the list of relations connected to the entities.
2. exploreKG[entity]=[list of relations]: Returns the corresponding tail entities in graph data starts from single entity in given entity and given relation.
3. Verification[list of entities]: If you can find the answer entities from collected evidences, give the answer.

You must follow the exact format of the given helper function. You can use multiple helper functions in one step by using '##' between functions.

Now, I will give you a Claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for my response. If response has made, continue your 'Statement and Helper function' task.
Importantly, you have to use inverse relation if you need. For example, if you want to find films starred by certain actors (when only actors were given), you have to use 'starred_actors' relation.

Here are some examples.

Example 1)
Claim: what genres do the films that share actors with [Man of Steel] fall under?
Given Entity: ['Man of Steel']

[ChatGPT]
Statement: I need the relations linked with the given entity.
Helper function: getRelation['Man of Steel']
[User]
Execution result: Relation_list['Man of Steel'] = ['release_year', 'starred_actors', 'written_by', 'has_tags', 'directed_by']
[ChatGPT]
Statement: First, to solve the claim, I have to know the actors starred in 'Man of Steel'.
Helper function: exploreKG['Man of Steel']=['starred_actors']
[User]
Execution result: ['Man of Steel', 'starred_actors', 'michael_shannon'], ['Man of Steel', 'starred_actors', 'henry_cavill'], ['Man of Steel', 'starred_actors', 'amy_adams'], ['Man of Steel', 'starred_actors', 'diane_lane']
[ChatGPT]
Statement: Next, I need films starred by previous given actors. To find the films, I need relations linked with the actors.
Helper function: getRelation['michael_shannon'] ## getRelation['henry_cavill'] ## getRelation['amy_adams'] ## getRelation['diane_lane']
[User]
Execution result: Relation_list['michael_shannon'] = ['has_tags', 'starred_actors'], Relation_list['henry_cavill'] = ['starred_actors'], Relation_list['amy_adams'] = ['has_tags', 'starred_actors'], getRelations['diane_lane'] = ['has_tags', 'starred_actors']
[ChatGPT]
Statement: To get the films starred by previous actors, I need to explore the graph with each actors and related relations.
Helper function: exploreKG['michael_shannon']=['starred_actors'] ## exploreKG['henry_cavill']=['starred_actors'] ## exploreKG['amy_adams']=['starred_actors'] ## exploreKG['diane_lane']=['starred_actors']
[User]
Execution result: ['michael_shannon', 'starred_actors', 'bug'], ['michael_shannon', 'starred_actors', 'machine_gun_preacher'], ['michael_shannon', 'starred_actors', 'young_ones'], ['michael_shannon', 'starred_actors', 'the_missing_person'], ['henry_cavill', 'starred_actors', 'immortals'], ['henry_cavill', 'starred_actors', 'blood_creek'], ['henry_cavill', 'starred_actors', 'the_cold_light_of_day'], ['amy_adams', 'starred_actors', 'moonlight_serenade'], ['amy_adams', 'starred_actors', 'american_hustle'], ['amy_adams', 'starred_actors', 'sunshine_cleaning'], ['amy_adams', 'starred_actors', 'the_fighter'], ['diane_lane', 'starred_actors', 'wild_bill'], ['diane_lane', 'starred_actors', 'the_glass_house'], ['diane_lane', 'starred_actors', 'jumper']
[ChatGPT]
Statement: To get the genres of the these films, I need to find the relations linked with all the films from previous step.
Helper function: getRelation['bug'] ## getRelation['machine_gun_preacher'] ## getRelation['young_ones'] ## getRelation['the_missing_person'] ## getRelation['immortals'] ## getRelation['blood_creek'] ## getRelation['the_cold_light_of_day'] ## getRelation['moonlight_serenade'] ## getRelation['american_hustle'] ## getRelation['sunshine_cleaning'] ## getRelation['the_fighter'] ## getRelation['wild_bill'] ## getRelation['the_glass_house'] ## getRelation['jumper']
[User]
Execution result: Relation_list['bug'] = ['starred_actors', 'has_tags', 'written_by', 'release_year', 'has_genre', 'directed_by'], Relation_list['machine_gun_preacher'] = ['starred_actors', 'has_tags', 'written_by', 'release_year', 'has_genre', 'directed_by'], Relation_list['young_ones'] = ['starred_actors', 'has_genre', 'release_year'], Relation_list['the_missing_person'] = ['starred_actors', 'written_by', 'release_year', 'has_genre'], Relation_list['immortals'] = 'starred_actors', 'has_tags', 'release_year', 'has_genre', 'in_language'], Relation_list['blood_creek'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list['the_cold_light_of_day'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list['moonlight_serenade'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list['american_hustle'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list['sunshine_cleaning'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list['the_fighter'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list['wild_bill'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list['the_glass_house'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list['jumper'] = ['starred_actors', 'has_tags', 'release_year', 'directed_by']
[ChatGPT]
Statement: To get the genres of the films, I need to explore the graph with each films and related relations.
Helper function: exploreKG['bug']=['has_genre'] ## exploreKG['machine_gun_preacher']=['has_genre'] ## exploreKG['young_ones']=['has_genre'] ## exploreKG['the_missing_person']=['has_genre'] ## exploreKG['immortals']=['has_genre'] ## exploreKG['blood_creek']=['has_genre'] ## exploreKG['the_cold_light_of_day']=['has_genre'] ## exploreKG['moonlight_serenade']=['has_genre'] ## exploreKG['american_hustle']=['has_genre'] ## exploreKG['sunshine_cleaning']=['has_genre'] ## exploreKG['the_fighter']=['has_genre'] ## exploreKG['wild_bill']=['has_genre'] ## exploreKG['the_glass_house']=['has_genre'] ## exploreKG['jumper']=[]
[User]
Execution result: ['bug', 'has_genre', 'horror'], ['machine_gun_preacher', 'has_genre', 'action'], ['young_ones', 'has_genre', 'action'], ['the_missing_person', 'has_genre', 'mystery'], ['the_missing_person', 'has_genre', 'drama'], ['the_missing_person', 'has_genre', 'comedy'], ['immortals', 'has_genre', 'fantasy'], ['blood_creek', 'has_genre', 'horror'], ['the_cold_light_of_day', 'has_genre', 'action'], ['moonlight_serenade', 'has_genre', 'romance'], ['moonlight_serenade', 'has_genre', 'drama'], ['moonlight_serenade', 'has_genre', 'musical'], ['american_hustle', 'has_genre', 'crime'], ['american_hustle', 'has_genre', 'drama'], ['sunshine_cleaning', 'has_genre', 'drama'], ['sunshine_cleaning', 'has_genre', 'comedy'], ['the_fighter', 'has_genre', 'drama'], ['the_fighter', 'has_genre', 'sport'], ['wild_bill', 'has_genre', 'western'], ['the_glass_house', 'has_genre', 'thriller']
[ChatGPT]
Statement: Now I get the genres of the films that share actors with 'Man of Steel'. The answer of the claim is as follows.
['horror', 'action', 'mystery', 'drama', 'comedy', 'fantasy', 'romance', 'musical', 'crime', 'sport', 'western', 'thriller']
Helper function: Verification['horror', 'action', 'mystery', 'drama', 'comedy', 'fantasy', 'romance', 'musical', 'crime', 'sport', 'western', 'thriller']


Example 2)
Claim: who are the actors in the films written by [John Travis]?
Given entity: ["John Travis"]

[ChatGPT]
Statement: I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function: getRelation['John Travis']
[User]
Execution result: Relation_list['John Travis'] = ['written_by']
[ChatGPT]
Statement: Now, to find the films that 'John Travis' written, I need to explore the graph from 'John Travis' with related relations.
Helper function: exploreKG['John Travis']=['written_by']
[User]
Execution result: ['John Travis', 'written_by', 'the_haunting_of_molly_hartley']
[ChatGPT]
Statement: Now, we have to find the actors in the previous given film.
Helper function: getRelation['the_haunting_of_molly_hartley']
[User]
Execution result: Relation_list['the_haunting_of_molly_hartley'] = ['has_genre', 'starred_actors', 'directed_by', 'release_year', 'written_by']
[ChatGPT]
Statement: To get the actors in the film, I need to explore the graph with the film and related relations.
Helper function: exploreKG['the_haunting_of_molly_hartley']=['starred_actors']
[User]
Execution result: ['the_haunting_of_molly_hartley', 'starred_actors', 'haley_bennett'], ['the_haunting_of_molly_hartley', 'starred_actors', 'chace_crawford'], ['the_haunting_of_molly_hartley', 'starred_actors', 'jake_weber']
[ChatGPT]
Statement: Now I get the actors of the films written by 'John Travis'. The answer of the claim is as follows.
['haley_bennett', 'chace_crawford', 'jake_weber']
Helper function: Verification['haley_bennett', 'chace_crawford', 'jake_weber']

Example 3)
Claim: what does [Hiromi Nagasaku] star in?
Given entity: ["Hiromi Nagasaku"]

[ChatGPT]
Statement: I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function: getRelation["Hiromi Nagasaku"]
[User]
Execution result: Relation_list[["Hiromi Nagasaku"]) = ['starred_actors']
[ChatGPT]
Statement: Now, to find the films that 'Hiromi Nagasaku' starred, I need to explore the graph from 'Hiromi Nagasaku' with related relations.
Helper function: exploreKG['Hiromi Nagasaku']=['starred_actors']
[User]
Execution result: ['Hiromi Nagasaku', 'starred_actors', 'doppleganger']
[ChatGPT]
Statement: Now I get the films starred by 'Hiromi Nagasaku'. The answer of the claim is as follows.
['doppleganger']
Helper function: Verification['doppleganger']

Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>

"""

pr_2 = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use below helper functions to find the evidence for finding labels.

<Helper functions>
1. getRelation[entity]: Returns the list of relations connected to the entities.
2. exploreKG[entity]=[list of relations]: Returns the corresponding tail entities in graph data starts from single entity in given entity and given relation.
3. Verification[list of entities]: If you can find the answer entities from collected evidences, give the answer.

You must follow the exact format of the given helper function. You can use multiple helper functions in one step by using '##' between functions.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for my response. If response has made, continue your 'Statement and Helper function' task.
Importantly, you have to use inverse relation if you need. For example, if you want to find films starred by certain actors (when only actors were given), you have to use 'starred_actors' relation.

Here are some examples.

Example 1)
Claim: who directed the movies written by the writer of [Millennium Actress]?
Given Entity: ['Millennium Actress']

[ChatGPT]
Statement: I need the relations linked with the given entity.
Helper function: getRelation['Millennium Actress']
[User]
Execution result: 
Relation_list['Millennium Actress'] = ['directed_by', 'written_by', 'release_year', 'in_language', 'has_tags']
[ChatGPT]
Statement: Now, to find the writer of 'Millennium Actress', I need to explore the graph with the given entity and related relations.
Helper function: exploreKG['Millennium Actress']=['written_by']
[User]
Execution result: 
['Millennium Actress', 'written_by', 'satoshi_kon']
[ChatGPT]
Statement: Now, to find the movies written by 'satoshi_kon', I need to explore the graph to find the proper relation.
Helper function: exploreKG['satoshi_kon']=['~written_by', '~directed_by', '~has_tags']
[User]
Execution result: 
['satoshi_kon', '~written_by', 'paprika'], ['satoshi_kon', '~written_by', 'tokyo_godfathers']
[ChatGPT]
Statement: Now, I have to find the director of the films found in previous step.
Helper function: getRelation['paprika'] ## getRelation['tokyo_godfathers']
[User]
Execution result: 
Relation_list['paprika'] = ['directed_by', 'written_by', 'release_year', 'in_language', 'has_tags']
Relation_list['tokyo_godfathers'] = ['directed_by', 'written_by', 'release_year', 'in_language', 'has_tags']
[ChatGPT]
Statement: Now, I have to find the director of the films found in previous step.
Helper function: exploreKG['paprika']=['directed_by'] ## exploreKG['tokyo_godfathers']=['directed_by']
[User]
Execution result: 
['paprika', 'directed_by', 'satoshi_kon']
['tokyo_godfathers', 'directed_by', 'satoshi_kon']
[ChatGPT]
Statement: Now I get the directors of the films written by the writer of 'Millennium Actress'. The answer of the claim is as follows.
['satoshi_kon']
Helper function: Verification['satoshi_kon']

Example 2)
Claim: when did the movies directed by the [The Champ] director release?
Given Entity: ['The Champ']

[ChatGPT]
Statement: I need the relations linked with the given entity.
Helper function: getRelation['The Champ']
[User]
Execution result: 
Relation_list['The Champ'] = ['directed_by', 'written_by', 'release_year', 'has_tags', 'starred_actors']
[ChatGPT]
Statement: Now, to find the director of 'The Champ', I need to explore the graph with the given entity and related relations.
Helper function: exploreKG['The Champ']=['directed_by']
[User]
Execution result: 
['The Champ', 'directed_by', 'king_vidor'], ['The Champ', 'directed_by', 'franco_zeffirelli']
[ChatGPT]
Statement: Now I get the directors of 'The Champ'. For the next step, I need to find the movies directed by the directors.
Helper function: getRelation['king_vidor'] ## getRelation['franco_zeffirelli']
[User]
Execution result: 
Relation_list['king_vidor'] = ['~written_by', '~directed_by', '~has_tags']
Relation_list['franco_zeffirelli'] = ['~written_by', '~directed_by', '~has_tags']
[ChatGPT]
Statement: Now, I need to find the movies directed by the directors using proper relations.
Helper function: exploreKG['king_vidor']=['~directed_by'] ## exploreKG['franco_zeffirelli']=['~directed_by']
[User]
Execution result: 
['king_vidor', '~directed_by', 'war_and_peace'], ['king_vidor', '~directed_by', 'bird_of_paradise'], ['king_vidor', '~directed_by', 'ruby_gentry'], ['king_vidor', '~directed_by', 'comrade_x'], ['king_vidor', '~directed_by', 'our_daily_bread'], ['king_vidor', '~directed_by', 'the_patsy'], ['king_vidor', '~directed_by', 'the_fountainhead'], ['king_vidor', '~directed_by', 'duel_in_the_sun']
['franco_zeffirelli', '~directed_by', 'endless_love'], ['franco_zeffirelli', '~directed_by', 'otello'], ['franco_zeffirelli', '~directed_by', 'hamlet'], ['franco_zeffirelli', '~directed_by', 'jane_eyre'], ['franco_zeffirelli', '~directed_by', 'callas_forever']
[ChatGPT]
Statement: Now I get the movies directed by the directors of 'The Champ'. Finally, I need to find the release year of the all movies.
Helper function: getRelation['war_and_peace'] ## getRelation['bird_of_paradise'] ## getRelation['ruby_gentry'] ## getRelation['comrade_x'] ## getRelation['our_daily_bread'] ## getRelation['the_patsy'] ## getRelation['the_fountainhead'] ## getRelation['duel_in_the_sun'] ## getRelation['endless_love'] ## getRelation['otello'] ## getRelation['hamlet'] ## getRelation['jane_eyre'] ## getRelation['callas_forever']
[User]
Execution result: 
Relation_list['war_and_peace'] = ['directed_by', 'written_by', 'release_year', 'has_genre', 'in_language', 'has_tags', 'starred_actors']
Relation_list['bird_of_paradise'] = ['has_genre', 'directed_by', 'starred_actors', 'release_year']
Relation_list['ruby_gentry'] = ['starred_actors', 'directed_by', 'release_year']
Relation_list['comrade_x'] = ['has_genre', 'directed_by', 'starred_actors', 'release_year']
Relation_list['our_daily_bread'] = ['directed_by', 'written_by', 'release_year', 'starred_actors', 'has_tags', 'has_genre']
Relation_list['the_patsy'] = ['directed_by', 'written_by', 'release_year', 'has_genre', 'has_tags', 'starred_actors']
Relation_list['the_fountainhead'] = ['directed_by', 'written_by', 'release_year', 'has_genre', 'has_tags', 'starred_actors']
Relation_list['duel_in_the_sun'] = ['directed_by', 'written_by', 'release_year', 'has_genre', 'has_tags', 'starred_actors']
Relation_list['endless_love'] = ['has_genre', 'directed_by', 'starred_actors', 'release_year']
Relation_list['otello'] = ['has_genre', 'directed_by', 'starred_actors', 'release_year']
Relation_list['hamlet'] = ['has_genre', 'directed_by', 'starred_actors', 'release_year']
Relation_list['jane_eyre'] = ['directed_by', 'written_by', 'release_year', 'has_genre', 'has_tags', 'starred_actors']
Relation_list['callas_forever'] = ['has_genre', 'directed_by', 'starred_actors', 'release_year']
[ChatGPT]
Statement: Now to find the release year of the movies, I need to find the release year of the movies using proper relations.
Helper function: exploreKG['war_and_peace']=['release_year'] ## exploreKG['bird_of_paradise']=['release_year'] ## exploreKG['ruby_gentry']=['release_year'] ## exploreKG['comrade_x']=['release_year'] ## exploreKG['our_daily_bread']=['release_year'] ## exploreKG['the_patsy']=['release_year'] ## exploreKG['the_fountainhead']=['release_year'] ## exploreKG['duel_in_the_sun']=['release_year'] ## exploreKG['endless_love']=['release_year'] ## exploreKG['otello']=['release_year'] ## exploreKG['hamlet']=['release_year'] ## exploreKG['jane_eyre']=['release_year'] ## exploreKG['callas_forever']=['release_year']
[User]
Execution result: 
['war_and_peace', 'release_year', '1956'], ['war_and_peace', 'release_year', '1966']
['bird_of_paradise', 'release_year', '1932']
['ruby_gentry', 'release_year', '1952']
['comrade_x', 'release_year', '1940']
['our_daily_bread', 'release_year', '1934'], ['our_daily_bread', 'release_year', '2005']
['the_patsy', 'release_year', '1928'], ['the_patsy', 'release_year', '1964']
['the_fountainhead', 'release_year', '1949']
['duel_in_the_sun', 'release_year', '1946']
['endless_love', 'release_year', '2014'], ['endless_love', 'release_year', '1981']
['otello', 'release_year', '1986']
['hamlet', 'release_year', '2009'], ['hamlet', 'release_year', '1996'], ['hamlet', 'release_year', '1964'], ['hamlet', 'release_year', '1990'], ['hamlet', 'release_year', '2000'], ['hamlet', 'release_year', '1969'], ['hamlet', 'release_year', '1948']
['jane_eyre', 'release_year', '1970'], ['jane_eyre', 'release_year', '2011'], ['jane_eyre', 'release_year', '1943'], ['jane_eyre', 'release_year', '1996']
['callas_forever', 'release_year', '2002']
[ChatGPT]
Statement: Now I get the release year of the movies directed by the director of 'The Champ'. The answer of the claim is as follows.
['1928', '1932', '1934', '1940', '1943', '1946', '1948', '1949', '1952', '1956', '1964', '1966', '1969', '1970', '1981', '1986', '1990', '1996', '2000', '2002', '2005', '2009', '2011', '2014']
Helper function: Verification['1928', '1932', '1934', '1940', '1943', '1946', '1948', '1949', '1952', '1956', '1964', '1966', '1969', '1970', '1981', '1986', '1990', '1996', '2000', '2002', '2005', '2009', '2011', '2014']

Example 3)
Claim: what film genre is [Crazy Safari]?
Given Entity: ['Crazy Safari']

[ChatGPT]
Statement: I need the relations linked with the given entity.
Helper function: getRelation['Crazy Safari']    
[User]
Execution result: 
Relation_list['Crazy Safari'] = ['directed_by', 'release_year', 'has_genre']
[ChatGPT]
Statement: Now, to find the genre of 'Crazy Safari', I need to explore the graph with the given entity and related relations.
Helper function: exploreKG['Crazy Safari']=['has_genre']
[User]
Execution result: 
['Crazy Safari', 'has_genre', 'comedy']
[ChatGPT]
Statement: Now I get the genre of 'Crazy Safari'. The answer of the claim is as follows.
['comedy']
Helper function: Verification['comedy']


Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>

"""

pr_3 = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use below helper functions to find the evidence for finding labels.

<Helper functions>
1. getRelation[entity]: Returns the list of relations connected to the entities.
2. exploreKG[entity]=[list of relations]: Returns the corresponding tail entities in graph data starts from single entity in given entity and given relation.
3. Verification[list of entities]: If you can find the answer entities from collected evidences, give the answer.

You must follow the exact format of the given helper function. You can use multiple helper functions in one step by using '##' between functions.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for my response. If response has made, continue your 'Statement and Helper function' task.
Importantly, you have to use inverse relation if you need. For example, if you want to find films starred by certain actors (when only actors were given), you have to use 'starred_actors' relation.

Here are some examples.

Example 1)
Claim: who co-wrote films with [Veikko Huovinen]?
Given Entity: ['Veikko Huovinen']

[ChatGPT]
Statement: I need the relations linked with the given entity.
Helper function: getRelation['Veikko Huovinen']
[User]
Execution result: 
Relation_list['Veikko Huovinen'] = ['~written_by']
[ChatGPT]
Statement: Now, to find the films co-written by 'Veikko Huovinen', I need to first find the film written by 'Veikko Huovinen'. I need to explore the graph with the given entity and related relations.
Helper function: exploreKG['Veikko Huovinen']=['~written_by']
[User]
Execution result: 
['Veikko Huovinen', '~written_by', 'dog_nail_clipper']
[ChatGPT]
Statement: Now I get the films written by 'Veikko Huovinen'. I need to find the writers of the film co-written by 'Veikko Huovinen'.
Helper function: getRelation['dog_nail_clipper']
[User]
Execution result: 
Relation_list['dog_nail_clipper'] = ['directed_by', 'written_by', 'starred_actors', 'in_language', 'release_year']
[ChatGPT]
Statement: To find the writers of the film co-written by 'Veikko Huovinen', I need to explore the graph with the given entity and related relations.
Helper function: exploreKG['dog_nail_clipper']=['written_by']
[User]
Execution result: 
['dog_nail_clipper', 'written_by', 'markku_pölönen']
[ChatGPT]
Statement: Now I get the writers of the film co-written by 'Veikko Huovinen'. The answer of the claim is as follows.
['markku_pölönen']
Helper function: Verification['markku_pölönen']

Example 2)
Claim: the films that share actors with the film [Enid] were in which languages?
Given Entity: ['Enid']  

[ChatGPT]
Statement: I need the relations linked with the given entity.
Helper function: getRelation['Enid']
[User]
Execution result: 
Relation_list['Enid'] = ['release_year', 'has_genre', 'directed_by', 'starred_actors']
[ChatGPT]
Statement: Now, to find the films that share actors with the film 'Enid', I need to explore the graph with the given entity and related relations.
Helper function: exploreKG['Enid']=['starred_actors']
[User]
Execution result: 
['Enid', 'starred_actors', 'helena_bonham_carter'], ['Enid', 'starred_actors', 'matthew_macfadyen'], ['Enid', 'starred_actors', 'denis_lawson']
[ChatGPT]
Statement: Now I get the actors that share actors with the film 'Enid'. I need to find the films of the actors from the previous result.
Helper function: getRelation['helena_bonham_carter'] ## getRelation['matthew_macfadyen'] ## getRelation['denis_lawson']
[User]
Execution result: 
Relation_list['helena_bonham_carter'] = ['~starred_actors', '~has_tags']
Relation_list['matthew_macfadyen'] = ['~starred_actors', '~has_tags']
Relation_list['denis_lawson'] = ['~starred_actors']
[ChatGPT]
Statement: To find the films that share actors with the film 'Enid', I need to explore the graph with the given entity and related relations.
Helper function: exploreKG['helena_bonham_carter']=['~starred_actors'] ## exploreKG['matthew_macfadyen']=['~starred_actors'] ## exploreKG['denis_lawson']=['~starred_actors']
[User]
Execution result: 
['helena_bonham_carter', '~starred_actors', 'conversations_with_other_women'], ['helena_bonham_carter', '~starred_actors', 'the_gruffalo'], ['helena_bonham_carter', '~starred_actors', 'planet_of_the_apes'], ['helena_bonham_carter', '~starred_actors', 'lady_jane'], ['helena_bonham_carter', '~starred_actors', 'the_young_and_prodigious_t.s._spivet']
['matthew_macfadyen', '~starred_actors', 'the_three_musketeers'], ['matthew_macfadyen', '~starred_actors', 'anna_karenina'], ['matthew_macfadyen', '~starred_actors', 'incendiary']
['denis_lawson', '~starred_actors', 'local_hero']
[ChatGPT]
Statement: Now I get the films that share actors with the film 'Enid'. Finally, I need to find the languages of the films.
Helper function: getRelation['conversations_with_other_women'] ## getRelation['the_gruffalo'] ## getRelation['planet_of_the_apes'] ## getRelation['lady_jane'] ## getRelation['the_young_and_prodigious_t.s._spivet'] ## getRelation['the_three_musketeers'] ## getRelation['anna_karenina'] ## getRelation['incendiary'] ## getRelation['local_hero']
[User]
Execution result: 
Relation_list['conversations_with_other_women'] = ['directed_by', 'written_by', 'starred_actors', 'release_year', 'has_tags', 'has_genre']
Relation_list['the_gruffalo'] = ['directed_by', 'written_by', 'starred_actors', 'release_year', 'has_genre']
Relation_list['planet_of_the_apes'] = ['directed_by', 'written_by', 'starred_actors', 'in_language', 'release_year', 'has_tags']
Relation_list['lady_jane'] = ['directed_by', 'written_by', 'starred_actors', 'release_year', 'has_genre']
Relation_list['the_young_and_prodigious_t.s._spivet'] = ['written_by', 'release_year', 'starred_actors', 'has_genre']
Relation_list['the_three_musketeers'] = ['directed_by', 'written_by', 'starred_actors', 'release_year', 'has_tags', 'has_genre']
Relation_list['anna_karenina'] = ['directed_by', 'written_by', 'starred_actors', 'release_year', 'has_tags', 'has_imdb_votes', 'has_genre']
Relation_list['incendiary'] = ['directed_by', 'written_by', 'starred_actors', 'release_year', 'has_genre']
Relation_list['local_hero'] = ['directed_by', 'written_by', 'starred_actors', 'release_year', 'has_genre']
[ChatGPT]
Statement: To find the languages of the films that share actors with the film 'Enid', I need to explore the graph with the given entity and related relations.
Helper function: exploreKG['planet_of_the_apes']=['in_language']
[User]
Execution result: 
['planet_of_the_apes', 'in_language', 'english']
[ChatGPT]
Statement: Now I get the languages of the films that share actors with the film 'Enid'. The answer of the claim is as follows.
['english']
Helper function: Verification['english']

Example 3)
Claim: which movie was [Diane Kurys] the director for?
Given Entity: ['Diane Kurys']

[ChatGPT]
Statement: I need the relations linked with the given entity.
Helper function: getRelation['Diane Kurys']
[User]
Execution result: 
Relation_list['Diane Kurys'] = ['~directed_by', '~written_by']
[ChatGPT]
Statement: Now, to find the movie that Diane Kurys was the director for, I need to explore the graph with the given entity and related relations.
Helper function: exploreKG['Diane Kurys']=['~directed_by']
[User]
Execution result: 
['Diane Kurys', '~directed_by', 'peppermint_soda'], ['Diane Kurys', '~directed_by', 'entre_nous']
[ChatGPT]
Statement: Now I get the movie that Diane Kurys was the director for. The answer of the claim is as follows.
['peppermint_soda', 'entre_nous']
Helper function: Verification['peppermint_soda', 'entre_nous']

Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>

"""


# stop_sig recommended to low-capacity LLMs
pr_1_stop_sig = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use below helper functions to find the evidence for finding labels.

<Helper functions>
1. getRelation[entity]: Returns the list of relations connected to the entities.
2. exploreKG[entity]=[list of relations]: Returns the corresponding tail entities in graph data starts from single entity in given entity and given relation.
3. Verification[list of entities]: If you can find the answer entities from collected evidences, give the answer.

You must follow the exact format of the given helper function. You can use multiple helper functions in one step by using '##' between functions.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for [User] response. If response has made, continue your [Your Task] (Do not make multiple 'Helper function: ' lines).
Importantly, you have to use inverse relation if you need. For example, if you want to find films starred by certain actors (when only actors were given), you have to use '~starred_actors' relation such as exploreKG['actor']=['~starred_actors'].

Here are some examples.

Example 1)
Claim: what genres do the films that share actors with [Man of Steel] fall under?
Given Entity: ['Man of Steel']

[Your Task]
Statement: I need the relations linked with the given entity.
Helper function: getRelation['Man of Steel']
*** Stop for [User] response ***
[User]
Execution result: Relation_list['Man of Steel'] = ['release_year', 'starred_actors', 'written_by', 'has_tags', 'directed_by']
[Your Task]
Statement: First, to solve the claim, I have to know the actors starred in 'Man of Steel'.
Helper function: exploreKG['Man of Steel']=['starred_actors']
*** Stop for [User] response ***
[User]
Execution result: ['Man of Steel', 'starred_actors', 'michael_shannon'], ['Man of Steel', 'starred_actors', 'henry_cavill'], ['Man of Steel', 'starred_actors', 'amy_adams'], ['Man of Steel', 'starred_actors', 'diane_lane']
[Your Task]
Statement: Next, I need films starred by previous given actors. To find the films, I need relations linked with the actors.
Helper function: getRelation['michael_shannon'] ## getRelation['henry_cavill'] ## getRelation['amy_adams'] ## getRelation['diane_lane']
*** Stop for [User] response ***
[User]
Execution result: Relation_list['michael_shannon'] = ['has_tags', 'starred_actors'], Relation_list['henry_cavill'] = ['starred_actors'], Relation_list['amy_adams'] = ['has_tags', 'starred_actors'], getRelations['diane_lane'] = ['has_tags', 'starred_actors']
[Your Task]
Statement: To get the films starred by previous actors, I need to explore the graph with each actors and related relations.
Helper function: exploreKG['michael_shannon']=['starred_actors'] ## exploreKG['henry_cavill']=['starred_actors'] ## exploreKG['amy_adams']=['starred_actors'] ## exploreKG['diane_lane']=['starred_actors']
*** Stop for [User] response ***
[User]
Execution result: ['michael_shannon', 'starred_actors', 'bug'], ['michael_shannon', 'starred_actors', 'machine_gun_preacher'], ['michael_shannon', 'starred_actors', 'young_ones'], ['michael_shannon', 'starred_actors', 'the_missing_person'], ['henry_cavill', 'starred_actors', 'immortals'], ['henry_cavill', 'starred_actors', 'blood_creek'], ['henry_cavill', 'starred_actors', 'the_cold_light_of_day'], ['amy_adams', 'starred_actors', 'moonlight_serenade'], ['amy_adams', 'starred_actors', 'american_hustle'], ['amy_adams', 'starred_actors', 'sunshine_cleaning'], ['amy_adams', 'starred_actors', 'the_fighter'], ['diane_lane', 'starred_actors', 'wild_bill'], ['diane_lane', 'starred_actors', 'the_glass_house'], ['diane_lane', 'starred_actors', 'jumper']
[Your Task]
Statement: To get the genres of the these films, I need to find the relations linked with all the films from previous step.
Helper function: getRelation['bug'] ## getRelation['machine_gun_preacher'] ## getRelation['young_ones'] ## getRelation['the_missing_person'] ## getRelation['immortals'] ## getRelation['blood_creek'] ## getRelation['the_cold_light_of_day'] ## getRelation['moonlight_serenade'] ## getRelation['american_hustle'] ## getRelation['sunshine_cleaning'] ## getRelation['the_fighter'] ## getRelation['wild_bill'] ## getRelation['the_glass_house'] ## getRelation['jumper']
*** Stop for [User] response ***
[User]
Execution result: Relation_list['bug'] = ['starred_actors', 'has_tags', 'written_by', 'release_year', 'has_genre', 'directed_by'], Relation_list['machine_gun_preacher'] = ['starred_actors', 'has_tags', 'written_by', 'release_year', 'has_genre', 'directed_by'], Relation_list['young_ones'] = ['starred_actors', 'has_genre', 'release_year'], Relation_list['the_missing_person'] = ['starred_actors', 'written_by', 'release_year', 'has_genre'], Relation_list['immortals'] = 'starred_actors', 'has_tags', 'release_year', 'has_genre', 'in_language'], Relation_list['blood_creek'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list['the_cold_light_of_day'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list['moonlight_serenade'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list['american_hustle'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list['sunshine_cleaning'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list['the_fighter'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list['wild_bill'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list['the_glass_house'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list['jumper'] = ['starred_actors', 'has_tags', 'release_year', 'directed_by']
[Your Task]
Statement: To get the genres of the films, I need to explore the graph with each films and related relations.
Helper function: exploreKG['bug']=['has_genre'] ## exploreKG['machine_gun_preacher']=['has_genre'] ## exploreKG['young_ones']=['has_genre'] ## exploreKG['the_missing_person']=['has_genre'] ## exploreKG['immortals']=['has_genre'] ## exploreKG['blood_creek']=['has_genre'] ## exploreKG['the_cold_light_of_day']=['has_genre'] ## exploreKG['moonlight_serenade']=['has_genre'] ## exploreKG['american_hustle']=['has_genre'] ## exploreKG['sunshine_cleaning']=['has_genre'] ## exploreKG['the_fighter']=['has_genre'] ## exploreKG['wild_bill']=['has_genre'] ## exploreKG['the_glass_house']=['has_genre'] ## exploreKG['jumper']=[]
*** Stop for [User] response ***
[User]
Execution result: ['bug', 'has_genre', 'horror'], ['machine_gun_preacher', 'has_genre', 'action'], ['young_ones', 'has_genre', 'action'], ['the_missing_person', 'has_genre', 'mystery'], ['the_missing_person', 'has_genre', 'drama'], ['the_missing_person', 'has_genre', 'comedy'], ['immortals', 'has_genre', 'fantasy'], ['blood_creek', 'has_genre', 'horror'], ['the_cold_light_of_day', 'has_genre', 'action'], ['moonlight_serenade', 'has_genre', 'romance'], ['moonlight_serenade', 'has_genre', 'drama'], ['moonlight_serenade', 'has_genre', 'musical'], ['american_hustle', 'has_genre', 'crime'], ['american_hustle', 'has_genre', 'drama'], ['sunshine_cleaning', 'has_genre', 'drama'], ['sunshine_cleaning', 'has_genre', 'comedy'], ['the_fighter', 'has_genre', 'drama'], ['the_fighter', 'has_genre', 'sport'], ['wild_bill', 'has_genre', 'western'], ['the_glass_house', 'has_genre', 'thriller']
[Your Task]
Statement: Now I get the genres of the films that share actors with 'Man of Steel'. The answer of the claim is as follows.
['horror', 'action', 'mystery', 'drama', 'comedy', 'fantasy', 'romance', 'musical', 'crime', 'sport', 'western', 'thriller']
Helper function: Verification['horror', 'action', 'mystery', 'drama', 'comedy', 'fantasy', 'romance', 'musical', 'crime', 'sport', 'western', 'thriller']


Example 2)
Claim: who are the actors in the films written by [John Travis]?
Given entity: ["John Travis"]

[Your Task]
Statement: I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function: getRelation['John Travis']
*** Stop for [User] response. ***
[User]
Execution result: Relation_list['John Travis'] = ['written_by']
[Your Task]
Statement: Now, to find the films that 'John Travis' written, I need to explore the graph from 'John Travis' with related relations.
Helper function: exploreKG['John Travis']=['written_by']
*** Stop for [User] response. ***
[User]
Execution result: ['John Travis', 'written_by', 'the_haunting_of_molly_hartley']
[Your Task]
Statement: Now, we have to find the actors in the previous given film.
Helper function: getRelation['the_haunting_of_molly_hartley']
*** Stop for [User] response. ***
[User]
Execution result: Relation_list['the_haunting_of_molly_hartley'] = ['has_genre', 'starred_actors', 'directed_by', 'release_year', 'written_by']
[Your Task]
Statement: To get the actors in the film, I need to explore the graph with the film and related relations.
Helper function: exploreKG['the_haunting_of_molly_hartley']=['starred_actors']
*** Stop for [User] response. ***
[User]
Execution result: ['the_haunting_of_molly_hartley', 'starred_actors', 'haley_bennett'], ['the_haunting_of_molly_hartley', 'starred_actors', 'chace_crawford'], ['the_haunting_of_molly_hartley', 'starred_actors', 'jake_weber']
[Your Task]
Statement: Now I get the actors of the films written by 'John Travis'. The answer of the claim is as follows.
['haley_bennett', 'chace_crawford', 'jake_weber']
Helper function: Verification['haley_bennett', 'chace_crawford', 'jake_weber']

Example 3)
Claim: what does [Hiromi Nagasaku] star in?
Given entity: ["Hiromi Nagasaku"]

[Your Task]
Statement: I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function: getRelation["Hiromi Nagasaku"]
*** Stop for [User] response. ***
[User]
Execution result: Relation_list["Hiromi Nagasaku"] = ['starred_actors']
[Your Task]
Statement: Now, to find the films that 'Hiromi Nagasaku' starred, I need to explore the graph from 'Hiromi Nagasaku' with related relations.
Helper function: exploreKG['Hiromi Nagasaku']=['starred_actors']
*** Stop for [User] response. ***
[User]
Execution result: ['Hiromi Nagasaku', 'starred_actors', 'doppleganger']
[Your Task]
Statement: Now I get the films starred by 'Hiromi Nagasaku'. The answer of the claim is as follows.
['doppleganger']
Helper function: Verification['doppleganger']

Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>

"""

pr_2_stop_sig = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use below helper functions to find the evidence for finding labels.

<Helper functions>
1. getRelation[entity]: Returns the list of relations connected to the entities.
2. exploreKG[entity]=[list of relations]: Returns the corresponding tail entities in graph data starts from single entity in given entity and given relation.
3. Verification[list of entities]: If you can find the answer entities from collected evidences, give the answer.

You must follow the exact format of the given helper function. You can use multiple helper functions in one step by using '##' between functions.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for [User] response. If response has made, continue your [Your Task] (Do not make multiple 'Helper function: ' lines).
Importantly, you have to use inverse relation if you need. For example, if you want to find films starred by certain actors (when only actors were given), you have to use '~starred_actors' relation such as exploreKG['actor']=['~starred_actors'].

Here are some examples.

Example 1)
Claim: who directed the movies written by the writer of [Millennium Actress]?
Given Entity: ['Millennium Actress']

[Your Task]
Statement: I need the relations linked with the given entity.
Helper function: getRelation['Millennium Actress']
*** Stop for [User] response. ***
[User]
Execution result: 
Relation_list['Millennium Actress'] = ['directed_by', 'written_by', 'release_year', 'in_language', 'has_tags']
[Your Task]
Statement: Now, to find the writer of 'Millennium Actress', I need to explore the graph with the given entity and related relations.
Helper function: exploreKG['Millennium Actress']=['written_by']
*** Stop for [User] response. ***
[User]
Execution result: 
['Millennium Actress', 'written_by', 'satoshi_kon']
[Your Task]
Statement: Now, to find the movies written by 'satoshi_kon', I need to explore the graph to find the proper relation.
Helper function: exploreKG['satoshi_kon']=['~written_by', '~directed_by', '~has_tags']
*** Stop for [User] response. ***
[User]
Execution result: 
['satoshi_kon', '~written_by', 'paprika'], ['satoshi_kon', '~written_by', 'tokyo_godfathers']
[Your Task]
Statement: Now, I have to find the director of the films found in previous step.
Helper function: getRelation['paprika'] ## getRelation['tokyo_godfathers']
*** Stop for [User] response. ***
[User]
Execution result: 
Relation_list['paprika'] = ['directed_by', 'written_by', 'release_year', 'in_language', 'has_tags']
Relation_list['tokyo_godfathers'] = ['directed_by', 'written_by', 'release_year', 'in_language', 'has_tags']
[Your Task]
Statement: Now, I have to find the director of the films found in previous step.
Helper function: exploreKG['paprika']=['directed_by'] ## exploreKG['tokyo_godfathers']=['directed_by']
*** Stop for [User] response. ***
[User]
Execution result: 
['paprika', 'directed_by', 'satoshi_kon']
['tokyo_godfathers', 'directed_by', 'satoshi_kon']
[Your Task]
Statement: Now I get the directors of the films written by the writer of 'Millennium Actress'. The answer of the claim is as follows.
['satoshi_kon']
Helper function: Verification['satoshi_kon']

Example 2)
Claim: when did the movies directed by the [The Champ] director release?
Given Entity: ['The Champ']

[Your Task]
Statement: I need the relations linked with the given entity.
Helper function: getRelation['The Champ']
*** Stop for [User] response. ***
[User]
Execution result: 
Relation_list['The Champ'] = ['directed_by', 'written_by', 'release_year', 'has_tags', 'starred_actors']
[Your Task]
Statement: Now, to find the director of 'The Champ', I need to explore the graph with the given entity and related relations.
Helper function: exploreKG['The Champ']=['directed_by']
*** Stop for [User] response. ***
[User]
Execution result: 
['The Champ', 'directed_by', 'king_vidor'], ['The Champ', 'directed_by', 'franco_zeffirelli']
[Your Task]
Statement: Now I get the directors of 'The Champ'. For the next step, I need to find the movies directed by the directors.
Helper function: getRelation['king_vidor'] ## getRelation['franco_zeffirelli']
*** Stop for [User] response. ***
[User]
Execution result: 
Relation_list['king_vidor'] = ['~written_by', '~directed_by', '~has_tags']
Relation_list['franco_zeffirelli'] = ['~written_by', '~directed_by', '~has_tags']
[Your Task]
Statement: Now, I need to find the movies directed by the directors using proper relations.
Helper function: exploreKG['king_vidor']=['~directed_by'] ## exploreKG['franco_zeffirelli']=['~directed_by']
*** Stop for [User] response. ***
[User]
Execution result: 
['king_vidor', '~directed_by', 'war_and_peace'], ['king_vidor', '~directed_by', 'bird_of_paradise'], ['king_vidor', '~directed_by', 'ruby_gentry'], ['king_vidor', '~directed_by', 'comrade_x'], ['king_vidor', '~directed_by', 'our_daily_bread'], ['king_vidor', '~directed_by', 'the_patsy'], ['king_vidor', '~directed_by', 'the_fountainhead'], ['king_vidor', '~directed_by', 'duel_in_the_sun']
['franco_zeffirelli', '~directed_by', 'endless_love'], ['franco_zeffirelli', '~directed_by', 'otello'], ['franco_zeffirelli', '~directed_by', 'hamlet'], ['franco_zeffirelli', '~directed_by', 'jane_eyre'], ['franco_zeffirelli', '~directed_by', 'callas_forever']
[Your Task]
Statement: Now I get the movies directed by the directors of 'The Champ'. Finally, I need to find the release year of the all movies.
Helper function: getRelation['war_and_peace'] ## getRelation['bird_of_paradise'] ## getRelation['ruby_gentry'] ## getRelation['comrade_x'] ## getRelation['our_daily_bread'] ## getRelation['the_patsy'] ## getRelation['the_fountainhead'] ## getRelation['duel_in_the_sun'] ## getRelation['endless_love'] ## getRelation['otello'] ## getRelation['hamlet'] ## getRelation['jane_eyre'] ## getRelation['callas_forever']
*** Stop for [User] response. ***
[User]
Execution result: 
Relation_list['war_and_peace'] = ['directed_by', 'written_by', 'release_year', 'has_genre', 'in_language', 'has_tags', 'starred_actors']
Relation_list['bird_of_paradise'] = ['has_genre', 'directed_by', 'starred_actors', 'release_year']
Relation_list['ruby_gentry'] = ['starred_actors', 'directed_by', 'release_year']
Relation_list['comrade_x'] = ['has_genre', 'directed_by', 'starred_actors', 'release_year']
Relation_list['our_daily_bread'] = ['directed_by', 'written_by', 'release_year', 'starred_actors', 'has_tags', 'has_genre']
Relation_list['the_patsy'] = ['directed_by', 'written_by', 'release_year', 'has_genre', 'has_tags', 'starred_actors']
Relation_list['the_fountainhead'] = ['directed_by', 'written_by', 'release_year', 'has_genre', 'has_tags', 'starred_actors']
Relation_list['duel_in_the_sun'] = ['directed_by', 'written_by', 'release_year', 'has_genre', 'has_tags', 'starred_actors']
Relation_list['endless_love'] = ['has_genre', 'directed_by', 'starred_actors', 'release_year']
Relation_list['otello'] = ['has_genre', 'directed_by', 'starred_actors', 'release_year']
Relation_list['hamlet'] = ['has_genre', 'directed_by', 'starred_actors', 'release_year']
Relation_list['jane_eyre'] = ['directed_by', 'written_by', 'release_year', 'has_genre', 'has_tags', 'starred_actors']
Relation_list['callas_forever'] = ['has_genre', 'directed_by', 'starred_actors', 'release_year']
[Your Task]
Statement: Now to find the release year of the movies, I need to find the release year of the movies using proper relations.
Helper function: exploreKG['war_and_peace']=['release_year'] ## exploreKG['bird_of_paradise']=['release_year'] ## exploreKG['ruby_gentry']=['release_year'] ## exploreKG['comrade_x']=['release_year'] ## exploreKG['our_daily_bread']=['release_year'] ## exploreKG['the_patsy']=['release_year'] ## exploreKG['the_fountainhead']=['release_year'] ## exploreKG['duel_in_the_sun']=['release_year'] ## exploreKG['endless_love']=['release_year'] ## exploreKG['otello']=['release_year'] ## exploreKG['hamlet']=['release_year'] ## exploreKG['jane_eyre']=['release_year'] ## exploreKG['callas_forever']=['release_year']
*** Stop for [User] response. ***
[User]
Execution result: 
['war_and_peace', 'release_year', '1956'], ['war_and_peace', 'release_year', '1966']
['bird_of_paradise', 'release_year', '1932']
['ruby_gentry', 'release_year', '1952']
['comrade_x', 'release_year', '1940']
['our_daily_bread', 'release_year', '1934'], ['our_daily_bread', 'release_year', '2005']
['the_patsy', 'release_year', '1928'], ['the_patsy', 'release_year', '1964']
['the_fountainhead', 'release_year', '1949']
['duel_in_the_sun', 'release_year', '1946']
['endless_love', 'release_year', '2014'], ['endless_love', 'release_year', '1981']
['otello', 'release_year', '1986']
['hamlet', 'release_year', '2009'], ['hamlet', 'release_year', '1996'], ['hamlet', 'release_year', '1964'], ['hamlet', 'release_year', '1990'], ['hamlet', 'release_year', '2000'], ['hamlet', 'release_year', '1969'], ['hamlet', 'release_year', '1948']
['jane_eyre', 'release_year', '1970'], ['jane_eyre', 'release_year', '2011'], ['jane_eyre', 'release_year', '1943'], ['jane_eyre', 'release_year', '1996']
['callas_forever', 'release_year', '2002']
[Your Task]
Statement: Now I get the release year of the movies directed by the director of 'The Champ'. The answer of the claim is as follows.
['1928', '1932', '1934', '1940', '1943', '1946', '1948', '1949', '1952', '1956', '1964', '1966', '1969', '1970', '1981', '1986', '1990', '1996', '2000', '2002', '2005', '2009', '2011', '2014']
Helper function: Verification['1928', '1932', '1934', '1940', '1943', '1946', '1948', '1949', '1952', '1956', '1964', '1966', '1969', '1970', '1981', '1986', '1990', '1996', '2000', '2002', '2005', '2009', '2011', '2014']

Example 3)
Claim: what film genre is [Crazy Safari]?
Given Entity: ['Crazy Safari']

[Your Task]
Statement: I need the relations linked with the given entity.
Helper function: getRelation['Crazy Safari']    
*** Stop for [User] response. ***
[User]
Execution result: 
Relation_list['Crazy Safari'] = ['directed_by', 'release_year', 'has_genre']
[Your Task]
Statement: Now, to find the genre of 'Crazy Safari', I need to explore the graph with the given entity and related relations.
Helper function: exploreKG['Crazy Safari']=['has_genre']
*** Stop for [User] response. ***
[User]
Execution result: 
['Crazy Safari', 'has_genre', 'comedy']
[Your Task]
Statement: Now I get the genre of 'Crazy Safari'. The answer of the claim is as follows.
['comedy']
Helper function: Verification['comedy']


Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>

"""

pr_3_stop_sig = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use below helper functions to find the evidence for finding labels.

<Helper functions>
1. getRelation[entity]: Returns the list of relations connected to the entities.
2. exploreKG[entity]=[list of relations]: Returns the corresponding tail entities in graph data starts from single entity in given entity and given relation.
3. Verification[list of entities]: If you can find the answer entities from collected evidences, give the answer.

You must follow the exact format of the given helper function. You can use multiple helper functions in one step by using '##' between functions.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for [User] response. If response has made, continue your [Your Task] (Do not make multiple 'Helper function: ' lines).
Importantly, you have to use inverse relation if you need. For example, if you want to find films starred by certain actors (when only actors were given), you have to use '~starred_actors' relation such as exploreKG['actor']=['~starred_actors'].

Here are some examples.

Example 1)
Claim: who co-wrote films with [Veikko Huovinen]?
Given Entity: ['Veikko Huovinen']

[Your Task]
Statement: I need the relations linked with the given entity.
Helper function: getRelation['Veikko Huovinen']
*** Stop for [User] response. ***
[User]
Execution result: 
Relation_list['Veikko Huovinen'] = ['~written_by']
[Your Task]
Statement: Now, to find the films co-written by 'Veikko Huovinen', I need to first find the film written by 'Veikko Huovinen'. I need to explore the graph with the given entity and related relations.
Helper function: exploreKG['Veikko Huovinen']=['~written_by']
*** Stop for [User] response. ***
[User]
Execution result: 
['Veikko Huovinen', '~written_by', 'dog_nail_clipper']
[Your Task]
Statement: Now I get the films written by 'Veikko Huovinen'. I need to find the writers of the film co-written by 'Veikko Huovinen'.
Helper function: getRelation['dog_nail_clipper']
*** Stop for [User] response. ***
[User]
Execution result: 
Relation_list['dog_nail_clipper'] = ['directed_by', 'written_by', 'starred_actors', 'in_language', 'release_year']
[Your Task]
Statement: To find the writers of the film co-written by 'Veikko Huovinen', I need to explore the graph with the given entity and related relations.
Helper function: exploreKG['dog_nail_clipper']=['written_by']
*** Stop for [User] response. ***
[User]
Execution result: 
['dog_nail_clipper', 'written_by', 'markku_pölönen']
[Your Task]
Statement: Now I get the writers of the film co-written by 'Veikko Huovinen'. The answer of the claim is as follows.
['markku_pölönen']
Helper function: Verification['markku_pölönen']

Example 2)
Claim: the films that share actors with the film [Enid] were in which languages?
Given Entity: ['Enid']  

[Your Task]
Statement: I need the relations linked with the given entity.
Helper function: getRelation['Enid']
*** Stop for [User] response. ***
[User]
Execution result: 
Relation_list['Enid'] = ['release_year', 'has_genre', 'directed_by', 'starred_actors']
[Your Task]
Statement: Now, to find the films that share actors with the film 'Enid', I need to explore the graph with the given entity and related relations.
Helper function: exploreKG['Enid']=['starred_actors']
*** Stop for [User] response. ***
[User]
Execution result: 
['Enid', 'starred_actors', 'helena_bonham_carter'], ['Enid', 'starred_actors', 'matthew_macfadyen'], ['Enid', 'starred_actors', 'denis_lawson']
[Your Task]
Statement: Now I get the actors that share actors with the film 'Enid'. I need to find the films of the actors from the previous result.
Helper function: getRelation['helena_bonham_carter'] ## getRelation['matthew_macfadyen'] ## getRelation['denis_lawson']
*** Stop for [User] response. ***
[User]
Execution result: 
Relation_list['helena_bonham_carter'] = ['~starred_actors', '~has_tags']
Relation_list['matthew_macfadyen'] = ['~starred_actors', '~has_tags']
Relation_list['denis_lawson'] = ['~starred_actors']
[Your Task]
Statement: To find the films that share actors with the film 'Enid', I need to explore the graph with the given entity and related relations.
Helper function: exploreKG['helena_bonham_carter']=['~starred_actors'] ## exploreKG['matthew_macfadyen']=['~starred_actors'] ## exploreKG['denis_lawson']=['~starred_actors']
*** Stop for [User] response. ***
[User]
Execution result: 
['helena_bonham_carter', '~starred_actors', 'conversations_with_other_women'], ['helena_bonham_carter', '~starred_actors', 'the_gruffalo'], ['helena_bonham_carter', '~starred_actors', 'planet_of_the_apes'], ['helena_bonham_carter', '~starred_actors', 'lady_jane'], ['helena_bonham_carter', '~starred_actors', 'the_young_and_prodigious_t.s._spivet']
['matthew_macfadyen', '~starred_actors', 'the_three_musketeers'], ['matthew_macfadyen', '~starred_actors', 'anna_karenina'], ['matthew_macfadyen', '~starred_actors', 'incendiary']
['denis_lawson', '~starred_actors', 'local_hero']
[Your Task]
Statement: Now I get the films that share actors with the film 'Enid'. Finally, I need to find the languages of the films.
Helper function: getRelation['conversations_with_other_women'] ## getRelation['the_gruffalo'] ## getRelation['planet_of_the_apes'] ## getRelation['lady_jane'] ## getRelation['the_young_and_prodigious_t.s._spivet'] ## getRelation['the_three_musketeers'] ## getRelation['anna_karenina'] ## getRelation['incendiary'] ## getRelation['local_hero']
*** Stop for [User] response. ***
[User]
Execution result: 
Relation_list['conversations_with_other_women'] = ['directed_by', 'written_by', 'starred_actors', 'release_year', 'has_tags', 'has_genre']
Relation_list['the_gruffalo'] = ['directed_by', 'written_by', 'starred_actors', 'release_year', 'has_genre']
Relation_list['planet_of_the_apes'] = ['directed_by', 'written_by', 'starred_actors', 'in_language', 'release_year', 'has_tags']
Relation_list['lady_jane'] = ['directed_by', 'written_by', 'starred_actors', 'release_year', 'has_genre']
Relation_list['the_young_and_prodigious_t.s._spivet'] = ['written_by', 'release_year', 'starred_actors', 'has_genre']
Relation_list['the_three_musketeers'] = ['directed_by', 'written_by', 'starred_actors', 'release_year', 'has_tags', 'has_genre']
Relation_list['anna_karenina'] = ['directed_by', 'written_by', 'starred_actors', 'release_year', 'has_tags', 'has_imdb_votes', 'has_genre']
Relation_list['incendiary'] = ['directed_by', 'written_by', 'starred_actors', 'release_year', 'has_genre']
Relation_list['local_hero'] = ['directed_by', 'written_by', 'starred_actors', 'release_year', 'has_genre']
[Your Task]
Statement: To find the languages of the films that share actors with the film 'Enid', I need to explore the graph with the given entity and related relations.
Helper function: exploreKG['planet_of_the_apes']=['in_language']
*** Stop for [User] response. ***
[User]
Execution result: 
['planet_of_the_apes', 'in_language', 'english']
[Your Task]
Statement: Now I get the languages of the films that share actors with the film 'Enid'. The answer of the claim is as follows.
['english']
Helper function: Verification['english']

Example 3)
Claim: which movie was [Diane Kurys] the director for?
Given Entity: ['Diane Kurys']

[Your Task]
Statement: I need the relations linked with the given entity.
Helper function: getRelation['Diane Kurys']
*** Stop for [User] response. ***
[User]
Execution result: 
Relation_list['Diane Kurys'] = ['~directed_by', '~written_by']
[Your Task]
Statement: Now, to find the movie that Diane Kurys was the director for, I need to explore the graph with the given entity and related relations.
Helper function: exploreKG['Diane Kurys']=['~directed_by']
*** Stop for [User] response. ***
[User]
Execution result: 
['Diane Kurys', '~directed_by', 'peppermint_soda'], ['Diane Kurys', '~directed_by', 'entre_nous']
[Your Task]
Statement: Now I get the movie that Diane Kurys was the director for. The answer of the claim is as follows.
['peppermint_soda', 'entre_nous']
Helper function: Verification['peppermint_soda', 'entre_nous']

Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>

"""
