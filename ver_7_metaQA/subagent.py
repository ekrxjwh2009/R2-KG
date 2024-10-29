import openai
from openai import OpenAI
import prompts


openai.api_key = "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"
client = OpenAI(api_key=openai.api_key)


def feedback(claim,gold_set,gold_relations,f,sub_prompt):
    
    #engine="gpt-3.5-turbo-0125"
    #engine = "gpt-4o-mini-2024-07-18"
    engine = "gpt-4o-2024-08-06"
    
    f.write(f"\nGOLD SET!!!!!!!!!!!!!!!!!!!!!!\n{gold_set}") 
    f.write(f"\nGOLD RELATIONS!!!!!!!!!!!!!!!!\n{gold_relations}")    
    final_evidence=[]
    
    
    for tri in gold_set:
        if tri not in final_evidence:
            final_evidence.append(tri)
      
    f.write(f"\nFinal Evidence!!!!!!!!!!!!!!!!!!!!!!\n{final_evidence}")       
    
    conversation = [{"role": "system", "content": "You are a helpful assistant."}]
    prompt = sub_prompt.replace('<<<<CLAIM>>>>', claim).replace('<<<<Triple set>>>>', str(final_evidence)).replace('<<<<GOLD RELATIONS>>>>', gold_relations)
    conversation.append({"role": "user", "content": prompt})
    
    # Initialize variables
    sub_response = None
    case = None
    prediction = None
    
    
    for i in range(5):

        
        try :  
            response = client.chat.completions.create( model=engine, messages=conversation, temperature= 0.3, top_p = 0.1)
            assistant_response = response.choices[0].message.content.strip()
            #print(assistant_response)
            
            try:
                sub_statement = assistant_response.split("Statement")[1].split("Evaluation")[0].strip()
                sub_result = assistant_response.split("Evaluation")[1].strip()
                print(f"SUb result: {sub_result}")
                
                if "(Insufficient evidence)" in sub_result:
                    #sub_response = "We don't have enough evidence to verify the claim. You must extract more information from the graph data."
                    sub_response = sub_statement
                    case =1
                    prediction = sub_result
                    break
                elif "(Complex claim)" in sub_result:
                    sub_response = "Done!! Abstain"
                    case=2
                    prediction = "Abstain"
                    break
                else: 
                    sub_response = "Done!!"
                    case = 3
                    prediction = sub_result.split('[')[1].split(']')[0][1:-1]
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