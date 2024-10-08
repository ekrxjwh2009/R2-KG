import openai
from openai import OpenAI
import prompts


openai.api_key = "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"
client = OpenAI(api_key=openai.api_key)


def feedback(claim,gold_chat):
    #engine="gpt-3.5-turbo-0125"         
    engine = "gpt-4o-mini-2024-07-18"
    conversation = [{"role": "system", "content": "You are a helpful assistant."}]
    prompt = prompts.sub_agent.replace('<<<<CLAIM>>>>', claim).replace('<<<<Triple set>>>>', str(gold_chat))
    conversation.append({"role": "user", "content": prompt})
    
    for i in range(3):

        
        try :  
            response = client.chat.completions.create( model=engine, messages=conversation, temperature= 0.3, top_p = 0.1)
            assistant_response = response.choices[0].message.content.strip()
            
            sub_result = assistant_response.split("Evaluation")[1].strip()
            print(sub_result)
            if "(Insufficient evidence)" in sub_result:
                prompt = "We don't have enough evidence to verify the claim. You must extract more information from the graph data."
                case =1
                break
            elif "(Complex claim)" in sub_result:
                prompt = "Done!!"
                case=2
                break
            else: 
                #Executable case
                prompt = "Done!!"
                case=3
                break

        

        except openai.APIError as e:
                #Handle API error here, e.g. retry or log
                print(f"OpenAI API returned an API Error: {e}")
                continue
    
    
    
    return prompt, case