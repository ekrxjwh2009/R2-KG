pr_1 = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use one of the helper functions below to find the evidence for finding labels.

Helper Functions
1.getRelation[entity]: Returns the list of relations linked to the entity. You can choose several relations from the list that seem related to the claim.
2.exploreKG[entity]=[relation_1,relation_2, ... relation_K]: Returns the triple set around the entity. For example, [entity, relation_1, tail entity] etc. You can choose relation from [User]'s execution result.
3.Verification[list of entities]: If you can find the answer entities from collected evidences, give the answer.

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
Helper function: Verification['Padmé Amidala']


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
Helper function: Verification['Unbroken', 'A Place in Time', 'By the Sea', 'In the Land of Blood and Honey']


Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>

"""

pr_1_stop_sig = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use one of the helper functions below to find the evidence for finding labels.

Helper Functions
1.getRelation[entity]: Returns the list of relations linked to the entity. You can choose several relations from the list that seem related to the claim.
2.exploreKG[entity]=[relation_1,relation_2, ... relation_K]: Returns the triple set around the entity. For example, [entity, relation_1, tail entity] etc. You can choose relation from [User]'s execution result.
3.Verification[list of entities]: If you can find the answer entities from collected evidences, give the answer.

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
Helper function: Verification['Jaxon Bieber']


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
Helper function: Verification['Padmé Amidala']


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
Helper function: Verification['Unbroken', 'A Place in Time', 'By the Sea', 'In the Land of Blood and Honey']


Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>

"""

pr_2 = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use one of the helper functions below to find the evidence for finding labels.

Helper Functions
1.getRelation[entity]: Returns the list of relations linked to the entity. You can choose several relations from the list that seem related to the claim.
2.exploreKG[entity]=[relation_1,relation_2, ... relation_K]: Returns the triple set around the entity. For example, [entity, relation_1, tail entity] etc. You can choose relation from [User]'s execution result.
3.Verification[list of entities]: If you can find the answer entities from collected evidences, give the answer.

You must follow the exact format of the given helper function. You can use multiple helper functions in one step by using '##' between functions.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for [User] response. If response has made, continue your [Your Task] (Do not make multiple 'Helper function: ' lines).
Importantly, if there is an entity starting with 'm.', it is a MID entity. Additional information must be found from that entity.
Also, when you verify the answer, you must not modify the exact name of the answer entity from the evidences (Do not change the name or form of the entity).


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
Helper function: Verification['Denethor II']

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
Helper function: Verification['Italy', 'Lazio', 'Province of Rome']

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
Helper function: Verification['Chaz Bono', 'Elijah Blue Allman']


Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>

"""

pr_2_stop_sig = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use one of the helper functions below to find the evidence for finding labels.

Helper Functions
1.getRelation[entity]: Returns the list of relations linked to the entity. You can choose several relations from the list that seem related to the claim.
2.exploreKG[entity]=[relation_1,relation_2, ... relation_K]: Returns the triple set around the entity. For example, [entity, relation_1, tail entity] etc. You can choose relation from [User]'s execution result.
3.Verification[list of entities]: If you can find the answer entities from collected evidences, give the answer.

You must follow the exact format of the given helper function. You can use multiple helper functions in one step by using '##' between functions.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for [User] response. If response has made, continue your [Your Task] (Do not make multiple 'Helper function: ' lines).
Importantly, if there is an entity starting with 'm.', it is a MID entity. Additional information must be found from that entity.
Also, when you verify the answer, you must not modify the exact name of the answer entity from the evidences (Do not change the name or form of the entity).


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
Helper function: Verification['Denethor II']

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
Helper function: Verification['Italy', 'Lazio', 'Province of Rome']

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
Helper function: Verification['Chaz Bono', 'Elijah Blue Allman']


Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>

"""

pr_3 = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use one of the helper functions below to find the evidence for finding labels.

Helper Functions
1.getRelation[entity]: Returns the list of relations linked to the entity. You can choose several relations from the list that seem related to the claim.
2.exploreKG[entity]=[relation_1,relation_2, ... relation_K]: Returns the triple set around the entity. For example, [entity, relation_1, tail entity] etc. You can choose relation from [User]'s execution result.
3.Verification[list of entities]: If you can find the answer entities from collected evidences, give the answer.

You must follow the exact format of the given helper function. You can use multiple helper functions in one step by using '##' between functions.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for [User] response. If response has made, continue your [Your Task] (Do not make multiple 'Helper function: ' lines).
Importantly, if there is an entity starting with 'm.', it is a MID entity. Additional information must be found from that entity.
Also, when you verify the answer, you must not modify the exact name of the answer entity from the evidences (Do not change the name or form of the entity).


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
Helper function: Verification['Why Is the Negro Lynched', 'A Black diplomat in Haiti', 'Three African-American Classics', 'The Frederick Douglass Papers, Series 1, Vol. 1: 1841-46', 'Words of Ages', 'Standing with the slave', 'Abolition fanaticism in New York']

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
Helper function: Verification['David Silver']

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
Helper function: Verification['United States of America', 'California', 'Santa Clara']


Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>

"""

pr_3_stop_sig = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use one of the helper functions below to find the evidence for finding labels.

Helper Functions
1.getRelation[entity]: Returns the list of relations linked to the entity. You can choose several relations from the list that seem related to the claim.
2.exploreKG[entity]=[relation_1,relation_2, ... relation_K]: Returns the triple set around the entity. For example, [entity, relation_1, tail entity] etc. You can choose relation from [User]'s execution result.
3.Verification[list of entities]: If you can find the answer entities from collected evidences, give the answer.

You must follow the exact format of the given helper function. You can use multiple helper functions in one step by using '##' between functions.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for [User] response. If response has made, continue your [Your Task] (Do not make multiple 'Helper function: ' lines).
Importantly, if there is an entity starting with 'm.', it is a MID entity. Additional information must be found from that entity.
Also, when you verify the answer, you must not modify the exact name of the answer entity from the evidences (Do not change the name or form of the entity).


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
Helper function: Verification['Why Is the Negro Lynched', 'A Black diplomat in Haiti', 'Three African-American Classics', 'The Frederick Douglass Papers, Series 1, Vol. 1: 1841-46', 'Words of Ages', 'Standing with the slave', 'Abolition fanaticism in New York']

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
Helper function: Verification['David Silver']

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
Helper function: Verification['United States of America', 'California', 'Santa Clara']


Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>

"""