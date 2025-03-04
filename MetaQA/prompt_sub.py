sub_prompt = """
You are the evaluator. I will show you a claim and a triple set extracted from a graph. 
Based on the given triple set and relation list of each entity, find the proper labels for given question.
If given triple sets are lack of information to verify the claim, give the the combination of entity and relation you need. You can refer the given relations list and choosed what relation information is more needed.
The triple set takes the form [Head, Relation, Tail], which means 'Head's Relation is Tail.' 
If the relation starts with '~', it indicates a reverse relation, meaning 'Tail's relation is head.' 
The following cases may arise: Choose one option from 'Executable ([list of labels])' or 'Not executable(Insufficient evidence)'.
If you choose 'Not executable(Insufficient evidence)', You must specify in the statement which additional relation information is needed for a particular entity. However, the relation can only be selected from the given Relation_list and cannot be created arbitrarily.
Refer to the explanations of the two options below to answer the Statement and Evaluation.

***Important: If you think you need additional information using certain relation, you have to check the relation is actually linked with the entity. If not, you have to give the label entities only linked with the relation using Executable([list of labels]).
(e.g. If there are 5 films to find 'release_year' but only 3 of them have 'release_year' relation, you have to give the label of the 3 films using Executable([list of labels]) regardless of the remaining 2 films.)

<Cases> 
1. If answer labels can be extracted from the triple sets --> Executable ([list of labels])
2. If the triple sets are insufficient or ambiguous to determine the answer labels of the claim --> Not executable (Insufficient evidence) 

Below are examples of your task.

<Example 1>
[User]
Claim : what genres do the films that share actors with [Man of Steel] fall under?
Triple sets : [['Man of Steel', 'starred_actors', 'michael_shannon'], ['Man of Steel', 'starred_actors', 'henry_cavill'], ['Man of Steel', 'starred_actors', 'amy_adams'], ['Man of Steel', 'starred_actors', 'diane_lane'],['michael_shannon', '~starred_actors', 'bug'], ['michael_shannon', '~starred_actors', 'machine_gun_preacher'], ['michael_shannon', '~starred_actors', 'young_ones'], ['michael_shannon', '~starred_actors', 'the_missing_person'], ['henry_cavill', '~starred_actors', 'immortals'], ['henry_cavill', '~starred_actors', 'blood_creek'], ['henry_cavill', '~starred_actors', 'the_cold_light_of_day'], ['amy_adams', '~starred_actors', 'moonlight_serenade'], ['amy_adams', '~starred_actors', 'american_hustle'], ['amy_adams', '~starred_actors', 'sunshine_cleaning'], ['amy_adams', '~starred_actors', 'the_fighter'], ['diane_lane', '~starred_actors', 'wild_bill'], ['diane_lane', '~starred_actors', 'the_glass_house'], ['diane_lane', '~starred_actors', 'jumper'], ['bug', 'has_genre', 'horror'], ['machine_gun_preacher', 'has_genre', 'action'], ['young_ones', 'has_genre', 'action'], ['the_missing_person', 'has_genre', 'mystery'], ['the_missing_person', 'has_genre', 'drama'], ['the_missing_person', 'has_genre', 'comedy'], ['immortals', 'has_genre', 'fantasy'], ['blood_creek', 'has_genre', 'horror'], ['the_cold_light_of_day', 'has_genre', 'action'], ['moonlight_serenade', 'has_genre', 'romance'], ['moonlight_serenade', 'has_genre', 'drama'], ['moonlight_serenade', 'has_genre', 'musical'], ['american_hustle', 'has_genre', 'crime'], ['american_hustle', 'has_genre', 'drama'], ['sunshine_cleaning', 'has_genre', 'drama'], ['sunshine_cleaning', 'has_genre', 'comedy'], ['the_fighter', 'has_genre', 'drama'], ['the_fighter', 'has_genre', 'sport'], ['wild_bill', 'has_genre', 'western'], ['the_glass_house', 'has_genre', 'thriller']]
Relations of Entity :
Relations_list['Man of Steel'] = ['release_year', 'starred_actors', 'written_by', 'has_tags', 'directed_by']
Relations_list['michael_shannon'] = ['~has_tags', '~starred_actors']
Relations_list['henry_cavill'] = ['~starred_actors']
Relations_list['amy_adams'] = ['~has_tags', '~starred_actors']
Relations_list['diane_lane'] = ['~has_tags', '~starred_actors']
Relations_list['bug'] = ['starred_actors', 'has_tags', 'written_by', 'release_year', 'has_genre', 'directed_by']
Relations_list['machine_gun_preacher'] = ['starred_actors', 'has_tags', 'written_by', 'release_year', 'has_genre', 'directed_by']
Relations_list['young_ones'] = ['starred_actors', 'has_genre', 'release_year']
Relations_list['the_missing_person'] = ['starred_actors', 'written_by', 'release_year', 'has_genre']
Relations_list['immortals'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'in_language']
Relations_list['blood_creek'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by']
Relations_list['the_cold_light_of_day'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by']
Relations_list['moonlight_serenade'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by']
Relations_list['american_hustle'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by']
Relations_list['sunshine_cleaning'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by']
Relations_list['the_fighter'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by']
Relations_list['wild_bill'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by']
Relations_list['the_glass_house'] = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by']
Relations_list['jumper'] = ['starred_actors', 'has_tags', 'release_year', 'directed_by']
[ChatGPT]
Statement: For the films having 'release_year' relation, I can get the genres of the films that share actors with 'Man of Steel'. The answer of the claim is as follows. ['horror', 'action', 'mystery', 'drama', 'comedy', 'fantasy', 'romance', 'musical', 'crime', 'sport', 'western', 'thriller']
Evaluation: Executable(['horror', 'action', 'mystery', 'drama', 'comedy', 'fantasy', 'romance', 'musical', 'crime', 'sport', 'western', 'thriller'])

<Example 2>
[User]
Claim : who are the actors in the films written by [John Travis]?
Triple sets : [['John Travis', '~written_by', 'the_haunting_of_molly_hartley'], ['the_haunting_of_molly_hartley', 'starred_actors', 'haley_bennett'], ['the_haunting_of_molly_hartley', 'starred_actors', 'chace_crawford'], ['the_haunting_of_molly_hartley', 'starred_actors', 'jake_weber']]
Relations of Entity : 
Relations_list['John Travis'] = ['~written_by']
Relations_list['the_haunting_of_molly_hartley'] = ['has_genre', 'starred_actors', 'directed_by', 'release_year', 'written_by']
[ChatGPT]
Statement: The film written by 'John Travis' is 'the_haunting_of_molly_hartley'. And by using 'starred_actors' relation, I can get the actors of the films written by 'John Travis'. The answer of the claim is as follows. ['haley_bennett', 'chace_crawford', 'jake_weber']
Evaluation: Executable(['haley_bennett', 'chace_crawford', 'jake_weber'])

<Example 3>
[User]
Claim : which movies have the same screenwriter of [The Ambushers]?
Triple sets : [['the_ambushers', 'written_by', 'donald_hamilton']]
Relations of Entity :
Relations_list['The Ambushers'] = ['written_by', 'starred_actors', 'has_genre', 'release_year']
Relations_list['donald_hamilton'] = ['~written_by', '~directed_by']
[ChatGPT]
Statement: We need additional information about movies written by 'donald_hamilton'. Try to look relation '~written_by' of 'donald_hamilton'.
Evaluation: Not executable (Insufficient evidence)

<Example 4>
[User]
Claim : when did the movies release whose writers also wrote [Twelve O'Clock High]?
Triple sets : [["twelve_o'clock_high", 'written_by', 'sy_bartlett'],['sy_bartlett', '~written_by', 'the_princess_and_the_pirate'], ['sy_bartlett', '~written_by', 'road_to_zanzibar'], ['sy_bartlett', '~written_by', 'a_gathering_of_eagles']]
Relations of Entity :
Relations_list['Twelve O'Clock High'] = ['has_tags', 'release_year', 'starred_actors', 'has_genre', 'written_by', 'directed_by']
Relations_list['sy_bartlett'] = ['~written_by']
Relations_list['the_princess_and_the_pirate'] = ['release_year', 'starred_actors', 'has_genre', 'written_by', 'directed_by', 'has_tags']
Relations_list['road_to_zanzibar'] = ['release_year', 'starred_actors', 'has_genre', 'written_by', 'has_tags']
Relations_list['a_gathering_of_eagles'] = ['release_year', 'starred_actors', 'written_by', 'has_imdb_votes', 'in_language', 'directed_by']
[ChatGPT]
Statement: We need more information to answer the release time of the movies. Try to look relation 'release_year' of 'the_princess_and_the_pirate', relation 'release_year' of 'road_to_zanzibar' and relation 'release_year' of 'a_gathering_of_eagles'.
Evaluation: Not executable (Insufficient evidence)

<Example 5>
[User]
Claim : when did the movies release whose writers also wrote [Twelve O'Clock High]?
Triple sets : [["twelve_o'clock_high", 'written_by', 'sy_bartlett'],['sy_bartlett', '~written_by', 'the_princess_and_the_pirate'], ['sy_bartlett', '~written_by', 'road_to_zanzibar'], ['sy_bartlett', '~written_by', 'a_gathering_of_eagles'], ['the_princess_and_the_pirate', 'release_year', '1944'], ['road_to_zanzibar', 'release_year', '1941'], ['a_gathering_of_eagles', 'release_year', '1963']]
Relations of Entity :
Relations_list['Twelve O'Clock High'] = ['has_tags', 'release_year', 'starred_actors', 'has_genre', 'written_by', 'directed_by']
Relations_list['sy_bartlett'] = ['~written_by']
Relations_list['the_princess_and_the_pirate'] = ['release_year', 'starred_actors', 'has_genre', 'written_by', 'directed_by', 'has_tags']
Relations_list['road_to_zanzibar'] = ['release_year', 'starred_actors', 'has_genre', 'written_by', 'has_tags']
Relations_list['a_gathering_of_eagles'] = ['release_year', 'starred_actors', 'written_by', 'has_imdb_votes', 'in_language', 'directed_by']
[ChatGPT]
Statement: The writer of 'Twelve O'Clock High' is 'sy_bartlet', and films written by 'sy_bartlett' are 'the_princess_and_the_pirate', 'road_to_zanzibar', 'a_gathering_of_eagles'. By using 'release_year' relation, We can get the release year of the movies. The answer of the claim is as follows. ['1944', '1941', '1963']
Evaluation: Executable(['1944', '1941', '1963'])

<Example 6>
[User]
Claim : what movies did [Caroline Aaron] star in?
Triple sets : [['caroline_aaron', '~starred_actors', 'a_modern_affair']]
Relations of Entity :
Relations_list['caroline_aaron'] = ['~starred_actors']
[ChatGPT]
Statement: We get the movie starred by 'Caroline Aaron'.The answer of the claim is as follows. ['a_modern_affair']
Evaluation: Executable(['a_modern_affair'])


Now, it's your turn. Continue your 'Statement and Evaluation' task. Response must have same form with upper examples.
[User]
Claim : <<<<CLAIM>>>>
Triple set : <<<<Triple set>>>>
Relations of Entity : <<<<GOLD RELATIONS>>>>

"""