import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# 환경 변수 로드 및 API 클라이언트 설정
load_dotenv()
api_key = os.getenv("OPEN_AI_SECRET_KEY")
client = OpenAI(api_key=api_key)

# 현재 스크립트 위치 기준으로 상대 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
engineering_dir = os.path.join(current_dir, 'Engineering')

# 파일 경로와 이름 정의
prompt_files = {
    "report": os.path.join(engineering_dir, 'reportPr.txt')
}
history_files = {name: f"history_{name}.txt" for name in prompt_files}

# 프롬프트 파일 읽기
def load_prompt(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

# 히스토리 파일 저장
def save_history(history, filename):
    with open(filename, "w", encoding="utf-8") as file:
        for entry in history:
            file.write(f"{entry['role']}: {entry['content']}\n")

# 응답 생성 및 출력
def generate_response(client, model, messages):
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content

# 응답 출력
def print_response(target_prompt, clean_answer):
    try:
        response_json = json.loads(clean_answer)
        print(f"{target_prompt}:\n", json.dumps(response_json, indent=4, ensure_ascii=False))
    except json.JSONDecodeError:
        print(f"{target_prompt}:\n", clean_answer)

# 히스토리 파일 저장 함수
def save_history(history, filename):
    with open(filename, "w", encoding="utf-8") as file:
        for entry in history:
            file.write(f"{entry['role']}: {entry['content']}\n")

# 히스토리 관리 함수
def manage_history(histories, key, max_length=10):
    if len(histories[key]) > max_length:
        # 오래된 항목 제거
        histories[key].pop(1)


# 프롬프트와 히스토리 초기화
histories = {name: [{"role": "system", "content": load_prompt(path)}] for name, path in prompt_files.items()}


attack_time =  "2024년 09월 18일 07:20 KST"
attack_type = "Exfiltration, Exfiltration Over Alternative Protocol" 
user_json_logs = ''' '''

# 동적 값을 삽입하여 최종 프롬프트 구성
prompt_text = histories["report"][0]['content']
report_prompt = prompt_text.format(
    attack_time=attack_time,
    attack_type=attack_type,
    logs=user_json_logs
)
# 사용자 질문 추가 (Classify 프롬프트에 대해 질문을 보냄)
histories["report"].append({"role": "user", "content": report_prompt})

# Classify 프롬프트에 대해 응답 생성
report_response = generate_response(client, "gpt-4o-mini", histories["report"])
print_response("생성된 공격 탐지 보고서", report_response)

histories["report"].append({"role": "assistant", "content": report_response})
save_history(histories["report"], history_files["report"])


    


