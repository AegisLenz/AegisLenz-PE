import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from function import load_and_fill, prompt_files, load_prompt, save_history, print_response, manage_history, text_response

# 환경 변수 로드 및 API 클라이언트 설정
load_dotenv()
api_key = os.getenv("OPEN_AI_SECRET_KEY")
client = OpenAI(api_key=api_key)


# 템플릿 파일 로드
template_content = load_prompt(prompt_files["report"])  # 파일 내용을 읽어옴

First = input("\n수정: ")
Second = input("\n수정: ")
Third = input("\n수정: ")
Fourth = input("\n수정: ")

attack_time =  "2024년 09월 21일 08:20 KST"
attack_type = "Execution, Command and Scripting Interpreter" 
logs = """ 

"""

# 템플릿에서 직접 변수 치환
template_content = template_content.format(**locals())

prompt_txt = {"report": {"role": "system", "content": template_content}}

# Classify 프롬프트에 대해 응답 생성
report_response = text_response(client, "gpt-4o-mini", [prompt_txt["report"]])
print_response("생성된 공격 탐지 보고서", report_response)




    


