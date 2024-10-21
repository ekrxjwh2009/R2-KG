import openai
from openai import OpenAI
import sys
import os
import re
from dotenv import load_dotenv
from prompt.factkg_prompt import paraphrase_prompt

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(root_dir)
load_dotenv()

# GITIGNORE WHEN MAKING REPO PUBLIC
openai.api_key = os.getenv('OPENAI_KEY')

client = OpenAI(
    api_key = os.getenv('OPENAI_KEY')
)


def paraphrase(claim):
    
    engine="gpt-3.5-turbo-0125"
    #engine = "gpt-4o-mini-2024-07-18"

    conversation = [{"role": "system", "content": "You are a helpful assistant."}]
    prompt = paraphrase_prompt.replace('<<<<CLAIM>>>>', claim)
    conversation.append({"role": "user", "content": prompt})
    
    for i in range(1):
        try :  
            response = client.chat.completions.create( model=engine, messages=conversation, temperature= 0.1, top_p = 0.1)
            assistant_response = response.choices[0].message.content.strip()
            print(assistant_response)

            pattern = r'\d+\.\s*(.*)'
            matches = re.findall(pattern, assistant_response)

            return matches

        except openai.APIError as e:
                #Handle API error here, e.g. retry or log
                print(f"OpenAI API returned an API Error: {e}")
                continue
    
    return []