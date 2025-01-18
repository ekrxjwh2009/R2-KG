import time
from openai import OpenAI
time_gap = {}

# Modify OpenAI's API key and API base to use vLLM's API server.
VLLM_API_KEY = "EMPTY"
VLLM_API_BASE = "http://localhost:9123/v1"
vllm_client = OpenAI(api_key=VLLM_API_KEY, base_url=VLLM_API_BASE)


def vllm_response(message: list, model=None, temperature=0, max_tokens=500):
    assert model in [
        "meta-llama/Meta-Llama-3.1-70B-Instruct",
    ]
    time.sleep(time_gap.get(model, 3))

    try:
        res = vllm_client.chat.completions.create(
            model=model,
            messages=message,
            temperature=temperature,
            n=1,
            max_tokens=max_tokens,
        )
        return res.choices[0].message.content
    except Exception as e:
        print(e)
        time.sleep(time_gap.get(model, 3) * 2)
        return vllm_response(message, model, temperature, max_tokens)

model_name = "meta-llama/Meta-Llama-3-70B-Instruct"
messages = [{"role": "user", "content": "What is your name?"}]
response = vllm_response(messages=messages, model=model_name)