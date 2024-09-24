prompt2 = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use below helper functions to find the evidence for finding labels.

<Helper functions>
1. getRelation([list of entities]): Returns the list of relations connected to the entities.
2. exploreKG([list of entities]: [relation]): Returns the corresponding tail entities in graph data starts from single entity in entity list and given relation.
3. Verification([list of entities]): Once verification is done, call this function with labels.

You must follow the exact format of the given helper function.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for my response. If response has made, continue your Statement task.
Importantly, you have to you inverse relation if you need. For example, if you want to find films starred by certain actors (when only actors were given), you have to use 'starred_actors' relation.

Here are some examples.

Example 1)
Claim: what genres do the films that share actors with [Man of Steel] fall under?
Given Entity: [‘Man of Steel’]

[ChatGPT]
Statement: I need the relations linked with the given entity.
Helper function: getRelation([’Man of Steel’])
[User]
Execution result: Relation_list(['Man of Steel']) = ['release_year', 'starred_actors', 'written_by', 'has_tags', 'directed_by']
[ChatGPT]
Statement: First, to solve the claim, I have to know the actors starred in ‘Man of Steel’.
Helper function: exploreKG(['Man of Steel']: ['starred_actors'])
[User]
Execution result: ['michael_shannon', 'henry_cavill', 'amy_adams', 'diane_lane']
[ChatGPT]
Statement: Next, I need films starred by previous given actors. To find the films, I need relations linked with the actors.
Helper function: getRelation(['michael_shannon', 'henry_cavill', 'amy_adams', 'diane_lane'])
[User]
Execution result: Relation_list(['michael_shannon', 'henry_cavill', 'amy_adams', 'diane_lane']) = ['starred_actors', 'has_tags']
[ChatGPT]
Statement: To get the films starred by previous actors, I need to explore the graph with each actors and related relations.
Helper function: exploreKG(['michael_shannon', 'henry_cavill', 'amy_adams', 'diane_lane']: ['starred_actors'])
[User]
Execution result: ['the_wedding_date', 'the_cold_light_of_day', 'cinema_verite', 'standing_still', 'six_pack', 'the_cotton_club', 'my_new_gun', 'untraceable', 'shotgun_stories', 'return', 'nights_in_rodanthe', 'a_little_romance', 'cruel_intentions_2', 'the_glass_house', '99_homes', 'doubt', 'jack', 'blood_creek', 'wild_bill', 'sunshine_cleaning', 'the_runaways', "charlie_wilson's_war", 'american_hustle', 'a_streetcar_named_desire', 'jumper', 'leap_year', 'the_fighter', 'a_walk_on_the_moon', 'the_missing_person', 'on_the_road', 'moonlight_serenade', 'enchanted', 'immortals', 'machine_gun_preacher', 'the_muppets', 'hollywoodland', 'young_ones', 'the_big_town', 'under_the_tuscan_sun', 'bug', 'unfaithful', 'the_perfect_storm', 'must_love_dogs', 'big_eyes', 'fierce_people', 'secretariat', 'man_of_steel', 'the_iceman', 'take_shelter', 'streets_of_fire', 'murder_at_1600', 'killshot']
[ChatGPT]
Statement: To get the genres of the these films, I need to find the relations linked with the films from previous step.
Helper function: getRelation(['the_wedding_date', 'the_cold_light_of_day', 'cinema_verite', 'standing_still', 'six_pack', 'the_cotton_club', 'my_new_gun', 'untraceable', 'shotgun_stories', 'return', 'nights_in_rodanthe', 'a_little_romance', 'cruel_intentions_2', 'the_glass_house', '99_homes', 'doubt', 'jack', 'blood_creek', 'wild_bill', 'sunshine_cleaning', 'the_runaways', "charlie_wilson's_war", 'american_hustle', 'a_streetcar_named_desire', 'jumper', 'leap_year', 'the_fighter', 'a_walk_on_the_moon', 'the_missing_person', 'on_the_road', 'moonlight_serenade', 'enchanted', 'immortals', 'machine_gun_preacher', 'the_muppets', 'hollywoodland', 'young_ones', 'the_big_town', 'under_the_tuscan_sun', 'bug', 'unfaithful', 'the_perfect_storm', 'must_love_dogs', 'big_eyes', 'fierce_people', 'secretariat', 'man_of_steel', 'the_iceman', 'take_shelter', 'streets_of_fire', 'murder_at_1600', 'killshot'])
[User]
Execution result: Relation_list(['the_wedding_date', 'the_cold_light_of_day', 'cinema_verite', 'standing_still', 'six_pack', 'the_cotton_club', 'my_new_gun', 'untraceable', 'shotgun_stories', 'return', 'nights_in_rodanthe', 'a_little_romance', 'cruel_intentions_2', 'the_glass_house', '99_homes', 'doubt', 'jack', 'blood_creek', 'wild_bill', 'sunshine_cleaning', 'the_runaways', "charlie_wilson's_war", 'american_hustle', 'a_streetcar_named_desire', 'jumper', 'leap_year', 'the_fighter', 'a_walk_on_the_moon', 'the_missing_person', 'on_the_road', 'moonlight_serenade', 'enchanted', 'immortals', 'machine_gun_preacher', 'the_muppets', 'hollywoodland', 'young_ones', 'the_big_town', 'under_the_tuscan_sun', 'bug', 'unfaithful', 'the_perfect_storm', 'must_love_dogs', 'big_eyes', 'fierce_people', 'secretariat', 'man_of_steel', 'the_iceman', 'take_shelter', 'streets_of_fire', 'murder_at_1600', 'killshot']) = ['release_year', 'in_language', 'starred_actors', 'written_by', 'has_tags', 'has_imdb_rating', 'has_genre', 'has_tags', 'directed_by']
[ChatGPT]
Statement: To get the genres of the films, I need to explore the graph with each films and related relations.
Helper function: exploreKG(['the_wedding_date', 'the_cold_light_of_day', 'cinema_verite', 'standing_still', 'six_pack', 'the_cotton_club', 'my_new_gun', 'untraceable', 'shotgun_stories', 'return', 'nights_in_rodanthe', 'a_little_romance', 'cruel_intentions_2', 'the_glass_house', '99_homes', 'doubt', 'jack', 'blood_creek', 'wild_bill', 'sunshine_cleaning', 'the_runaways', "charlie_wilson's_war", 'american_hustle', 'a_streetcar_named_desire', 'jumper', 'leap_year', 'the_fighter', 'a_walk_on_the_moon', 'the_missing_person', 'on_the_road', 'moonlight_serenade', 'enchanted', 'immortals', 'machine_gun_preacher', 'the_muppets', 'hollywoodland', 'young_ones', 'the_big_town', 'under_the_tuscan_sun', 'bug', 'unfaithful', 'the_perfect_storm', 'must_love_dogs', 'big_eyes', 'fierce_people', 'secretariat', 'man_of_steel', 'the_iceman', 'take_shelter', 'streets_of_fire', 'murder_at_1600', 'killshot']: ['has_genre'])
[User]
Execution result: ['crime', 'sport', 'horror', 'musical', 'comedy', 'mystery', 'drama', 'romance', 'western', 'adventure', 'action', 'thriller', 'fantasy']
[ChatGPT]
Statement: Now I get the genres of the films that share actors with 'Man of Steel'. The answer of the claim is as follows.
['crime', 'sport', 'horror', 'musical', 'comedy', 'mystery', 'drama', 'romance', 'western', 'adventure', 'action', 'thriller', 'fantasy']
Helper function: Verification(['crime', 'sport', 'horror', 'musical', 'comedy', 'mystery', 'drama', 'romance', 'western', 'adventure', 'action', 'thriller', 'fantasy'])

Example 2)
Claim: the films that share actors with the film [Creepshow] were in which languages?
Given entity: ["Creepshow"]

Statement: I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function: getRelation(['Creepshow'])
[User]
Execution result: Relation_list(['Creepshow']) = ['has_genre', 'has_tags', 'starred_actors', 'directed_by', 'written_by', 'release_year']
[ChatGPT]
Statement: Now, to find the actors starred in 'Creepshow', I need to explore the graph from 'Creepshow' with related relations.
Helper function: exploreKG(['Creepshow']: ['starred_actors'])
[User]
Execution result: ['fritz_weaver', 'hal_holbrook', 'adrienne_barbeau', 'leslie_nielsen']
[ChatGPT]
Statement: Now, we need to find the films starred by previous actors.
Helper function: getRelation(['fritz_weaver', 'hal_holbrook', 'adrienne_barbeau', 'leslie_nielsen']) 
[User]
Execution result: Relation_list(['fritz_weaver', 'hal_holbrook', 'adrienne_barbeau', 'leslie_nielsen']) = ['has_tags', 'starred_actors']
[ChatGPT]
Statement: To get the films, I need to explore the graph with each actors and related relation.
Helper function: exploreKG(['fritz_weaver', 'hal_holbrook', 'adrienne_barbeau', 'leslie_nielsen']: ['starred_actors'])
[User]
Execution result: ['wild_in_the_streets', "the_creature_wasn't_nice", 'repossessed', 'the_sheepman', 'creepshow', 'harvey', 'superhero_movie', 'the_kidnapping_of_the_president', "someone's_watching_me!", 'two_evil_eyes', 'camouflage', 'the_firm', 'forbidden_planet', 'rent-a-kid', 'that_evening_sun', 'spy_hard', 'the_majestic', 'the_fog', 'wrongfully_accused', 'they_only_kill_their_masters', 'santa_who?', 'tammy_and_the_bachelor', 'prom_night', 'swamp_thing', 'the_star_chamber', 'mr._magoo', 'unholy']
[ChatGPT]
Statement: Now, we need to find the language of the films.
Helper function: getRelation(['wild_in_the_streets', "the_creature_wasn't_nice", 'repossessed', 'the_sheepman', 'creepshow', 'harvey', 'superhero_movie', 'the_kidnapping_of_the_president', "someone's_watching_me!", 'two_evil_eyes', 'camouflage', 'the_firm', 'forbidden_planet', 'rent-a-kid', 'that_evening_sun', 'spy_hard', 'the_majestic', 'the_fog', 'wrongfully_accused', 'they_only_kill_their_masters', 'santa_who?', 'tammy_and_the_bachelor', 'prom_night', 'swamp_thing', 'the_star_chamber', 'mr._magoo', 'unholy']) 
[User]
Execution result: Relation_list(['wild_in_the_streets', "the_creature_wasn't_nice", 'repossessed', 'the_sheepman', 'creepshow', 'harvey', 'superhero_movie', 'the_kidnapping_of_the_president', "someone's_watching_me!", 'two_evil_eyes', 'camouflage', 'the_firm', 'forbidden_planet', 'rent-a-kid', 'that_evening_sun', 'spy_hard', 'the_majestic', 'the_fog', 'wrongfully_accused', 'they_only_kill_their_masters', 'santa_who?', 'tammy_and_the_bachelor', 'prom_night', 'swamp_thing', 'the_star_chamber', 'mr._magoo', 'unholy']) = ['has_genre', 'has_tags', 'starred_actors', 'has_imdb_rating', 'in_language', 'directed_by', 'written_by', 'release_year']
[ChatGPT]
Statement: To get the languages of several films, I need to explore the graph with each films and related relations.
Helper function: exploreKG(['wild_in_the_streets', "the_creature_wasn't_nice", 'repossessed', 'the_sheepman', 'creepshow', 'harvey', 'superhero_movie', 'the_kidnapping_of_the_president', "someone's_watching_me!", 'two_evil_eyes', 'camouflage', 'the_firm', 'forbidden_planet', 'rent-a-kid', 'that_evening_sun', 'spy_hard', 'the_majestic', 'the_fog', 'wrongfully_accused', 'they_only_kill_their_masters', 'santa_who?', 'tammy_and_the_bachelor', 'prom_night', 'swamp_thing', 'the_star_chamber', 'mr._magoo', 'unholy']: ['in_language'])
[User]
Execution result: ['polish', 'english']
[ChatGPT]
Statement: Now I get the language of the films that share actors starred by 'Creepshow'. The answer of the claim is as follows.
['polish', 'english']
Helper function: Verification(['polish', 'english'])

Example 3)
Claim: who are the actors in the films written by [John Travis]?
Given entity: ["John Travis"]

Statement: I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function: getRelation(['John Travis'])
[User]
Execution result: Relation_list(['John Travis']) = ['written_by']
[ChatGPT]
Statement: Now, to find the films that 'John Travis' written, I need to explore the graph from 'John Travis' with related relations.
Helper function: exploreKG(['John Travis']: ['written_by'])
[User]
Execution result: ['the_haunting_of_molly_hartley']
[ChatGPT]
Statement: Now, we have to find the actors in the previous given film.
Helper function: getRelation(['the_haunting_of_molly_hartley'])
[User]
Execution result: Relation_list(['the_haunting_of_molly_hartley']) = ['has_genre', 'starred_actors', 'directed_by', 'release_year', 'written_by']
[ChatGPT]
Statement: To get the actors in the film, I need to explore the graph with the film and related relations.
Helper function: exploreKG(['the_haunting_of_molly_hartley']: ['starred_actors'])
[User]
Execution result: ['haley_bennett', 'chace_crawford', 'jake_weber']
[ChatGPT]
Statement: Now I get the actors of the films written by 'John Travis'. The answer of the claim is as follows.
['haley_bennett', 'chace_crawford', 'jake_weber']
Helper function: Verification(['haley_bennett', 'chace_crawford', 'jake_weber'])

Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>
"""

# Upper prompt is integrating all the relations for the candidate entities. However, our FactKG framework doesn't. It looks all the relations for each entity.
# This below prompt is the same way with it.
prompt_integrated = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use below helper functions to find the evidence for finding labels.

<Helper functions>
1. getRelation(entity): Returns the list of relations connected to the entities.
2. exploreKG(entity: [relation]): Returns the corresponding tail entities in graph data starts from single entity in given entity and given relation.
3. Verification([list of entities]): After getting enough evidence after exploreKG() helper function and if verification can be done, call this function with labels.

You must follow the exact format of the given helper function.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for my response. If response has made, continue your 'Statement' task.
Importantly, you have to use inverse relation if you need. For example, if you want to find films starred by certain actors (when only actors were given), you have to use 'starred_actors' relation.

Here are some examples.

Example 1)
Claim: what genres do the films that share actors with [Man of Steel] fall under?
Given Entity: ['Man of Steel']

[ChatGPT]
Statement: I need the relations linked with the given entity.
Helper function: getRelation('Man of Steel')
[User]
Execution result: Relation_list('Man of Steel') = ['release_year', 'starred_actors', 'written_by', 'has_tags', 'directed_by']
[ChatGPT]
Statement: First, to solve the claim, I have to know the actors starred in ‘Man of Steel’.
Helper function: exploreKG('Man of Steel': ['starred_actors'])
[User]
Execution result: ['michael_shannon', 'henry_cavill', 'amy_adams', 'diane_lane']
[ChatGPT]
Statement: Next, I need films starred by previous given actors. To find the films, I need relations linked with the actors.
Helper function: getRelation('michael_shannon'), getRelation('henry_cavill'), getRelation('amy_adams'), getRelation('diane_lane')
[User]
Execution result: Relation_list('michael_shannon') = ['has_tags', 'starred_actors'], Relation_list('henry_cavill') = ['starred_actors'], Relation_list('amy_adams') = ['has_tags', 'starred_actors'], getRelations('diane_lane') = ['has_tags', 'starred_actors']
[ChatGPT]
Statement: To get the films starred by previous actors, I need to explore the graph with each actors and related relations.
Helper function: exploreKG('michael_shannon': ['starred_actors']), exploreKG('henry_cavill': ['starred_actors']), exploreKG('amy_adams': ['starred_actors']), exploreKG('diane_lane': ['starred_actors'])
[User]
Execution result: ['michael_shannon', 'starred_actors', 'bug'], ['michael_shannon', 'starred_actors', 'machine_gun_preacher'], ['michael_shannon', 'starred_actors', 'young_ones'], ['michael_shannon', 'starred_actors', 'the_missing_person'], ['henry_cavill', 'starred_actors', 'immortals'], ['henry_cavill', 'starred_actors', 'blood_creek'], ['henry_cavill', 'starred_actors', 'the_cold_light_of_day'], ['amy_adams', 'starred_actors', 'moonlight_serenade'], ['amy_adams', 'starred_actors', 'american_hustle'], ['amy_adams', 'starred_actors', 'sunshine_cleaning'], ['amy_adams', 'starred_actors', 'the_fighter'], ['diane_lane', 'starred_actors', 'wild_bill'], ['diane_lane', 'starred_actors', 'the_glass_house'], ['diane_lane', 'starred_actors', 'jumper']
[ChatGPT]
Statement: To get the genres of the these films, I need to find the relations linked with all the films from previous step.
Helper function: getRelation('bug'), getRelation('machine_gun_preacher'), getRelation('young_ones'), getRelation('the_missing_person'), getRelation('immortals'), getRelation('blood_creek'), getRelation('the_cold_light_of_day'), getRelation('moonlight_serenade'), getRelation('american_hustle'), getRelation('sunshine_cleaning'), getRelation('the_fighter'), getRelation('wild_bill'), getRelation('the_glass_house'), getRelation('jumper')
[User]
Execution result: Relation_list('bug') = ['starred_actors', 'has_tags', 'written_by', 'release_year', 'has_genre', 'directed_by'], Relation_list('machine_gun_preacher') = ['starred_actors', 'has_tags', 'written_by', 'release_year', 'has_genre', 'directed_by'], Relation_list('young_ones') = ['starred_actors', 'has_genre', 'release_year'], Relation_list('the_missing_person') = ['starred_actors', 'written_by', 'release_year', 'has_genre'], Relation_list('immortals') = 'starred_actors', 'has_tags', 'release_year', 'has_genre', 'in_language'], Relation_list('blood_creek') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('the_cold_light_of_day') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('moonlight_serenade') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('american_hustle') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('sunshine_cleaning') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('the_fighter') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('wild_bill') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('the_glass_house') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('jumper') = ['starred_actors', 'has_tags', 'release_year', 'directed_by']
[ChatGPT]
Statement: To get the genres of the films, I need to explore the graph with each films and related relations.
Helper function: exploreKG('bug': ['has_genre']), exploreKG('machine_gun_preacher': ['has_genre']), exploreKG('young_ones': ['has_genre']), exploreKG('the_missing_person': ['has_genre']), exploreKG('immortals': ['has_genre']), exploreKG('blood_creek': ['has_genre']), exploreKG('the_cold_light_of_day': ['has_genre']), exploreKG('moonlight_serenade': ['has_genre']), exploreKG('american_hustle': ['has_genre']), exploreKG('sunshine_cleaning': ['has_genre']), exploreKG('the_fighter': ['has_genre']), exploreKG('wild_bill': ['has_genre']), exploreKG('the_glass_house': ['has_genre']), exploreKG('jumper': [])
[User]
Execution result: ['bug', 'has_genre', 'horror'], ['machine_gun_preacher', 'has_genre', 'action'], ['young_ones', 'has_genre', 'action'], ['the_missing_person', 'has_genre', 'mystery'], ['the_missing_person', 'has_genre', 'drama'], ['the_missing_person', 'has_genre', 'comedy'], ['immortals', 'has_genre', 'fantasy'], ['blood_creek', 'has_genre', 'horror'], ['the_cold_light_of_day', 'has_genre', 'action'], ['moonlight_serenade', 'has_genre', 'romance'], ['moonlight_serenade', 'has_genre', 'drama'], ['moonlight_serenade', 'has_genre', 'musical'], ['american_hustle', 'has_genre', 'crime'], ['american_hustle', 'has_genre', 'drama'], ['sunshine_cleaning', 'has_genre', 'drama'], ['sunshine_cleaning', 'has_genre', 'comedy'], ['the_fighter', 'has_genre', 'drama'], ['the_fighter', 'has_genre', 'sport'], ['wild_bill', 'has_genre', 'western'], ['the_glass_house', 'has_genre', 'thriller']
[ChatGPT]
Statement: Now I get the genres of the films that share actors with 'Man of Steel'. The answer of the claim is as follows.
['horror', 'action', 'mystery', 'drama', 'comedy', 'fantasy', 'romance', 'musical', 'crime', 'sport', 'western', 'thriller']
Helper function: Verification(['horror', 'action', 'mystery', 'drama', 'comedy', 'fantasy', 'romance', 'musical', 'crime', 'sport', 'western', 'thriller'])


Example 2)
Claim: who are the actors in the films written by [John Travis]?
Given entity: ["John Travis"]

Statement: I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function: getRelation('John Travis')
[User]
Execution result: Relation_list('John Travis') = ['written_by']
[ChatGPT]
Statement: Now, to find the films that 'John Travis' written, I need to explore the graph from 'John Travis' with related relations.
Helper function: exploreKG('John Travis': ['written_by'])
[User]
Execution result: ['the_haunting_of_molly_hartley']
[ChatGPT]
Statement: Now, we have to find the actors in the previous given film.
Helper function: getRelation('the_haunting_of_molly_hartley')
[User]
Execution result: Relation_list('the_haunting_of_molly_hartley') = ['has_genre', 'starred_actors', 'directed_by', 'release_year', 'written_by']
[ChatGPT]
Statement: To get the actors in the film, I need to explore the graph with the film and related relations.
Helper function: exploreKG('the_haunting_of_molly_hartley': ['starred_actors'])
[User]
Execution result: ['the_haunting_of_molly_hartley', 'starred_actors', 'haley_bennett'], ['the_haunting_of_molly_hartley', 'starred_actors', 'chace_crawford'], ['the_haunting_of_molly_hartley', 'starred_actors', 'jake_weber']
[ChatGPT]
Statement: Now I get the actors of the films written by 'John Travis'. The answer of the claim is as follows.
['haley_bennett', 'chace_crawford', 'jake_weber']
Helper function: Verification(['haley_bennett', 'chace_crawford', 'jake_weber'])

Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>
"""

# prompt2 shows better performance rather than prompt_integrated. Here, if we change triple providing form, we can use exact same code for both FactKG and MetaQA.
# This below prompt is the solution for it.
prompt_fusion = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use below helper functions to find the evidence for finding labels.

<Helper functions>
1. getRelation([list of entities]): Returns the list of relations connected to the entities.
2. exploreKG([list of entities]: [relation]): Returns the triples with tail entities in graph data starts from single head entity in entity list and given relation. Be sure to divide entity part and relation part using ':' symbol.
3. Verification([list of entities]): Once verification is done, call this function with labels.

You must follow the exact format of the given helper function.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for my response. If response has made, continue your Statement task.
Importantly, you have to you inverse relation if you need. For example, if you want to find films starred by certain actors (when only actors were given), you have to use 'starred_actors' relation.

Here are some examples.

Example 1)
Claim: what genres do the films that share actors with [Man of Steel] fall under?
Given Entity: ['Man of Steel']

[ChatGPT]
Statement: I need the relations linked with the given entity.
Helper function: getRelation('Man of Steel')
[User]
Execution result: Relation_list('Man of Steel') = ['release_year', 'starred_actors', 'written_by', 'has_tags', 'directed_by']
[ChatGPT]
Statement: First, to solve the claim, I have to know the actors starred in 'Man of Steel'.
Helper function: exploreKG('Man of Steel': ['starred_actors'])
[User]
Execution result: ['Man of Steel', 'starred_actors', 'michael_shannon'], ['Man of Steel', 'starred_actors', 'henry_cavill'], ['Man of Steel', 'starred_actors', 'amy_adams'], ['Man of Steel', 'starred_actors', 'diane_lane']
[ChatGPT]
Statement: Next, I need films starred by previous given actors. To find the films, I need relations linked with the actors.
Helper function: getRelation(['michael_shannon', 'henry_cavill', 'amy_adams', 'diane_lane'])
[User]
Execution result: Relation_list('michael_shannon') = ['has_tags', 'starred_actors'], Relation_list('henry_cavill') = ['starred_actors'], Relation_list('amy_adams') = ['has_tags', 'starred_actors'], getRelations('diane_lane') = ['has_tags', 'starred_actors']
[ChatGPT]
Statement: To get the films starred by previous actors, I need to explore the graph with each actors and related relations.
Helper function: exploreKG(['michael_shannon', 'henry_cavill', 'amy_adams', 'diane_lane']: ['starred_actors'])
[User]
Execution result: ['michael_shannon', 'starred_actors', 'bug'], ['michael_shannon', 'starred_actors', 'machine_gun_preacher'], ['michael_shannon', 'starred_actors', 'young_ones'], ['michael_shannon', 'starred_actors', 'the_missing_person'], ['henry_cavill', 'starred_actors', 'immortals'], ['henry_cavill', 'starred_actors', 'blood_creek'], ['henry_cavill', 'starred_actors', 'the_cold_light_of_day'], ['amy_adams', 'starred_actors', 'moonlight_serenade'], ['amy_adams', 'starred_actors', 'american_hustle'], ['amy_adams', 'starred_actors', 'sunshine_cleaning'], ['amy_adams', 'starred_actors', 'the_fighter'], ['diane_lane', 'starred_actors', 'wild_bill'], ['diane_lane', 'starred_actors', 'the_glass_house'], ['diane_lane', 'starred_actors', 'jumper']
[ChatGPT]
Statement: To get the genres of the these films, I need to find the relations linked with all the films from previous step.
Helper function: getRelation(['bug', 'machine_gun_preacher', 'young_ones', 'the_missing_person', 'immortals', 'blood_creek', 'the_cold_light_of_day', 'moonlight_serenade', 'american_hustle', 'sunshine_cleaning', 'the_fighter', 'wild_bill', 'the_glass_house', 'jumper'])
[User]
Execution result: Relation_list('bug') = ['starred_actors', 'has_tags', 'written_by', 'release_year', 'has_genre', 'directed_by'], Relation_list('machine_gun_preacher') = ['starred_actors', 'has_tags', 'written_by', 'release_year', 'has_genre', 'directed_by'], Relation_list('young_ones') = ['starred_actors', 'has_genre', 'release_year'], Relation_list('the_missing_person') = ['starred_actors', 'written_by', 'release_year', 'has_genre'], Relation_list('immortals') = 'starred_actors', 'has_tags', 'release_year', 'has_genre', 'in_language'], Relation_list('blood_creek') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('the_cold_light_of_day') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('moonlight_serenade') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('american_hustle') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('sunshine_cleaning') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('the_fighter') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('wild_bill') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('the_glass_house') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('jumper') = ['starred_actors', 'has_tags', 'release_year', 'directed_by']
[ChatGPT]
Statement: To get the genres of the films, I need to explore the graph with each films and related relations.
Helper function: exploreKG(['bug', 'machine_gun_preacher', 'young_ones', 'the_missing_person', 'immortals', 'blood_creek', 'the_cold_light_of_day', 'moonlight_serenade', 'american_hustle', 'sunshine_cleaning', 'the_fighter', 'wild_bill', 'the_glass_house', 'jumper']: ['has_genre'])
[User]
Execution result: ['bug', 'has_genre', 'horror'], ['machine_gun_preacher', 'has_genre', 'action'], ['young_ones', 'has_genre', 'action'], ['the_missing_person', 'has_genre', 'mystery'], ['the_missing_person', 'has_genre', 'drama'], ['the_missing_person', 'has_genre', 'comedy'], ['immortals', 'has_genre', 'fantasy'], ['blood_creek', 'has_genre', 'horror'], ['the_cold_light_of_day', 'has_genre', 'action'], ['moonlight_serenade', 'has_genre', 'romance'], ['moonlight_serenade', 'has_genre', 'drama'], ['moonlight_serenade', 'has_genre', 'musical'], ['american_hustle', 'has_genre', 'crime'], ['american_hustle', 'has_genre', 'drama'], ['sunshine_cleaning', 'has_genre', 'drama'], ['sunshine_cleaning', 'has_genre', 'comedy'], ['the_fighter', 'has_genre', 'drama'], ['the_fighter', 'has_genre', 'sport'], ['wild_bill', 'has_genre', 'western'], ['the_glass_house', 'has_genre', 'thriller']
[ChatGPT]
Statement: Now I get the genres of the films that share actors with 'Man of Steel'. The answer of the claim is as follows.
['horror', 'action', 'mystery', 'drama', 'comedy', 'fantasy', 'romance', 'musical', 'crime', 'sport', 'western', 'thriller']
Helper function: Verification(['horror', 'action', 'mystery', 'drama', 'comedy', 'fantasy', 'romance', 'musical', 'crime', 'sport', 'western', 'thriller'])


Example 2)
Claim: who are the actors in the films written by [John Travis]?
Given entity: ["John Travis"]

[ChatGPT]
Statement: I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function: getRelation(['John Travis'])
[User]
Execution result: Relation_list(['John Travis']) = ['written_by']
[ChatGPT]
Statement: Now, to find the films that 'John Travis' written, I need to explore the graph from 'John Travis' with related relations.
Helper function: exploreKG(['John Travis']: ['written_by'])
[User]
Execution result: ['John Travis', 'written_by', 'the_haunting_of_molly_hartley']
[ChatGPT]
Statement: Now, we have to find the actors in the previous given film.
Helper function: getRelation(['the_haunting_of_molly_hartley'])
[User]
Execution result: Relation_list('the_haunting_of_molly_hartley') = ['has_genre', 'starred_actors', 'directed_by', 'release_year', 'written_by']
[ChatGPT]
Statement: To get the actors in the film, I need to explore the graph with the film and related relations.
Helper function: exploreKG(['the_haunting_of_molly_hartley']: ['starred_actors'])
[User]
Execution result: ['the_haunting_of_molly_hartley', 'starred_actors', 'haley_bennett'], ['the_haunting_of_molly_hartley', 'starred_actors', 'chace_crawford'], ['the_haunting_of_molly_hartley', 'starred_actors', 'jake_weber']
[ChatGPT]
Statement: Now I get the actors of the films written by 'John Travis'. The answer of the claim is as follows.
['haley_bennett', 'chace_crawford', 'jake_weber']
Helper function: Verification(['haley_bennett', 'chace_crawford', 'jake_weber'])

Example 3)
Claim: what does [Hiromi Nagasaku] star in?
Given entity: ["Hiromi Nagasaku"]

[ChatGPT]
Statement: I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function: getRelation(["Hiromi Nagasaku"])
[User]
Execution result: Relation_list(["Hiromi Nagasaku"]) = ['starred_actors']
[ChatGPT]
Statement: Now, to find the films that 'Hiromi Nagasaku' starred, I need to explore the graph from 'Hiromi Nagasaku' with related relations.
Helper function: exploreKG(['Hiromi Nagasaku']: ['starred_actors'])
[User]
Execution result: ['Hiromi Nagasaku', 'starred_actors', 'doppleganger']
[ChatGPT]
Statement: Now I get the films starred by 'Hiromi Nagasaku'. The answer of the claim is as follows.
['doppleganger']
Helper function: Verification(['doppleganger'])

Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>
"""

prompt_confidence = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use below helper functions to find the evidence for finding labels.

<Helper functions>
1. getRelation([list of entities]): Returns the list of relations connected to the entities.
2. exploreKG([list of entities]: [relation]): Returns the corresponding tail entities in graph data starts from single entity in entity list and given relation.
3. confidenceCheck(): Please review the previous conversation between the you and the user. This helper function must be called every step before verification.
4. Verification([list of entities]): Once verification is done, call this function with labels.

You must follow the exact format of the given helper function.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for my response. If response has made, continue your Statement task.
Importantly, you have to you inverse relation if you need. For example, if you want to find films starred by certain actors (when only actors were given), you have to use 'starred_actors' relation.

Here are some examples.

Example 1)
Claim: what genres do the films that share actors with [Man of Steel] fall under?
Given Entity: [‘Man of Steel’]

[ChatGPT]
Statement: I need the relations linked with the given entity.
Helper function: getRelation([’Man of Steel’])
[User]
Execution result: Relation_list(['Man of Steel']) = ['release_year', 'starred_actors', 'written_by', 'has_tags', 'directed_by']
[ChatGPT]
Statement: I need to check the process is going well.
Helper function: confidenceCheck()
[User]
Execution result: <Previous chat history>
[ChatGPT]
Statement: Everything is on track. Now, to solve the claim, I have to know the actors starred in ‘Man of Steel’.
Helper function: exploreKG(['Man of Steel']: ['starred_actors'])
[User]
Execution result: ['michael_shannon', 'henry_cavill', 'amy_adams', 'diane_lane']
[ChatGPT]
Statement: I need to check the process is going well.
Helper function: confidenceCheck()
[User]
Execution result: <Previous chat history>
[ChatGPT]
Statement: Everything is on track. Then, I need films starred by previous given actors. To find the films, I need relations linked with the actors.
Helper function: getRelation(['michael_shannon', 'henry_cavill', 'amy_adams', 'diane_lane'])
[User]
Execution result: Relation_list(['michael_shannon', 'henry_cavill', 'amy_adams', 'diane_lane']) = ['starred_actors', 'has_tags']
[ChatGPT]
Statement: I need to check the process is going well.
Helper function: confidenceCheck()
[User]
Execution result: <Previous chat history>
[ChatGPT]
Statement: Everything is on track. To get the films starred by previous actors, I need to explore the graph with each actors and related relations.
Helper function: exploreKG(['michael_shannon', 'henry_cavill', 'amy_adams', 'diane_lane']: ['starred_actors'])
[User]
Execution result: ['the_wedding_date', 'the_cold_light_of_day', 'cinema_verite', 'standing_still', 'six_pack', 'the_cotton_club', 'my_new_gun', 'untraceable', 'shotgun_stories', 'return', 'nights_in_rodanthe', 'a_little_romance', 'cruel_intentions_2', 'the_glass_house', '99_homes', 'doubt', 'jack', 'blood_creek', 'wild_bill', 'sunshine_cleaning', 'the_runaways', "charlie_wilson's_war", 'american_hustle', 'a_streetcar_named_desire', 'jumper', 'leap_year', 'the_fighter', 'a_walk_on_the_moon', 'the_missing_person', 'on_the_road', 'moonlight_serenade', 'enchanted', 'immortals', 'machine_gun_preacher', 'the_muppets', 'hollywoodland', 'young_ones', 'the_big_town', 'under_the_tuscan_sun', 'bug', 'unfaithful', 'the_perfect_storm', 'must_love_dogs', 'big_eyes', 'fierce_people', 'secretariat', 'man_of_steel', 'the_iceman', 'take_shelter', 'streets_of_fire', 'murder_at_1600', 'killshot']
[ChatGPT]
Statement: I need to check the process is going well.
Helper function: confidenceCheck()
[User]
Execution result: <Previous chat history>
[ChatGPT]
Statement: Everything is on track. To get the genres of the these films, I need to find the relations linked with the films from previous step.
Helper function: getRelation(['the_wedding_date', 'the_cold_light_of_day', 'cinema_verite', 'standing_still', 'six_pack', 'the_cotton_club', 'my_new_gun', 'untraceable', 'shotgun_stories', 'return', 'nights_in_rodanthe', 'a_little_romance', 'cruel_intentions_2', 'the_glass_house', '99_homes', 'doubt', 'jack', 'blood_creek', 'wild_bill', 'sunshine_cleaning', 'the_runaways', "charlie_wilson's_war", 'american_hustle', 'a_streetcar_named_desire', 'jumper', 'leap_year', 'the_fighter', 'a_walk_on_the_moon', 'the_missing_person', 'on_the_road', 'moonlight_serenade', 'enchanted', 'immortals', 'machine_gun_preacher', 'the_muppets', 'hollywoodland', 'young_ones', 'the_big_town', 'under_the_tuscan_sun', 'bug', 'unfaithful', 'the_perfect_storm', 'must_love_dogs', 'big_eyes', 'fierce_people', 'secretariat', 'man_of_steel', 'the_iceman', 'take_shelter', 'streets_of_fire', 'murder_at_1600', 'killshot'])
[User]
Execution result: Relation_list(['the_wedding_date', 'the_cold_light_of_day', 'cinema_verite', 'standing_still', 'six_pack', 'the_cotton_club', 'my_new_gun', 'untraceable', 'shotgun_stories', 'return', 'nights_in_rodanthe', 'a_little_romance', 'cruel_intentions_2', 'the_glass_house', '99_homes', 'doubt', 'jack', 'blood_creek', 'wild_bill', 'sunshine_cleaning', 'the_runaways', "charlie_wilson's_war", 'american_hustle', 'a_streetcar_named_desire', 'jumper', 'leap_year', 'the_fighter', 'a_walk_on_the_moon', 'the_missing_person', 'on_the_road', 'moonlight_serenade', 'enchanted', 'immortals', 'machine_gun_preacher', 'the_muppets', 'hollywoodland', 'young_ones', 'the_big_town', 'under_the_tuscan_sun', 'bug', 'unfaithful', 'the_perfect_storm', 'must_love_dogs', 'big_eyes', 'fierce_people', 'secretariat', 'man_of_steel', 'the_iceman', 'take_shelter', 'streets_of_fire', 'murder_at_1600', 'killshot']) = ['release_year', 'in_language', 'starred_actors', 'written_by', 'has_tags', 'has_imdb_rating', 'has_genre', 'has_tags', 'directed_by']
[ChatGPT]
Statement: I need to check the process is going well.
Helper function: confidenceCheck()
[User]
Execution result: <Previous chat history>
[ChatGPT]
Statement: Everything is on track. To get the genres of the films, I need to explore the graph with each films and related relations.
Helper function: exploreKG(['the_wedding_date', 'the_cold_light_of_day', 'cinema_verite', 'standing_still', 'six_pack', 'the_cotton_club', 'my_new_gun', 'untraceable', 'shotgun_stories', 'return', 'nights_in_rodanthe', 'a_little_romance', 'cruel_intentions_2', 'the_glass_house', '99_homes', 'doubt', 'jack', 'blood_creek', 'wild_bill', 'sunshine_cleaning', 'the_runaways', "charlie_wilson's_war", 'american_hustle', 'a_streetcar_named_desire', 'jumper', 'leap_year', 'the_fighter', 'a_walk_on_the_moon', 'the_missing_person', 'on_the_road', 'moonlight_serenade', 'enchanted', 'immortals', 'machine_gun_preacher', 'the_muppets', 'hollywoodland', 'young_ones', 'the_big_town', 'under_the_tuscan_sun', 'bug', 'unfaithful', 'the_perfect_storm', 'must_love_dogs', 'big_eyes', 'fierce_people', 'secretariat', 'man_of_steel', 'the_iceman', 'take_shelter', 'streets_of_fire', 'murder_at_1600', 'killshot']: ['has_genre'])
[User]
Execution result: ['crime', 'sport', 'horror', 'musical', 'comedy', 'mystery', 'drama', 'romance', 'western', 'adventure', 'action', 'thriller', 'fantasy']
[ChatGPT]
Statement: I need to check the process is going well.
Helper function: confidenceCheck()
[User]
Execution result: <Previous chat history>
[ChatGPT]
Statement: Everything is on track. Now I get the genres of the films that share actors with 'Man of Steel'. The answer of the claim is as follows.
['crime', 'sport', 'horror', 'musical', 'comedy', 'mystery', 'drama', 'romance', 'western', 'adventure', 'action', 'thriller', 'fantasy']
Helper function: Verification(['crime', 'sport', 'horror', 'musical', 'comedy', 'mystery', 'drama', 'romance', 'western', 'adventure', 'action', 'thriller', 'fantasy'])

Example 2)
Claim: who are the actors in the films written by [John Travis]?
Given entity: ["John Travis"]

Statement: I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function: getRelation(['John Travis'])
[User]
Execution result: Relation_list(['John Travis']) = ['written_by']
[ChatGPT]
Statement: I need to check the process is going well.
Helper function: confidenceCheck()
[User]
Execution result: <Previous chat history>
[ChatGPT]
Statement: Everything is on track. Now, to find the films that 'John Travis' written, I need to explore the graph from 'John Travis' with related relations.
Helper function: exploreKG(['John Travis']: ['written_by'])
[User]
Execution result: ['the_haunting_of_molly_hartley']
[ChatGPT]
Statement: I need to check the process is going well.
Helper function: confidenceCheck()
[User]
Execution result: <Previous chat history>
[ChatGPT]
Statement: Everything is on track. Now, we have to find the actors in the previous given film.
Helper function: getRelation(['the_haunting_of_molly_hartley'])
[User]
Execution result: Relation_list(['the_haunting_of_molly_hartley']) = ['has_genre', 'starred_actors', 'directed_by', 'release_year', 'written_by']
[ChatGPT]
Statement: I need to check the process is going well.
Helper function: confidenceCheck()
[User]
Execution result: <Previous chat history>
[ChatGPT]
Statement: Everything is on track. To get the actors in the film, I need to explore the graph with the film and related relations.
Helper function: exploreKG(['the_haunting_of_molly_hartley']: ['starred_actors'])
[User]
Execution result: ['haley_bennett', 'chace_crawford', 'jake_weber']
[ChatGPT]
Statement: I need to check the process is going well.
Helper function: confidenceCheck()
[User]
Execution result: <Previous chat history>
[ChatGPT]
Statement: Everything is on track. Now I get the actors of the films written by 'John Travis'. The answer of the claim is as follows.
['haley_bennett', 'chace_crawford', 'jake_weber']
Helper function: Verification(['haley_bennett', 'chace_crawford', 'jake_weber'])

Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>
"""

ex_prompt = """
Claim: what does [Cab Calloway] act in?
Given entity: ["Cab Calloway"]

Statement: I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function: getRelation(['Cab Calloway'])
[User]
Execution result: Relation_list(['Cab Calloway']) = ['starred_actors']
[ChatGPT]
Statement: Now, to find the films that 'Cab Calloway' starred, I need to explore the graph from 'Cab Calloway' with related relations.
Helper function: exploreKG(['Cab Calloway']: ['starred_actors'])
[User]
Execution result: ['the_blues_brothers']
[ChatGPT]
Statement: Now I get the films starred by 'Cab Calloway'. The answer of the claim is as follows.
['the_blues_brothers']
Helper function: Verification(['the_blues_brothers'])
"""

ex = """
Claim: which person directed the movies starred by [John Krasinski]?
Given entity: ["John Krasinski"]

Statement: I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function: getRelation('John Krasinski')
## (Stop for User Response)
(User Given) Execution result: Relation_list('John Krasinski') = ['starred_actors']
Statement: Now, to guess the films starred by 'John Krasinski', I need to explore the graph from 'John Krasinski' with related relations.
Helper function: exploreKG(['John Krasinski']: ['starred_actors'])
## (Stop for User Response) 
(User Given) Execution result: ['license_to_wed', 'away_we_go', 'nobody_walks', "it's_complicated", 'leatherheads', 'something_borrowed']
Statement: Now, we need to find the director of the films starred by 'John Krasinski'.
Helper function: getRelation(['license_to_wed', 'away_we_go', 'nobody_walks', "it's_complicated", 'leatherheads', 'something_borrowed']) 
## (Stop for User Response) 
(User Given) Execution result: Relation_list(['license_to_wed', 'away_we_go', 'nobody_walks', "it's_complicated", 'leatherheads', 'something_borrowed']) = ['release_year', 'starred_actors', 'written_by', 'has_genre', 'has_tags', 'directed_by']
Statement: To get the directors of several films, I need to explore the graph with each films and related relations.
Helper function: exploreKG(['license_to_wed', 'away_we_go', 'nobody_walks', "it's_complicated", 'leatherheads', 'something_borrowed']: ['directed_by'])
## (Stop for User Response) 
(User Given) Execution result: ['ken_kwapis', 'sam_mendes', 'nancy_meyers', 'george_clooney', 'luke_greenfield']
Statement: Now I get the directors of the films that starred by 'John Krasinski'. The answer of the claim is as follows.
['ken_kwapis', 'sam_mendes', 'nancy_meyers', 'george_clooney', 'luke_greenfield']
Helper function: Verification(['ken_kwapis', 'sam_mendes', 'nancy_meyers', 'george_clooney', 'luke_greenfield'])

Claim: the films that share actors with the film [Creepshow] were in which languages?
Given entity: ["Creepshow"]

Statement: I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function: getRelation('Creepshow')
## (Stop for User Response)
(User Given) Execution result: Relation_list('Creepshow') = ['has_genre', 'has_tags', 'starred_actors', 'directed_by', 'written_by', 'release_year']
Statement: Now, to find the actors starred in 'Creepshow', I need to explore the graph from 'Creepshow' with related relations.
Helper function: exploreKG(['Creepshow']: ['starred_actors'])
## (Stop for User Response) 
(User Given) Execution result: ['fritz_weaver', 'hal_holbrook', 'adrienne_barbeau', 'leslie_nielsen']
Statement: Now, we need to find the films starred by previous actors.
Helper function: getRelation(['fritz_weaver', 'hal_holbrook', 'adrienne_barbeau', 'leslie_nielsen']) 
## (Stop for User Response) 
(User Given) Execution result: Relation_list(['fritz_weaver', 'hal_holbrook', 'adrienne_barbeau', 'leslie_nielsen']) = ['has_tags', 'starred_actors']
Statement: To get the films, I need to explore the graph with each actors and related relation.
Helper function: exploreKG(['fritz_weaver', 'hal_holbrook', 'adrienne_barbeau', 'leslie_nielsen']: ['starred_actors'])
## (Stop for User Response) 
(User Given) Execution result: ['wild_in_the_streets', "the_creature_wasn't_nice", 'repossessed', 'the_sheepman', 'creepshow', 'harvey', 'superhero_movie', 'the_kidnapping_of_the_president', "someone's_watching_me!", 'two_evil_eyes', 'camouflage', 'the_firm', 'forbidden_planet', 'rent-a-kid', 'that_evening_sun', 'spy_hard', 'the_majestic', 'the_fog', 'wrongfully_accused', 'they_only_kill_their_masters', 'santa_who?', 'tammy_and_the_bachelor', 'prom_night', 'swamp_thing', 'the_star_chamber', 'mr._magoo', 'unholy']
Statement: Now, we need to find the language of the films.
Helper function: getRelation(['wild_in_the_streets', "the_creature_wasn't_nice", 'repossessed', 'the_sheepman', 'creepshow', 'harvey', 'superhero_movie', 'the_kidnapping_of_the_president', "someone's_watching_me!", 'two_evil_eyes', 'camouflage', 'the_firm', 'forbidden_planet', 'rent-a-kid', 'that_evening_sun', 'spy_hard', 'the_majestic', 'the_fog', 'wrongfully_accused', 'they_only_kill_their_masters', 'santa_who?', 'tammy_and_the_bachelor', 'prom_night', 'swamp_thing', 'the_star_chamber', 'mr._magoo', 'unholy']) 
## (Stop for User Response) 
(User Given) Execution result: Relation_list(['wild_in_the_streets', "the_creature_wasn't_nice", 'repossessed', 'the_sheepman', 'creepshow', 'harvey', 'superhero_movie', 'the_kidnapping_of_the_president', "someone's_watching_me!", 'two_evil_eyes', 'camouflage', 'the_firm', 'forbidden_planet', 'rent-a-kid', 'that_evening_sun', 'spy_hard', 'the_majestic', 'the_fog', 'wrongfully_accused', 'they_only_kill_their_masters', 'santa_who?', 'tammy_and_the_bachelor', 'prom_night', 'swamp_thing', 'the_star_chamber', 'mr._magoo', 'unholy']) = ['has_genre', 'has_tags', 'starred_actors', 'has_imdb_rating', 'in_language', 'directed_by', 'written_by', 'release_year']
Statement: To get the languages of several films, I need to explore the graph with each films and related relations.
Helper function: exploreKG(['wild_in_the_streets', "the_creature_wasn't_nice", 'repossessed', 'the_sheepman', 'creepshow', 'harvey', 'superhero_movie', 'the_kidnapping_of_the_president', "someone's_watching_me!", 'two_evil_eyes', 'camouflage', 'the_firm', 'forbidden_planet', 'rent-a-kid', 'that_evening_sun', 'spy_hard', 'the_majestic', 'the_fog', 'wrongfully_accused', 'they_only_kill_their_masters', 'santa_who?', 'tammy_and_the_bachelor', 'prom_night', 'swamp_thing', 'the_star_chamber', 'mr._magoo', 'unholy']: ['in_language'])
## (Stop for User Response) 
(User Given) Execution result: ['polish', 'english']
Statement: Now I get the language of the films that share actors starred by 'Creepshow'. The answer of the claim is as follows.
['polish', 'english']
Helper function: Verification(['polish', 'english'])
"""