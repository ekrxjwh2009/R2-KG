
initial_prompt = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use below helper functions to find the evidence for finding labels.

<Helper functions>
1. getRelation[entity]: Returns the list of relations connected to the entities.
2. exploreKG[entity]=[list of relations]: Returns the corresponding tail entities in graph data starts from single entity in given entity and given relation.
3. Verification[]: After getting enough evidence after exploreKG() helper function and if verification can be done, call this function with labels.

You must follow the exact format of the given helper function.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for my response. If response has made, continue your 'Statement and Helper function' task.
Importantly, you have to use inverse relation if you need. For example, if you want to find films starred by certain actors (when only actors were given), you have to use 'starred_actors' relation.

Here are some examples.

Example 1)
Claim: what genres do the films that share actors with [Man of Steel] fall under?
Given Entity: ['Man of Steel']

[ChatGPT]
Statement : I need the relations linked with the given entity.
Helper function : getRelation['Man of Steel']
[User]
Execution result : Relation_list['Man of Steel'] = ['release_year', 'starred_actors', 'written_by', 'has_tags', 'directed_by']
[ChatGPT]
Statement : First, to solve the claim, I have to know the actors starred in ‘Man of Steel’.
Helper function : exploreKG['Man of Steel']=['starred_actors']
[User]
Execution result : ['Man of Steel', 'starred_actors', 'michael_shannon'], ['Man of Steel', 'starred_actors', 'henry_cavill'], ['Man of Steel', 'starred_actors', 'amy_adams'], ['Man of Steel', 'starred_actors', 'diane_lane']
[ChatGPT]
Statement : Next, I need films starred by previous given actors. To find the films, I need relations linked with the actors.
Helper function : getRelation['michael_shannon'] ## getRelation('henry_cavill') ## getRelation('amy_adams') ## getRelation('diane_lane')
[User]
Execution result : Relation_list('michael_shannon') = ['has_tags', 'starred_actors'], Relation_list('henry_cavill') = ['starred_actors'], Relation_list('amy_adams') = ['has_tags', 'starred_actors'], Relation_list('diane_lane') = ['has_tags', 'starred_actors']
[ChatGPT]
Statement : To get the films starred by previous actors, I need to explore the graph with each actors and related relations.
Helper function : exploreKG('michael_shannon')=['starred_actors'] ## exploreKG('henry_cavill')=['starred_actors'] ## exploreKG('amy_adams')=['starred_actors'] ## exploreKG('diane_lane')=['starred_actors']
[User]
Execution result : ['michael_shannon', 'starred_actors', 'bug'], ['michael_shannon', 'starred_actors', 'machine_gun_preacher'], ['michael_shannon', 'starred_actors', 'young_ones'], ['michael_shannon', 'starred_actors', 'the_missing_person'], ['henry_cavill', 'starred_actors', 'immortals'], ['henry_cavill', 'starred_actors', 'blood_creek'], ['henry_cavill', 'starred_actors', 'the_cold_light_of_day'], ['amy_adams', 'starred_actors', 'moonlight_serenade'], ['amy_adams', 'starred_actors', 'american_hustle'], ['amy_adams', 'starred_actors', 'sunshine_cleaning'], ['amy_adams', 'starred_actors', 'the_fighter'], ['diane_lane', 'starred_actors', 'wild_bill'], ['diane_lane', 'starred_actors', 'the_glass_house'], ['diane_lane', 'starred_actors', 'jumper']
[ChatGPT]
Statement : To get the genres of the these films, I need to find the relations linked with all the films from previous step.
Helper function : getRelation('bug') ## getRelation('machine_gun_preacher') ## getRelation('young_ones') ## getRelation('the_missing_person') ## getRelation('immortals') ## getRelation('blood_creek') ## getRelation('the_cold_light_of_day') ## getRelation('moonlight_serenade') ## getRelation('american_hustle') ## getRelation('sunshine_cleaning') ## getRelation('the_fighter') ## getRelation('wild_bill') ## getRelation('the_glass_house') ## getRelation('jumper')
[User]
Execution result : Relation_list('bug') = ['starred_actors', 'has_tags', 'written_by', 'release_year', 'has_genre', 'directed_by'], Relation_list('machine_gun_preacher') = ['starred_actors', 'has_tags', 'written_by', 'release_year', 'has_genre', 'directed_by'], Relation_list('young_ones') = ['starred_actors', 'has_genre', 'release_year'], Relation_list('the_missing_person') = ['starred_actors', 'written_by', 'release_year', 'has_genre'], Relation_list('immortals') = 'starred_actors', 'has_tags', 'release_year', 'has_genre', 'in_language'], Relation_list('blood_creek') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('the_cold_light_of_day') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('moonlight_serenade') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('american_hustle') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('sunshine_cleaning') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('the_fighter') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('wild_bill') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('the_glass_house') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('jumper') = ['starred_actors', 'has_tags', 'release_year', 'directed_by']
[ChatGPT]
Statement : To get the genres of the films, I need to explore the graph with each films and related relations.
Helper function : exploreKG('bug')=['has_genre'] ## exploreKG('machine_gun_preacher')=['has_genre'] ## exploreKG('young_ones')=['has_genre'] ## exploreKG('the_missing_person')=['has_genre'] ## exploreKG('immortals')=['has_genre'] ## exploreKG('blood_creek')=['has_genre'] ## exploreKG('the_cold_light_of_day')=['has_genre'] ## exploreKG('moonlight_serenade')=['has_genre'] ## exploreKG('american_hustle')=['has_genre'] ## exploreKG('sunshine_cleaning')=['has_genre'] ## exploreKG('the_fighter')=['has_genre'] ## exploreKG('wild_bill')=['has_genre'] ## exploreKG('the_glass_house')=['has_genre'] ## exploreKG('jumper')=[]
[User]
Execution result : ['bug', 'has_genre', 'horror'], ['machine_gun_preacher', 'has_genre', 'action'], ['young_ones', 'has_genre', 'action'], ['the_missing_person', 'has_genre', 'mystery'], ['the_missing_person', 'has_genre', 'drama'], ['the_missing_person', 'has_genre', 'comedy'], ['immortals', 'has_genre', 'fantasy'], ['blood_creek', 'has_genre', 'horror'], ['the_cold_light_of_day', 'has_genre', 'action'], ['moonlight_serenade', 'has_genre', 'romance'], ['moonlight_serenade', 'has_genre', 'drama'], ['moonlight_serenade', 'has_genre', 'musical'], ['american_hustle', 'has_genre', 'crime'], ['american_hustle', 'has_genre', 'drama'], ['sunshine_cleaning', 'has_genre', 'drama'], ['sunshine_cleaning', 'has_genre', 'comedy'], ['the_fighter', 'has_genre', 'drama'], ['the_fighter', 'has_genre', 'sport'], ['wild_bill', 'has_genre', 'western'], ['the_glass_house', 'has_genre', 'thriller']
[ChatGPT]
Statement : Now I get the genres of the films that share actors with 'Man of Steel'. The answer of the claim is as follows.
['horror', 'action', 'mystery', 'drama', 'comedy', 'fantasy', 'romance', 'musical', 'crime', 'sport', 'western', 'thriller']
Helper function : Verification(['horror', 'action', 'mystery', 'drama', 'comedy', 'fantasy', 'romance', 'musical', 'crime', 'sport', 'western', 'thriller'])


Example 2)
Claim: who are the actors in the films written by [John Travis]?
Given entity: ["John Travis"]

Statement : I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function : getRelation('John Travis')
[User]
Execution result : Relation_list('John Travis') = ['written_by']
[ChatGPT]
Statement : Now, to find the films that 'John Travis' written, I need to explore the graph from 'John Travis' with related relations.
Helper function : exploreKG('John Travis')=['written_by']
[User]
Execution result : ['John Travis', 'written_by', 'the_haunting_of_molly_hartley']
[ChatGPT]
Statement : Now, we have to find the actors in the previous given film.
Helper function : getRelation('the_haunting_of_molly_hartley')
[User]
Execution result : Relation_list('the_haunting_of_molly_hartley') = ['has_genre', 'starred_actors', 'directed_by', 'release_year', 'written_by']
[ChatGPT]
Statement : To get the actors in the film, I need to explore the graph with the film and related relations.
Helper function : exploreKG('the_haunting_of_molly_hartley')=['starred_actors']
[User]
Execution result : ['the_haunting_of_molly_hartley', 'starred_actors', 'haley_bennett'], ['the_haunting_of_molly_hartley', 'starred_actors', 'chace_crawford'], ['the_haunting_of_molly_hartley', 'starred_actors', 'jake_weber']
[ChatGPT]
Statement : Now I get the actors of the films written by 'John Travis'. The answer of the claim is as follows.
['haley_bennett', 'chace_crawford', 'jake_weber']
Helper function : Verification(['haley_bennett', 'chace_crawford', 'jake_weber'])

Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>
"""

main_agent_with_sub = """ 
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use below helper functions to find the evidence for finding labels.

<Helper functions>
1.getRelation[entity]: Returns the list of relations linked to the entity. You can choose several relations from the list that seem related to the claim.
2.exploreKG[entity]=[relation_1,relation_2, ... relation_K]: Returns the triple set around the entity. For example, [entity, relation_1, tail entity] etc. You can choose relation from [User]'s execution result.
3.Verification[]: Call you think you collected enough evidence to answer the claim. 
Based on the evidence gathered so far, [User] will answer labels of the claim. If [User] think the evidence is insufficient, [User] will ask you to collect more evidence. If [User] say the evidence is insufficient, continue the evidence collection process using a different helper function.

You must follow the exact format of the given helper function.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for my response. If response has made, continue your 'Statement and Helper function' task.
Importantly, Do not change the format of the entity or relation including '~'.

Example 1)
Claim: what genres do the films that share actors with [Man of Steel] fall under?
Given Entity: ['Man of Steel']

[ChatGPT]
Statement : I need the relations linked with the given entity.
Helper function : getRelation['Man of Steel']
[User]
Execution result : Relation_list['Man of Steel'] = ['release_year', 'starred_actors', 'written_by', 'has_tags', 'directed_by']
[ChatGPT]
Statement : First, to solve the claim, I have to know the actors starred in ‘Man of Steel’.
Helper function : exploreKG['Man of Steel']=['starred_actors']
[User]
Execution result : ['Man of Steel', 'starred_actors', 'michael_shannon'], ['Man of Steel', 'starred_actors', 'henry_cavill'], ['Man of Steel', 'starred_actors', 'amy_adams'], ['Man of Steel', 'starred_actors', 'diane_lane']
[ChatGPT]
Statement : Now, I need films starred by michael_shannon, henry_cavill, amy_adams, diane_lane. To find the films, I need relations linked with the actors.
Helper function : getRelation['michael_shannon'] ## getRelation['henry_cavill'] ## getRelation['amy_adams'] ## getRelation['diane_lane']
[User]
Execution result : Relation_list['michael_shannon'] = ['has_tags', 'starred_actors'], Relation_list['henry_cavill'] = ['starred_actors'], Relation_list['amy_adams'] = ['has_tags', 'starred_actors'], Relation_list['diane_lane'] = ['has_tags', 'starred_actors']
[ChatGPT]
Statement : To get the films starred by previous actors, I need to explore the graph with each actors and related relations.
Helper function : exploreKG['michael_shannon']=['starred_actors'] ## exploreKG['henry_cavill']=['starred_actors'] ## exploreKG['amy_adams']=['starred_actors'] ## exploreKG['diane_lane']=['starred_actors']
[User]
Execution result : ['michael_shannon', 'starred_actors', 'bug'], ['michael_shannon', 'starred_actors', 'machine_gun_preacher'], ['michael_shannon', 'starred_actors', 'young_ones'], ['michael_shannon', 'starred_actors', 'the_missing_person'], ['henry_cavill', 'starred_actors', 'immortals'], ['henry_cavill', 'starred_actors', 'blood_creek'], ['henry_cavill', 'starred_actors', 'the_cold_light_of_day'], ['amy_adams', 'starred_actors', 'moonlight_serenade'], ['amy_adams', 'starred_actors', 'american_hustle'], ['amy_adams', 'starred_actors', 'sunshine_cleaning'], ['amy_adams', 'starred_actors', 'the_fighter'], ['diane_lane', 'starred_actors', 'wild_bill'], ['diane_lane', 'starred_actors', 'the_glass_house'], ['diane_lane', 'starred_actors', 'jumper']
[ChatGPT]
Statement : To get the genres of the these films, I need to find the relations linked with all the films from previous step.
Helper function : getRelation['bug'] ## getRelation['machine_gun_preacher'] ## getRelation['young_ones'] ## getRelation['the_missing_person'] ## getRelation['immortals'] ## getRelation['blood_creek'] ## getRelation['the_cold_light_of_day'] ## getRelation['moonlight_serenade'] ## getRelation['american_hustle'] ## getRelation['sunshine_cleaning'] ## getRelation['the_fighter'] ## getRelation['wild_bill'] ## getRelation['the_glass_house'] ## getRelation['jumper']
[User]
Execution result : Relation_list['bug'] = ['starred_actors', 'has_tags', 'written_by', 'release_year', 'has_genre', 'directed_by'], Relation_list['machine_gun_preacher'] = ['starred_actors', 'has_tags', 'written_by', 'release_year', 'has_genre', 'directed_by'], Relation_list['young_ones'] = ['starred_actors', 'has_genre', 'release_year'], Relation_list['the_missing_person'] = ['starred_actors', 'written_by', 'release_year', 'has_genre'], Relation_list['immortals'] = 'starred_actors', 'has_tags', 'release_year', 'has_genre', 'in_language'], Relation_list['blood_creek'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list['the_cold_light_of_day'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list['moonlight_serenade'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list['american_hustle'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list['sunshine_cleaning'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list['the_fighter'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list['wild_bill'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list['the_glass_house'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list['jumper'] = ['starred_actors', 'has_tags', 'release_year', 'directed_by']
[ChatGPT]
Statement : To get the genres of the films, I need to explore the graph with each films and related relations.
Helper function : exploreKG['bug']=['has_genre'] ## exploreKG['machine_gun_preacher']=['has_genre'] ## exploreKG['young_ones']=['has_genre'] ## exploreKG['the_missing_person']=['has_genre'] ## exploreKG['immortals']=['has_genre'] ## exploreKG['blood_creek']=['has_genre'] ## exploreKG['the_cold_light_of_day']=['has_genre'] ## exploreKG['moonlight_serenade']=['has_genre'] ## exploreKG['american_hustle']=['has_genre'] ## exploreKG['sunshine_cleaning']=['has_genre'] ## exploreKG['the_fighter']=['has_genre'] ## exploreKG['wild_bill']=['has_genre'] ## exploreKG['the_glass_house']=['has_genre']
[User]
Execution result : ['bug', 'has_genre', 'horror'], ['machine_gun_preacher', 'has_genre', 'action'], ['young_ones', 'has_genre', 'action'], ['the_missing_person', 'has_genre', 'mystery'], ['the_missing_person', 'has_genre', 'drama'], ['the_missing_person', 'has_genre', 'comedy'], ['immortals', 'has_genre', 'fantasy'], ['blood_creek', 'has_genre', 'horror'], ['the_cold_light_of_day', 'has_genre', 'action'], ['moonlight_serenade', 'has_genre', 'romance'], ['moonlight_serenade', 'has_genre', 'drama'], ['moonlight_serenade', 'has_genre', 'musical'], ['american_hustle', 'has_genre', 'crime'], ['american_hustle', 'has_genre', 'drama'], ['sunshine_cleaning', 'has_genre', 'drama'], ['sunshine_cleaning', 'has_genre', 'comedy'], ['the_fighter', 'has_genre', 'drama'], ['the_fighter', 'has_genre', 'sport'], ['wild_bill', 'has_genre', 'western'], ['the_glass_house', 'has_genre', 'thriller']
[ChatGPT]
Statement : Now I get the genres of the films that share actors with 'Man of Steel'. The answer of the claim is as follows.
['horror', 'action', 'mystery', 'drama', 'comedy', 'fantasy', 'romance', 'musical', 'crime', 'sport', 'western', 'thriller']
Helper function : Verification[]


Example 2)
Claim: who are the actors in the films written by [John Travis]?
Given entity: ["John Travis"]

Statement: I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function : getRelation['John Travis']
[User]
Execution result : Relation_list['John Travis'] = ['written_by', '~directed_by']
[ChatGPT]
Statement : Now, let's look what film John Travis directed
Helper function : exploreKG['John Travis']=['~directed_by']
[User]
Execution result : ['John Travis', '~directed_by', 'machine_gun_preacher'], ['John Travis', '~directed_by', 'the_missing_person']
[ChatGPT]
Statement : According to the evidence, John Travis directed machine gun preacher and the missing person.
Helper function : Verification[]
[User]
Execution result : We don't have enough evidence to answer the claim. Try to look triples linked with 'written_by' with 'John Travis'.
[ChatGPT]
Statement: Alright. We need information about John Travis' written films.
Helper function : exploreKG['John Travis']=['written_by']
[User]
Execution result: ['John Travis', 'written_by', 'the_haunting_of_molly_hartley']
[ChatGPT]
Statement: Now, we have to find the actors in the previous given film.
Helper function : getRelation['the_haunting_of_molly_hartley']
[User]
Execution result: Relation_list['the_haunting_of_molly_hartley'] = ['has_genre', 'starred_actors', 'directed_by', 'release_year', 'written_by']
[ChatGPT]
Statement: To get the actors in the film, I need to explore the graph with the film and related relations.
Helper function : exploreKG['the_haunting_of_molly_hartley']=['starred_actors']
[User]
Execution result : ['the_haunting_of_molly_hartley', 'starred_actors', 'haley_bennett'], ['the_haunting_of_molly_hartley', 'starred_actors', 'chace_crawford'], ['the_haunting_of_molly_hartley', 'starred_actors', 'jake_weber']
[ChatGPT]
Statement : Now I get the actors of the films written by 'John Travis'. The answer of the claim is as follows.
['haley_bennett', 'chace_crawford', 'jake_weber']
Helper function : Verification[]


Example 3)
Claim: what does [Cab Calloway] act in?
Given entity: ["Cab Calloway"]

[ChatGPT]
Statement : I need to look aro/home/smjo/KG-gpt2/ver_8_factKG/result_multi_hop_gpt-3.5-turbo_maxiter_15_multicalls_temp0und the the given entities. First, I need the relation list actually linked with the entity.
Helper function : getRelation['Cab Calloway']
[User]
Execution result : Relation_list['Cab Calloway'] = ['starred_actors']
[ChatGPT]
Statement : Now, to find the films that 'Cab Calloway' starred, I need to explore the graph from 'Cab Calloway' with related relations.
Helper function : exploreKG['Cab Calloway']=['starred_actors']
[User]
Execution result : ['Cab Calloway', 'starred_actors', 'the_blues_brothers']
[ChatGPT]
Statement : Now I get the films starred by 'Cab Calloway'. The answer of the claim is as follows.
['the_blues_brothers']
Helper function : Verification[]


Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>

"""

sub_prompt = """
You are the evaluator. I will show you a claim and a triple set extracted from a graph. 
Based on the given triple set and relation list of each entity, find proper labels for given question.
If given triple sets are lack of information to verify the claim, give the the combination of entity and relation you need. You can refer the given relations list and choose what relation information is more needed.
The triple set takes the form [Head, Relation, Tail], which means 'Head's Relation is Tail.' 
If the relation starts with '~', it indicates a reverse relation, meaning 'Tail's relation is head.' 
The following cases may arise: Choose one option from 'Executable ([list of labels])' or 'Not executable(Insufficient evidence)'.
If you choose 'Not executable(Insufficient evidence)', You must specify in the statement which additional relation information is needed for a particular entity. However, the relation can only be selected from the given Relation_list and cannot be created arbitrarily.
Refer to the explanations of the two options below to answer the Statement and Evaluation.


<Cases> 
1. If there is a sufficient triple set to answer the question, you must select all possible answers if multiple answers seem possible --> Executable ([list of possible answers])
2. If the triple set is insufficient or ambiguos to determine the True/False of the claim --> Not executable (Insufficient evidence) 

<Example 1>
[User]
Claim : what genres do the films that share actors with [Man of Steel] fall under?
Triple sets : [['Man of Steel', 'starred_actors', 'michael_shannon'], ['Man of Steel', 'starred_actors', 'henry_cavill'], ['Man of Steel', 'starred_actors', 'amy_adams'], ['Man of Steel', 'starred_actors', 'diane_lane'],['michael_shannon', 'starred_actors', 'bug'], ['michael_shannon', 'starred_actors', 'machine_gun_preacher'], ['michael_shannon', 'starred_actors', 'young_ones'], ['michael_shannon', 'starred_actors', 'the_missing_person'], ['henry_cavill', 'starred_actors', 'immortals'], ['henry_cavill', 'starred_actors', 'blood_creek'], ['henry_cavill', 'starred_actors', 'the_cold_light_of_day'], ['amy_adams', 'starred_actors', 'moonlight_serenade'], ['amy_adams', 'starred_actors', 'american_hustle'], ['amy_adams', 'starred_actors', 'sunshine_cleaning'], ['amy_adams', 'starred_actors', 'the_fighter'], ['diane_lane', 'starred_actors', 'wild_bill'], ['diane_lane', 'starred_actors', 'the_glass_house'], ['diane_lane', 'starred_actors', 'jumper'], ['bug', 'has_genre', 'horror'], ['machine_gun_preacher', 'has_genre', 'action'], ['young_ones', 'has_genre', 'action'], ['the_missing_person', 'has_genre', 'mystery'], ['the_missing_person', 'has_genre', 'drama'], ['the_missing_person', 'has_genre', 'comedy'], ['immortals', 'has_genre', 'fantasy'], ['blood_creek', 'has_genre', 'horror'], ['the_cold_light_of_day', 'has_genre', 'action'], ['moonlight_serenade', 'has_genre', 'romance'], ['moonlight_serenade', 'has_genre', 'drama'], ['moonlight_serenade', 'has_genre', 'musical'], ['american_hustle', 'has_genre', 'crime'], ['american_hustle', 'has_genre', 'drama'], ['sunshine_cleaning', 'has_genre', 'drama'], ['sunshine_cleaning', 'has_genre', 'comedy'], ['the_fighter', 'has_genre', 'drama'], ['the_fighter', 'has_genre', 'sport'], ['wild_bill', 'has_genre', 'western'], ['the_glass_house', 'has_genre', 'thriller']]
Relations of Entity :
Relation_list['Man of Steel'] = ['release_year', 'starred_actors', 'written_by', 'has_tags', 'directed_by']
Relation_list['michael_shannon'] = ['has_tags', 'starred_actors']
Relation_list['henry_cavill'] = ['starred_actors'], Relation_list('amy_adams') = ['has_tags', 'starred_actors']
Relation_list['diane_lane'] = ['has_tags', 'starred_actors']
Relation_list['bug'] = ['starred_actors', 'has_tags', 'written_by', 'release_year', 'has_genre', 'directed_by']
Relation_list['machine_gun_preacher'] = ['starred_actors', 'has_tags', 'written_by', 'release_year', 'has_genre', 'directed_by']
Relation_list['young_ones'] = ['starred_actors', 'has_genre', 'release_year']
Relation_list['the_missing_person'] = ['starred_actors', 'written_by', 'release_year', 'has_genre']
Relation_list['immortals'] = 'starred_actors', 'has_tags', 'release_year', 'has_genre', 'in_language']
Relation_list['blood_creek'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by']
Relation_list['the_cold_light_of_day'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by']
Relation_list['moonlight_serenade'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by']
Relation_list['american_hustle'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by']
Relation_list['sunshine_cleaning'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by']
Relation_list['the_fighter'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by']
Relation_list['wild_bill'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by']
Relation_list['the_glass_house'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by']
Relation_list['jumper'] = ['starred_actors', 'has_tags', 'release_year', 'directed_by']
[ChatGPT]
Statement : Now I get the genres of the films that share actors with 'Man of Steel'. The answer of the claim is as follows. ['horror', 'action', 'mystery', 'drama', 'comedy', 'fantasy', 'romance', 'musical', 'crime', 'sport', 'western', 'thriller']
Evaluation : Executable(['horror', 'action', 'mystery', 'drama', 'comedy', 'fantasy', 'romance', 'musical', 'crime', 'sport', 'western', 'thriller'])


<Example 2>
[User]
Claim : who are the actors in the films written by [John Travis]?
Triple sets :
[['John Travis', 'written_by', 'the_haunting_of_molly_hartley'], ['the_haunting_of_molly_hartley', 'starred_actors', 'haley_bennett'], ['the_haunting_of_molly_hartley', 'starred_actors', 'chace_crawford'], ['the_haunting_of_molly_hartley', 'starred_actors', 'jake_weber']]
Relations of Entity : 
Relation_list['John Travis'] = ['written_by']
Relation_list['the_haunting_of_molly_hartley'] = ['has_genre', 'starred_actors', 'directed_by', 'release_year', 'written_by']
[ChatGPT]
Statement : Now I get the actors of the films written by 'John Travis'. The answer of the claim is as follows. ['haley_bennett', 'chace_crawford', 'jake_weber']
Evaluation : Executable(['haley_bennett', 'chace_crawford', 'jake_weber'])


<Example 3>
[User]
Claim : which movies have the same screenwriter of [The Ambushers]?
Triple sets : [['the_ambushers', 'written_by', 'donald_hamilton']]
Relations of Entity :
Relation_list['The Ambushers'] = ['written_by', 'starred_actors', 'has_genre', 'release_year']
Relation_list['donald_hamilton'] = ['~written_by', '~directed_by']
[ChatGPT]
Statement : We need more information to anwer the claim. Try to look relation '~written_by' of donald_hamilton
Evaluation : Not executable (Insufficient evidence)


<Example 4>
[User]
Claim : when did the movies release whose writers also wrote [Twelve O'Clock High]?
Triple sets : [["twelve_o'clock_high", 'written_by', 'sy_bartlett'],['sy_bartlett', '~written_by', 'the_princess_and_the_pirate'], ['sy_bartlett', '~written_by', 'road_to_zanzibar'], ['sy_bartlett', '~written_by', 'a_gathering_of_eagles'], ['sy_bartlett', '~written_by', "twelve_o'clock_high"]]
Relations of Entity :
Relation_list['Twelve O'Clock High'] = ['has_tags', 'release_year', 'starred_actors', 'has_genre', 'written_by', 'directed_by']
Relation_list['sy_bartlett'] = ['~written_by']
Relation_list['the_princess_and_the_pirate'] = ['release_year', 'starred_actors', 'has_genre', 'written_by', 'directed_by', 'has_tags']
Relation_list['road_to_zanzibar'] = ['release_year', 'starred_actors', 'has_genre', 'written_by', 'has_tags']
Relation_list['a_gathering_of_eagles'] = ['release_year', 'starred_actors', 'written_by', 'has_imdb_votes', 'in_language', 'directed_by']
[ChatGPT]
Statement :  We need more information to answer the release time of the movies. Try to look relation 'release_year' of the_princess_and_the_pirate, relation 'release_year' of road_to_zanzibar and relation 'release_year' of a_gathering_of_eagles.
Evaluation : Not executable (Insufficient evidence)


<Example 5>
[User]
Claim : In which films did [Roger Perry] perform as an actor?GT entity:['Roger Perry']?
Triple sets : ['roger_perry', '~starred_actors', 'the_thing_with_two_heads']
Relations of Entity :
Relations_list["roger_perry"] = ['~starred_actors']
[ChatGPT]
Statement : The starred actors of the thing with two heads are roger perry.
Evaluation : Executable(['roger_perry'])

Now, it's your turn. Continue your 'Statement and Evaluation' task. Response must have same form with upper examples.
[User]
Claim : <<<<CLAIM>>>>
Triple set : <<<<Triple set>>>>
Relations of Entity : <<<<GOLD RELATIONS>>>>

"""
