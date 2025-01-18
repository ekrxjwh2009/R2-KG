import time
from openai import OpenAI
time_gap = {"meta-llama/Meta-Llama-3.1-70B-Instruct": 3, 
            "mistralai/Mistral-7B-Instruct-v0.3": 3, 
            "mistralai/Mixtral-8x7B-Instruct-v0.1": 3,
            "mistralai/Mistral-Nemo-Instruct-2407": 3,
            "Qwen/Qwen2.5-14B-Instruct": 3,
            "Qwen/Qwen2.5-32B-Instruct": 3,
            "mistralai/Mistral-Small-Instruct-2409": 3}

# Modify OpenAI's API key and API base to use vLLM's API server.
VLLM_API_KEY = "EMPTY" # No needed!
VLLM_API_BASE_LLAMA = "http://143.248.157.77:8044/v1" # _LLAMA
VLLM_API_BASE_QWEN14B = "http://143.248.157.68:8043/v1" # _QWEN14B / _MISTRAL
VLLM_API_BASE_QWEN32B = "http://143.248.157.77:8043/v1" # _QWEN32B
VLLM_API_BASE_MISTRAL_SMALL = "http://143.248.157.51:8043/v1" # _MISTRAL_SMALL

class LLMBot:
    def __init__(self, model, temperature, top_p, max_tokens):
        self.conversation = [{"role": "system", "content": "You are a helpful assistant."}]
        self.model = model
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens

        if model == "meta-llama/Meta-Llama-3.1-70B-Instruct":
            self.api_base = VLLM_API_BASE_LLAMA
        elif model == "Qwen/Qwen2.5-32B-Instruct":
            self.api_base = VLLM_API_BASE_QWEN32B
        elif model == "Qwen/Qwen2.5-14B-Instruct":
            self.api_base = VLLM_API_BASE_QWEN14B
        elif model == "mistralai/Mistral-Small-Instruct-2409":
            self.api_base = VLLM_API_BASE_MISTRAL_SMALL
        
        self.vllm_client = OpenAI(api_key=VLLM_API_KEY, base_url=self.api_base)


    def add_message(self, role, message):
        self.conversation.append({"role": role, "content": message})
    
    def generate_response(self, prompt):
        self.add_message('user', prompt)
        response =  vllm_response(self.conversation, self.model, self.temperature, self.top_p, self.max_tokens, self.vllm_client)
        self.add_message('assistant', response)
        return response


def vllm_response(message: list, model=None, temperature=0.7, top_p=0.9, max_tokens=500, client=None):
    assert model in [
        "meta-llama/Meta-Llama-3.1-70B-Instruct",
        "mistralai/Mixtral-8x7B-Instruct-v0.1", # .130:8044 server
        "mistralai/Mistral-Nemo-Instruct-2407",
        "Qwen/Qwen2.5-32B-Instruct", # .51:8043 server
        "Qwen/Qwen2.5-14B-Instruct",
        "mistralai/Mistral-Small-Instruct-2409"
    ]
    time.sleep(time_gap.get(model, 3))

    try:

        res = client.chat.completions.create(
            model=model,
            messages= message,  # Required argument
            temperature=temperature,
            top_p=top_p,
            n=1,
            max_tokens=max_tokens,
        )
        return res.choices[0].message.content
    except Exception as e:
        print(e)
        # time.sleep(time_gap.get(model, 3) * 2)
        # return vllm_response(messages, model, temperature, max_tokens)

if __name__ == '__main__':
    model_name = "mistralai/Mistral-Small-Instruct-2409"
    # model_name = "mistralai/Mistral-Nemo-Instruct-2407"
    # model_name = "meta-llama/Meta-Llama-3.1-70B-Instruct"
    # messages = [
    #     {"role": "system", "content": "You are a helpful assistant."},
    #     {"role": "user", "content": "What model are you?"}
    # ]  # Ensure messages are in list format
    chatbot = LLMBot(model_name, 1.0, 0.5, 2000)
    response = chatbot.generate_response("what was the previous question?")
    print(response)