
### Version History
- ver_0 : Confidence check() 없음, iteration N회 이상
- ver_1 : Confidence check() 있음. 이전 chat 내용 보여줌
- ver_2 : Confidence check() 있음. LLM이 새로 요청한 helper function으로 gold chat 업데이트. gold chat만 보여줌
- ver_3 : chat에 [helper function, execution result] 만 보여줌. Reasoning은 제외 → chat 자체를 단순화
- ver_4 : ver_0 (iteration N = 10) + exploreKG - 똑같은 (entity, relation) 반복해서 물어보면 abstain
- ver_5 : ver_0 (iteration N varies) + exploreKG - 똑같은 (entity, relation) 반복 + token length error 나는 경우 abstain + tail entity 구하지 못할 시 잘못하기 직전 시점부터 LLM regeneration

### TODO
- make .env file at root directory and add below line
```
OPENAI_KEY = <YOUR_OPENAI_API_KEY>
```
- below pip install is required
```
pip install python-dotenv
```

### VLLM Serving Code
- 대괄호가 씌워져 있는 parameter의 경우 상황에 따라 자주 바뀌기 때문에 상황에 맞게 parameter 수정 후 대괄호 제거 후 실행
```
CUDA_VISIBLE_DEVICES=[6,7] python -m vllm.entrypoints.openai.api_server --model meta-llama/Meta-Llama-3.1-8B-Instruct \
                            --load-format safetensors --max-model-len 8192 --download-dir /nfs_data_storage/huggingface \
                            --tensor-parallel-size [2] --port [8043] --dtype bfloat16 --chat-template ./tool_chat_template_llama3.1_json.jinja
```
- 실행 시 "http://server_url:server_port/v1" url로 요청 가능
- test code : /model.py