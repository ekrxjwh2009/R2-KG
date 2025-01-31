import openai
from openai import OpenAI
import prompts


openai.api_key = "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"
client = OpenAI(api_key=openai.api_key)


def feedback(subagent,claim,gold_set,gold_relations,sub_prompt):
    if subagent=='gpt-4o-mini':engine = "gpt-4o-mini-2024-07-18"
    elif subagent=='gpt-4o' : engine = "gpt-4o-2024-08-06"
    

    
    final_evidence=[]
    
    
    for tri in gold_set:
        if tri not in final_evidence:
            final_evidence.append(tri)
    
    
    conversation = [{"role": "system", "content": "You are a helpful assistant."}]
    prompt = sub_prompt.replace('<<<<CLAIM>>>>', claim).replace('<<<<Triple set>>>>', str(final_evidence)).replace('<<<<GOLD RELATIONS>>>>', gold_relations)
    conversation.append({"role": "user", "content": prompt})
    
    # Initialize variables
    sub_response = None
    case = None
    prediction = None
    
    
    for i in range(5):

        
        try :  
            response = client.chat.completions.create( model=engine, messages=conversation, temperature= 0.95, top_p = 0.95)
            assistant_response = response.choices[0].message.content.strip()
            print(assistant_response)
            
            try:
                sub_statement = assistant_response.split("Statement")[1].split("Evaluation")[0].strip()
                sub_result = assistant_response.split("Evaluation")[1].strip()
                print(f"SUb result: {sub_result}")
                
                if "(Insufficient evidence)" in sub_result:
                    #sub_response = "We don't have enough evidence to verify the claim. You must extract more information from the graph data."
                    sub_response = sub_statement
                    case =1
                    prediction = None
                    break
                elif "(Complex claim)" in sub_result:
                    sub_response = "Done!! Abstain"
                    case=2
                    prediction = "Abstain"
                    break
                else: 
                    if 'True' in sub_result or 'true' in sub_result:
                        sub_response = "Done!! True"
                        prediction = 'True'
                        case = 3
                        break  # Ensure the loop exits
                    elif 'False' in sub_result or 'false' in sub_result:
                        sub_response = "Done!! False"
                        prediction = 'False'
                        case = 3
                        break  # Ensure the loop exits
            except Exception as e:
                print(f"Error parsing assistant response: {e}")
                continue


        

        except openai.APIError as e:
                #Handle API error here, e.g. retry or log
                print(f"OpenAI API returned an API Error: {e}")
                continue
    
    # Ensure sub_response has a value before returning
    if sub_response is None:
        sub_response = "There is problem in server. Please call Verification[] one more time/"
        case = -1
        prediction = None
    
    
    return sub_response, case, prediction