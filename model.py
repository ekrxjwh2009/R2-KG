from openai import OpenAI

# Modify OpenAI's API key and API base to use vLLM's API server.
VLLM_API_KEY = "EMPTY" # No needed!
VLLM_API_BASE_LLAMA_70B = "[VLLM SERVER URL]"
VLLM_API_BASE_QWEN_14B = "[VLLM SERVER URL]"
VLLM_API_BASE_QWEN_32B = "[VLLM SERVER URL]"
VLLM_API_BASE_MISTRAL_SMALL = "[VLLM SERVER URL]"

class LLMBot:
    def __init__(self, model, temperature, top_p, max_tokens):
        self.conversation = [{"role": "system", "content": "You are a helpful assistant."}]
        self.model = model
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens

        if model == 'mistral-small':
            self.model = "mistralai/Mistral-Small-Instruct-2409"
            self.api_base = VLLM_API_BASE_MISTRAL_SMALL
        elif model =='qwen_14b':
            self.model = "Qwen/Qwen2.5-14B-Instruct"
            self.api_base = VLLM_API_BASE_QWEN_14B
        elif model == 'qwen_32b':
            self.model = "Qwen/Qwen2.5-32B-Instruct"
            self.api_base = VLLM_API_BASE_QWEN_32B
        elif model=='llama':
            self.model = "meta-llama/Meta-Llama-3.1-70B-Instruct"  
            self.api_base = VLLM_API_BASE_LLAMA_70B 
        
        self.vllm_client = OpenAI(api_key=VLLM_API_KEY, base_url=self.api_base)


    def add_message(self, role, message):
        self.conversation.append({"role": role, "content": message})
    
    def generate_response(self, prompt):
        self.add_message('user', prompt)
        
        try:
            response = self.vllm_client.chat.completions.create(
                model=self.model,
                messages=self.conversation,
                temperature=self.temperature,
                top_p=self.top_p,
                max_tokens=self.max_tokens,
            )
            assistant_response = response.choices[0].message.content.strip()
            self.add_message('assistant', assistant_response)
            return assistant_response

        except Exception as e:
            print(f"Error during API call: {e}")
            return "I'm sorry, something went wrong."