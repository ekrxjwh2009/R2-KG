import os
import openai
from openai import OpenAI
from mistralai import Mistral


class OpenAIBot:
    def __init__(self,model,engine, temperature, top_p):
        # Initialize conversation with a system message
        self.conversation = [{"role": "system", "content": "You are a helpful assistant."}]
        self.model = model
        self.engine = engine
        self.temp = temperature
        self.top_p = top_p
        if self.model == "gpt":
            openai.api_key = "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"
            self.client = OpenAI(api_key=openai.api_key)
        
        elif self.model == "mixtral":
            mistral_api_key = "vqEwVLjtDQcL6zJTUj9Q1R6MKHNkuB6F"
            self.client = Mistral(api_key=mistral_api_key)
            
        elif self.model == 'qwen':
            qwen_api_key = ""
            self.client = None
        
        elif self.model == 'llama':
            self.client = None
            
    def add_message(self, role, content):
        # Adds a message to the conversation.

        self.conversation.append({"role": role, "content": content})
    def generate_response(self, prompt):
        # Add user prompt to conversation
        self.add_message("user", prompt)

        try:
            # Make a request to the API using the chat-based endpoint with conversation context
            if self.model == "gpt":
                
                response = self.client.chat.completions.create( model=self.engine, messages=self.conversation, temperature= self.temp, top_p =  self.top_p)
                assistant_response = response.choices[0].message.content.strip()

            elif self.model == "mixtral":
                
                response = self.client.chat.complete(model= self.engine, messages=self.conversation, temperature= 0.3, top_p = 0.1)
                assistant_response = response.choices[0].message.content.strip()
            # Add assistant response to conversation
            self.add_message("assistant", assistant_response)
            # Return the response
            return assistant_response

        except openai.APIError as e:
            #Handle API error here, e.g. retry or log
            print(f"OpenAI API returned an API Error: {e}")
            return f"OpenAI API returned an API Error: {e}"





'''
parser = argparse.ArgumentParser()
parser.add_argument("type", type=str, default="before_after")
parser.add_argument("prompt", type=str, default='pr_1')
parser.add_argument("model", type = str, default="mixtral")
parser.add_argument("engine", type=str, default="mixtral-8x22b")


'''
