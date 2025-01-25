import time
from openai import OpenAI
import tiktoken

VLLM_API_BASE_MISTRAL_SMALL = "http://143.248.157.70:8334/v1"       #RTX 3090 * 8
VLLM_API_QWEN_14B = ""
VLLM_API_QWEN_32B = ""
VLLM_API_LLAMA_70B = "http://143.248.157.130:8334/v1"  # A6000*4
VLLM_API_KEY = "EMPTY"  # No API key required for vLLM

class LLMBot:
    def __init__(self, model, temperature, top_p, max_tokens):
        self.conversation = [{"role": "system", "content": "You are a helpful assistant."}]
        self.max_context_length = 16384  # 모델의 최대 입력 길이
        self.max_tokens = max_tokens
        
        if model == 'mistral-small':
            self.model = "mistralai/Mistral-Small-Instruct-2409"
            self.url = VLLM_API_BASE_MISTRAL_SMALL
        elif model =='qwen_14b':
            self.model = "Qwen/Qwen2.5-14B-Instruct"
            self.url = VLLM_API_QWEN_14B
        elif model == 'qwne_32b':
            self.model = "Qwen/Qwen2.5-32B-Instruct"
            self.url = VLLM_API_QWEN_32B
        elif model=='llama':
            self.model = "meta-llama/Meta-Llama-3.1-70B-Instruct"  
            self.url = VLLM_API_LLAMA_70B 

        self.temperature = temperature
        self.top_p = top_p
        self.vllm_client = OpenAI(api_key=VLLM_API_KEY, base_url=self.url)
        self.tokenizer = tiktoken.get_encoding("cl100k_base")

    def add_message(self, role, message):
        self.conversation.append({"role": role, "content": message})
        while self.calculate_total_tokens() >= (self.max_context_length - self.max_tokens):
            self.conversation.pop(0)
            
    def calculate_total_tokens(self):
        # 대화 내 모든 메시지의 토큰 수 계산
        total_tokens = 0
        for msg in self.conversation:
            total_tokens += len(self.tokenizer.encode(msg["content"]))
        return total_tokens

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
            
        

if __name__ == "__main__":
    bot = LLMBot("mistralai/Mistral-Small-Instruct-2409", 0.7, 0.9, 2000)
    print(bot.generate_response("What is the purpose of life?"))





'''

CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 python -m vllm.entrypoints.openai.api_server \
    --model mistralai/Mistral-Small-Instruct-2409 \
    --tensor-parallel-size 8 \
    --port 8334 \
    --dtype bfloat16 \
    --max-model-len 16384

    '''