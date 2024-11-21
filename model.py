import time
from openai import OpenAI
time_gap = {}

# Modify OpenAI's API key and API base to use vLLM's API server.
VLLM_API_KEY = "EMPTY" # No needed!
VLLM_API_BASE = "http://143.248.157.130:8044/v1"
vllm_client = OpenAI(api_key=VLLM_API_KEY, base_url=VLLM_API_BASE)

class LLMBot:
    def __init__(self, model, temperature, top_p, max_tokens):
        self.conversation = [{"role": "system", "content": "You are a helpful assistant."}]
        self.model = model
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens

    def add_message(self, message):
        self.conversation.append({"role": "user", "content": message})
    
    def generate_response(self, prompt):
        self.add_message(prompt)
        return vllm_response(self.conversation, self.model, self.temperature, self.top_p, self.max_tokens)


def vllm_response(message: list, model=None, temperature=0.7, top_p=0.9, max_tokens=500):
    assert model in [
        "meta-llama/Meta-Llama-3.1-8B-Instruct",
        "mistralai/Mistral-7B-Instruct-v0.3", # .130:8044 server
        "Qwen/Qwen2.5-14B-Instruct" # .51:8043 server
    ]
    time.sleep(time_gap.get(model, 3))

    try:

        res = vllm_client.chat.completions.create(
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
        # return vllm_response(message, model, temperature, max_tokens)

if __name__ == '__main__':
    model_name = "Qwen/Qwen2.5-14B-Instruct"
    model_name = "mistralai/Mistral-7B-Instruct-v0.3"
    # messages = [
    #     {"role": "system", "content": "You are a helpful assistant."},
    #     {"role": "user", "content": "What model are you?"}
    # ]  # Ensure messages are in list format
    chatbot = LLMBot(model_name, 0.7, 0.9, 500)
    response = chatbot.generate_response("What model are you?")
    print(response)
