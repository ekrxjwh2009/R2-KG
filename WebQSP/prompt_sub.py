sub_prompt = """
You are the evaluator. I will show you a claim and a triple set extracted from a graph. 
Based on the given triple set and relation list of each entity, find the proper labels for given question.
If given triple sets are lack of information to verify the claim, give the the combination of entity and relation you need. You can refer the given relations list and choosed what relation information is more needed.
The triple set takes the form [Head, Relation, Tail], which means 'Head's Relation is Tail.' 
If the relation starts with '~', it indicates a reverse relation, meaning 'Tail's relation is head.' 
The following cases may arise: Choose one option from 'Executable ([list of labels])' or 'Not executable(Insufficient evidence)'.
If you choose 'Not executable(Insufficient evidence)', You must specify in the statement which additional relation information is needed for a particular entity. However, the relation can only be selected from the given Relation_list and cannot be created arbitrarily.
Refer to the explanations of the two options below to answer the Statement and Evaluation.

Important: If you think you need additional information using certain relation, you have to check the relation is actually linked with the entity. If not, you have to give the label entities only linked with the relation using Executable([list of labels])
(e.g. If there are 5 films to find 'release_year' but only 3 of them have 'release_year' relation, you have to give the label of the 3 films using Executable([list of labels]) regardless of the remaining 2 films.)

<Cases> 
1. If answer labels can be extracted from the triple sets --> Executable ([list of labels])
2. If the triple sets are insufficient or ambiguous to determine the answer labels of the claim --> Not executable (Insufficient evidence) 

Below are examples of your task.

<Example 1>
[User]
Claim : what is the name of justin bieber brother?
Triple sets : [['Justin Bieber', 'people.person.sibling_s', 'm.0gxnnwc'], ['Justin Bieber', 'people.person.sibling_s', 'm.0gxnnwp'], ['m.0gxnnwc', 'people.sibling_relationship.sibling', 'Jazmyn Bieber'], ['m.0gxnnwp', 'people.sibling_relationship.sibling', 'Jaxon Bieber'], ['Jazmyn Bieber', 'people.person.gender', 'Female'], ['Jaxon Bieber', 'people.person.gender', 'Male']]
Relations of Entity :
Relations_list["Justin Bieber"] = ['music.artist.origin', 'people.person.sibling_s', 'base.popstra.celebrity.hangout', 'type.object.name', 'freebase.valuenotation.has_no_value', 'music.group_member.membership', 'authority.musicbrainz.artist', 'type.object.type', 'people.person.place_of_birth', 'music.lyricist.lyrics_written', 'music.artist.concert_tours', 'music.composer.compositions', 'people.person.height_meters', 'user.avh.default_domain.ellerdale_topic.ellerdale_id', 'music.artist.genre', 'music.artist.album', 'music.artist.track_contributions', 'common.topic.image', 'authority.netflix.role', 'type.object.key', 'authority.musicbrainz', 'freebase.valuenotation.is_reviewed', 'source.videosurf', 'dataworld.freeq', 'celebrities.celebrity.sexual_relationships']
Relations_list["m.0gxnnwc"] = ['type.object.type', 'people.sibling_relationship.sibling']
Relations_list["m.0gxnnwp"] = ['type.object.type', 'people.sibling_relationship.sibling']
Relations_list["Jazmyn Bieber"] = ['kg.object_profile.prominent_type', 'people.person.parents', 'people.person.gender', 'people.person.sibling_s', 'common.topic.notable_for', 'people.person.nationality', 'people.person.place_of_birth', 'common.topic.description', 'type.object.type', 'common.topic.notable_types', 'people.person.date_of_birth', 'type.object.name']
Relations_list["Jaxon Bieber"] = ['kg.object_profile.prominent_type', 'people.person.parents', 'people.person.gender', 'people.person.sibling_s', 'common.topic.notable_for', 'people.person.nationality', 'people.person.place_of_birth', 'common.topic.description', 'type.object.type', 'common.topic.notable_types', 'people.person.date_of_birth', 'type.object.name']
[ChatGPT]
Statement: The siblings of 'Justin Bieber' are 'Jazmyn Bieber' and 'Jaxon Bieber'. Claim is asking about the brother of 'Justin Bieber', and only 'Jaxon Bieber' is male among the siblings. Therefore, the answer of the claim is as follows. ['Jaxon Bieber']
Evaluation: Executable(['Jaxon Bieber'])

<Example 2>
[User]
Claim : what character did natalie portman play in star wars?
Triple sets : [['Natalie Portman', 'film.actor.film', 'm.040myw2'], ['Natalie Portman', 'film.actor.film', 'm.0k80dr'], ['Natalie Portman', 'film.actor.film', 'm.0k3qy8'], ['m.040myw2', 'film.performance.film', 'Brothers'], ['m.0k80dr', 'film.performance.film', 'Where the Heart Is'], ['m.0k3qy8', 'film.performance.film', 'Star Wars Episode I: The Phantom Menace'], ['m.0k3qy8', 'film.performance.character', 'Padmé Amidala']]
Relations of Entity : 
Relations_list["Natalie Portman"] = ['source.filmstarts.personen', 'music.artist.track_contributions', 'type.object.name', 'imdb.topic.name_id', 'film.producer.film', 'source.allocine.fr.personne', 'award.ranked_item.appears_in_ranked_lists', 'people.person.date_of_birth', 'common.topic.article', 'base.ontologies.ontology_instance.equivalent_instances', 'user.avh.ellerdale', 'freebase.valuenotation.has_no_value', 'base.schemastaging.context_name.nickname', 'award.award_winner.awards_won', 'authority.tvrage.person', 'film.person_or_entity_appearing_in_film.films', 'music.featured_artist.recordings', 'common.topic.topic_equivalent_webpage', 'tv.tv_actor.guest_roles', 'source.sensacine.actores', 'people.person.religion', 'base.popstra.celebrity.canoodled', 'type.object.type', 'source.nytimes', 'common.identity.daylife_topic', 'kg.object_profile.prominent_type', 'people.person.places_lived', 'award.award_nominee.award_nominations', 'common.topic.alias', 'people.person.spouse_s', 'base.celebarchiv.celebrity', 'base.popstra.celebrity.dated', 'common.topic.notable_types', 'authority.musicbrainz.artist', 'common.topic.webpage', 'film.director.film', 'people.measured_person.sizes', 'film.writer.film', 'base.saturdaynightlive.snl_host.episodes_hosted', 'nytimes.topic.uri', 'common.topic.description', 'user.robert.default_domain.daylife.hero_image_id', 'celebrities.celebrity.sexual_relationships', 'people.person.children', 'film.producer.films_executive_produced', 'film.actor.film', 'en', 'common.topic.topical_webpage', 'authority.imdb.name', 'people.person.education', 'type.object.key', 'common.topic.notable_for', 'authority.netflix.api', 'base.eating.practicer_of_diet.diet', 'people.person.parents', 'source.videosurf', 'base.popstra.celebrity.wears', 'user.avh.default_domain.ellerdale_topic.ellerdale_id', 'authority.netflix.role', 'user.narphorium.people.nndb_person.nndb_id', 'tv.tv_program_guest.appeared_on', 'source.entertainmentweekly.person', 'people.person.profession', 'base.chickipedia.topic.chickipedia_id', 'book.author.works_written', 'people.person.nationality', 'authority.discogs.artist', 'common.topic.image', 'base.ranker.rankerurlname', 'base.popstra.celebrity.friendship', 'people.measured_person.measurements', 'people.person.ethnicity', 'people.person.employment_history', 'celebrities.celebrity.sexual_orientation', 'authority.musicbrainz', 'base.popstra.celebrity.breakup', 'base.chickipedia.chickipedia_id', 'common.topic.social_media_presence', 'people.person.height_meters', 'base.schemastaging.context_name.official_name', 'people.person.gender', 'authority.daylife.topic', 'authority.nndb', 'people.person.place_of_birth', 'people.person.weight_kg', 'base.popstra.celebrity.vacations_in', 'freebase.valuenotation.is_reviewed']
Relations_list["m.040myw2"] = ['film.performance.actor', 'type.object.type', 'film.performance.character', 'film.performance.film']
Relations_list["m.0k80dr"] = ['film.performance.actor', 'type.object.type', 'film.performance.character', 'film.performance.film']
Relations_list["m.0k3qy8"] = ['film.performance.actor', 'type.object.type', 'film.performance.character', 'film.performance.film']
Relations_list["m.0k3qy8"] = ['film.performance.actor', 'type.object.type', 'film.performance.character', 'film.performance.film']
[ChatGPT]
Statement: "m.0k3qy8" is related to star wars film (Star Wars Episode I: The Phantom Menace), and by using 'film.performance.character' relation, we can get the character played by 'Natalie Portman' in the film. The answer of the claim is as follows. ['Padmé Amidala']
Evaluation: Executable(['Padmé Amidala'])

<Example 3>
[User]
Claim : what character did natalie portman play in star wars?
Triple sets : [['Natalie Portman', 'film.actor.film', 'm.040myw2'], ['Natalie Portman', 'film.actor.film', 'm.0k80dr'], ['Natalie Portman', 'film.actor.film', 'm.0k3qy8'], ['m.040myw2', 'film.performance.film', 'Brothers'], ['m.0k80dr', 'film.performance.film', 'Where the Heart Is'], ['m.0k3qy8', 'film.performance.film', 'Star Wars Episode I: The Phantom Menace']]
Relations of Entity : 
Relations_list["Natalie Portman"] = ['source.filmstarts.personen', 'music.artist.track_contributions', 'type.object.name', 'imdb.topic.name_id', 'film.producer.film', 'source.allocine.fr.personne', 'award.ranked_item.appears_in_ranked_lists', 'people.person.date_of_birth', 'common.topic.article', 'base.ontologies.ontology_instance.equivalent_instances', 'user.avh.ellerdale', 'freebase.valuenotation.has_no_value', 'base.schemastaging.context_name.nickname', 'award.award_winner.awards_won', 'authority.tvrage.person', 'film.person_or_entity_appearing_in_film.films', 'music.featured_artist.recordings', 'common.topic.topic_equivalent_webpage', 'tv.tv_actor.guest_roles', 'source.sensacine.actores', 'people.person.religion', 'base.popstra.celebrity.canoodled', 'type.object.type', 'source.nytimes', 'common.identity.daylife_topic', 'kg.object_profile.prominent_type', 'people.person.places_lived', 'award.award_nominee.award_nominations', 'common.topic.alias', 'people.person.spouse_s', 'base.celebarchiv.celebrity', 'base.popstra.celebrity.dated', 'common.topic.notable_types', 'authority.musicbrainz.artist', 'common.topic.webpage', 'film.director.film', 'people.measured_person.sizes', 'film.writer.film', 'base.saturdaynightlive.snl_host.episodes_hosted', 'nytimes.topic.uri', 'common.topic.description', 'user.robert.default_domain.daylife.hero_image_id', 'celebrities.celebrity.sexual_relationships', 'people.person.children', 'film.producer.films_executive_produced', 'film.actor.film', 'en', 'common.topic.topical_webpage', 'authority.imdb.name', 'people.person.education', 'type.object.key', 'common.topic.notable_for', 'authority.netflix.api', 'base.eating.practicer_of_diet.diet', 'people.person.parents', 'source.videosurf', 'base.popstra.celebrity.wears', 'user.avh.default_domain.ellerdale_topic.ellerdale_id', 'authority.netflix.role', 'user.narphorium.people.nndb_person.nndb_id', 'tv.tv_program_guest.appeared_on', 'source.entertainmentweekly.person', 'people.person.profession', 'base.chickipedia.topic.chickipedia_id', 'book.author.works_written', 'people.person.nationality', 'authority.discogs.artist', 'common.topic.image', 'base.ranker.rankerurlname', 'base.popstra.celebrity.friendship', 'people.measured_person.measurements', 'people.person.ethnicity', 'people.person.employment_history', 'celebrities.celebrity.sexual_orientation', 'authority.musicbrainz', 'base.popstra.celebrity.breakup', 'base.chickipedia.chickipedia_id', 'common.topic.social_media_presence', 'people.person.height_meters', 'base.schemastaging.context_name.official_name', 'people.person.gender', 'authority.daylife.topic', 'authority.nndb', 'people.person.place_of_birth', 'people.person.weight_kg', 'base.popstra.celebrity.vacations_in', 'freebase.valuenotation.is_reviewed']
Relations_list["m.040myw2"] = ['film.performance.actor', 'type.object.type', 'film.performance.character', 'film.performance.film']
Relations_list["m.0k80dr"] = ['film.performance.actor', 'type.object.type', 'film.performance.character', 'film.performance.film']
Relations_list["m.0k3qy8"] = ['film.performance.actor', 'type.object.type', 'film.performance.character', 'film.performance.film']
[ChatGPT]
Statement: "m.0k3qy8" is related to star wars film (Star Wars Episode I: The Phantom Menace), but we don't have information about the character played by 'Natalie Portman' in the film. Try to look relation 'film.performance.character' of 'm.0k3qy8'.
Evaluation: Not executable (Insufficient evidence)

<Example 4>
[User]
Claim : what country is the grand bahama island in?
Triple sets : ['Grand Bahama', 'location.location.containedby', 'Bahamas'], ['Grand Bahama', 'location.location.area', '1373.0']
Relations of Entity :
Relation_list['Grand Bahama'] = ['location.location.containedby', 'location.location.area']
[ChatGPT]
Statement: The Grand Bahama Island is in the country 'Bahamas'. Therefore, the answer of the claim is as follows. ['Bahamas']
Evaluation: Executable(['Bahamas'])

<Example 5>
[User]
Claim : what airport do you fly into maui?
Triple sets : [['Maui', 'location.location.containedby', 'Hawaii'], ['Maui', 'location.location.containedby', 'Maui County'], ['Maui', 'location.location.containedby', 'Hawaiian Islands'], ['Maui', 'location.location.contains', 'Kealia Pond National Wildlife Refuge'], ['Maui', 'location.location.contains', 'West Maui Mountains'], ['Maui', 'location.location.contains', 'Wailuku'], ['Maui', 'location.location.contains', 'Haleakalā'], ['Maui', 'location.location.contains', 'Puu Kukui'], ['Maui', 'location.location.contains', 'Makahiku Falls'], ['Maui', 'location.location.contains', 'Kahului Airport'], ['Maui', 'location.location.contains', 'Hana Airport'], ['Maui', 'location.location.contains', 'Kanaha Pond State Wildlife Sanctuary'], ['Maui', 'location.location.contains', 'Kapalua Airport']]
Relations of Entity :
Relation_list['Maui'] = ['location.location.containedby', 'location.location.contains']
[ChatGPT]
Statement: The airport in 'Maui' is 'Kahului Airport', 'Hana Airport', and 'Kapalua Airport'. Therefore, the answer of the claim is as follows. ['Kahului Airport', 'Hana Airport', 'Kapalua Airport']
Evaluation: Executable(['Kahului Airport', 'Hana Airport', 'Kapalua Airport'])


Now, it's your turn. Continue your 'Statement and Evaluation' task. Response must have same form with upper examples.
[User]
Claim : <<<<CLAIM>>>>
Triple set : <<<<Triple set>>>>
Relations of Entity : <<<<GOLD RELATIONS>>>>

"""