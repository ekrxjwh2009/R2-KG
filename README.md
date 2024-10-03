
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
