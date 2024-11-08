# AegisLenz-PE
 프롬프트 엔지니어링 및 api 호출 코드


## 디렉토리 설명
- NowPrompt : 현재 작업 프롬프트 (페르소나 세분화, 최신 버전)


## 파일 설명
### NowPrompt
- Engineering/ClassifyPr.txt : ES, DB, policy 분류하여 json 반환 PE
- Engineering/DetailPr.txt : 설명만 json 반환 PE
- Engineering/onlyES.txt : ES 쿼리만 json 반환 PE
- Engineering/onlyMDB.txt : MongoDB 쿼리만 json 반환 PE
- Engineering/policy.txt : 정책관련 질의 처리 텍스트 반환 PE
- Engineering/recomm.txt : 추천 질문 처리 텍스트 반환 (큰따옴표로 세개 질의 구분) PE 
- Engineering/reportPr.txt : 공격 보고서 작성 markdown 형식 반환 PE
- attack.py : 공격 탐지 시, 질문 생성 + 그 뒤 로직 코드
- normal.py : 일반적인 상황에서 질의하는 로직 코드
- reporttest.py : 공격 보고서 작성 코드

