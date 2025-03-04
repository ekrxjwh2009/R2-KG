import sys, os
import ast
import openai
from openai import OpenAI
from dotenv import load_dotenv


current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(root_dir)
load_dotenv()

openai.api_key = os.getenv('OPENAI_KEY')

client = OpenAI(
    api_key = os.getenv('OPENAI_KEY')
)


def feedback(supervisor, claim, gold_set, gold_relations, sub_prompt):
    if supervisor == 'gpt-4o-mini': engine = "gpt-4o-mini-2024-07-18"
    elif supervisor == 'gpt-4o': engine = "gpt-4o-2024-08-06"
    
    final_evidence = []
    
    for tri in gold_set:
        if tri not in final_evidence:
            final_evidence.append(tri)
      
    conversation = [{"role": "system", "content": "You are a helpful assistant."}]
    prompt = sub_prompt.replace('<<<<CLAIM>>>>', claim).replace('<<<<Triple set>>>>', str(final_evidence)).replace('<<<<GOLD RELATIONS>>>>', gold_relations)
    conversation.append({"role": "user", "content": prompt})
    
    # Initialize variables
    sub_response = None
    prediction = None
    
    
    for i in range(3):
        try :  
            response = client.chat.completions.create(model=engine, messages=conversation, temperature=0.95, top_p=0.95)
            assistant_response = response.choices[0].message.content.strip()
            # print(assistant_response)
            
            try:
                sub_statement = assistant_response.split("Statement")[1].split("Evaluation")[0].strip()
                sub_result = assistant_response.split("Evaluation: ")[1].strip()
                
                if "(Insufficient evidence)" in sub_result:
                    #sub_response = "We don't have enough evidence to verify the claim. You must extract more information from the graph data."
                    sub_response = sub_statement
                    prediction = None
                    break
                elif "(Complex claim)" in sub_result:
                    sub_response = "Done!! Abstain"
                    prediction = "Abstain"
                    break
                else: 
                    sub_response = "Done!!"
                    prediction = sub_result.split('Executable(')[1].split(")")[0]
                    prediction = list(set(ast.literal_eval(prediction)))
                    for i in range(len(prediction)): prediction[i] = str(prediction[i])
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
        prediction = None
    
    
    return sub_response, prediction