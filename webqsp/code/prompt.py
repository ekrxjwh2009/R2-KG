freebase_main_agent_singlestep = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use one of the helper functions below to find the evidence for finding labels.

Helper Functions
1.getRelation[entity]: Returns the list of relations linked to the entity. You can choose several relations from the list that seem related to the claim.
2.exploreKG[entity]=[relation_1,relation_2, ... relation_K]: Returns the triple set around the entity. For example, [entity, relation_1, tail entity] etc. You can choose relation from [User]'s execution result.
3.Verification[entity]: If you can find the answer entity from collected evidences, give the answer.

You must follow the exact format of the given helper function.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for my response. If response has made, continue your 'Statement and Helper function' task.
Importantly, if there is an entity starting with 'm.', it is a MID entity. Additional information must be found from that entity.

Example 1)
Claim: what is the name of justin bieber brother?
Given entity: ('Justin Bieber', 'm.06w2sn5')

[ChatGPT]
Statement: I need to look around the the given entities. First, I need the relation list linked to Justin Bieber.
Helper function: getRelation['Justin Bieber']
[User]
Execution result: 
Relation_list['Justin Bieber'] = ['people.person.education', 'music.artist.track', 'authority.musicbrainz', 'people.person.places_lived', 'common.topic.notable_types', 'celebrities.celebrity.celebrity_friends', 'award.award_nominee.award_nominations', 'base.popstra.celebrity.friendship', 'people.person.parents', 'people.person.sibling_s', 'type.object.key', 'authority.netflix.api']
[ChatGPT]
Statement: To find the brother of Justin Bieber, I need to explore the graph about the siblings of Justin Bieber.
Helper function: exploreKG['Justin Bieber']=['people.person.sibling_s']
[User]
Execution result: 
['Justin Bieber', 'people.person.sibling_s', 'm.0gxnnwp'], ['Justin Bieber', 'people.person.sibling_s', 'm.0gxnnwc']
[ChatGPT]
Statement: There are MIDs connected to Justin Bieber, and we have to find additional information from the MIDs. I need the relation list linked to those MIDs.
Helper function: getRelation['m.0gxnnwp']
[User]
Execution result: 
Relation_list['m.0gxnnwp'] = ['people.sibling_relationship.sibling', 'type.objet.type']
[ChatGPT]
Statement: Since we have to find connected sibling from the MIDs, I need to explore the graph from MID to related relations.
Helper function: exploreKG['m.gxnnwp']=['people.sibling_relationship.sibling']
[User]
Execution result: 
['m.gxnnwp', 'people.sibling_relationship.sibling', 'Jaxon Bieber']
[ChatGPT]
Statement: For the other MIDs, I have to find siblings connected to them.
Helper function: getRelation['m.0gxnnwc']
[User]
Execution result: 
Relation_list['m.0gxnnwc'] = ['people.sibling_relationship.sibling', 'type.objet.type']
[ChatGPT]
Statement: Since we have to find connected sibling from the MIDs, I need to explore the graph from MID to related relations.
Helper function: exploreKG['m.0gxnnwc']=['people.sibling_relationship.sibling']
[User]
Execution result:
['m.0gxnnwc', 'people.sibling_relationship.sibling', 'Jazmyn Bieber']
[ChatGPT]
Statement: We have two siblings, 'Jaxon Bieber' and 'Jazmyn Bieber'. Claim is asking about the brother of Justin Bieber, therefore we have to find the gender of each sibling.
Helper function: getRelation['Jaxon Bieber']
[User]
Execution result: 
Relation_list('Jaxon Bieber') = ['people.person.nationality', 'people.person.date_of_birth', 'type.object.name', 'people.person.gender', 'people.person.sibling_s', 'people.person.place_of_birth', 'people.person.parents']
[ChatGPT]
Statement: To find the gender of Jaxon Bieber, I need to explore the graph related to gender.
Helper function: exploreKG['Jaxon Bieber']=['people.person.gender'] 
[User]
Execution result: 
['Jaxon Bieber', 'people.person.gener', 'Male']
[ChatGPT]
Statement: For 'Jazmyn Bieber', I have to follow same process.
Helper function: getRelation['Jazmyn Bieber']
[User]
Execution result: 
['people.person.nationality', 'people.person.date_of_birth', 'type.object.name', 'people.person.gender', 'people.person.sibling_s', 'people.person.place_of_birth', 'people.person.parents']
[ChatGPT]
Statement: Now, let's check the gender of Jazmyn Bieber.
Helper function: exploreKG['Jazmyn Bieber']=['people.person.gender']
[User]
Execution result: 
['Jazmyn Bieber', 'people.person.gender', 'Female']
[ChatGPT]
Statement: Since only Jaxon Bieber is the male among Justin Bieber's siblings, the name of Justin Bieber's brother is 'Jaxon Bieber'.
Helper function: Verification['Jaxon Bieber']


Example 2)
Claim: what character did natalie portman play in star wars?
Given entity: ('Natalie Portman', 'm.09l3p')

[ChatGPT]
Statement: First, I need relations linked to Natalie Portman.
Helper function: getRelation['Natalie Portman']
[User]
Execution result: 
Relation_list('Natalie Portman') = ['people.person.education', 'authority.nndb', 'people.person.religion', 'film.actor.film', 'people.person.places_lived', 'nytimes.topic.uri', 'common.topic.article', 'user.avh.default_domain.ellerdale_topic.ellerdale_id', 'authority.musicbrainz']
[ChatGPT]
Statemnt: I need the information about Natalie Portman's character in Star Wars. Therefore, I need triples linked with the relation about films or characters.
Helper function: exploreKG['Natalie Portman']=['film.actor.film']
[User]
Execution result: 
['Natalie Portman', 'film.actor.film', 'm.07zm_x0'], ['Natalie Portman', 'film.actor.film', 'm.0jv4ds'], ['Natalie Portman', 'film.actor.film', 'm.04dcjy9'], ['Natalie Portman', 'film.actor.film', 'm.0k3qy8']
[ChatGPT]
Statemn : There are MIDs connected to Justin Bieber, and we have to find additional information from the MIDs. I need the relation list linked to those MIDs.
Helper function: getRelation['m.07zm_x0'] 
[User]
Execution result: 
Relation_list['m.07zm_x0'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
[ChatGPT]
Statement: Since we have to find the film 'Star Wars', I need to explore graph to find film from the MID.
Helper function: exploreKG['m.07zm_x0']=['film.performance.film']
[User]
Execution result:
['m.07zm_x0', 'film.performance.film', 'Your Highness']
[ChatGPT]
Statement: Given MID is not related to 'Star Wars'. I have to explore other MIDs that I got so far.
Helper function: getRelation['m.0jv4ds'] 
[User]
Execution result:
Relation_list['m.0jv4ds'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
[ChatGPT]
Statement: Since we have to find the film 'Star Wars', I need to explore graph to find film from the MID.
Helper function: exploreKG['m.0jv4ds']=['film.performance.film']
[User]
Execution result: 
['m.0jv4ds', 'film.performance.film', 'Beautiful Girls']
[ChatGPT]
Statement: Given MID is not related to 'Star Wars'. I have to explore other MIDs that I got so far.
Helper function: getRelation['m.04dcjy9'] 
[User]
Execution result:
Relation_list['m.04dcjy9'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
[ChatGPT]
Statement: Since we have to find the film 'Star Wars', I need to explore graph to find film from the MID.
Helper function: exploreKG['m.04dcjy9']=['film.performance.film']
[User]
Execution result: 
['m.04dcjy9', 'film.performance.film', 'New York, I Love You']
[ChatGPT]
Statement: Given MID is not related to 'Star Wars'. I have to explore other MIDs that I got so far.
Helper function: getRelation['m.0k3qy8'] 
[User]
Execution result:
Relation_list['m.0k3qy8'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
[ChatGPT]
Statement: Since we have to find the film 'Star Wars', I need to explore graph to find film from the MID.
Helper function: exploreKG['m.0k3qy8']=['film.performance.film']
[User]
Execution result: 
['m.0k3qy8', 'film.performance.film', 'Star Wars Episode I: The Phantom Menace']
[ChatGPT]
Statement: We found the MID connected between Natalie Porman and Star Wars Episode I: The Phantom Menace. Here, we have to find the character that Natalie Portman played. We can find it from connected MID.
Helper function: getRelation['m.0k3qy8']
[User]
Execution result:
Relation_list['m.0k3qy8'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
[ChatGPT]
Statement: Since we have to find the character, I need to explore graph with using related relations.
Helper function: exploreKG['m.0k3qy8']=['film.performance.character']
[User]
Execution result: 
['m.0k3qy8', 'film.performance.character', 'Padmé Amidala']
[ChatGPT]
Statement: Since Natalie Portman played 'Padmé Amidala' character in 'Star Wars Episode I: The Phantom Menace', the answer for given claim is 'Padmé Amidala'.
Helper function: Verification['Padmé Amidala']


Example 3)
Claim: what country is the grand bahama island in?
Given entity: ('Grand Bahama', 'm.03st9j')

[ChatGPT]
Statement: First, I need information about Grand Bahama.
Helper function: getRelation['Grand Bahama']
[User]
Execution result: 
Relation_list['Grand Bahama'] = ['location.location.nearby_airports', 'location.location.time_zones', 'common.topic.description', 'common.identity.daylife_topic', 'location.location.people_born_here', 'common.topic.notable_for', 'location.location.containedby', 'location.location.area']
[ChatGPT]
Statement: To know the where the Grand Bahama is located in, we have to explore graph using related relations.
Helper function: exploreKG['Grand Bahama']=['location.location.containedby', 'location.location.area']
[User]
Execution result:
['Grand Bahama', 'location.location.containedby', 'Bahamas'], ['Grand Bahama', 'location.location.area', '1373.0']
[ChatGPT]
Statement: From the evidences, Grand Bahama is in the country 'Bahamas'. Therefore, the answer for the claim is 'Bahamas'.
Helper function: Verifiation['Bahamas']



Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>

"""

freebase_main_agent_multistep = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use one of the helper functions below to find the evidence for finding labels.

Helper Functions
1.getRelation[entity]: Returns the list of relations linked to the entity. You can choose several relations from the list that seem related to the claim.
2.exploreKG[entity]=[relation_1,relation_2, ... relation_K]: Returns the triple set around the entity. For example, [entity, relation_1, tail entity] etc. You can choose relation from [User]'s execution result.
3.Verification[[list of entities]]: If you can find the answer entities from collected evidences, give the answer.

You must follow the exact format of the given helper function. You can use multiple helper functions in one step by using '##' between functions.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for my response. If response has made, continue your 'Statement and Helper function' task.
Importantly, if there is an entity starting with 'm.', it is a MID entity. Additional information must be found from that entity.
Also, when you verify the answer, you must not bring the exact name of the answer entity from the evidences (Do not change the name or form of the entity).

Example 1)
Claim: what is the name of justin bieber brother?
Given entity: ('Justin Bieber', 'm.06w2sn5')

[ChatGPT]
Statement: I need to look around the the given entities. First, I need the relation list linked to Justin Bieber.
Helper function: getRelation['Justin Bieber']
[User]
Execution result: 
Relation_list['Justin Bieber'] = ['people.person.education', 'music.artist.track', 'authority.musicbrainz', 'people.person.places_lived', 'common.topic.notable_types', 'celebrities.celebrity.celebrity_friends', 'award.award_nominee.award_nominations', 'base.popstra.celebrity.friendship', 'people.person.parents', 'people.person.sibling_s', 'type.object.key', 'authority.netflix.api']
[ChatGPT]
Statement: To find the brother of Justin Bieber, I need to explore the graph about the siblings of Justin Bieber.
Helper function: exploreKG['Justin Bieber']=['people.person.sibling_s']
[User]
Execution result: 
['Justin Bieber', 'people.person.sibling_s', 'm.0gxnnwp'], ['Justin Bieber', 'people.person.sibling_s', 'm.0gxnnwc']
[ChatGPT]
Statement: There are MIDs connected to Justin Bieber, and we have to find additional information from the MIDs. I need the relation list linked to those MIDs.
Helper function: getRelation['m.0gxnnwp'] ## getRelation['m.0gxnnwc']
[User]
Execution result: 
Relation_list['m.0gxnnwp'] = ['people.sibling_relationship.sibling', 'type.objet.type']
Relation_list['m.0gxnnwc'] = ['people.sibling_relationship.sibling', 'type.objet.type']
[ChatGPT]
Statement: Since we have to find connected sibling from the MIDs, I need to explore the graph from MID to related relations.
Helper function: exploreKG['m.gxnnwp']=['people.sibling_relationship.sibling'] ## exploreKG['m.0gxnnwc']=['people.sibling_relationship.sibling']
[User]
Execution result: 
['m.gxnnwp', 'people.sibling_relationship.sibling', 'Jaxon Bieber']
['m.0gxnnwc', 'people.sibling_relationship.sibling', 'Jazmyn Bieber']
[ChatGPT]
Statement: We have two siblings, 'Jaxon Bieber' and 'Jazmyn Bieber'. Claim is asking about the brother of Justin Bieber, therefore we have to find the gender of each sibling.
Helper function: getRelation['Jaxon Bieber'] ## getRelation['Jazmyn Bieber']
[User]
Execution result: 
Relation_list('Jaxon Bieber') = ['people.person.nationality', 'people.person.date_of_birth', 'type.object.name', 'people.person.gender', 'people.person.sibling_s', 'people.person.place_of_birth', 'people.person.parents']
Relation_list('Jazmyn Bieber') = ['people.person.nationality', 'people.person.date_of_birth', 'type.object.name', 'people.person.gender', 'people.person.sibling_s', 'people.person.place_of_birth', 'people.person.parents']
[ChatGPT]
Statement: To find the gender of Jaxon Bieber, I need to explore the graph related to gender.
Helper function: exploreKG['Jaxon Bieber']=['people.person.gender'] ## exploreKG['Jazmyn Bieber']=['people.person.gender']
[User]
Execution result: 
['Jaxon Bieber', 'people.person.gener', 'Male']
['Jazmyn Bieber', 'people.person.gender', 'Female']
[ChatGPT]
Statement: Since only Jaxon Bieber is the male among Justin Bieber's siblings, the name of Justin Bieber's brother is 'Jaxon Bieber'.
Helper function: Verification[['Jaxon Bieber']]


Example 2)
Claim: what character did natalie portman play in star wars?
Given entity: ('Natalie Portman', 'm.09l3p')

[ChatGPT]
Statement: First, I need relations linked to Natalie Portman.
Helper function: getRelation['Natalie Portman']
[User]
Execution result: 
Relation_list('Natalie Portman') = ['people.person.education', 'authority.nndb', 'people.person.religion', 'film.actor.film', 'people.person.places_lived', 'nytimes.topic.uri', 'common.topic.article', 'user.avh.default_domain.ellerdale_topic.ellerdale_id', 'authority.musicbrainz']
[ChatGPT]
Statemnt: I need the information about Natalie Portman's character in Star Wars. Therefore, I need triples linked with the relation about films or characters.
Helper function: exploreKG['Natalie Portman']=['film.actor.film']
[User]
Execution result: 
['Natalie Portman', 'film.actor.film', 'm.07zm_x0'], ['Natalie Portman', 'film.actor.film', 'm.0jv4ds'], ['Natalie Portman', 'film.actor.film', 'm.04dcjy9'], ['Natalie Portman', 'film.actor.film', 'm.0k3qy8']
[ChatGPT]
Statemn : There are MIDs connected to Justin Bieber, and we have to find additional information from the MIDs. I need the relation list linked to those MIDs.
Helper function: getRelation['m.07zm_x0'] ## getRelation['m.0jv4ds'] ## getRelation['m.04dcjy9'] ## getRelation['m.0k3qy8']
[User]
Execution result: 
Relation_list['m.07zm_x0'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
Relation_list['m.0jv4ds'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
Relation_list['m.04dcjy9'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
Relation_list['m.0k3qy8'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
[ChatGPT]
Statement: Since we have to find the film 'Star Wars', I need to explore graph to find film from the MID.
Helper function: exploreKG['m.07zm_x0']=['film.performance.film'] ## exploreKG['m.0jv4ds']=['film.performance.film'] ## exploreKG['m.04dcjy9']=['film.performance.film'] ## exploreKG['m.0k3qy8']=['film.performance.film']
[User]
Execution result:
['m.07zm_x0', 'film.performance.film', 'Your Highness']
['m.0jv4ds', 'film.performance.film', 'Beautiful Girls']
['m.04dcjy9', 'film.performance.film', 'New York, I Love You']
['m.0k3qy8', 'film.performance.film', 'Star Wars Episode I: The Phantom Menace']
[ChatGPT]
Statement: The MID 'm.0k3qy8' is connected to 'Star Wars Episode I: The Phantom Menace', which is 'star wars' mentioned in the claim. Here, I need to find the character that Natalie Portman played.
Helper function: getRelation['m.0k3qy8']
[User]
Execution result:
Relation_list['m.0k3qy8'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
[ChatGPT]
Statement: Since we have to find the character, I need to explore graph with using related relations.
Helper function: exploreKG['m.0k3qy8']=['film.performance.character']
[User]
Execution result: 
['m.0k3qy8', 'film.performance.character', 'Padmé Amidala']
[ChatGPT]
Statement: Since Natalie Portman played 'Padmé Amidala' character in 'Star Wars Episode I: The Phantom Menace', the answer for given claim is 'Padmé Amidala'.
Helper function: Verification[['Padmé Amidala']]


Example 3)
Claim: what movie did angelina jolie direct?
Given entity: ('Angelina Jolie', 'm.0f4vbz')

[ChatGPT]
Statement: First, I need information about Angelina Jolie.
Helper function: getRelation['Angelina Jolie']
[User]
Execution result: 
Relation_list['Angelina Jolie'] = ['people.person.place_of_birth', 'source.videosurf', 'user.alust.default_domain.processed_with_review_queue.question_id', 'film.director.film', 'people.person.education', 'base.popstra.celebrity.eats_at', 'authority.tvrage.person', 'common.topic.notable_types', 'celebrities.celebrity.celebrity_rivals', 'music.group_member.membership', 'type.object.key', 'source.entertainmentweekly.person', 'film.producer.film']
[ChatGPT]
Statement: To find the movie that Angelina Jolie directed, I need to explore the graph about the films that she directed.
Helper function: exploreKG['Angelina Jolie']=['film.director.film']
[User]
Execution result:
['Angelina Jolie', 'film.director.film', 'Unbroken'], ['Angelina Jolie', 'film.director.film', 'A Place in Time'], ['Angelina Jolie', 'film.director.film', 'By the Sea'], ['Angelina Jolie', 'film.director.film', 'In the Land of Blood and Honey']
[ChtGPT]
Statement: We have four movies that Angelina Jolie directed. Claim is asking about the movie that she directed, therefore we have to find the movie that she directed.
Helper function: Verification[['Unbroken', 'A Place in Time', 'By the Sea', 'In the Land of Blood and Honey']]


Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>

"""

freebase_main_agent_multistep_stop_sig = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use one of the helper functions below to find the evidence for finding labels.

Helper Functions
1.getRelation[entity]: Returns the list of relations linked to the entity. You can choose several relations from the list that seem related to the claim.
2.exploreKG[entity]=[relation_1,relation_2, ... relation_K]: Returns the triple set around the entity. For example, [entity, relation_1, tail entity] etc. You can choose relation from [User]'s execution result.
3.Verification[[list of entities]]: If you can find the answer entities from collected evidences, give the answer.

You must follow the exact format of the given helper function. You can use multiple helper functions in one step by using '##' between functions.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for [User] response. If response has made, continue your [Your Task] (Do not make multiple 'Helper function: ' lines).
Importantly, if there is an entity starting with 'm.', it is a MID entity. Additional information must be found from that entity.
Also, when you verify the answer, you must not modify the exact name of the answer entity from the evidences (Do not change the name or form of the entity).

Example 1)
Claim: what is the name of justin bieber brother?
Given entity: ('Justin Bieber', 'm.06w2sn5')

[Your Task]
Statement: I need to look around the the given entities. First, I need the relation list linked to Justin Bieber.
Helper function: getRelation['Justin Bieber']
*** Stop for [User] response ***
[User]
Execution result: 
Relation_list['Justin Bieber'] = ['people.person.education', 'music.artist.track', 'authority.musicbrainz', 'people.person.places_lived', 'common.topic.notable_types', 'celebrities.celebrity.celebrity_friends', 'award.award_nominee.award_nominations', 'base.popstra.celebrity.friendship', 'people.person.parents', 'people.person.sibling_s', 'type.object.key', 'authority.netflix.api']
[Your Task]
Statement: To find the brother of Justin Bieber, I need to explore the graph about the siblings of Justin Bieber.
Helper function: exploreKG['Justin Bieber']=['people.person.sibling_s']
*** Stop for [User] response ***
[User]
Execution result: 
['Justin Bieber', 'people.person.sibling_s', 'm.0gxnnwp'], ['Justin Bieber', 'people.person.sibling_s', 'm.0gxnnwc']
[Your Task]
Statement: There are MIDs connected to Justin Bieber, and we have to find additional information from the MIDs. I need the relation list linked to those MIDs.
Helper function: getRelation['m.0gxnnwp'] ## getRelation['m.0gxnnwc']
*** Stop for [User] response ***
[User]
Execution result: 
Relation_list['m.0gxnnwp'] = ['people.sibling_relationship.sibling', 'type.objet.type']
Relation_list['m.0gxnnwc'] = ['people.sibling_relationship.sibling', 'type.objet.type']
[Your Task]
Statement: Since we have to find connected sibling from the MIDs, I need to explore the graph from MID to related relations.
Helper function: exploreKG['m.gxnnwp']=['people.sibling_relationship.sibling'] ## exploreKG['m.0gxnnwc']=['people.sibling_relationship.sibling']
*** Stop for [User] response ***
[User]
Execution result: 
['m.gxnnwp', 'people.sibling_relationship.sibling', 'Jaxon Bieber']
['m.0gxnnwc', 'people.sibling_relationship.sibling', 'Jazmyn Bieber']
[Your Task]
Statement: We have two siblings, 'Jaxon Bieber' and 'Jazmyn Bieber'. Claim is asking about the brother of Justin Bieber, therefore we have to find the gender of each sibling.
Helper function: getRelation['Jaxon Bieber'] ## getRelation['Jazmyn Bieber']
*** Stop for [User] response ***
[User]
Execution result: 
Relation_list('Jaxon Bieber') = ['people.person.nationality', 'people.person.date_of_birth', 'type.object.name', 'people.person.gender', 'people.person.sibling_s', 'people.person.place_of_birth', 'people.person.parents']
Relation_list('Jazmyn Bieber') = ['people.person.nationality', 'people.person.date_of_birth', 'type.object.name', 'people.person.gender', 'people.person.sibling_s', 'people.person.place_of_birth', 'people.person.parents']
[Your Task]
Statement: To find the gender of Jaxon Bieber, I need to explore the graph related to gender.
Helper function: exploreKG['Jaxon Bieber']=['people.person.gender'] ## exploreKG['Jazmyn Bieber']=['people.person.gender']
*** Stop for [User] response ***
[User]
Execution result: 
['Jaxon Bieber', 'people.person.gener', 'Male']
['Jazmyn Bieber', 'people.person.gender', 'Female']
[Your Task]
Statement: Since only Jaxon Bieber is the male among Justin Bieber's siblings, the name of Justin Bieber's brother is 'Jaxon Bieber'.
Helper function: Verification[['Jaxon Bieber']]


Example 2)
Claim: what character did natalie portman play in star wars?
Given entity: ('Natalie Portman', 'm.09l3p')

[Your Task]
Statement: First, I need relations linked to Natalie Portman.
Helper function: getRelation['Natalie Portman']
*** Stop for [User] response ***
[User]
Execution result: 
Relation_list('Natalie Portman') = ['people.person.education', 'authority.nndb', 'people.person.religion', 'film.actor.film', 'people.person.places_lived', 'nytimes.topic.uri', 'common.topic.article', 'user.avh.default_domain.ellerdale_topic.ellerdale_id', 'authority.musicbrainz']
[Your Task]
Statemnt: I need the information about Natalie Portman's character in Star Wars. Therefore, I need triples linked with the relation about films or characters.
Helper function: exploreKG['Natalie Portman']=['film.actor.film']
*** Stop for [User] response ***
[User]
Execution result: 
['Natalie Portman', 'film.actor.film', 'm.07zm_x0'], ['Natalie Portman', 'film.actor.film', 'm.0jv4ds'], ['Natalie Portman', 'film.actor.film', 'm.04dcjy9'], ['Natalie Portman', 'film.actor.film', 'm.0k3qy8']
[Your Task]
Statemn : There are MIDs connected to Justin Bieber, and we have to find additional information from the MIDs. I need the relation list linked to those MIDs.
Helper function: getRelation['m.07zm_x0'] ## getRelation['m.0jv4ds'] ## getRelation['m.04dcjy9'] ## getRelation['m.0k3qy8']
*** Stop for [User] response ***
[User]
Execution result: 
Relation_list['m.07zm_x0'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
Relation_list['m.0jv4ds'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
Relation_list['m.04dcjy9'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
Relation_list['m.0k3qy8'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
[Your Task]
Statement: Since we have to find the film 'Star Wars', I need to explore graph to find film from the MID.
Helper function: exploreKG['m.07zm_x0']=['film.performance.film'] ## exploreKG['m.0jv4ds']=['film.performance.film'] ## exploreKG['m.04dcjy9']=['film.performance.film'] ## exploreKG['m.0k3qy8']=['film.performance.film']
*** Stop for [User] response ***
[User]
Execution result:
['m.07zm_x0', 'film.performance.film', 'Your Highness']
['m.0jv4ds', 'film.performance.film', 'Beautiful Girls']
['m.04dcjy9', 'film.performance.film', 'New York, I Love You']
['m.0k3qy8', 'film.performance.film', 'Star Wars Episode I: The Phantom Menace']
[Your Task]
Statement: The MID 'm.0k3qy8' is connected to 'Star Wars Episode I: The Phantom Menace', which is 'star wars' mentioned in the claim. Here, I need to find the character that Natalie Portman played.
Helper function: getRelation['m.0k3qy8']
*** Stop for [User] response ***
[User]
Execution result:
Relation_list['m.0k3qy8'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
[Your Task]
Statement: Since we have to find the character, I need to explore graph with using related relations.
Helper function: exploreKG['m.0k3qy8']=['film.performance.character']
*** Stop for [User] response ***
[User]
Execution result: 
['m.0k3qy8', 'film.performance.character', 'Padmé Amidala']
[Your Task]
Statement: Since Natalie Portman played 'Padmé Amidala' character in 'Star Wars Episode I: The Phantom Menace', the answer for given claim is 'Padmé Amidala'.
Helper function: Verification[['Padmé Amidala']]


Example 3)
Claim: what movie did angelina jolie direct?
Given entity: ('Angelina Jolie', 'm.0f4vbz')

[Your Task]
Statement: First, I need information about Angelina Jolie.
Helper function: getRelation['Angelina Jolie']
*** Stop for [User] response ***
[User]
Execution result: 
Relation_list['Angelina Jolie'] = ['people.person.place_of_birth', 'source.videosurf', 'user.alust.default_domain.processed_with_review_queue.question_id', 'film.director.film', 'people.person.education', 'base.popstra.celebrity.eats_at', 'authority.tvrage.person', 'common.topic.notable_types', 'celebrities.celebrity.celebrity_rivals', 'music.group_member.membership', 'type.object.key', 'source.entertainmentweekly.person', 'film.producer.film']
[Your Task]
Statement: To find the movie that Angelina Jolie directed, I need to explore the graph about the films that she directed.
Helper function: exploreKG['Angelina Jolie']=['film.director.film']
*** Stop for [User] response ***
[User]
Execution result:
['Angelina Jolie', 'film.director.film', 'Unbroken'], ['Angelina Jolie', 'film.director.film', 'A Place in Time'], ['Angelina Jolie', 'film.director.film', 'By the Sea'], ['Angelina Jolie', 'film.director.film', 'In the Land of Blood and Honey']
[Your Task]
Statement: We have four movies that Angelina Jolie directed. Claim is asking about the movie that she directed, therefore we have to find the movie that she directed.
Helper function: Verification[['Unbroken', 'A Place in Time', 'By the Sea', 'In the Land of Blood and Honey']]


Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>

"""

freebase_main_agent_multistep_subagent = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use one of the helper functions below to find the evidence for finding labels.

Helper Functions
1.getRelation[entity]: Returns the list of relations linked to the entity. You can choose several relations from the list that seem related to the claim.
2.exploreKG[entity]=[relation_1,relation_2, ... relation_K]: Returns the triple set around the entity. For example, [entity, relation_1, tail entity] etc. You can choose relation from [User]'s execution result.
3.Verification[]: If you can answer the claim with enought evidence, call this function. If [User] requires more information, you need to collect more triples in following steps.

You must follow the exact format of the given helper function. You can use multiple helper functions in one step by using '##' between functions.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for my response. If response has made, continue your 'Statement and Helper function' task.
Importantly, if there is an entity starting with 'm.', it is a MID entity. Additional information must be found from that entity.

Example 1)
Claim: what is the name of justin bieber brother?
Given entity: ('Justin Bieber', 'm.06w2sn5')

[ChatGPT]
Statement: I need to look around the the given entities. First, I need the relation list linked to Justin Bieber.
Helper function: getRelation['Justin Bieber']
[User]
Execution result: 
Relation_list['Justin Bieber'] = ['people.person.education', 'music.artist.track', 'authority.musicbrainz', 'people.person.places_lived', 'common.topic.notable_types', 'celebrities.celebrity.celebrity_friends', 'award.award_nominee.award_nominations', 'base.popstra.celebrity.friendship', 'people.person.parents', 'people.person.sibling_s', 'type.object.key', 'authority.netflix.api']
[ChatGPT]
Statement: To find the brother of Justin Bieber, I need to explore the graph about the siblings of Justin Bieber.
Helper function: exploreKG['Justin Bieber']=['people.person.sibling_s']
[User]
Execution result: 
['Justin Bieber', 'people.person.sibling_s', 'm.0gxnnwp'], ['Justin Bieber', 'people.person.sibling_s', 'm.0gxnnwc']
[ChatGPT]
Statement: There are MIDs connected to Justin Bieber, and we have to find additional information from the MIDs. I need the relation list linked to those MIDs.
Helper function: getRelation['m.0gxnnwp'] ## getRelation['m.0gxnnwc']
[User]
Execution result: 
Relation_list['m.0gxnnwp'] = ['people.sibling_relationship.sibling', 'type.objet.type']
Relation_list['m.0gxnnwc'] = ['people.sibling_relationship.sibling', 'type.objet.type']
[ChatGPT]
Statement: Since we have to find connected sibling from the MIDs, I need to explore the graph from MID to related relations.
Helper function: exploreKG['m.gxnnwp']=['people.sibling_relationship.sibling'] ## exploreKG['m.0gxnnwc']=['people.sibling_relationship.sibling']
[User]
Execution result: 
['m.gxnnwp', 'people.sibling_relationship.sibling', 'Jaxon Bieber']
['m.0gxnnwc', 'people.sibling_relationship.sibling', 'Jazmyn Bieber']
[ChatGPT]
Statement: We have two siblings, 'Jaxon Bieber' and 'Jazmyn Bieber'. Claim is asking about the brother of Justin Bieber, therefore we have to find the gender of each sibling.
Helper function: getRelation['Jaxon Bieber'] ## getRelation['Jazmyn Bieber']
[User]
Execution result: 
Relation_list('Jaxon Bieber') = ['people.person.nationality', 'people.person.date_of_birth', 'type.object.name', 'people.person.gender', 'people.person.sibling_s', 'people.person.place_of_birth', 'people.person.parents']
Relation_list('Jazmyn Bieber') = ['people.person.nationality', 'people.person.date_of_birth', 'type.object.name', 'people.person.gender', 'people.person.sibling_s', 'people.person.place_of_birth', 'people.person.parents']
[ChatGPT]
Statement: To find the gender of Jaxon Bieber, I need to explore the graph related to gender.
Helper function: exploreKG['Jaxon Bieber']=['people.person.gender'] ## exploreKG['Jazmyn Bieber']=['people.person.gender']
[User]
Execution result: 
['Jaxon Bieber', 'people.person.gener', 'Male']
['Jazmyn Bieber', 'people.person.gender', 'Female']
[ChatGPT]
Statement: Since only Jaxon Bieber is the male among Justin Bieber's siblings, the name of Justin Bieber's brother is 'Jaxon Bieber'.
Helper function: Verification[]


Example 2)
Claim: what character did natalie portman play in star wars?
Given entity: ('Natalie Portman', 'm.09l3p')

[ChatGPT]
Statement: First, I need relations linked to Natalie Portman.
Helper function: getRelation['Natalie Portman']
[User]
Execution result: 
Relation_list('Natalie Portman') = ['people.person.education', 'authority.nndb', 'people.person.religion', 'film.actor.film', 'people.person.places_lived', 'nytimes.topic.uri', 'common.topic.article', 'user.avh.default_domain.ellerdale_topic.ellerdale_id', 'authority.musicbrainz']
[ChatGPT]
Statemnt: I need the information about Natalie Portman's character in Star Wars. Therefore, I need triples linked with the relation about films or characters.
Helper function: exploreKG['Natalie Portman']=['film.actor.film']
[User]
Execution result: 
['Natalie Portman', 'film.actor.film', 'm.07zm_x0'], ['Natalie Portman', 'film.actor.film', 'm.0jv4ds'], ['Natalie Portman', 'film.actor.film', 'm.04dcjy9'], ['Natalie Portman', 'film.actor.film', 'm.0k3qy8']
[ChatGPT]
Statemn : There are MIDs connected to Justin Bieber, and we have to find additional information from the MIDs. I need the relation list linked to those MIDs.
Helper function: getRelation['m.07zm_x0'] ## getRelation['m.0jv4ds'] ## getRelation['m.04dcjy9'] ## getRelation['m.0k3qy8']
[User]
Execution result: 
Relation_list['m.07zm_x0'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
Relation_list['m.0jv4ds'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
Relation_list['m.04dcjy9'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
Relation_list['m.0k3qy8'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
[ChatGPT]
Statement: Since we have to find the film 'Star Wars', I need to explore graph to find film from the MID.
Helper function: exploreKG['m.07zm_x0']=['film.performance.film'] ## exploreKG['m.0jv4ds']=['film.performance.film'] ## exploreKG['m.04dcjy9']=['film.performance.film'] ## exploreKG['m.0k3qy8']=['film.performance.film']
[User]
Execution result:
['m.07zm_x0', 'film.performance.film', 'Your Highness']
['m.0jv4ds', 'film.performance.film', 'Beautiful Girls']
['m.04dcjy9', 'film.performance.film', 'New York, I Love You']
['m.0k3qy8', 'film.performance.film', 'Star Wars Episode I: The Phantom Menace']
[ChatGPT]
Statement: The MID 'm.0k3qy8' is connected to 'Star Wars Episode I: The Phantom Menace', which is 'star wars' mentioned in the claim. Here, I need to find the character that Natalie Portman played.
Helper function: getRelation['m.0k3qy8']
[User]
Execution result:
Relation_list['m.0k3qy8'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
[ChatGPT]
Statement: Since we have to find the character, I need to explore graph with using related relations.
Helper function: exploreKG['m.0k3qy8']=['film.performance.character']
[User]
Execution result: 
['m.0k3qy8', 'film.performance.character', 'Padmé Amidala']
[ChatGPT]
Statement: Since Natalie Portman played 'Padmé Amidala' character in 'Star Wars Episode I: The Phantom Menace', the answer for given claim is 'Padmé Amidala'.
Helper function: Verification[]


Example 3)
Claim: what country is the grand bahama island in?
Given entity: ('Grand Bahama', 'm.03st9j')

[ChatGPT]
Statement: First, I need information about Grand Bahama.
Helper function: getRelation['Grand Bahama']
[User]
Execution result: 
Relation_list['Grand Bahama'] = ['location.location.nearby_airports', 'location.location.time_zones', 'common.topic.description', 'common.identity.daylife_topic', 'location.location.people_born_here', 'common.topic.notable_for', 'location.location.containedby', 'location.location.area']
[ChatGPT]
Statement: To know the where the Grand Bahama is located in, we have to explore graph using related relations.
Helper function: exploreKG['Grand Bahama']=['location.location.containedby', 'location.location.area']
[User]
Execution result:
['Grand Bahama', 'location.location.containedby', 'Bahamas'], ['Grand Bahama', 'location.location.area', '1373.0']
[ChatGPT]
Statement: From the evidences, Grand Bahama is in the country 'Bahamas'. Therefore, the answer for the claim is 'Bahamas'.
Helper function: Verification[]



Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>

"""
freebase_main_agent_multistep_subagent_stop_sig = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use one of the helper functions below to find the evidence for finding labels.

Helper Functions
1.getRelation[entity]: Returns the list of relations linked to the entity. You can choose several relations from the list that seem related to the claim.
2.exploreKG[entity]=[relation_1,relation_2, ... relation_K]: Returns the triple set around the entity. For example, [entity, relation_1, tail entity] etc. You can choose relation from [User]'s execution result.
3.Verification[]: If you can answer the claim with enought evidence, call this function. If [User] requires more information, you need to collect more triples in following steps.

You must follow the exact format of the given helper function. You can use multiple helper functions in one step by using '##' between functions.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for [User] response. If response has made, continue your [Your Task] (Do not make multiple 'Helper function: ' lines).
Importantly, if there is an entity starting with 'm.', it is a MID entity. Additional information must be found from that entity.


Example 1)
Claim: what character did john noble play in lord of the rings?
Given entity: ('John Noble', 'm.02fgm7')

[Your Task]
Statement: I need to look around the the given entities. First, I need the relation list linked to John Noble.
Helper function: getRelation['John Noble']
*** Stop for [User] response ***
[User]
Execution result: 
Relation_list['John Noble'] = ['film.actor.film', 'type.object.key', 'award.award_winner.awards_won', 'type.object.name', 'user.robert.default_domain.daylife.hero_image_id', 'authority.tvrage.person', 'people.person.profession', 'base.ranker.rankerurlname', 'source.filmstarts.personen', 'user.avh.default_domain.ellerdale_topic.ellerdale_id']
[Your Task]
Statement: To find the character that John Noble played in 'Lord of the Rings', I need to explore the graph about the films that John Noble acted.
Helper function: exploreKG['John Noble']=['film.actor.film']
*** Stop for [User] response ***
[User]
Execution result: 
['John Noble', 'film.actor.film', 'm.0h5jyl5'], ['John Noble', 'film.actor.film', 'm.010h3gm8], ['John Noble', 'film.actor.film', 'm.0cf_87h'], ['John Noble', 'film.actor.film', 'm.03l6qx7'], ['John Noble', 'film.actor.film', 'm.0h5jyj9'], ['John Noble', 'film.actor.film', 'm.0h5jyfk'], ['John Noble', 'film.actor.film', 'm.0528y98']
[Your Task]
Statement: To find which MID is connected to 'Lord of the Rings', I need to check the relation list.
Helper function: getRelation['m.0h5jyl5'] ## getRelation['m.010h3gm8'] ## getRelation['m.0cf_87h'] ## getRelation['m.03l6qx7'] ## getRelation['m.0h5jyj9'] ## getRelation['m.0h5jyfk'] ## getRelation['m.0528y98']
*** Stop for [User] response ***
[User]
Execution result:
Relation_list['m.0h5jyl5'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
Relation_list['m.010h3gm8'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
Relation_list['m.0cf_87h'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
Relation_list['m.03l6qx7'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
Relation_list['m.0h5jyj9'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
Relation_list['m.0h5jyfk'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
Relation_list['m.0528y98'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
[Your Task]
Statement: To find the MID connected to 'Lord of the Rings', I need to explore the graph using the relation list.
Helper function: exploreKG['m.0h5jyl5']=['film.performance.film'] ## exploreKG['m.010h3gm8']=['film.performance.film'] ## exploreKG['m.0cf_87h']=['film.performance.film'] ## exploreKG['m.03l6qx7']=['film.performance.film'] ## exploreKG['m.0h5jyj9']=['film.performance.film'] ## exploreKG['m.0h5jyfk']=['film.performance.film'] ## exploreKG['m.0528y98']=['film.performance.film']
*** Stop for [User] response ***
[User]
Execution result:
['m.0h5jyl5', 'film.performance.film', 'Call Me Mr. Brown']
['m.010h3gm8', 'film.performance.film', 'The Mule']
['m.0cf_87h', 'film.performance.film', 'Running Scared']
['m.03l6qx7', 'film.performance.film', 'The Lord of the Rings: The Return of the King']
['m.0h5jyj9', 'film.performance.film', 'The Dreaming']
['m.0h5jyfk', 'film.performance.film', 'Virtual Nightmare']
['m.0528y98', 'film.performance.film', 'The Lord of the Rings: The Two Towers']
[Your Task]
Statement: There are two 'Lord of the Rings' films, and I need to find the character that John Noble played in those films. Therefore, I need to explore the graph using the relation list.
Helper function: exploreKG['m.03l6qx7']=['film.performance.character'] ## exploreKG['m.0528y98']=['film.performance.character']
*** Stop for [User] response ***
[User]
Execution result:
['m.03l6qx7', 'film.performance.character', 'Denethor II']
['m.0528y98', 'film.performance.character', 'Denethor II']
[Your Task]
Statement: Since John Noble played 'Denethor II' character in 'Lord of the Rings', the answer for given claim is 'Denethor II'.
Helper function: Verification[]

Example 2)
Claim: where is rome italy located on a map?
Given entity: ('Rome', 'm.06c62')

[Your Task]
Statement: First, I need to find the information about Rome.
Helper function: getRelation['Rome']
*** Stop for [User] response ***
[User]
Execution result:
Relation_list['Rome'] = ['location.location.nearby_airports', 'location.location.time_zones', 'common.topic.description', 'common.identity.daylife_topic', 'location.location.people_born_here', 'common.topic.notable_for', 'location.location.containedby', 'location.location.area', 'location.location.geolocation']
[Your Task]
Statement: To find the location of Rome on a map, I need to explore the graph using the relation list.
Helper function: exploreKG['Rome']=['location.location.containedby']
*** Stop for [User] response ***
[User]
Execution result:
['Rome', 'location.location.containedby', 'Italy'], ['Rome', 'location.location.containedby', 'Lazio'], ['Rome', 'location.location.containedby', 'Province of Rome']
[Your Task]
Statement: From the evidence, Rome is contained within the region of 'Italy', 'Lazio', and 'Province of Rome'. Therefore, the answer for the claim is 'Italy', 'Lazio', and 'Province of Rome'.
Helper function: Verification[]

Example 3)
Claim: what is cher's son's name?
Given entity: ('Cher', 'm.01vtj38')

[Your Task]
Statement: First, I need to find the information about Cher.
Helper function: getRelation['Cher']
*** Stop for [User] response ***
[User]
Execution result:
Relation_list['Cher'] = ['people.person.children', 'people.person.profession', 'people.person.gender', 'people.person.height_meters', 'people.person.sibling_s', 'common.topic.notable_for', 'common.topic.alias', 'common.topic.article', 'common.topic.topical_webpage', 'common.topic.notable_types', 'common.identity.daylife_topic', 'user.robert.default_domain.daylife.hero_image_id', 'user.brendan.default_domain.top_architectural_city.structure_count', 'user.enrico_speranza.default_domain.italian_city.cod_istat', 'base.ranker.rankerurlname', 'base.chickipedia.topic.chickipedia_id', 'source.allocine.fr.personne', 'people.person.ethnicity']
[Your Task]
Statement: To find the son of Cher, I need to explore the graph using the relation list.
Helper function: exploreKG['Cher']=['people.person.children']
*** Stop for [User] response ***
[User]
Execution result:
['Cher', 'people.person.children', 'Chaz Bono'], ['Cher', 'people.person.children', 'Elijah Blue Allman']
[Your Task]
Statement: 'Cher' has two children, 'Chaz Bono' and 'Elijah Blue Allman'. Here, we have to find the gender of the children to find the son of Cher.
Helper function: getRelation['Chaz Bono'] ## getRelation['Elijah Blue Allman']
*** Stop for [User] response ***
[User]
Execution result:
Relation_list['Chaz Bono'] = ['people.person.gender', 'common.topic.article', 'people.person.sibling_s', 'common.topic.description', 'film.film_subject.films', 'kg.object_profile.prominent_type', 'film.actor.film', 'tv.tv_program_guest.appeared_on', 'type.object.key', 'base.activism.activist.area_of_activism']
Relation_list['Elijah Blue Allman'] = ['people.person.gender', 'common.topic.article', 'people.person.sibling_s', 'common.topic.description', 'film.film_subject.films', 'kg.object_profile.prominent_type', 'film.actor.film', 'tv.tv_program_guest.appeared_on', 'type.object.key', 'base.activism.activist.area_of_activism']
[Your Task]
Statement: To find the gender of 'Chaz Bono' and 'Elijah Blue Allman', I need to explore the graph using the relation list.
Helper function: exploreKG['Chaz Bono']=['people.person.gender'] ## exploreKG['Elijah Blue Allman']=['people.person.gender']
*** Stop for [User] response ***
[User]
Execution result:
['Chaz Bono', 'people.person.gender', 'Male']
['Elijah Blue Allman', 'people.person.gender', 'Male']
[Your Task]
Statement: Since both 'Chaz Bono' and 'Elijah Blue Allman' are male, the sons of Cher are 'Chaz Bono' and 'Elijah Blue Allman'.
Helper function: Verification[]


Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>

"""

freebase_main_agent_multistep_2 = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use one of the helper functions below to find the evidence for finding labels.

Helper Functions
1.getRelation[entity]: Returns the list of relations linked to the entity. You can choose several relations from the list that seem related to the claim.
2.exploreKG[entity]=[relation_1,relation_2, ... relation_K]: Returns the triple set around the entity. For example, [entity, relation_1, tail entity] etc. You can choose relation from [User]'s execution result.
3.Verification[]: If you can answer the claim with enought evidence, call this function. If [User] requires more information, you need to collect more triples in following steps.

You must follow the exact format of the given helper function. You can use multiple helper functions in one step by using '##' between functions.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for my response. If response has made, continue your 'Statement and Helper function' task.
Importantly, if there is an entity starting with 'm.', it is a MID entity. Additional information must be found from that entity.


Example 1)
Claim: what character did john noble play in lord of the rings?
Given entity: ('John Noble', 'm.02fgm7')

[ChatGPT]
Statement: I need to look around the the given entities. First, I need the relation list linked to John Noble.
Helper function: getRelation['John Noble']
[User]
Execution result: 
Relation_list['John Noble'] = ['film.actor.film', 'type.object.key', 'award.award_winner.awards_won', 'type.object.name', 'user.robert.default_domain.daylife.hero_image_id', 'authority.tvrage.person', 'people.person.profession', 'base.ranker.rankerurlname', 'source.filmstarts.personen', 'user.avh.default_domain.ellerdale_topic.ellerdale_id']
[ChatGPT]
Statement: To find the character that John Noble played in 'Lord of the Rings', I need to explore the graph about the films that John Noble acted.
Helper function: exploreKG['John Noble']=['film.actor.film']
[User]
Execution result: 
['John Noble', 'film.actor.film', 'm.0h5jyl5'], ['John Noble', 'film.actor.film', 'm.010h3gm8], ['John Noble', 'film.actor.film', 'm.0cf_87h'], ['John Noble', 'film.actor.film', 'm.03l6qx7'], ['John Noble', 'film.actor.film', 'm.0h5jyj9'], ['John Noble', 'film.actor.film', 'm.0h5jyfk'], ['John Noble', 'film.actor.film', 'm.0528y98']
[ChatGPT]
Statement: To find which MID is connected to 'Lord of the Rings', I need to check the relation list.
Helper function: getRelation['m.0h5jyl5'] ## getRelation['m.010h3gm8'] ## getRelation['m.0cf_87h'] ## getRelation['m.03l6qx7'] ## getRelation['m.0h5jyj9'] ## getRelation['m.0h5jyfk'] ## getRelation['m.0528y98']
[User]
Execution result:
Relation_list['m.0h5jyl5'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
Relation_list['m.010h3gm8'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
Relation_list['m.0cf_87h'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
Relation_list['m.03l6qx7'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
Relation_list['m.0h5jyj9'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
Relation_list['m.0h5jyfk'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
Relation_list['m.0528y98'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
[ChatGPT]
Statement: To find the MID connected to 'Lord of the Rings', I need to explore the graph using the relation list.
Helper function: exploreKG['m.0h5jyl5']=['film.performance.film'] ## exploreKG['m.010h3gm8']=['film.performance.film'] ## exploreKG['m.0cf_87h']=['film.performance.film'] ## exploreKG['m.03l6qx7']=['film.performance.film'] ## exploreKG['m.0h5jyj9']=['film.performance.film'] ## exploreKG['m.0h5jyfk']=['film.performance.film'] ## exploreKG['m.0528y98']=['film.performance.film']
[User]
Execution result:
['m.0h5jyl5', 'film.performance.film', 'Call Me Mr. Brown']
['m.010h3gm8', 'film.performance.film', 'The Mule']
['m.0cf_87h', 'film.performance.film', 'Running Scared']
['m.03l6qx7', 'film.performance.film', 'The Lord of the Rings: The Return of the King']
['m.0h5jyj9', 'film.performance.film', 'The Dreaming']
['m.0h5jyfk', 'film.performance.film', 'Virtual Nightmare']
['m.0528y98', 'film.performance.film', 'The Lord of the Rings: The Two Towers']
[ChatGPT]
Statement: There are two 'Lord of the Rings' films, and I need to find the character that John Noble played in those films. Therefore, I need to explore the graph using the relation list.
Helper function: exploreKG['m.03l6qx7']=['film.performance.character'] ## exploreKG['m.0528y98']=['film.performance.character']
[User]
Execution result:
['m.03l6qx7', 'film.performance.character', 'Denethor II']
['m.0528y98', 'film.performance.character', 'Denethor II']
[ChatGPT]
Statement: Since John Noble played 'Denethor II' character in 'Lord of the Rings', the answer for given claim is 'Denethor II'.
Helper function: Verification[['Denethor II']]

Example 2)
Claim: where is rome italy located on a map?
Given entity: ('Rome', 'm.06c62')

[ChatGPT]
Statement: First, I need to find the information about Rome.
Helper function: getRelation['Rome']
[User]
Execution result:
Relation_list['Rome'] = ['location.location.nearby_airports', 'location.location.time_zones', 'common.topic.description', 'common.identity.daylife_topic', 'location.location.people_born_here', 'common.topic.notable_for', 'location.location.containedby', 'location.location.area', 'location.location.geolocation']
[ChatGPT]
Statement: To find the location of Rome on a map, I need to explore the graph using the relation list.
Helper function: exploreKG['Rome']=['location.location.containedby']
[User]
Execution result:
['Rome', 'location.location.containedby', 'Italy'], ['Rome', 'location.location.containedby', 'Lazio'], ['Rome', 'location.location.containedby', 'Province of Rome']
[ChatGPT]
Statement: From the evidence, Rome is contained within the region of 'Italy', 'Lazio', and 'Province of Rome'. Therefore, the answer for the claim is 'Italy', 'Lazio', and 'Province of Rome'.
Helper function: Verification[['Italy', 'Lazio', 'Province of Rome']]

Example 3)
Claim: what is cher's son's name?
Given entity: ('Cher', 'm.01vtj38')

[ChatGPT]
Statement: First, I need to find the information about Cher.
Helper function: getRelation['Cher']
[User]
Execution result:
Relation_list['Cher'] = ['people.person.children', 'people.person.profession', 'people.person.gender', 'people.person.height_meters', 'people.person.sibling_s', 'common.topic.notable_for', 'common.topic.alias', 'common.topic.article', 'common.topic.topical_webpage', 'common.topic.notable_types', 'common.identity.daylife_topic', 'user.robert.default_domain.daylife.hero_image_id', 'user.brendan.default_domain.top_architectural_city.structure_count', 'user.enrico_speranza.default_domain.italian_city.cod_istat', 'base.ranker.rankerurlname', 'base.chickipedia.topic.chickipedia_id', 'source.allocine.fr.personne', 'people.person.ethnicity']
[ChatGPT]
Statement: To find the son of Cher, I need to explore the graph using the relation list.
Helper function: exploreKG['Cher']=['people.person.children']
[User]
Execution result:
['Cher', 'people.person.children', 'Chaz Bono'], ['Cher', 'people.person.children', 'Elijah Blue Allman']
[ChatGPT]
Statement: 'Cher' has two children, 'Chaz Bono' and 'Elijah Blue Allman'. Here, we have to find the gender of the children to find the son of Cher.
Helper function: getRelation['Chaz Bono'] ## getRelation['Elijah Blue Allman']
[User]
Execution result:
Relation_list['Chaz Bono'] = ['people.person.gender', 'common.topic.article', 'people.person.sibling_s', 'common.topic.description', 'film.film_subject.films', 'kg.object_profile.prominent_type', 'film.actor.film', 'tv.tv_program_guest.appeared_on', 'type.object.key', 'base.activism.activist.area_of_activism']
Relation_list['Elijah Blue Allman'] = ['people.person.gender', 'common.topic.article', 'people.person.sibling_s', 'common.topic.description', 'film.film_subject.films', 'kg.object_profile.prominent_type', 'film.actor.film', 'tv.tv_program_guest.appeared_on', 'type.object.key', 'base.activism.activist.area_of_activism']
[ChatGPT]
Statement: To find the gender of 'Chaz Bono' and 'Elijah Blue Allman', I need to explore the graph using the relation list.
Helper function: exploreKG['Chaz Bono']=['people.person.gender'] ## exploreKG['Elijah Blue Allman']=['people.person.gender']
[User]
Execution result:
['Chaz Bono', 'people.person.gender', 'Male']
['Elijah Blue Allman', 'people.person.gender', 'Male']
[ChatGPT]
Statement: Since both 'Chaz Bono' and 'Elijah Blue Allman' are male, the sons of Cher are 'Chaz Bono' and 'Elijah Blue Allman'.
Helper function: Verification[['Chaz Bono', 'Elijah Blue Allman']]


Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>

"""

freebase_main_agent_multistep_2_stop_sig = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use one of the helper functions below to find the evidence for finding labels.

Helper Functions
1.getRelation[entity]: Returns the list of relations linked to the entity. You can choose several relations from the list that seem related to the claim.
2.exploreKG[entity]=[relation_1,relation_2, ... relation_K]: Returns the triple set around the entity. For example, [entity, relation_1, tail entity] etc. You can choose relation from [User]'s execution result.
3.Verification[]: If you can answer the claim with enought evidence, call this function. If [User] requires more information, you need to collect more triples in following steps.

You must follow the exact format of the given helper function. You can use multiple helper functions in one step by using '##' between functions.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for [User] response. If response has made, continue your [Your Task] (Do not make multiple 'Helper function: ' lines).
Importantly, if there is an entity starting with 'm.', it is a MID entity. Additional information must be found from that entity.


Example 1)
Claim: what character did john noble play in lord of the rings?
Given entity: ('John Noble', 'm.02fgm7')

[Your Task]
Statement: I need to look around the the given entities. First, I need the relation list linked to John Noble.
Helper function: getRelation['John Noble']
*** Stop for [User] response ***
[User]
Execution result: 
Relation_list['John Noble'] = ['film.actor.film', 'type.object.key', 'award.award_winner.awards_won', 'type.object.name', 'user.robert.default_domain.daylife.hero_image_id', 'authority.tvrage.person', 'people.person.profession', 'base.ranker.rankerurlname', 'source.filmstarts.personen', 'user.avh.default_domain.ellerdale_topic.ellerdale_id']
[Your Task]
Statement: To find the character that John Noble played in 'Lord of the Rings', I need to explore the graph about the films that John Noble acted.
Helper function: exploreKG['John Noble']=['film.actor.film']
*** Stop for [User] response ***
[User]
Execution result: 
['John Noble', 'film.actor.film', 'm.0h5jyl5'], ['John Noble', 'film.actor.film', 'm.010h3gm8], ['John Noble', 'film.actor.film', 'm.0cf_87h'], ['John Noble', 'film.actor.film', 'm.03l6qx7'], ['John Noble', 'film.actor.film', 'm.0h5jyj9'], ['John Noble', 'film.actor.film', 'm.0h5jyfk'], ['John Noble', 'film.actor.film', 'm.0528y98']
[Your Task]
Statement: To find which MID is connected to 'Lord of the Rings', I need to check the relation list.
Helper function: getRelation['m.0h5jyl5'] ## getRelation['m.010h3gm8'] ## getRelation['m.0cf_87h'] ## getRelation['m.03l6qx7'] ## getRelation['m.0h5jyj9'] ## getRelation['m.0h5jyfk'] ## getRelation['m.0528y98']
*** Stop for [User] response ***
[User]
Execution result:
Relation_list['m.0h5jyl5'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
Relation_list['m.010h3gm8'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
Relation_list['m.0cf_87h'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
Relation_list['m.03l6qx7'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
Relation_list['m.0h5jyj9'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
Relation_list['m.0h5jyfk'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
Relation_list['m.0528y98'] = ['film.performance.actor', 'film.performance.character', 'film.performance.film', 'type.object.type']
[Your Task]
Statement: To find the MID connected to 'Lord of the Rings', I need to explore the graph using the relation list.
Helper function: exploreKG['m.0h5jyl5']=['film.performance.film'] ## exploreKG['m.010h3gm8']=['film.performance.film'] ## exploreKG['m.0cf_87h']=['film.performance.film'] ## exploreKG['m.03l6qx7']=['film.performance.film'] ## exploreKG['m.0h5jyj9']=['film.performance.film'] ## exploreKG['m.0h5jyfk']=['film.performance.film'] ## exploreKG['m.0528y98']=['film.performance.film']
*** Stop for [User] response ***
[User]
Execution result:
['m.0h5jyl5', 'film.performance.film', 'Call Me Mr. Brown']
['m.010h3gm8', 'film.performance.film', 'The Mule']
['m.0cf_87h', 'film.performance.film', 'Running Scared']
['m.03l6qx7', 'film.performance.film', 'The Lord of the Rings: The Return of the King']
['m.0h5jyj9', 'film.performance.film', 'The Dreaming']
['m.0h5jyfk', 'film.performance.film', 'Virtual Nightmare']
['m.0528y98', 'film.performance.film', 'The Lord of the Rings: The Two Towers']
[Your Task]
Statement: There are two 'Lord of the Rings' films, and I need to find the character that John Noble played in those films. Therefore, I need to explore the graph using the relation list.
Helper function: exploreKG['m.03l6qx7']=['film.performance.character'] ## exploreKG['m.0528y98']=['film.performance.character']
*** Stop for [User] response ***
[User]
Execution result:
['m.03l6qx7', 'film.performance.character', 'Denethor II']
['m.0528y98', 'film.performance.character', 'Denethor II']
[Your Task]
Statement: Since John Noble played 'Denethor II' character in 'Lord of the Rings', the answer for given claim is 'Denethor II'.
Helper function: Verification[['Denethor II']]

Example 2)
Claim: where is rome italy located on a map?
Given entity: ('Rome', 'm.06c62')

[Your Task]
Statement: First, I need to find the information about Rome.
Helper function: getRelation['Rome']
*** Stop for [User] response ***
[User]
Execution result:
Relation_list['Rome'] = ['location.location.nearby_airports', 'location.location.time_zones', 'common.topic.description', 'common.identity.daylife_topic', 'location.location.people_born_here', 'common.topic.notable_for', 'location.location.containedby', 'location.location.area', 'location.location.geolocation']
[Your Task]
Statement: To find the location of Rome on a map, I need to explore the graph using the relation list.
Helper function: exploreKG['Rome']=['location.location.containedby']
*** Stop for [User] response ***
[User]
Execution result:
['Rome', 'location.location.containedby', 'Italy'], ['Rome', 'location.location.containedby', 'Lazio'], ['Rome', 'location.location.containedby', 'Province of Rome']
[Your Task]
Statement: From the evidence, Rome is contained within the region of 'Italy', 'Lazio', and 'Province of Rome'. Therefore, the answer for the claim is 'Italy', 'Lazio', and 'Province of Rome'.
Helper function: Verification[['Italy', 'Lazio', 'Province of Rome']]

Example 3)
Claim: what is cher's son's name?
Given entity: ('Cher', 'm.01vtj38')

[Your Task]
Statement: First, I need to find the information about Cher.
Helper function: getRelation['Cher']
*** Stop for [User] response ***
[User]
Execution result:
Relation_list['Cher'] = ['people.person.children', 'people.person.profession', 'people.person.gender', 'people.person.height_meters', 'people.person.sibling_s', 'common.topic.notable_for', 'common.topic.alias', 'common.topic.article', 'common.topic.topical_webpage', 'common.topic.notable_types', 'common.identity.daylife_topic', 'user.robert.default_domain.daylife.hero_image_id', 'user.brendan.default_domain.top_architectural_city.structure_count', 'user.enrico_speranza.default_domain.italian_city.cod_istat', 'base.ranker.rankerurlname', 'base.chickipedia.topic.chickipedia_id', 'source.allocine.fr.personne', 'people.person.ethnicity']
[Your Task]
Statement: To find the son of Cher, I need to explore the graph using the relation list.
Helper function: exploreKG['Cher']=['people.person.children']
*** Stop for [User] response ***
[User]
Execution result:
['Cher', 'people.person.children', 'Chaz Bono'], ['Cher', 'people.person.children', 'Elijah Blue Allman']
[Your Task]
Statement: 'Cher' has two children, 'Chaz Bono' and 'Elijah Blue Allman'. Here, we have to find the gender of the children to find the son of Cher.
Helper function: getRelation['Chaz Bono'] ## getRelation['Elijah Blue Allman']
*** Stop for [User] response ***
[User]
Execution result:
Relation_list['Chaz Bono'] = ['people.person.gender', 'common.topic.article', 'people.person.sibling_s', 'common.topic.description', 'film.film_subject.films', 'kg.object_profile.prominent_type', 'film.actor.film', 'tv.tv_program_guest.appeared_on', 'type.object.key', 'base.activism.activist.area_of_activism']
Relation_list['Elijah Blue Allman'] = ['people.person.gender', 'common.topic.article', 'people.person.sibling_s', 'common.topic.description', 'film.film_subject.films', 'kg.object_profile.prominent_type', 'film.actor.film', 'tv.tv_program_guest.appeared_on', 'type.object.key', 'base.activism.activist.area_of_activism']
[Your Task]
Statement: To find the gender of 'Chaz Bono' and 'Elijah Blue Allman', I need to explore the graph using the relation list.
Helper function: exploreKG['Chaz Bono']=['people.person.gender'] ## exploreKG['Elijah Blue Allman']=['people.person.gender']
*** Stop for [User] response ***
[User]
Execution result:
['Chaz Bono', 'people.person.gender', 'Male']
['Elijah Blue Allman', 'people.person.gender', 'Male']
[Your Task]
Statement: Since both 'Chaz Bono' and 'Elijah Blue Allman' are male, the sons of Cher are 'Chaz Bono' and 'Elijah Blue Allman'.
Helper function: Verification[['Chaz Bono', 'Elijah Blue Allman']]


Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>

"""

freebase_main_agent_multistep_3 = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use one of the helper functions below to find the evidence for finding labels.

Helper Functions
1.getRelation[entity]: Returns the list of relations linked to the entity. You can choose several relations from the list that seem related to the claim.
2.exploreKG[entity]=[relation_1,relation_2, ... relation_K]: Returns the triple set around the entity. For example, [entity, relation_1, tail entity] etc. You can choose relation from [User]'s execution result.
3.Verification[]: If you can answer the claim with enought evidence, call this function. If [User] requires more information, you need to collect more triples in following steps.

You must follow the exact format of the given helper function. You can use multiple helper functions in one step by using '##' between functions.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for my response. If response has made, continue your 'Statement and Helper function' task.
Importantly, if there is an entity starting with 'm.', it is a MID entity. Additional information must be found from that entity.


Example 1)
Claim: what was the name of frederick dougalss book?
Given entity: ('Frederick Douglass', 'm.02zg0')

[ChatGPT]
Statement: First, I need to find the information about Frederick Douglass.
Helper function: getRelation['Frederick Douglass']
[User]
Execution result:
Relation_list['Frederick Douglass'] = ['book.author.openlibrary_id', 'authority.openlibrary.author', 'people.person.quotations', 'book.book_subject.works', 'organization.organization_founder.organizations_founded', 'people.deceased_person.cause_of_death', 'people.person.nationality', 'freebase.valuenotation.is_reviewed', 'book.author.works_written']
[ChatGPT]
Statement: To find the name of Frederick Douglass's book, I need to explore the graph using the relation list.
Helper function: exploreKG['Frederick Douglass']=['book.author.works_written']
[User]
Execution result:
['Frederick Douglass', 'book.author.works_written', 'Why Is the Negro Lynched'], ['Frederick Douglass', 'book.author.works_written', 'A Black diplomat in Haiti'], ['Frederick Douglass', 'book.author.works_written', 'Three African-American Classics'], ['Frederick Douglass', 'book.author.works_written', 'The Frederick Douglass Papers, Series 1, Vol. 1: 1841-46'], ['Frederick Douglass', 'book.author.works_written', 'Words of Ages'], ['Frederick Douglass', 'book.author.works_written', 'Standing with the slave'], ['Frederick Douglass', 'book.author.works_written', 'Abolition fanaticism in New York']
[ChatGPT]
Statement: The books that Frederick Douglass wrote are 'Why Is the Negro Lynched', 'A Black diplomat in Haiti', 'Three African-American Classics', 'The Frederick Douglass Papers, Series 1, Vol. 1: 1841-46', 'Words of Ages', 'Standing with the slave', 'Abolition fanaticism in New York'.
Helper function: Verification[['Why Is the Negro Lynched', 'A Black diplomat in Haiti', 'Three African-American Classics', 'The Frederick Douglass Papers, Series 1, Vol. 1: 1841-46', 'Words of Ages', 'Standing with the slave', 'Abolition fanaticism in New York']]

Example 2)
Claim: what character did brian austin green play on 90210?
Given entity: ('Beverly Hills, 90210', 'm.0n2bh')

[ChatGPT]
Statement: First, I need to find the information about Beverly Hills, 90210.
Helper function: getRelation['Beverly Hills, 90210']
[User]
Execution result:
Relation_list['Beverly Hills, 90210'] = ['user.robert.default_domain.rated_tv_program.ew_rating', 'source.videosurf', 'tv.tv_program.thetvdb_id', 'tv.tv_program.spin_offs', 'media_common.netflix_title.netflix_genres', 'tv.tv_program.program_creator', 'common.topic.article', 'tv.tv_program.regular_cast', 'common.topic.description', 'award.award_winning_work.awards_won']
[ChatGPT]
Statement: To find the character that Brian Austin Green played on Beverly Hills, 90210, I need to explore the graph using the relation list.
Helper function: exploreKG['Beverly Hills, 90210']=['tv.tv_program.regular_cast']
[User]
Execution result:
['Beverly Hills, 90210', 'tv.tv_program.regular_cast', 'm.02t94lh'], ['Beverly Hills, 90210', 'tv.tv_program.regular_cast', 'm.04fgn00'], ['Beverly Hills, 90210', 'tv.tv_program.regular_cast', 'm.0220tdl'], ['Beverly Hills, 90210', 'tv.tv_program.regular_cast', 'm.0220tgk'], ['Beverly Hills, 90210', 'tv.tv_program.regular_cast', 'm.0k94mzp']
[ChatGPT]
Statement: There are several MIDs connected to Beverly Hills, 90210. I need to find the MID that is connected to Brian Austin Green.
Helper function: getRelation['m.02t94lh'] ## getRelation['m.04fgn00'] ## getRelation['m.0220tdl'] ## getRelation['m.0220tgk'] ## getRelation['m.0k94mzp']
[User]
Execution result:
Relation_list['m.02t94lh'] = ['tv.regular_tv_appearance.seasons', 'tv.regular_tv_appearance.series', 'tv.regular_tv_appearance.to', 'type.object.type', 'tv.regular_tv_appearance.from', 'tv.regular_tv_appearance.actor', 'tv.regular_tv_appearance.character']
Relation_list['m.04fgn00'] = ['tv.regular_tv_appearance.seasons', 'tv.regular_tv_appearance.series', 'tv.regular_tv_appearance.to', 'type.object.type', 'tv.regular_tv_appearance.from', 'tv.regular_tv_appearance.actor', 'tv.regular_tv_appearance.character']
Relation_list['m.0220tdl'] = ['tv.regular_tv_appearance.seasons', 'tv.regular_tv_appearance.series', 'tv.regular_tv_appearance.to', 'type.object.type', 'tv.regular_tv_appearance.from', 'tv.regular_tv_appearance.actor', 'tv.regular_tv_appearance.character']
Relation_list['m.0220tgk'] = ['tv.regular_tv_appearance.seasons', 'tv.regular_tv_appearance.series', 'tv.regular_tv_appearance.to', 'type.object.type', 'tv.regular_tv_appearance.from', 'tv.regular_tv_appearance.actor', 'tv.regular_tv_appearance.character']
Relation_list['m.0k94mzp'] = ['tv.regular_tv_appearance.seasons', 'tv.regular_tv_appearance.series', 'tv.regular_tv_appearance.to', 'type.object.type', 'tv.regular_tv_appearance.from', 'tv.regular_tv_appearance.actor', 'tv.regular_tv_appearance.character']
[ChatGPT]
Statement: To find the which MID is connected to Brian Austin Green, I need to explore the graph using the relation list.
Helper function: exploreKG['m.02t94lh']=['tv.regular_tv_appearance.actor'] ## exploreKG['m.04fgn00']=['tv.regular_tv_appearance.actor'] ## exploreKG['m.0220tdl']=['tv.regular_tv_appearance.actor'] ## exploreKG['m.0220tgk']=['tv.regular_tv_appearance.actor'] ## exploreKG['m.0k94mzp']=['tv.regular_tv_appearance.actor']
[User]
Execution result:
['m.02t94lh', 'tv.regular_tv_appearance.actor', 'Tiffani Thiessen']
['m.04fgn00', 'tv.regular_tv_appearance.actor', 'Carol Potter']
['m.0220tdl', 'tv.regular_tv_appearance.actor', 'Luke Perry']
['m.0220tgk', 'tv.regular_tv_appearance.actor', 'Brian Austin Green']
['m.0k94mzp', 'tv.regular_tv_appearance.actor', 'Vanessa Marcil']
[ChatGPT]
Statement: The MID connected to Brian Austin Green is 'm.0220tgk'. To find the character that Brian Austin Green played, I need to explore the graph using the relation list.
Helper function: exploreKG['m.0220tgk']=['tv.regular_tv_appearance.character']
[User]
Execution result:
['m.0220tgk', 'tv.regular_tv_appearance.character', 'David Silver']
[ChatGPT]
Statement: The character that Brian Austin Green played is 'David Silver'.
Helper function: Verification[['David Silver']]

Example 3)
Claim: where is santa clara university?
Given entity: ('Santa Clara University', 'm.027xx3')

[ChatGPT]
Statement: First, I need to find the information about Santa Clara University.
Helper function: getRelation['Santa Clara University']
[User]
Execution result:
Relation_list['Santa Clara University'] = ['location.location.containedby', 'location.location.geolocation', 'location.location.nearby_airports', 'location.location.time_zones', 'common.topic.description', 'common.identity.daylife_topic', 'common.topic.notable_for', 'location.location.people_born_here']
[ChatGPT]
Statement: To find the location of Santa Clara University, I need to explore the graph using the relation list.
Helper function: exploreKG['Santa Clara University']=['location.location.containedby']
[User]
Execution result:
['Santa Clara University', 'location.location.containedby', 'United States of America'], ['Santa Clara University', 'location.location.containedby', 'California'], ['Santa Clara University', 'location.location.containedby', 'Santa Clara']
[ChatGPT]
Statement: From the evidence, Santa Clara University is located in 'United States of America', 'California', and 'Santa Clara'.
Helper function: Verification[['United States of America', 'California', 'Santa Clara']]


Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>

"""

freebase_main_agent_multistep_3_stop_sig = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use one of the helper functions below to find the evidence for finding labels.

Helper Functions
1.getRelation[entity]: Returns the list of relations linked to the entity. You can choose several relations from the list that seem related to the claim.
2.exploreKG[entity]=[relation_1,relation_2, ... relation_K]: Returns the triple set around the entity. For example, [entity, relation_1, tail entity] etc. You can choose relation from [User]'s execution result.
3.Verification[]: If you can answer the claim with enought evidence, call this function. If [User] requires more information, you need to collect more triples in following steps.

You must follow the exact format of the given helper function. You can use multiple helper functions in one step by using '##' between functions.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for [User] response. If response has made, continue your [Your Task] (Do not make multiple 'Helper function: ' lines).
Importantly, if there is an entity starting with 'm.', it is a MID entity. Additional information must be found from that entity.


Example 1)
Claim: what was the name of frederick dougalss book?
Given entity: ('Frederick Douglass', 'm.02zg0')

[Your Task]
Statement: First, I need to find the information about Frederick Douglass.
Helper function: getRelation['Frederick Douglass']
*** Stop for [User] response ***
[User]
Execution result:
Relation_list['Frederick Douglass'] = ['book.author.openlibrary_id', 'authority.openlibrary.author', 'people.person.quotations', 'book.book_subject.works', 'organization.organization_founder.organizations_founded', 'people.deceased_person.cause_of_death', 'people.person.nationality', 'freebase.valuenotation.is_reviewed', 'book.author.works_written']
[Your Task]
Statement: To find the name of Frederick Douglass's book, I need to explore the graph using the relation list.
Helper function: exploreKG['Frederick Douglass']=['book.author.works_written']
*** Stop for [User] response ***
[User]
Execution result:
['Frederick Douglass', 'book.author.works_written', 'Why Is the Negro Lynched'], ['Frederick Douglass', 'book.author.works_written', 'A Black diplomat in Haiti'], ['Frederick Douglass', 'book.author.works_written', 'Three African-American Classics'], ['Frederick Douglass', 'book.author.works_written', 'The Frederick Douglass Papers, Series 1, Vol. 1: 1841-46'], ['Frederick Douglass', 'book.author.works_written', 'Words of Ages'], ['Frederick Douglass', 'book.author.works_written', 'Standing with the slave'], ['Frederick Douglass', 'book.author.works_written', 'Abolition fanaticism in New York']
[Your Task]
Statement: The books that Frederick Douglass wrote are 'Why Is the Negro Lynched', 'A Black diplomat in Haiti', 'Three African-American Classics', 'The Frederick Douglass Papers, Series 1, Vol. 1: 1841-46', 'Words of Ages', 'Standing with the slave', 'Abolition fanaticism in New York'.
Helper function: Verification[['Why Is the Negro Lynched', 'A Black diplomat in Haiti', 'Three African-American Classics', 'The Frederick Douglass Papers, Series 1, Vol. 1: 1841-46', 'Words of Ages', 'Standing with the slave', 'Abolition fanaticism in New York']]

Example 2)
Claim: what character did brian austin green play on 90210?
Given entity: ('Beverly Hills, 90210', 'm.0n2bh')

[Your Task]
Statement: First, I need to find the information about Beverly Hills, 90210.
Helper function: getRelation['Beverly Hills, 90210']
*** Stop for [User] response ***
[User]
Execution result:
Relation_list['Beverly Hills, 90210'] = ['user.robert.default_domain.rated_tv_program.ew_rating', 'source.videosurf', 'tv.tv_program.thetvdb_id', 'tv.tv_program.spin_offs', 'media_common.netflix_title.netflix_genres', 'tv.tv_program.program_creator', 'common.topic.article', 'tv.tv_program.regular_cast', 'common.topic.description', 'award.award_winning_work.awards_won']
[Your Task]
Statement: To find the character that Brian Austin Green played on Beverly Hills, 90210, I need to explore the graph using the relation list.
Helper function: exploreKG['Beverly Hills, 90210']=['tv.tv_program.regular_cast']
*** Stop for [User] response ***
[User]
Execution result:
['Beverly Hills, 90210', 'tv.tv_program.regular_cast', 'm.02t94lh'], ['Beverly Hills, 90210', 'tv.tv_program.regular_cast', 'm.04fgn00'], ['Beverly Hills, 90210', 'tv.tv_program.regular_cast', 'm.0220tdl'], ['Beverly Hills, 90210', 'tv.tv_program.regular_cast', 'm.0220tgk'], ['Beverly Hills, 90210', 'tv.tv_program.regular_cast', 'm.0k94mzp']
[Your Task]
Statement: There are several MIDs connected to Beverly Hills, 90210. I need to find the MID that is connected to Brian Austin Green.
Helper function: getRelation['m.02t94lh'] ## getRelation['m.04fgn00'] ## getRelation['m.0220tdl'] ## getRelation['m.0220tgk'] ## getRelation['m.0k94mzp']
*** Stop for [User] response ***
[User]
Execution result:
Relation_list['m.02t94lh'] = ['tv.regular_tv_appearance.seasons', 'tv.regular_tv_appearance.series', 'tv.regular_tv_appearance.to', 'type.object.type', 'tv.regular_tv_appearance.from', 'tv.regular_tv_appearance.actor', 'tv.regular_tv_appearance.character']
Relation_list['m.04fgn00'] = ['tv.regular_tv_appearance.seasons', 'tv.regular_tv_appearance.series', 'tv.regular_tv_appearance.to', 'type.object.type', 'tv.regular_tv_appearance.from', 'tv.regular_tv_appearance.actor', 'tv.regular_tv_appearance.character']
Relation_list['m.0220tdl'] = ['tv.regular_tv_appearance.seasons', 'tv.regular_tv_appearance.series', 'tv.regular_tv_appearance.to', 'type.object.type', 'tv.regular_tv_appearance.from', 'tv.regular_tv_appearance.actor', 'tv.regular_tv_appearance.character']
Relation_list['m.0220tgk'] = ['tv.regular_tv_appearance.seasons', 'tv.regular_tv_appearance.series', 'tv.regular_tv_appearance.to', 'type.object.type', 'tv.regular_tv_appearance.from', 'tv.regular_tv_appearance.actor', 'tv.regular_tv_appearance.character']
Relation_list['m.0k94mzp'] = ['tv.regular_tv_appearance.seasons', 'tv.regular_tv_appearance.series', 'tv.regular_tv_appearance.to', 'type.object.type', 'tv.regular_tv_appearance.from', 'tv.regular_tv_appearance.actor', 'tv.regular_tv_appearance.character']
[Your Task]
Statement: To find the which MID is connected to Brian Austin Green, I need to explore the graph using the relation list.
Helper function: exploreKG['m.02t94lh']=['tv.regular_tv_appearance.actor'] ## exploreKG['m.04fgn00']=['tv.regular_tv_appearance.actor'] ## exploreKG['m.0220tdl']=['tv.regular_tv_appearance.actor'] ## exploreKG['m.0220tgk']=['tv.regular_tv_appearance.actor'] ## exploreKG['m.0k94mzp']=['tv.regular_tv_appearance.actor']
*** Stop for [User] response ***
[User]
Execution result:
['m.02t94lh', 'tv.regular_tv_appearance.actor', 'Tiffani Thiessen']
['m.04fgn00', 'tv.regular_tv_appearance.actor', 'Carol Potter']
['m.0220tdl', 'tv.regular_tv_appearance.actor', 'Luke Perry']
['m.0220tgk', 'tv.regular_tv_appearance.actor', 'Brian Austin Green']
['m.0k94mzp', 'tv.regular_tv_appearance.actor', 'Vanessa Marcil']
[Your Task]
Statement: The MID connected to Brian Austin Green is 'm.0220tgk'. To find the character that Brian Austin Green played, I need to explore the graph using the relation list.
Helper function: exploreKG['m.0220tgk']=['tv.regular_tv_appearance.character']
*** Stop for [User] response ***
[User]
Execution result:
['m.0220tgk', 'tv.regular_tv_appearance.character', 'David Silver']
[Your Task]
Statement: The character that Brian Austin Green played is 'David Silver'.
Helper function: Verification[['David Silver']]

Example 3)
Claim: where is santa clara university?
Given entity: ('Santa Clara University', 'm.027xx3')

[Your Task]
Statement: First, I need to find the information about Santa Clara University.
Helper function: getRelation['Santa Clara University']
*** Stop for [User] response ***
[User]
Execution result:
Relation_list['Santa Clara University'] = ['location.location.containedby', 'location.location.geolocation', 'location.location.nearby_airports', 'location.location.time_zones', 'common.topic.description', 'common.identity.daylife_topic', 'common.topic.notable_for', 'location.location.people_born_here']
[Your Task]
Statement: To find the location of Santa Clara University, I need to explore the graph using the relation list.
Helper function: exploreKG['Santa Clara University']=['location.location.containedby']
*** Stop for [User] response ***
[User]
Execution result:
['Santa Clara University', 'location.location.containedby', 'United States of America'], ['Santa Clara University', 'location.location.containedby', 'California'], ['Santa Clara University', 'location.location.containedby', 'Santa Clara']
[Your Task]
Statement: From the evidence, Santa Clara University is located in 'United States of America', 'California', and 'Santa Clara'.
Helper function: Verification[['United States of America', 'California', 'Santa Clara']]


Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>

"""

freebase_main_agent_multistep_4 = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use one of the helper functions below to find the evidence for finding labels.

Helper Functions
1.getRelation[entity]: Returns the list of relations linked to the entity. You can choose several relations from the list that seem related to the claim.
2.exploreKG[entity]=[relation_1,relation_2, ... relation_K]: Returns the triple set around the entity. For example, [entity, relation_1, tail entity] etc. You can choose relation from [User]'s execution result.
3.Verification[]: If you can answer the claim with enought evidence, call this function. If [User] requires more information, you need to collect more triples in following steps.

You must follow the exact format of the given helper function. You can use multiple helper functions in one step by using '##' between functions.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for my response. If response has made, continue your 'Statement and Helper function' task.
Importantly, if there is an entity starting with 'm.', it is a MID entity. Additional information must be found from that entity.


Example 1)
Claim: where did timothy mcveigh go to prison?
Given entity: ('Timothy McVeigh', 'm.07rp8')

[ChatGPT]
Statement: First, I need to find the information about Timothy McVeigh.
Helper function: getRelation['Timothy McVeigh']
[User]
Execution result:
Relation_list['Timothy McVeigh'] = ['source.nytimes', 'people.person.date_of_birth', 'common.topic.notable_types', 'base.disaster2.attacker.attack_s', 'people.person.parents', 'people.deceased_person.place_of_death', 'source.videosurf', 'people.person.gender', 'base.prison.prisoner.imprisoned', 'common.topic.article', 'common.topic.description', 'en', 'authority.nndb', 'kg.object_profile.prominent_type', 'type.object.key', 'type.object.name', 'people.person.religion', 'military.military_person.participated_in_conflicts', 'people.person.profession', 'user.avh.default_domain.ellerdale_topic.ellerdale_id']
[ChatGPT]
Statement: To find the location of Timothy McVeigh's prison, I need to explore the graph using the relation list.
Helper function: exploreKG['Timothy McVeigh']=['base.prison.prisoner.imprisoned']
[User]
Execution result:
['Timothy McVeigh', 'base.prison.prisoner.imprisoned', 'm.04dn9gc']
[ChatGPT]
Statement: The MID connected to Timothy McVeigh's prison is 'm.04dn9gc'. To find the location of the prison, I need to explore the graph using the relation list.
Helper function: getRelation['m.04dn9gc']
[User]
Execution result:
Relation_list['m.04dn9gc'] = ['base.prison.imprisonment.to', 'base.prison.imprisonment.prison', 'type.object.type', 'base.prison.imprisonment.prisoner']
[ChatGPT]
Statement: To find the location of the prison, I need to explore the graph using the relation list.
Helper function: exploreKG['m.04dn9gc']=['base.prison.imprisonment.prison']
[User]
Execution result:
['m.04dn9gc', 'base.prison.imprisonment.prison', 'ADX Florence']
[ChatGPT]
Statement: The prison that Timothy McVeigh was imprisoned in is 'ADX Florence'.
Helper function: Verification[['ADX Florence']]

Example 2)
Claim: what awards has louis sachar won?
Given entity: ('Louis Sachar', 'm.01bq8d')

[ChatGPT]
Statement: First, I need to find the information about Louis Sachar.
Helper function: getRelation['Louis Sachar']
[User]
Execution result:
Relation_list['Louis Sachar'] = ['authority.openlibrary.author', 'award.award_winner.awards_won', 'film.writer.film', 'influence.influence_node.influenced', 'common.topic.webpage', 'people.person.place_of_birth', 'people.person.gender', 'authority.daylife.topic', 'film.film_story_contributor.film_story_credits', 'people.person.parents', 'people.person.nationality', 'people.person.religion', 'people.person.children', 'common.topic.notable_for', 'film.actor.film', 'common.topic.article', 'user.avh.default_domain.ellerdale_topic.ellerdale_id']
[ChatGPT]
Statement: To find the awards that Louis Sachar won, I need to explore the graph using the relation list.
Helper function: exploreKG['Louis Sachar']=['award.award_winner.awards_won']
[User]
Execution result:
['Louis Sachar', 'award.award_winner.awards_won', 'm.09kkr46'], ['Louis Sachar', 'award.award_winner.awards_won', 'm.0432ld1'], ['Louis Sachar', 'award.award_winner.awards_won', 'm.087149h'], ['Louis Sachar', 'award.award_winner.awards_won', 'm.045wy6v']
[ChatGPT]
Statement: To find the awards that Louis Sachar won, I need to explore the graph connected to several MIDs using the relation list.
Helper function: getRelation['m.09kkr46'] ## getRelation['m.0432ld1'] ## getRelation['m.087149h'] ## getRelation['m.045wy6v']
[User]
Execution result:
Relation_list['m.09kkr46'] = ['award.award_honor.year', 'award.award_honor.award', 'type.object.type', 'award.award_honor.award_winner']
Relation_list['m.0432ld1'] = ['award.award_honor.year', 'award.award_honor.award', 'type.object.type', 'award.award_honor.award_winner']
Relation_list['m.087149h'] = ['award.award_honor.year', 'award.award_honor.award', 'type.object.type', 'award.award_honor.award_winner']
Relation_list['m.045wy6v'] = ['award.award_honor.year', 'award.award_honor.award', 'type.object.type', 'award.award_honor.award_winner']
[ChatGPT]
Statement: To find the awards that Louis Sachar won, I need to explore the graph using the relation list.
Helper function: exploreKG['m.09kkr46']=['award.award_honor.award'] ## exploreKG['m.0432ld1']=['award.award_honor.award'] ## exploreKG['m.087149h']=['award.award_honor.award'] ## exploreKG['m.045wy6v']=['award.award_honor.award']
[User]
Execution result:
['m.09kkr46', 'award.award_honor.award', "Anne V. Zarrow Award for Young Readers' Literature"]
['m.0432ld1', 'award.award_honor.award', "John Newbery Medal"]
['m.087149h', 'award.award_honor.award', "Dorothy Canfield Fisher Children's Book Award"]
['m.045wy6v', 'award.award_honor.award', "National Book Award for Young People's Literature"]
[ChatGPT]
Statement: The awards that Louis Sachar won are "Anne V. Zarrow Award for Young Readers' Literature", "John Newbery Medal", "Dorothy Canfield Fisher Children's Book Award", "National Book Award for Young People's Literature".
Helper function: Verification[["Anne V. Zarrow Award for Young Readers' Literature", "John Newbery Medal", "Dorothy Canfield Fisher Children's Book Award", "National Book Award for Young People's Literature"]]

Example 3)
Claim: what is the best currency to take to egypt 2013?
Given entity: ('Egypt', 'm.02k54')

[ChatGPT]
Statement: First, I need to find the information about Egyzt.
Helper function: getRelation['Egypt']
[User]
Execution result:
Relation_list['Egypt'] = ['base.aareas.schema.administrative_area.administrative_parent', 'location.location.containedby', 'organization.organization_scope.organizations_with_this_scope', 'film.film_location.featured_in_films', 'base.biblioness.bibs_location.loc_type', 'location.country.currency_used', 'military.military_combatant.military_conflicts', 'common.topic.webpage', 'location.country.national_anthem', 'location.statistical_region.diesel_price_liter', 'base.militaryinfiction.location_in_fiction.contains']
[ChatGPT]
Statement: To find the best currency to take to Egypt in 2013, I need to explore the graph using the relation list.
Helper function: exploreKG['Egypt']=['location.country.currency_used']
[User]
Execution result:
['Egypt', 'location.country.currency_used', 'Egyptian pound']
[ChatGPT]
Statement: The best currency to take to Egypt in 2013 is 'Egyptian pound'.
Helper function: Verification[['Egyptian pound']]


Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>

"""

freebase_main_agent_multistep_4_stop_sig = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use one of the helper functions below to find the evidence for finding labels.

Helper Functions
1.getRelation[entity]: Returns the list of relations linked to the entity. You can choose several relations from the list that seem related to the claim.
2.exploreKG[entity]=[relation_1,relation_2, ... relation_K]: Returns the triple set around the entity. For example, [entity, relation_1, tail entity] etc. You can choose relation from [User]'s execution result.
3.Verification[]: If you can answer the claim with enought evidence, call this function. If [User] requires more information, you need to collect more triples in following steps.

You must follow the exact format of the given helper function. You can use multiple helper functions in one step by using '##' between functions.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for [User] response. If response has made, continue your [Your Task] (Do not make multiple 'Helper function: ' lines).
Importantly, if there is an entity starting with 'm.', it is a MID entity. Additional information must be found from that entity.


Example 1)
Claim: where did timothy mcveigh go to prison?
Given entity: ('Timothy McVeigh', 'm.07rp8')

[Your Task]
Statement: First, I need to find the information about Timothy McVeigh.
Helper function: getRelation['Timothy McVeigh']
*** Stop for [User] response ***
[User]
Execution result:
Relation_list['Timothy McVeigh'] = ['source.nytimes', 'people.person.date_of_birth', 'common.topic.notable_types', 'base.disaster2.attacker.attack_s', 'people.person.parents', 'people.deceased_person.place_of_death', 'source.videosurf', 'people.person.gender', 'base.prison.prisoner.imprisoned', 'common.topic.article', 'common.topic.description', 'en', 'authority.nndb', 'kg.object_profile.prominent_type', 'type.object.key', 'type.object.name', 'people.person.religion', 'military.military_person.participated_in_conflicts', 'people.person.profession', 'user.avh.default_domain.ellerdale_topic.ellerdale_id']
[Your Task]
Statement: To find the location of Timothy McVeigh's prison, I need to explore the graph using the relation list.
Helper function: exploreKG['Timothy McVeigh']=['base.prison.prisoner.imprisoned']
*** Stop for [User] response ***
[User]
Execution result:
['Timothy McVeigh', 'base.prison.prisoner.imprisoned', 'm.04dn9gc']
[Your Task]
Statement: The MID connected to Timothy McVeigh's prison is 'm.04dn9gc'. To find the location of the prison, I need to explore the graph using the relation list.
Helper function: getRelation['m.04dn9gc']
*** Stop for [User] response ***
[User]
Execution result:
Relation_list['m.04dn9gc'] = ['base.prison.imprisonment.to', 'base.prison.imprisonment.prison', 'type.object.type', 'base.prison.imprisonment.prisoner']
[Your Task]
Statement: To find the location of the prison, I need to explore the graph using the relation list.
Helper function: exploreKG['m.04dn9gc']=['base.prison.imprisonment.prison']
*** Stop for [User] response ***
[User]
Execution result:
['m.04dn9gc', 'base.prison.imprisonment.prison', 'ADX Florence']
[Your Task]
Statement: The prison that Timothy McVeigh was imprisoned in is 'ADX Florence'.
Helper function: Verification[['ADX Florence']]

Example 2)
Claim: what awards has louis sachar won?
Given entity: ('Louis Sachar', 'm.01bq8d')

[Your Task]
Statement: First, I need to find the information about Louis Sachar.
Helper function: getRelation['Louis Sachar']
*** Stop for [User] response ***
[User]
Execution result:
Relation_list['Louis Sachar'] = ['authority.openlibrary.author', 'award.award_winner.awards_won', 'film.writer.film', 'influence.influence_node.influenced', 'common.topic.webpage', 'people.person.place_of_birth', 'people.person.gender', 'authority.daylife.topic', 'film.film_story_contributor.film_story_credits', 'people.person.parents', 'people.person.nationality', 'people.person.religion', 'people.person.children', 'common.topic.notable_for', 'film.actor.film', 'common.topic.article', 'user.avh.default_domain.ellerdale_topic.ellerdale_id']
[Your Task]
Statement: To find the awards that Louis Sachar won, I need to explore the graph using the relation list.
Helper function: exploreKG['Louis Sachar']=['award.award_winner.awards_won']
*** Stop for [User] response ***
[User]
Execution result:
['Louis Sachar', 'award.award_winner.awards_won', 'm.09kkr46'], ['Louis Sachar', 'award.award_winner.awards_won', 'm.0432ld1'], ['Louis Sachar', 'award.award_winner.awards_won', 'm.087149h'], ['Louis Sachar', 'award.award_winner.awards_won', 'm.045wy6v']
[Your Task]
Statement: To find the awards that Louis Sachar won, I need to explore the graph connected to several MIDs using the relation list.
Helper function: getRelation['m.09kkr46'] ## getRelation['m.0432ld1'] ## getRelation['m.087149h'] ## getRelation['m.045wy6v']
*** Stop for [User] response ***
[User]
Execution result:
Relation_list['m.09kkr46'] = ['award.award_honor.year', 'award.award_honor.award', 'type.object.type', 'award.award_honor.award_winner']
Relation_list['m.0432ld1'] = ['award.award_honor.year', 'award.award_honor.award', 'type.object.type', 'award.award_honor.award_winner']
Relation_list['m.087149h'] = ['award.award_honor.year', 'award.award_honor.award', 'type.object.type', 'award.award_honor.award_winner']
Relation_list['m.045wy6v'] = ['award.award_honor.year', 'award.award_honor.award', 'type.object.type', 'award.award_honor.award_winner']
[Your Task]
Statement: To find the awards that Louis Sachar won, I need to explore the graph using the relation list.
Helper function: exploreKG['m.09kkr46']=['award.award_honor.award'] ## exploreKG['m.0432ld1']=['award.award_honor.award'] ## exploreKG['m.087149h']=['award.award_honor.award'] ## exploreKG['m.045wy6v']=['award.award_honor.award']
*** Stop for [User] response ***
[User]
Execution result:
['m.09kkr46', 'award.award_honor.award', "Anne V. Zarrow Award for Young Readers' Literature"]
['m.0432ld1', 'award.award_honor.award', "John Newbery Medal"]
['m.087149h', 'award.award_honor.award', "Dorothy Canfield Fisher Children's Book Award"]
['m.045wy6v', 'award.award_honor.award', "National Book Award for Young People's Literature"]
[Your Task]
Statement: The awards that Louis Sachar won are "Anne V. Zarrow Award for Young Readers' Literature", "John Newbery Medal", "Dorothy Canfield Fisher Children's Book Award", "National Book Award for Young People's Literature".
Helper function: Verification[["Anne V. Zarrow Award for Young Readers' Literature", "John Newbery Medal", "Dorothy Canfield Fisher Children's Book Award", "National Book Award for Young People's Literature"]]

Example 3)
Claim: what is the best currency to take to egypt 2013?
Given entity: ('Egypt', 'm.02k54')

[Your Task]
Statement: First, I need to find the information about Egyzt.
Helper function: getRelation['Egypt']
*** Stop for [User] response ***
[User]
Execution result:
Relation_list['Egypt'] = ['base.aareas.schema.administrative_area.administrative_parent', 'location.location.containedby', 'organization.organization_scope.organizations_with_this_scope', 'film.film_location.featured_in_films', 'base.biblioness.bibs_location.loc_type', 'location.country.currency_used', 'military.military_combatant.military_conflicts', 'common.topic.webpage', 'location.country.national_anthem', 'location.statistical_region.diesel_price_liter', 'base.militaryinfiction.location_in_fiction.contains']
[Your Task]
Statement: To find the best currency to take to Egypt in 2013, I need to explore the graph using the relation list.
Helper function: exploreKG['Egypt']=['location.country.currency_used']
*** Stop for [User] response ***
[User]
Execution result:
['Egypt', 'location.country.currency_used', 'Egyptian pound']
[Your Task]
Statement: The best currency to take to Egypt in 2013 is 'Egyptian pound'.
Helper function: Verification[['Egyptian pound']]


Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>

"""


freebase_main_agent_multistep_5 = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use one of the helper functions below to find the evidence for finding labels.

Helper Functions
1.getRelation[entity]: Returns the list of relations linked to the entity. You can choose several relations from the list that seem related to the claim.
2.exploreKG[entity]=[relation_1,relation_2, ... relation_K]: Returns the triple set around the entity. For example, [entity, relation_1, tail entity] etc. You can choose relation from [User]'s execution result.
3.Verification[]: If you can answer the claim with enought evidence, call this function. If [User] requires more information, you need to collect more triples in following steps.

You must follow the exact format of the given helper function. You can use multiple helper functions in one step by using '##' between functions.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for my response. If response has made, continue your 'Statement and Helper function' task.
Importantly, if there is an entity starting with 'm.', it is a MID entity. Additional information must be found from that entity.


Example 1)
Claim: what religion are people in russia?
Given entity: ('Russia', 'm.06bnz')

[ChatGPT]
Statement: First, I need to find the information about Russia.
Helper function: getRelation['Russia']
[User]
Execution result:
Relation_list['Russia'] = ['location.location.containedby', 'location.location.geolocation', 'location.location.nearby_airports', 'location.location.time_zones', 'common.topic.description', 'location.statistical_region.religions', 'common.identity.daylife_topic', 'common.topic.notable_for', 'location.location.people_born_here']
[ChatGPT]
Statement: To find the religion of people in Russia, I need to explore the graph using the relation list.
Helper function: exploreKG['Russia']=['location.statistical_region.religions']
[User]
Execution result:
['Russia', 'location.location.containedby', 'm.06jmmyb'], ['Russia', 'location.location.containedby', 'm.06jmmyk']
[ChatGPT]
Statement: The MIDs connected to Russia are 'm.06jmmyb' and 'm.06jmmyk'. To find the religion of people in Russia, I need to explore the graph using the relation list.
Helper function: getRelation['m.06jmmyb'] ## getRelation['m.06jmmyk']
[User]
Execution result:
Relation_list['m.06jmmyb'] = ['type.object.type', 'location.religion_percentage.percentage', 'location.religion_percentage.date', 'location.religion_percentage.religion']
Relation_list['m.06jmmyk'] = ['type.object.type', 'location.religion_percentage.percentage', 'location.religion_percentage.date', 'location.religion_percentage.religion']
[ChatGPT]
Statement: To find the religion of people in Russia, I need to explore the graph using the relation list.
Helper function: exploreKG['m.06jmmyb']=['location.religion_percentage.religion'] ## exploreKG['m.06jmmyk']=['location.religion_percentage.religion']
[User]
Execution result:
['m.06jmmyb', 'location.religion_percentage.religion', 'Russian Orthodox Church']
['m.06jmmyk', 'location.religion_percentage.religion', 'Islam']
[ChatGPT]
Statement: The religions of people in Russia are 'Russian Orthodox Church' and 'Islam'.
Helper function: Verification[['Russian Orthodox Church', 'Islam']]

Example 2)
Claim: who plays meg in family guy?
Given entity: ('Meg Griffin', 'm.035szd')

[ChatGPT]
Statement: First, I need to find the information about Meg Griffin.
Helper function: getRelation['Meg Griffin']
[User]
Execution result:
Relation_list['Meg Griffin'] = ['user.alust.default_domain.processed_with_review_queue.question_id', 'common.topic.notable_types', 'user.avh.ellerdale', 'fictional_universe.fictional_character.ethnicity', 'fictional_universe.fictional_character.occupation', 'fictional_universe.fictional_character.parents', 'tv.tv_character.appeared_in_tv_program', 'fictional_universe.fictional_character.character_created_by']
[ChatGPT]
Statement: To find the actor who plays Meg Griffin, I need to explore the graph using the relation list.
Helper function: exploreKG['Meg Griffin']=['tv.tv_character.appeared_in_tv_program']
[User]
Execution result:
['Meg Griffin', 'tv.tv_character.appeared_in_tv_program', 'm.0k6pxpv'], ['Meg Griffin', 'tv.tv_character.appeared_in_tv_program', 'm.0w0v0l2'], ['Meg Griffin', 'tv.tv_character.appeared_in_tv_program', 'm.04d4q86'], ['Meg Griffin', 'tv.tv_character.appeared_in_tv_program', 'm.02ntq_4']
[ChatGPT]
Statement: There are several MIDs connected to Meg Griffin. I need to find the MID that is connected to the family guy.
Helper function: getRelation['m.0k6pxpv'] ## getRelation['m.0w0v0l2'] ## getRelation['m.04d4q86'] ## getRelation['m.02ntq_4']
[User]
Execution result:
Relation_list['m.0k6pxpv'] = ['tv.regular_tv_appearance.from', 'tv.regular_tv_appearance.actor', 'tv.regular_tv_appearance.to', 'tv.regular_tv_appearance.series', 'tv.regular_tv_appearance.character', 'type.object.type', 'tv.regular_tv_appearance.special_performance_type']
Relation_list['m.0w0v0l2'] = ['tv.regular_tv_appearance.from', 'tv.regular_tv_appearance.actor', 'tv.regular_tv_appearance.to', 'tv.regular_tv_appearance.series', 'tv.regular_tv_appearance.character', 'type.object.type', 'tv.regular_tv_appearance.special_performance_type']
Relation_list['m.04d4q86'] = ['tv.regular_tv_appearance.from', 'tv.regular_tv_appearance.actor', 'tv.regular_tv_appearance.to', 'tv.regular_tv_appearance.series', 'tv.regular_tv_appearance.character', 'type.object.type', 'tv.regular_tv_appearance.special_performance_type']
Relation_list['m.02ntq_4'] = ['tv.regular_tv_appearance.from', 'tv.regular_tv_appearance.actor', 'tv.regular_tv_appearance.to', 'tv.regular_tv_appearance.series', 'tv.regular_tv_appearance.character', 'type.object.type', 'tv.regular_tv_appearance.special_performance_type']
[ChatGPT]
Statement: To find the MID connected to the family guy, I need to explore the graph using the relation list.
Helper function: exploreKG['m.0k6pxpv']=['tv.regular_tv_appearance.series'] ## exploreKG['m.0w0v0l2']=['tv.regular_tv_appearance.series'] ## exploreKG['m.04d4q86']=['tv.regular_tv_appearance.series'] ## exploreKG['m.02ntq_4']=['tv.regular_tv_appearance.series']
[User]
Execution result:
['m.0k6pxpv', 'tv.regular_tv_appearance.series', 'Family Guy']
['m.0w0v0l2', 'tv.regular_tv_appearance.series', 'The Cleveland Show']
['m.02ntq_4', 'tv.regular_tv_appearance.series', 'Family Guy']
[ChatGPT]
Statement: The MID connected to the family guy is 'm.0k6pxpv' and 'm.02ntq_4'. To find the actor who plays Meg Griffin, I need to explore the graph using the relation list.
Helper function: exploreKG['m.0k6pxpv']=['tv.regular_tv_appearance.actor'] ## exploreKG['m.02ntq_4']=['tv.regular_tv_appearance.actor']
[User]
Execution result:
['m.0k6pxpv', 'tv.regular_tv_appearance.actor', 'Lacey Chabert']
['m.02ntq_4', 'tv.regular_tv_appearance.actor', 'Mila Kunis']
[ChatGPT]
Statement: The actors who play Meg Griffin are 'Lacey Chabert' and 'Mila Kunis'.
Helper function: Verification[['Lacey Chabert', 'Mila Kunis']]

Example 3)
Claim: where did martin luther king got shot?
Given entity: ('Martin Luther King Jr.', 'm.051cc')

[ChatGPT]
Statement: First, I need to find the information about Martin Luther King Jr.
Helper function: getRelation['Martin Luther King Jr.']
[User]
Execution result:
Relation_list['Martin Luther King Jr.'] = ['common.identity.daylife_topic', 'authority.netflix.api', 'source.videosurf', 'film.person_or_entity_appearing_in_film.films', 'kg.object_profile.prominent_type', 'music.featured_artist.recordings', 'people.person.education', 'people.deceased_person.place_of_death', 'nytimes.topic.uri']
[ChatGPT]
Statement: To find the location of Martin Luther King Jr.'s death, I need to explore the graph using the relation list.
Helper function: exploreKG['Martin Luther King Jr.']=['people.deceased_person.place_of_death']
[User]
Execution result:
['Martin Luther King Jr.', 'people.deceased_person.place_of_death', 'Memphis']
[ChatGPT]
Statement: The location where Martin Luther King Jr. was shot is 'Memphis'.
Helper function: Verification[['Memphis']]


Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>

"""

freebase_main_agent_multistep_5_stop_sig = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use one of the helper functions below to find the evidence for finding labels.

Helper Functions
1.getRelation[entity]: Returns the list of relations linked to the entity. You can choose several relations from the list that seem related to the claim.
2.exploreKG[entity]=[relation_1,relation_2, ... relation_K]: Returns the triple set around the entity. For example, [entity, relation_1, tail entity] etc. You can choose relation from [User]'s execution result.
3.Verification[]: If you can answer the claim with enought evidence, call this function. If [User] requires more information, you need to collect more triples in following steps.

You must follow the exact format of the given helper function. You can use multiple helper functions in one step by using '##' between functions.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for [User] response. If response has made, continue your [Your Task] (Do not make multiple 'Helper function: ' lines).
Importantly, if there is an entity starting with 'm.', it is a MID entity. Additional information must be found from that entity.


Example 1)
Claim: what religion are people in russia?
Given entity: ('Russia', 'm.06bnz')

[Your Task]
Statement: First, I need to find the information about Russia.
Helper function: getRelation['Russia']
*** Stop for [User] response ***
[User]
Execution result:
Relation_list['Russia'] = ['location.location.containedby', 'location.location.geolocation', 'location.location.nearby_airports', 'location.location.time_zones', 'common.topic.description', 'location.statistical_region.religions', 'common.identity.daylife_topic', 'common.topic.notable_for', 'location.location.people_born_here']
[Your Task]
Statement: To find the religion of people in Russia, I need to explore the graph using the relation list.
Helper function: exploreKG['Russia']=['location.statistical_region.religions']
*** Stop for [User] response ***
[User]
Execution result:
['Russia', 'location.location.containedby', 'm.06jmmyb'], ['Russia', 'location.location.containedby', 'm.06jmmyk']
[Your Task]
Statement: The MIDs connected to Russia are 'm.06jmmyb' and 'm.06jmmyk'. To find the religion of people in Russia, I need to explore the graph using the relation list.
Helper function: getRelation['m.06jmmyb'] ## getRelation['m.06jmmyk']
*** Stop for [User] response ***
[User]
Execution result:
Relation_list['m.06jmmyb'] = ['type.object.type', 'location.religion_percentage.percentage', 'location.religion_percentage.date', 'location.religion_percentage.religion']
Relation_list['m.06jmmyk'] = ['type.object.type', 'location.religion_percentage.percentage', 'location.religion_percentage.date', 'location.religion_percentage.religion']
[Your Task]
Statement: To find the religion of people in Russia, I need to explore the graph using the relation list.
Helper function: exploreKG['m.06jmmyb']=['location.religion_percentage.religion'] ## exploreKG['m.06jmmyk']=['location.religion_percentage.religion']
*** Stop for [User] response ***
[User]
Execution result:
['m.06jmmyb', 'location.religion_percentage.religion', 'Russian Orthodox Church']
['m.06jmmyk', 'location.religion_percentage.religion', 'Islam']
[Your Task]
Statement: The religions of people in Russia are 'Russian Orthodox Church' and 'Islam'.
Helper function: Verification[['Russian Orthodox Church', 'Islam']]

Example 2)
Claim: who plays meg in family guy?
Given entity: ('Meg Griffin', 'm.035szd')

[Your Task]
Statement: First, I need to find the information about Meg Griffin.
Helper function: getRelation['Meg Griffin']
*** Stop for [User] response ***
[User]
Execution result:
Relation_list['Meg Griffin'] = ['user.alust.default_domain.processed_with_review_queue.question_id', 'common.topic.notable_types', 'user.avh.ellerdale', 'fictional_universe.fictional_character.ethnicity', 'fictional_universe.fictional_character.occupation', 'fictional_universe.fictional_character.parents', 'tv.tv_character.appeared_in_tv_program', 'fictional_universe.fictional_character.character_created_by']
[Your Task]
Statement: To find the actor who plays Meg Griffin, I need to explore the graph using the relation list.
Helper function: exploreKG['Meg Griffin']=['tv.tv_character.appeared_in_tv_program']
*** Stop for [User] response ***
[User]
Execution result:
['Meg Griffin', 'tv.tv_character.appeared_in_tv_program', 'm.0k6pxpv'], ['Meg Griffin', 'tv.tv_character.appeared_in_tv_program', 'm.0w0v0l2'], ['Meg Griffin', 'tv.tv_character.appeared_in_tv_program', 'm.04d4q86'], ['Meg Griffin', 'tv.tv_character.appeared_in_tv_program', 'm.02ntq_4']
[Your Task]
Statement: There are several MIDs connected to Meg Griffin. I need to find the MID that is connected to the family guy.
Helper function: getRelation['m.0k6pxpv'] ## getRelation['m.0w0v0l2'] ## getRelation['m.04d4q86'] ## getRelation['m.02ntq_4']
*** Stop for [User] response ***
[User]
Execution result:
Relation_list['m.0k6pxpv'] = ['tv.regular_tv_appearance.from', 'tv.regular_tv_appearance.actor', 'tv.regular_tv_appearance.to', 'tv.regular_tv_appearance.series', 'tv.regular_tv_appearance.character', 'type.object.type', 'tv.regular_tv_appearance.special_performance_type']
Relation_list['m.0w0v0l2'] = ['tv.regular_tv_appearance.from', 'tv.regular_tv_appearance.actor', 'tv.regular_tv_appearance.to', 'tv.regular_tv_appearance.series', 'tv.regular_tv_appearance.character', 'type.object.type', 'tv.regular_tv_appearance.special_performance_type']
Relation_list['m.04d4q86'] = ['tv.regular_tv_appearance.from', 'tv.regular_tv_appearance.actor', 'tv.regular_tv_appearance.to', 'tv.regular_tv_appearance.series', 'tv.regular_tv_appearance.character', 'type.object.type', 'tv.regular_tv_appearance.special_performance_type']
Relation_list['m.02ntq_4'] = ['tv.regular_tv_appearance.from', 'tv.regular_tv_appearance.actor', 'tv.regular_tv_appearance.to', 'tv.regular_tv_appearance.series', 'tv.regular_tv_appearance.character', 'type.object.type', 'tv.regular_tv_appearance.special_performance_type']
[Your Task]
Statement: To find the MID connected to the family guy, I need to explore the graph using the relation list.
Helper function: exploreKG['m.0k6pxpv']=['tv.regular_tv_appearance.series'] ## exploreKG['m.0w0v0l2']=['tv.regular_tv_appearance.series'] ## exploreKG['m.04d4q86']=['tv.regular_tv_appearance.series'] ## exploreKG['m.02ntq_4']=['tv.regular_tv_appearance.series']
*** Stop for [User] response ***
[User]
Execution result:
['m.0k6pxpv', 'tv.regular_tv_appearance.series', 'Family Guy']
['m.0w0v0l2', 'tv.regular_tv_appearance.series', 'The Cleveland Show']
['m.02ntq_4', 'tv.regular_tv_appearance.series', 'Family Guy']
[Your Task]
Statement: The MID connected to the family guy is 'm.0k6pxpv' and 'm.02ntq_4'. To find the actor who plays Meg Griffin, I need to explore the graph using the relation list.
Helper function: exploreKG['m.0k6pxpv']=['tv.regular_tv_appearance.actor'] ## exploreKG['m.02ntq_4']=['tv.regular_tv_appearance.actor']
*** Stop for [User] response ***
[User]
Execution result:
['m.0k6pxpv', 'tv.regular_tv_appearance.actor', 'Lacey Chabert']
['m.02ntq_4', 'tv.regular_tv_appearance.actor', 'Mila Kunis']
[Your Task]
Statement: The actors who play Meg Griffin are 'Lacey Chabert' and 'Mila Kunis'.
Helper function: Verification[['Lacey Chabert', 'Mila Kunis']]

Example 3)
Claim: where did martin luther king got shot?
Given entity: ('Martin Luther King Jr.', 'm.051cc')

[Your Task]
Statement: First, I need to find the information about Martin Luther King Jr.
Helper function: getRelation['Martin Luther King Jr.']
*** Stop for [User] response ***
[User]
Execution result:
Relation_list['Martin Luther King Jr.'] = ['common.identity.daylife_topic', 'authority.netflix.api', 'source.videosurf', 'film.person_or_entity_appearing_in_film.films', 'kg.object_profile.prominent_type', 'music.featured_artist.recordings', 'people.person.education', 'people.deceased_person.place_of_death', 'nytimes.topic.uri']
[Your Task]
Statement: To find the location of Martin Luther King Jr.'s death, I need to explore the graph using the relation list.
Helper function: exploreKG['Martin Luther King Jr.']=['people.deceased_person.place_of_death']
*** Stop for [User] response ***
[User]
Execution result:
['Martin Luther King Jr.', 'people.deceased_person.place_of_death', 'Memphis']
[Your Task]
Statement: The location where Martin Luther King Jr. was shot is 'Memphis'.
Helper function: Verification[['Memphis']]


Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>

"""

paraphrase_prompt_5phrase = """
You are the paraphrase assistant. Paraphrase the following claim while preserving the core semantic meaning.
Provide five paraphrases in different forms.


<Example 1>
Claim: what is the name of justin bieber brother?
[Response]
1. What is the name for Justin Bieber's brother?
2. Who is the brother of Justin Bieber?
3. Justin Bieber has a brother, what is his name?
4. What is the name of the sibling of Justin Bieber?
5. How is Justin Bieber's brother called?

<Example 2>
Claim: what country is the grand bahama island in?
[Response]
1. In which country is the Grand Bahama Island located?
2. What country does the Grand Bahama Island belong to?
3. The Grand Bahama Island is in which country?
4. What is the country of the Grand Bahama Island?
5. Where is the Grand Bahama Island located?

<Example 3>
Claim: what character did john noble play in lord of the rings?
[Response]
1. Which character was portrayed by John Noble in the Lord of the Rings?
2. In the Lord of the Rings, what character did John Noble act as?
3. John Noble played which character in the Lord of the Rings?
4. What role did John Noble take in the Lord of the Rings?
5. Which character did John Noble perform in the Lord of the Rings?

<Example 4>
Claim: what was the name of frederick dougalss book?
[Response]
1. What was the title of Frederick Douglass's book?
2. What book did Frederick Douglass write?
3. Frederick Douglass authored which book?
4. What is the name of the book by Frederick Douglass?
5. Which book was written by Frederick Douglass?

<Example 5>
Claim: what is the best currency to take to egypt 2013?
[Response]
1. What currency is recommended to take to Egypt in 2013?
2. Which currency is the best to take to Egypt in 2013?
3. What is the optimal currency to take to Egypt in 2013?
4. Which currency should be taken to Egypt in 2013?
5. What currency is the most suitable to take to Egypt in 2013?

<Example 6>
Claim: where did martin luther king got shot?
[Response]
1. Where was Martin Luther King Jr. shot?
2. In which location was Martin Luther King Jr. shot?
3. Where did Martin Luther King Jr. get shot?
4. The place where Martin Luther King Jr. was shot?
5. What is the location where Martin Luther King Jr. was shot?


Now, it's your turn. Paraphrase the following claim. Response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
"""