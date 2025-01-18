import openai
import sys, os
from openai import OpenAI
import json
import csv
import argparse
import re
import ast
import dbpedia_sparql as db
import numpy as np
import time
from prompt import initial_prompt_stop_sig, pr1_stop_sig, pr2, pr3_stop_sig, pr4_stop_sig, pr5_stop_sig, pr1_singlecall
from model import LLMBot
from paraphraser import paraphrase

initial_prompt_ = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use below helper functions to find the evidence for finding labels.

<Helper functions>
1. getRelation(entity): Returns the list of relations connected to the entities.
2. exploreKG(entity) = [list of relations]: Returns the corresponding tail entities in graph data starts from single entity in given entity and given relation.
3. Verification([list of entities]): After getting enough evidence after exploreKG() helper function and if verification can be done, call this function with labels.

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
Helper function: getRelation('Man of Steel')
[User]
Execution result: Relation_list('Man of Steel') = ['release_year', 'starred_actors', 'written_by', 'has_tags', 'directed_by']
[Your Task]
Statement: First, to solve the claim, I have to know the actors starred in 'Man of Steel'.
Helper function: exploreKG('Man of Steel')=['starred_actors']
[User]
Execution result: ['Man of Steel', 'starred_actors', 'michael_shannon'], ['Man of Steel', 'starred_actors', 'henry_cavill'], ['Man of Steel', 'starred_actors', 'amy_adams'], ['Man of Steel', 'starred_actors', 'diane_lane']
[Your Task]
Statement: Next, I need films starred by previous given actors. To find the films, I need relations linked with the actors.
Helper function: getRelation('michael_shannon') ## getRelation('henry_cavill') ## getRelation('amy_adams') ## getRelation('diane_lane')
[User]
Execution result: Relation_list('michael_shannon') = ['has_tags', 'starred_actors'], Relation_list('henry_cavill') = ['starred_actors'], Relation_list('amy_adams') = ['has_tags', 'starred_actors'], getRelations('diane_lane') = ['has_tags', 'starred_actors']
[Your Task]
Statement: To get the films starred by previous actors, I need to explore the graph with each actors and related relations.
Helper function: exploreKG('michael_shannon')=['starred_actors'] ## exploreKG('henry_cavill')=['starred_actors'] ## exploreKG('amy_adams')=['starred_actors'] ## exploreKG('diane_lane')=['starred_actors']
[User]
Execution result: ['michael_shannon', 'starred_actors', 'bug'], ['michael_shannon', 'starred_actors', 'machine_gun_preacher'], ['michael_shannon', 'starred_actors', 'young_ones'], ['michael_shannon', 'starred_actors', 'the_missing_person'], ['henry_cavill', 'starred_actors', 'immortals'], ['henry_cavill', 'starred_actors', 'blood_creek'], ['henry_cavill', 'starred_actors', 'the_cold_light_of_day'], ['amy_adams', 'starred_actors', 'moonlight_serenade'], ['amy_adams', 'starred_actors', 'american_hustle'], ['amy_adams', 'starred_actors', 'sunshine_cleaning'], ['amy_adams', 'starred_actors', 'the_fighter'], ['diane_lane', 'starred_actors', 'wild_bill'], ['diane_lane', 'starred_actors', 'the_glass_house'], ['diane_lane', 'starred_actors', 'jumper']
[Your Task]
Statement: To get the genres of the these films, I need to find the relations linked with all the films from previous step.
Helper function: getRelation('bug') ## getRelation('machine_gun_preacher') ## getRelation('young_ones') ## getRelation('the_missing_person') ## getRelation('immortals') ## getRelation('blood_creek') ## getRelation('the_cold_light_of_day') ## getRelation('moonlight_serenade') ## getRelation('american_hustle') ## getRelation('sunshine_cleaning') ## getRelation('the_fighter') ## getRelation('wild_bill') ## getRelation('the_glass_house') ## getRelation('jumper')
[User]
Execution result: Relation_list('bug') = ['starred_actors', 'has_tags', 'written_by', 'release_year', 'has_genre', 'directed_by'], Relation_list('machine_gun_preacher') = ['starred_actors', 'has_tags', 'written_by', 'release_year', 'has_genre', 'directed_by'], Relation_list('young_ones') = ['starred_actors', 'has_genre', 'release_year'], Relation_list('the_missing_person') = ['starred_actors', 'written_by', 'release_year', 'has_genre'], Relation_list('immortals') = 'starred_actors', 'has_tags', 'release_year', 'has_genre', 'in_language'], Relation_list('blood_creek') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('the_cold_light_of_day') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('moonlight_serenade') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('american_hustle') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('sunshine_cleaning') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('the_fighter') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('wild_bill') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('the_glass_house') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('jumper') = ['starred_actors', 'has_tags', 'release_year', 'directed_by']
[Your Task]
Statement: To get the genres of the films, I need to explore the graph with each films and related relations.
Helper function: exploreKG('bug')=['has_genre'] ## exploreKG('machine_gun_preacher')=['has_genre'] ## exploreKG('young_ones')=['has_genre'] ## exploreKG('the_missing_person')=['has_genre'] ## exploreKG('immortals')=['has_genre'] ## exploreKG('blood_creek')=['has_genre'] ## exploreKG('the_cold_light_of_day')=['has_genre'] ## exploreKG('moonlight_serenade')=['has_genre'] ## exploreKG('american_hustle')=['has_genre'] ## exploreKG('sunshine_cleaning')=['has_genre'] ## exploreKG('the_fighter')=['has_genre'] ## exploreKG('wild_bill')=['has_genre'] ## exploreKG('the_glass_house')=['has_genre'] ## exploreKG('jumper')=[]
[User]
Execution result: ['bug', 'has_genre', 'horror'], ['machine_gun_preacher', 'has_genre', 'action'], ['young_ones', 'has_genre', 'action'], ['the_missing_person', 'has_genre', 'mystery'], ['the_missing_person', 'has_genre', 'drama'], ['the_missing_person', 'has_genre', 'comedy'], ['immortals', 'has_genre', 'fantasy'], ['blood_creek', 'has_genre', 'horror'], ['the_cold_light_of_day', 'has_genre', 'action'], ['moonlight_serenade', 'has_genre', 'romance'], ['moonlight_serenade', 'has_genre', 'drama'], ['moonlight_serenade', 'has_genre', 'musical'], ['american_hustle', 'has_genre', 'crime'], ['american_hustle', 'has_genre', 'drama'], ['sunshine_cleaning', 'has_genre', 'drama'], ['sunshine_cleaning', 'has_genre', 'comedy'], ['the_fighter', 'has_genre', 'drama'], ['the_fighter', 'has_genre', 'sport'], ['wild_bill', 'has_genre', 'western'], ['the_glass_house', 'has_genre', 'thriller']
[Your Task]
Statement: Now I get the genres of the films that share actors with 'Man of Steel'. The answer of the claim is as follows.
['horror', 'action', 'mystery', 'drama', 'comedy', 'fantasy', 'romance', 'musical', 'crime', 'sport', 'western', 'thriller']
Helper function: Verification(['horror', 'action', 'mystery', 'drama', 'comedy', 'fantasy', 'romance', 'musical', 'crime', 'sport', 'western', 'thriller'])


Example 2)
Claim: who are the actors in the films written by [John Travis]?
Given entity: ["John Travis"]

[Your Task]
Statement: I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function: getRelation('John Travis')
[User]
Execution result: Relation_list('John Travis') = ['written_by']
[Your Task]
Statement: Now, to find the films that 'John Travis' written, I need to explore the graph from 'John Travis' with related relations.
Helper function: exploreKG('John Travis')=['written_by']
[User]
Execution result: ['John Travis', 'written_by', 'the_haunting_of_molly_hartley']
[Your Task]
Statement: Now, we have to find the actors in the previous given film.
Helper function: getRelation('the_haunting_of_molly_hartley')
[User]
Execution result: Relation_list('the_haunting_of_molly_hartley') = ['has_genre', 'starred_actors', 'directed_by', 'release_year', 'written_by']
[Your Task]
Statement: To get the actors in the film, I need to explore the graph with the film and related relations.
Helper function: exploreKG('the_haunting_of_molly_hartley')=['starred_actors']
[User]
Execution result: ['the_haunting_of_molly_hartley', 'starred_actors', 'haley_bennett'], ['the_haunting_of_molly_hartley', 'starred_actors', 'chace_crawford'], ['the_haunting_of_molly_hartley', 'starred_actors', 'jake_weber']
[Your Task]
Statement: Now I get the actors of the films written by 'John Travis'. The answer of the claim is as follows.
['haley_bennett', 'chace_crawford', 'jake_weber']
Helper function: Verification(['haley_bennett', 'chace_crawford', 'jake_weber'])

Example 3)
Claim: what does [Hiromi Nagasaku] star in?
Given entity: ["Hiromi Nagasaku"]

[Your Task]
Statement: I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function: getRelation(["Hiromi Nagasaku"])
[User]
Execution result: Relation_list(["Hiromi Nagasaku"]) = ['starred_actors']
[Your Task]
Statement: Now, to find the films that 'Hiromi Nagasaku' starred, I need to explore the graph from 'Hiromi Nagasaku' with related relations.
Helper function: exploreKG('Hiromi Nagasaku')=['starred_actors']
[User]
Execution result: ['Hiromi Nagasaku', 'starred_actors', 'doppleganger']
[Your Task]
Statement: Now I get the films starred by 'Hiromi Nagasaku'. The answer of the claim is as follows.
['doppleganger']
Helper function: Verification(['doppleganger'])

Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>
"""

initial_prompt_stop_sig = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use below helper functions to find the evidence for finding labels.

<Helper functions>
1. getRelation(entity): Returns the list of relations connected to the entity. If you don't have the information about the connected relations, ***you must use this function to get the relations***.
2. exploreKG(entity) = [list of relations]: Returns the corresponding tail entities in graph data starts from single entity in given entity and given relation.
3. Verification([list of entities]): After getting enough evidence after exploreKG() helper function and if verification can be done, call this function with labels.

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
Helper function: getRelation('Man of Steel')
*** STOP GENERATING ***
[User]
Execution result: Relation_list('Man of Steel') = ['release_year', 'starred_actors', 'written_by', 'has_tags', 'directed_by']
[Your Task]
Statement: First, to solve the claim, I have to know the actors starred in 'Man of Steel'.
Helper function: exploreKG('Man of Steel')=['starred_actors']
*** STOP GENERATING ***
[User]
Execution result: ['Man of Steel', 'starred_actors', 'michael_shannon'], ['Man of Steel', 'starred_actors', 'henry_cavill'], ['Man of Steel', 'starred_actors', 'amy_adams'], ['Man of Steel', 'starred_actors', 'diane_lane']
[Your Task]
Statement: Since I got new entities for the actors in 'Man of Steel', I need relations linked with the actors.
Helper function: getRelation('michael_shannon') ## getRelation('henry_cavill') ## getRelation('amy_adams') ## getRelation('diane_lane')
*** STOP GENERATING ***
[User]
Execution result: Relation_list('michael_shannon') = ['has_tags', 'starred_actors'], Relation_list('henry_cavill') = ['starred_actors'], Relation_list('amy_adams') = ['has_tags', 'starred_actors'], getRelations('diane_lane') = ['has_tags', 'starred_actors']
[Your Task]
Statement: To get the films starred by previous actors, I need to explore the graph with each actors and related relations.
Helper function: exploreKG('michael_shannon')=['starred_actors'] ## exploreKG('henry_cavill')=['starred_actors'] ## exploreKG('amy_adams')=['starred_actors'] ## exploreKG('diane_lane')=['starred_actors']
*** STOP GENERATING ***
[User]
Execution result: ['michael_shannon', 'starred_actors', 'bug'], ['michael_shannon', 'starred_actors', 'machine_gun_preacher'], ['michael_shannon', 'starred_actors', 'young_ones'], ['michael_shannon', 'starred_actors', 'the_missing_person'], ['henry_cavill', 'starred_actors', 'immortals'], ['henry_cavill', 'starred_actors', 'blood_creek'], ['henry_cavill', 'starred_actors', 'the_cold_light_of_day'], ['amy_adams', 'starred_actors', 'moonlight_serenade'], ['amy_adams', 'starred_actors', 'american_hustle'], ['amy_adams', 'starred_actors', 'sunshine_cleaning'], ['amy_adams', 'starred_actors', 'the_fighter'], ['diane_lane', 'starred_actors', 'wild_bill'], ['diane_lane', 'starred_actors', 'the_glass_house'], ['diane_lane', 'starred_actors', 'jumper']
[Your Task]
Statement: I need to find the relations linked with all the films from previous step.
Helper function: getRelation('bug') ## getRelation('machine_gun_preacher') ## getRelation('young_ones') ## getRelation('the_missing_person') ## getRelation('immortals') ## getRelation('blood_creek') ## getRelation('the_cold_light_of_day') ## getRelation('moonlight_serenade') ## getRelation('american_hustle') ## getRelation('sunshine_cleaning') ## getRelation('the_fighter') ## getRelation('wild_bill') ## getRelation('the_glass_house') ## getRelation('jumper')
*** STOP GENERATING ***
[User]
Execution result: Relation_list('bug') = ['starred_actors', 'has_tags', 'written_by', 'release_year', 'has_genre', 'directed_by'], Relation_list('machine_gun_preacher') = ['starred_actors', 'has_tags', 'written_by', 'release_year', 'has_genre', 'directed_by'], Relation_list('young_ones') = ['starred_actors', 'has_genre', 'release_year'], Relation_list('the_missing_person') = ['starred_actors', 'written_by', 'release_year', 'has_genre'], Relation_list('immortals') = 'starred_actors', 'has_tags', 'release_year', 'has_genre', 'in_language'], Relation_list('blood_creek') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('the_cold_light_of_day') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('moonlight_serenade') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('american_hustle') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('sunshine_cleaning') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('the_fighter') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('wild_bill') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('the_glass_house') = ['starred_actors', 'has_tags', 'release_year', 'has_genre', 'directed_by'], Relation_list('jumper') = ['starred_actors', 'has_tags', 'release_year', 'directed_by']
[Your Task]
Statement: To get the genres of the films, I need to explore the graph with each films and related relations.
Helper function: exploreKG('bug')=['has_genre'] ## exploreKG('machine_gun_preacher')=['has_genre'] ## exploreKG('young_ones')=['has_genre'] ## exploreKG('the_missing_person')=['has_genre'] ## exploreKG('immortals')=['has_genre'] ## exploreKG('blood_creek')=['has_genre'] ## exploreKG('the_cold_light_of_day')=['has_genre'] ## exploreKG('moonlight_serenade')=['has_genre'] ## exploreKG('american_hustle')=['has_genre'] ## exploreKG('sunshine_cleaning')=['has_genre'] ## exploreKG('the_fighter')=['has_genre'] ## exploreKG('wild_bill')=['has_genre'] ## exploreKG('the_glass_house')=['has_genre'] ## exploreKG('jumper')=[]
*** STOP GENERATING ***
[User]
Execution result: ['bug', 'has_genre', 'horror'], ['machine_gun_preacher', 'has_genre', 'action'], ['young_ones', 'has_genre', 'action'], ['the_missing_person', 'has_genre', 'mystery'], ['the_missing_person', 'has_genre', 'drama'], ['the_missing_person', 'has_genre', 'comedy'], ['immortals', 'has_genre', 'fantasy'], ['blood_creek', 'has_genre', 'horror'], ['the_cold_light_of_day', 'has_genre', 'action'], ['moonlight_serenade', 'has_genre', 'romance'], ['moonlight_serenade', 'has_genre', 'drama'], ['moonlight_serenade', 'has_genre', 'musical'], ['american_hustle', 'has_genre', 'crime'], ['american_hustle', 'has_genre', 'drama'], ['sunshine_cleaning', 'has_genre', 'drama'], ['sunshine_cleaning', 'has_genre', 'comedy'], ['the_fighter', 'has_genre', 'drama'], ['the_fighter', 'has_genre', 'sport'], ['wild_bill', 'has_genre', 'western'], ['the_glass_house', 'has_genre', 'thriller']
[Your Task]
Statement: Now I get the genres of the films that share actors with 'Man of Steel'. The answer of the claim is as follows.
['horror', 'action', 'mystery', 'drama', 'comedy', 'fantasy', 'romance', 'musical', 'crime', 'sport', 'western', 'thriller']
Helper function: Verification(['horror', 'action', 'mystery', 'drama', 'comedy', 'fantasy', 'romance', 'musical', 'crime', 'sport', 'western', 'thriller'])


Example 2)
Claim: who are the actors in the films written by [John Travis]?
Given entity: ["John Travis"]

[Your Task]
Statement: I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function: getRelation('John Travis')
*** STOP GENERATING ***
[User]
Execution result: Relation_list('John Travis') = ['written_by']
[Your Task]
Statement: Now, to find the films that 'John Travis' written, I need to explore the graph from 'John Travis' with related relations.
Helper function: exploreKG('John Travis')=['written_by']
*** STOP GENERATING ***
[User]
Execution result: ['John Travis', 'written_by', 'the_haunting_of_molly_hartley']
[Your Task]
Statement: We find new entity corresponding to film written by 'John Travis', I have to find the actors in the previous given film.
Helper function: getRelation('the_haunting_of_molly_hartley')
*** STOP GENERATING ***
[User]
Execution result: Relation_list('the_haunting_of_molly_hartley') = ['has_genre', 'starred_actors', 'directed_by', 'release_year', 'written_by']
[Your Task]
Statement: To get the actors in the film, I need to explore the graph with the film and related relations.
Helper function: exploreKG('the_haunting_of_molly_hartley')=['starred_actors']
*** STOP GENERATING ***
[User]
Execution result: ['the_haunting_of_molly_hartley', 'starred_actors', 'haley_bennett'], ['the_haunting_of_molly_hartley', 'starred_actors', 'chace_crawford'], ['the_haunting_of_molly_hartley', 'starred_actors', 'jake_weber']
[Your Task]
Statement: Now I get the actors of the films written by 'John Travis'. The answer of the claim is as follows.
['haley_bennett', 'chace_crawford', 'jake_weber']
Helper function: Verification(['haley_bennett', 'chace_crawford', 'jake_weber'])

Example 3)
Claim: what does [Hiromi Nagasaku] star in?
Given entity: ["Hiromi Nagasaku"]

[Your Task]
Statement: I need to look around the the given entities. First, I need the relation list actually linked with the entity.
Helper function: getRelation(["Hiromi Nagasaku"])
*** STOP GENERATING ***
[User]
Execution result: Relation_list(["Hiromi Nagasaku"]) = ['starred_actors']
[Your Task]
Statement: Now, to find the films that 'Hiromi Nagasaku' starred, I need to explore the graph from 'Hiromi Nagasaku' with related relations.
Helper function: exploreKG('Hiromi Nagasaku')=['starred_actors']
*** STOP GENERATING ***
[User]
Execution result: ['Hiromi Nagasaku', 'starred_actors', 'doppleganger']
[Your Task]
Statement: Now I get the films starred by 'Hiromi Nagasaku'. The answer of the claim is as follows.
['doppleganger']
Helper function: Verification(['doppleganger'])

Now, it's your turn. Your response must have same form with upper examples.
Claim: <<<<CLAIM>>>>
Given entity: <<<<GT_ENTITY>>>>
"""

openai.api_key = "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"
client = OpenAI(api_key=openai.api_key)

class OpenAIBot:
    def __init__(self,engine, client, temp, top_p):
        # Initialize conversation with a system message
        self.conversation = [{"role": "system", "content": "You are a helpful assistant."}]
        self.engine = engine
        self.client = client
        self.temp = temp
        self.top_p = top_p
    def add_message(self, role, content):
        # Adds a message to the conversation.
        self.conversation.append({"role": role, "content": content})
    def generate_response(self, prompt):
        # Add user prompt to conversation
        self.add_message("user", prompt)

        try:
            # Make a request to the API using the chat-based endpoint with conversation context
            response = self.client.chat.completions.create( model=self.engine, messages=self.conversation, temperature= self.temp, top_p=self.top_p)
            # Extract the response
            assistant_response = response.choices[0].message.content.strip()
            
            # Add assistant response to conversation
            self.add_message("assistant", assistant_response)
            # Return the response
            return assistant_response
        #except:
        #    print('Error Generating Response!')
        except openai.APIError as e:
            #Handle API error here, e.g. retry or log
            print(f"OpenAI API returned an API Error: {e}")
            return f"OpenAI API returned an API Error: {e}"

class Information:
    def __init__(self, gt_entity):
        self.entrel = []
        self.gt_entity = gt_entity
        self.state = 0

    def setState(self, state):
        self.state = state


def reasoning(prompt, label, entities, max_iter, model, temp, top_p, f):
            
    # engine= "gpt-3.5-turbo"
    # engine = "gpt-4o-mini"
    # engine = model
    # chatbot = OpenAIBot(engine, client, temp, top_p)
    engine = model
    chatbot = LLMBot(engine, temp, top_p, 2000)
    gt_entity = preprocess_ent(entities[0])
    info = Information(gt_entity)

    iter_limit=max_iter
    flag = False

    for i in range(iter_limit + 1):
        
        # Get Prompt from User
        if i == 0:
            pass
        else:
            #prompt = input()
            try:
                prompt, result = client_answer(response, label, info)
            except:
                break
            # if info.state == -1:
            #     break
            f.write(prompt)

        # f.write(prompt)
        if 'Done!!' in prompt:
            flag = True
            break

        # Generate and Print the Response from ChatBot
        f.write(f"\n************************************Iteration:{i}***********************************")

        response = chatbot.generate_response(prompt)
        print(response)
        time.sleep(2)

        if response == None or 'Error' in response:
            return 'Error', i
        
        f.write("\n"+response)
    
    if flag == False:
        result = 'Abstain' 
        
    return result, i
        
        
def client_answer(response, label, info):
    if response.count('[Your Task]') > 1:
        prompt = '\n[User]\nExecution result: ' + '\nYou should wait for the [User] response after calling helper function.'
        prompt = '\nGive the response for previous helper function again and wait for [User] response.'
        return prompt, []
    result = None
    #called multi helper functions
    #if not response.startswith('getRelation', 11) or not response.startswith('exploreKG',11) or not response.startswith('Verify', 11):
    #    prompt = '[Server]\nYou gave wrong format. Call the helper function again follow the right format'
    #    return prompt, result
    helper_ftn_calls = []
    helper_ftn_calls = split_functions(response)
    prompt = '\n[User]\nExecution result: '
    
    for ftn in helper_ftn_calls:
        if 'getRelation' in ftn:
            try :
                entity = ftn.split("getRelation(")[1].split(")")[0][1:-1]
                result = get_relation(entity)
                if len(result)==0:
                    prompt+= "\nDo not change the format of entity in helper function."
                else:
                    prompt += f"\nRelation_list('{entity}') = {result}"
            except :
                prompt += '\nYou gave wrong format. Call the helper function again follow the right format'
        elif 'exploreKG' in ftn:
            try:
                entity = ftn.split("exploreKG(")[1].split(")=")[0][1:-1]
                relations = ftn.split("=[")[1].split("]")[0].strip().split(', ')
                result = explore_kg(entity, relations, info)      # entity, string of relation list
                if len(result) == 0 :
                    continue
                else:
                    prompt += f"\n{', '.join([str(triple) for triple in result])}"
            except:
                prompt = '\nYou gave wrong format. Call the helper function again follow the right format'
        elif 'Verification' in ftn:
            try:
                result = ftn.split("Verification(")[1].split(")")[0]
                result = ast.literal_eval(result)
                result = list(set(result))
                # result = ftn.split("Verification(")[1].split(")")[0][1:-1]

                prompt += f"\nDone!!\nPrediction:{result}\nReal label:{label}"
            except:
                prompt += '\nYou gave wrong format. Call the helper function again follow the right format'
        else:
            prompt += '\nYou gave wrong format. Call the helper function again follow the right format'
    return prompt, result


def split_functions(response):
    helper_ftn_calls=[]
    response = response.replace("[Your Task]\n",'')
    statement = response.split("Statement: ")[0].split("Helper function: ")[0]
    functions = response.split("Helper function: ")[1]
    if '##' in functions:
        helper_ftn_calls = functions.split(' ## ')
    else :
        helper_ftn_calls = [functions]
    return helper_ftn_calls

def preprocess_ent(ent):
    ent = str(ent)
    if (ent[0]=='"' and ent[-1]=='"') or (ent[0]=="'" and ent[-1]=="'"):
        return ent[1:-1].replace(' ', '_').lower()
    else:
        return ent.replace(' ', '_').lower()

def get_relation(entity):
    #print(f"befor enetity:{entity}")
    entity = preprocess_ent(entity)
    #print(f"after entity:{entity}")
    relation_list = db.getRelationsFromEntity(entity)
    #print(f"reltaion list of called fucntion:{relation_list}")
    return relation_list

def explore_kg(entity, relations, info):
    #print(f"entity:{entity}, relations:{relations}")
    entity = preprocess_ent(entity)
    triple_sets= []
    for rel in relations:
        rel = rel[1:-1]
        if (entity, rel) in info.entrel:
            info.setState(-1)
            return []
        else: info.entrel.append((entity, rel))
        #print(f"looking entity:{entity}, relation:{rel}")
        tails = db.getEntityFromEntRel(entity, rel)
        for tail in tails:
            if tail == info.gt_entity: continue # MetaQA dataset doesn't contain gt_entity while the hop goes by.
            tmp = [entity,rel,tail]
            triple_sets.append(tmp)
    #print(f'triple sets:{triple_sets}')
    return triple_sets

def score(predict, label,f):
    per_score = len(label)
    abs, correct, wrong = 0, 0, 0
    print(f"predict:{predict}\nlabel:{label}")
    if 'abstain' in str(predict).lower():
        abs+=1
        f.write('\nabstain!')

    else:
        new_pred_list, new_label_list = [],[]
        # predict_list = predict.split(', ')
        predict_list = predict

        for pred in predict_list:
            new_pred_list.append(preprocess_ent(pred))
        for lab in label:
            # lab_tmp = re.sub(r"[^a-zA-Z0-9]", "", lab.lower())
            new_label_list.append(preprocess_ent(lab))
        
        # print(new_pred_list, new_label_list)

        for new_pred in new_pred_list:
            if new_pred in new_label_list:
                correct += 1/per_score
            else:
                wrong += 1/per_score

        if correct > 0: f.write('\nCorrect!')
        else: f.write('\nWrong')        
    
    f.write(f'\nscore: {correct}, {wrong}')

    return abs, correct, wrong
    
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", type=str, default="three_hop")
    parser.add_argument("--num_iter", type = int, default = "10")
    parser.add_argument("--model", type = str, default= "Qwen-32B")
    parser.add_argument("--prompt", type = str, default= "initial_prompt")
    parser.add_argument("--temp", type = float, default = 0.3)
    parser.add_argument("--top_p", type = float, default = 0.1)
    parser.add_argument("--paraphrase_num", type = int, default = 5)
    args = parser.parse_args()
    
    if args.model == 'Qwen-14B':
        save_path = f"./model_variant_result_20241107/Qwen-2.5-14B-Instruct"
    elif args.model == 'Qwen-32B':
        save_path = f"./model_variant_result_20241107/Qwen-2.5-32B-Instruct/paraphrase"
    elif args.model == 'Mistral-Small':
        save_path = f"./model_variant_result_20241107/Mistral-Small-Instruct-2409-t16384/paraphrase"
    elif args.model == 'llama':
        save_path = f"./model_variant_result_20241107/Meta-Llama-3.1-70B-Instruct/paraphrase"
    elif args.model == 'chatgpt':
        save_path = f"./model_variant_result_20241107/chatgpt/paraphrase"
    
    # save_path = f"./model_variant_result_20241107/Qwen-2.5-14B-Instruct"

    # save_path = f"./model_variant_result_20241107/Meta-Llama-3.1-70B-Instruct"
    
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    
    # Load proper dataset
    if args.type=='one_hop':
        file_pth = "../data/onehop_test_set.jsonl"
    elif args.type =='two_hop':
        file_pth = "../data/twohop_test_set.jsonl"
    elif args.type == 'three_hop':
        file_pth = "../data/threehop_test_set.jsonl"
    else:
        print("wrong argument")

    # Load prompt
    if args.prompt == "initial_prompt":
        prompt_template = initial_prompt_stop_sig
    elif args.prompt == "pr1":
        prompt_template = pr1_stop_sig
    elif args.prompt == "pr2":
        prompt_template = pr2
    elif args.prompt == "pr3":
        prompt_template = pr3_stop_sig
    elif args.prompt == "pr4":
        prompt_template = pr4_stop_sig
    elif args.prompt == "pr5":
        prompt_template = pr5_stop_sig
    elif args.prompt == "pr1_singlecall":
        prompt_template = pr1_singlecall
    
    # Load model
    if args.model == 'Qwen-14B':
        model_name = "Qwen/Qwen2.5-14B-Instruct"
    elif args.model == 'Qwen-32B':
        model_name = "Qwen/Qwen2.5-32B-Instruct"
    elif args.model == 'chatgpt':
        model_name = "gpt-4o-mini"
    elif args.model == 'Mistral-Small':
        model_name = "mistralai/Mistral-Small-Instruct-2409"
    elif args.model == 'llama':
        model_name = "meta-llama/Meta-Llama-3.1-70B-Instruct"

    result = {}
    questions_dict = {}
    entity_set_dict = {}
    label_set_dict = {}
    types_dict ={}
    answer_list = []
    
    with open(os.path.expanduser(file_pth)) as f:
        for line in f:
            if not line:
                continue
            q = json.loads(line)
            questions_dict[q["question_id"]] = q["question"]
            entity_set_dict[q["question_id"]] = q["entity_set"]
            label_set_dict[q["question_id"]] = q["Label"]
    
            
    iter_num_list=[]
    total_correct, total_abs,total_wrong, total_sample = 0, 0, 0, 0

    paraphrase_num = args.paraphrase_num

    for i in range(paraphrase_num):
        result_file = os.path.join(save_path, f"only_answer_{args.type}_{args.model}_maxiter_{args.num_iter}_prompt_{args.prompt}_temp_{args.temp}_topp_{args.top_p}_paraphrase_{i}.csv")
        result_file_csv = open(result_file, 'a')
        answer_list= [['qid','correct','wrong','prediction','gt_label']]
        result_file_csv.write(','.join(answer_list[0]) + '\n')
        result_file_csv.close()
    # with open(os.path.join(save_path,f"{args.type}.txt"),'a') as f:
    #     for qid, question in questions_dict.items():
    for qid, question in questions_dict.items():
        if qid > 2000:
                break
        if qid % 20 != 0:
            continue

        paraphrase_list = paraphrase(question)
        
        for i in range(paraphrase_num):
            question = paraphrase_list[0]

            with open(os.path.join(save_path, f"result_{args.type}_{args.model}_maxiter_{args.num_iter}_prompt_{args.prompt}_temp_{args.temp}_topp_{args.top_p}_paraphrase_{i}.txt"),'a') as f:
                print(f"Qid:{qid}")
                # question = questions_dict[qid]
                label = label_set_dict[qid]
                entities = entity_set_dict[qid]
                
                f.write(f"\n\n\nQid:{qid}\nQuestion :{question}")
                f.write(f"GT entity:{entities}")
                
                prompt = prompt_template.replace('<<<<CLAIM>>>>', question).replace('<<<<GT_ENTITY>>>>', str(entities))

                prediction, iter_num = reasoning(prompt, label, entities, args.num_iter, model_name, args.temp, args.top_p, f)
                abs, correct, wrong= score(prediction, label, f)
                total_correct += correct
                total_wrong += wrong
                total_abs += abs
                total_sample +=1
                iter_num_list.append(iter_num)
                answer_list.append([qid,correct,wrong,str(prediction), str(label)])

                f.close()
            
            # if (total_sample - total_abs) == 0:
            #     metric1 = 0
            # else:
            #     metric1 = (total_sample - total_abs) /  total_sample
            # if total_correct == 0:
            #     metric2 = 0
            # else:
            #     metric2 = total_correct / (total_sample - total_abs)
            # if (total_correct-total_wrong) == 0:
            #     metric3 = 0
            # else:
            #     metric3 = (total_correct-total_wrong) / (total_sample - total_abs)

            # with open(os.path.join(save_path, f"result_{args.type}_{args.model}_maxiter_{args.num_iter}_prompt_{args.prompt}_temp_{args.temp}_topp_{args.top_p}_multicall.txt"),'a') as f:
            #     f.write(f"\n\nTotal sample:{total_sample}, Total_Correct:{total_correct}, Total_Wrong:{total_wrong}, Total_abstain:{total_abs}")
            #     f.write(f"\nmetric1:{metric1}\nmetric2:{metric2}\nmetric3 :{metric3}")
            #     f.write(f"\navg iter:{np.average(iter_num_list)}\nmax_iter:{np.max(iter_num_list)}\nmin_iter:{np.min(iter_num_list)}")
            
            with open(os.path.join(save_path, f"only_answer_{args.type}_{args.model}_maxiter_{args.num_iter}_prompt_{args.prompt}_temp_{args.temp}_topp_{args.top_p}_paraphrase_{i}.csv"),'a') as f:
                writer= csv.writer(f)
                writer.writerow([qid, correct, wrong, str(prediction), str(label)])
        
    