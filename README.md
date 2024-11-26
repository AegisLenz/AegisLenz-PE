# AegisLenz-PE
 프롬프트 엔지니어링 및 api 호출 코드


## 디렉토리 설명
- NowPrompt : 현재 작업 프롬프트 (페르소나 세분화, 최신 버전)


## 파일 설명
### Engineering
- ClassifyPr.txt : ES, DB, policy 분류 PE (PromptEngineering) / 반환 형식 : json
- DetailPr.txt : ES와 DB 쿼리에 대한 설명 PE / 반환 형식 : text
- onlyES.txt : ES 쿼리 반환 PE / 반환 형식 : json
- onlyMDB.txt : MongoDB 쿼리 반환 PE / 반환 형식 : json
- policy.txt : 정책 질의 PE / 반환 형식 : text
- recomm.txt : 추천 질문 처리 PE / 반환 형식 : text (큰따옴표로 세개 질의 구분) 
- reportPr.txt : 공격 보고서 작성 PE / 반환 형식 : markdown

### sample_data
- Existing_policy.json : 초기 정책
- Changed_policy.json : 최소정책 추천 로직을 통해 변경된 정책

### Variable
- recom.txt : recomm.txt 변수 값 저장 파일

### NowPrompt
- attack.py : 공격 탐지 시, 질문 생성 + 그 뒤 로직 코드
- function.py : 반복적으로 사용되는 함수 정리 (코드 단편화 용도)
- normal.py : 일반적인 상황에서 질의하는 로직 코드
- reporttest.py : 공격 보고서 작성 코드

