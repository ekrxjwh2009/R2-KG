import openai
from openai import OpenAI
import sys
import os
import re
import prompts


openai.api_key = "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"
client = OpenAI(api_key=openai.api_key)

def paraphrase(claim):
    
    engine="gpt-3.5-turbo-0125"
    #engine = "gpt-4o-mini-2024-07-18"

    conversation = [{"role": "system", "content": "You are a helpful assistant."}]
    prompt = prompts.paraphrase_prompt.replace('<<<<CLAIM>>>>', claim)
    conversation.append({"role": "user", "content": prompt})
    
    for i in range(1):
        try :  
            response = client.chat.completions.create( model=engine, messages=conversation, temperature= 0.1, top_p = 0.1)
            assistant_response = response.choices[0].message.content.strip()
            #print(assistant_response)

            pattern = r'\d+\.\s*(.*)'
            matches = re.findall(pattern, assistant_response)

            return matches

        except openai.APIError as e:
                #Handle API error here, e.g. retry or log
                print(f"OpenAI API returned an API Error: {e}")
                continue
    
    return []