﻿# AegisLenz-PE
 프롬프트 엔지니어링 및 api 호출 코드


## 디렉토리 설명

- Backup : 백업용 코드 (단순 백업 용도)
- FirstPT : 1차 평가 발표 준비용
- NowPrompt : 현재 작업 프롬프트 (페르소나 세분화, 최신 버전)


## 파일 설명

### Backup
- ResultPr.txt : 쿼리 조회 결과 (더미 데이터) PE
- originprompt.txt : 최초 PE
- totalprompt.txt : ES 쿼리 + Dashboard 선택 PE
- totaltest.py : totalprompt 전용 api 호출 코드

### FirstPT
- PromptDash.txt : Dashboard 리스트만 반환하는 PE
- prompt.txt : 설명 + ES 쿼리 + Dashboard 리스트 반환 PE
- real_first.py : PromptDash + prompt 전용 api 호출 코드

### NowPrompt
- Engineering/DashbPr.txt : Dashboard만 json 반환 PE
- Engineering/DetailPr.txt : 설명만 json 반환 PE
- Engineering/PromptES.txt : ES 쿼리 + 설명 반환 PE (v1)
- Engineering/onlyES.txt : ES 쿼리만 json 반환 PE (v2 : v1과 통합 예정)
- asyntest.py : multi PE 비동기 처리한 api 호출 코드 (PE 파일들이 전 버전들과 섞여 있어 수정 예정)
- notasync.py : multi PE 비동기 처리 X api 호출 코드 (위와 동일)

