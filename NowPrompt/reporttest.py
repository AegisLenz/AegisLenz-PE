import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from function import load_and_fill, prompt_files, load_prompt, save_history, print_response, manage_history, text_response

# 환경 변수 로드 및 API 클라이언트 설정
load_dotenv()
api_key = os.getenv("OPEN_AI_SECRET_KEY")
client = OpenAI(api_key=api_key)


prompt_txt = {name: {"role": "system", "content": load_prompt(path)} for name, path in prompt_files.items()}

# 템플릿과 변수를 채워 최종 보고서 생성
prompt_txt["report"] = {"role": "system", "content": load_and_fill(prompt_files["report"], prompt_files["reportVB"])}

# Classify 프롬프트에 대해 응답 생성
report_response = text_response(client, "gpt-4o-mini", [prompt_txt["report"]])
print_response("생성된 공격 탐지 보고서", report_response)




    


