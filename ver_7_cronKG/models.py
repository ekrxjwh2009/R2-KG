import os
import openai
from openai import OpenAI
from mistralai import Mistral


###GPT 제외한 나머지 모델

#time_gap = {}

# Modify OpenAI's API key and API base to use vLLM's API server.
VLLM_API_KEY = "EMPTY"
#VLLM_API_BASE = "http://localhost:9123/v1"
#vllm_client = OpenAI(api_key=VLLM_API_KEY, base_url=VLLM_API_BASE)




class chatBot:
    def __init__(self,model,temperature, top_p):
        '''
        # Initialize conversation with a system message
        assert model in [
        "meta-llama/Meta-Llama-3.1-70B-Instruct",
    ]
    time.sleep(time_gap.get(model, 3))
'''
        
        
        self.conversation = [{"role": "system", "content": "You are a helpful assistant."}]
        self.model = model
        self.temp = temperature #base .95
        self.top_p = top_p #base 0.95
        self.max_tokens = 500
        
        if self.model == "mistral-large": 
            self.VLLM_API_BASE = "vqEwVLjtDQcL6zJTUj9Q1R6MKHNkuB6F"
            #self.VLLM_API_BASE = Mistral(api_key=self.api_key)
            
        elif self.model == 'mistral-instruct' : ##mistral instruct small
            self.VLLM_API_BASE = "http://143.248.157.51:8043/v1"
            
        elif self.model == 'qwen_2.5_32b': ##qwen2.5-32b
            self.VLLM_API_BASE = "http://143.248.157.77:8043/v1"

        elif self.model == 'qwen_2.5': ##qwen2.5-14b
            self.VLLM_API_BASE == "http://143.248.157.68:8043/v1"
        
        elif self.model == 'llama': ##llama3.1-70b
            self.VLLM_API_BASE ="http://143.248.157.77:8044/v1"

            
        self.client = OpenAI(api_key=VLLM_API_KEY, base_url=self.VLLM_API_BASE)
            
    def add_message(self, role, content):
        # Adds a message to the conversation.

        self.conversation.append({"role": role, "content": content})
    def generate_response(self, prompt):
        # Add user prompt to conversation
        self.add_message("user", prompt)

        try:
            res = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation,
                temperature=self.temperature,
                n=1,
                max_tokens=self.max_tokens,
            )
            self.response =  res.choices[0].message.content
        
        except Exception as e:
            print(e)
            #time.sleep(time_gap.get(model, 3) * 2)
            #return vllm_response(message, model, temperature, max_tokens)
        self.add_message('assistant', self.response)

            
model_name = "meta-llama/Meta-Llama-3-70B-Instruct"
messages = [{"role": "user", "content": "What is your name?"}]
response = chatBot(messages=messages, model=model_name)