import openai
from openai import OpenAI
import prompts


openai.api_key = "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"
client = OpenAI(api_key=openai.api_key)


def feedback(claim,gold_set,f,sub_prompt):
      
    #f.write(f"\nGOLD SET!!!!!!!!!!!!!!!!!!!!!!\n{gold_set}")       
    engine="gpt-3.5-turbo-0125"
    #engine = "gpt-4o-mini-2024-07-18"
    conversation = [{"role": "system", "content": "You are a helpful assistant."}]
    prompt = sub_prompt.replace('<<<<CLAIM>>>>', claim).replace('<<<<Triple set>>>>', str(gold_set))
    conversation.append({"role": "user", "content": prompt})
    
    for i in range(5):

        
        try :  
            response = client.chat.completions.create( model=engine, messages=conversation, temperature= 0.3, top_p = 0.1)
            assistant_response = response.choices[0].message.content.strip()
            #print(assistant_response)
            try:
                sub_result = assistant_response.split("Evaluation")[1].strip()
                
                
                if "(Insufficient evidence)" in sub_result:
                    sub_response = "We don't have enough evidence to verify the claim. You must extract more information from the graph data."
                    case =1
                    prediction = None
                    break
                elif "(Complex claim)" in sub_result:
                    sub_response = "Done!! Abstain"
                    case=2
                    prediction = "Abstain"
                    break
                else: 
                    #Executable case
                    if 'True' in sub_result or 'true' in sub_result:
                        sub_response = "Done!! True"
                        prediction = 'True'
                    else:
                        sub_response = "Done!! False"
                        prediction = 'False'
                    case=3
                    break
            except:
                continue

        

        except openai.APIError as e:
                #Handle API error here, e.g. retry or log
                print(f"OpenAI API returned an API Error: {e}")
                continue
    
    
    
    return sub_response, case, prediction