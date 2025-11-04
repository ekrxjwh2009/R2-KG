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
Claim : What is the mascot of the team that has Nicholas S. Zeppos as its leader?
Triple sets : [['Nicholas S. Zeppos', 'business.board_member.leader_of', 'm.0h6j7c4'], ['m.0h6j7c4', 'organization.leadership.organization', 'Vanderbilt University'], ['Vanderbilt University', 'education.educational_institution.mascot', 'Vanderbilt University Mr. Commodore']]
Relations of Entity :
Relation_list['Nicholas S. Zeppos'] = ['common.topic.alias', 'kg.object_profile.prominent_type', 'common.topic.article', 'source.videosurf', 'type.object.type', 'business.board_member.leader_of', 'common.topic.notable_for', 'people.person.employment_history', 'people.person.gender', 'people.person.place_of_birth', 'people.person.education', 'common.topic.image', 'people.person.date_of_birth', 'common.topic.topic_equivalent_webpage', 'en', 'type.object.name', 'common.topic.notable_types', 'type.object.key', 'common.topic.description']
Relation_list['m.0h6j7c4'] = ['organization.leadership.organization', 'organization.leadership.from', 'freebase.valuenotation.has_no_value', 'organization.leadership.role', 'organization.leadership.title', 'type.object.type', 'organization.leadership.person']
Relation_list['Vanderbilt University'] = ['common.topic.official_website', 'education.university.number_of_postgraduates', 'education.educational_institution.nickname', 'organization.endowed_organization.endowment', 'symbols.namesake.named_after', 'organization.organization.date_founded', 'user.avh.ellerdale', 'common.topic.article', 'organization.organization.headquarters', 'base.usnris.item', 'base.jewlib.parent_institution.judaica_owning_units', 'base.usnris.nris_listing.item_number', 'user.avh.default_domain.ellerdale_topic.ellerdale_id', 'education.university.fraternities_and_sororities', 'location.location.containedby', 'common.topic.topic_equivalent_webpage', 'education.university.local_tuition', 'type.object.name', 'education.educational_institution.mascot', 'base.schemastaging.organization_extra.contact_webpage', 'organization.non_profit_organization.registered_with', 'education.university.domestic_tuition', 'authority.daylife.topic', 'education.university.acceptance_rate', 'base.jewlib.parent_institution.jewish_studies_research_units', 'base.ranker.rankerurlname', 'authority.us.gov.irs.ein', 'education.educational_institution.athletics_brand']
[ChatGPT]
Statement: The team that Nicholas S. Zeppos is a leader is Vanderbilt University. Claim is asking about the mascot of the team, and by using 'education.educational_institution.mascot' we can get the mascot of Vanderbilt University. The answer of the claim is as follows. ['Vanderbilt University Mr. Commodore']
Evaluation: Executable(['Vanderbilt University Mr. Commodore'])

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
Claim : When did the champion of the 1999 World Series win their first World Series?
Triple sets : [['1999 World Series', 'sports.sports_championship_event.champion', 'New York Yankees'], ['New York Yankees', 'sports.sports_team.championships', '1962 World Series'], ['New York Yankees', 'sports.sports_team.championships', '1943 World Series'], ['New York Yankees', 'sports.sports_team.championships', '1923 World Series'], ['New York Yankees', 'sports.sports_team.championships', '1950 World Series'], ['New York Yankees', 'sports.sports_team.championships', '1937 World Series'], ['New York Yankees', 'sports.sports_team.championships', '2009 World Series']]
Relations of Entity :
Relation_list['1999 World Series'] = ['sports.sports_championship_event.runner_up', 'time.event.start_date', 'kg.object_profile.prominent_type', 'common.topic.article', 'sports.sports_championship_event.season', 'type.object.type', 'common.topic.notable_for', 'sports.sports_championship_event.championship', 'time.event.end_date', 'sports.sports_championship_event.result', 'common.topic.topic_equivalent_webpage', 'type.object.name', 'common.topic.notable_types', 'time.event.locations', 'type.object.key', 'sports.sports_championship_event.champion', 'common.topic.description', 'time.event.instance_of_recurring_event']
Relation_list['New York Yankees'] = ['baseball.baseball_team.league', 'authority.netflix.role', 'base.schemastaging.organization_extra.contact_webpage', 'sports.professional_sports_team.draft_picks', 'authority.daylife.topic', 'authority.netflix.api', 'common.topic.topical_webpage', 'sports.sports_team.arena_stadium', 'authority.google.google_plus_page', 'sports.sports_team.championships', 'common.topic.notable_for']
[ChatGPT]
Statement: The champion of the 1999 World Series is New York Yankees. The first World Series championship for New York Yankees is the 1923 World Series. Therefore, the answer of the claim is as follows. ['1923 World Series']
Evaluation: Executable(['1923 World Series'])

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