"""Generate answers with GPT-3.5"""
# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import openai
import time
import sys
import os
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(root_dir)
load_dotenv()

# GITIGNORE WHEN MAKING REPO PUBLIC
openai.api_key = os.getenv('OPENAI_KEY')

class Chatbot:
    def __init__(self):
        self.chatchat = []
        self.chat_history = [{"role": "system", "content": "You are a helpful assistant."}]
    
    def initialize_chat_history(self):
        self.chat_history = []
        return self.chat_history

    def add_chat_history(self, user_content, assistant_content):
        self.chat_history.append({"role" : "user", "content" : user_content})
        self.chat_history.append({"role" : "assistant", "content" : assistant_content})

        return self.chat_history

    def add_chatchat(self, user_content, assistant_content):
        self.chatchat.append({"role" : "user", "content" : user_content})
        self.chatchat.append({"role" : "assistant", "content" : assistant_content})

        return self.chatchat

    def chat(self, user_input):
        # print("user : ", user_input)
        try:
            response = openai.ChatCompletion.create(
                 model="gpt-3.5-turbo-0613",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {
                        "role": "user",
                        "content": user_input,
                    },
                ],
                max_tokens=1024,
                temperature=0.2,
                top_p = 0.1
            )
            response = response["choices"][0]["message"]["content"]
            # print("response : ", response)
        except Exception as e:
            print("[ERROR]", e)
            time.sleep(5)
            raise NotImplementedError
        
        return response
    
    # def chat_with_history(self, user_input):
    #     messages = [{"role": "system", "content": "You are a helpful assistant."}]
    #     for message in self.chatchat:
    #         messages.append(message)
        
    #     messages.append({"role": "user", "content": user_input})

    #     try:
    #         response = openai.ChatCompletion.create(
    #              model="gpt-3.5-turbo-0613",
    #             messages=messages,
    #             max_tokens=1024,
    #             temperature=0.2,
    #             top_p = 0.1
    #         )
    #         response = response["choices"][0]["message"]["content"]
    #         # print("response : ", response)
    #     except Exception as e:
    #         print("[ERROR]", e)
    #         time.sleep(5)
    #         raise NotImplementedError
        
    #     return response
    
    def chat_with_history2(self, user_input):
        self.chat_history.append({"role": "user", "content": user_input})

        try:
            response = openai.ChatCompletion.create(
                # model="gpt-3.5-turbo",
                model="gpt-4o-mini",
                messages=self.chat_history,
                max_tokens=1024,
                temperature=0.3,
                top_p = 0.1
            )
            response = response["choices"][0]["message"]["content"]

            # print("response : ", response)
        except Exception as e:
            print("[ERROR]", e)
            time.sleep(5)
            raise NotImplementedError
        
        self.chat_history.append({"role": "assistant", "content": response})

        return response