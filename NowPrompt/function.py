import os
import json

# 현재 스크립트 위치 기준으로 상대 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
engineering_dir = os.path.join(current_dir, 'Engineering')


# 파일 경로와 이름 정의
prompt_files = {
    "Classify": os.path.join(engineering_dir, 'ClassifyPr.txt'),
    "ES": os.path.join(engineering_dir, 'onlyES.txt'),
    "DB": os.path.join(engineering_dir, 'onlyMDB.txt'),
    "Detail": os.path.join(engineering_dir, 'DetailPr.txt'),
    "Policy": os.path.join(engineering_dir, 'policy.txt'),
    "report":os.path.join(engineering_dir, 'reportPr.txt'),
    "recom": os.path.join(engineering_dir, 'recomm.txt')
}

# 추천 질문 생성
def generate_response_recom(client, model, messages):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        presence_penalty=1.5
    )
    return response.choices[0].message.content

# 프롬프트 파일 읽기
def load_prompt(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

# 히스토리 파일 저장
def save_history(history, filename):
    with open(filename, "w", encoding="utf-8") as file:
        for entry in history:
            file.write(f"{entry['role']}: {entry['content']}\n")

# 응답 생성 
def generate_response(client, model, messages):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        response_format={"type": "json_object"}
    )
    return response.choices[0].message.content

# 응답 출력
def print_response(target_prompt, clean_answer):
    try:
        response_json = json.loads(clean_answer)
        print(f"{target_prompt}:\n", json.dumps(response_json, indent=4, ensure_ascii=False))
    except json.JSONDecodeError:
        print(f"{target_prompt}:\n", clean_answer)

# 히스토리 관리 함수
def manage_history(histories, key, max_length=10):
    if len(histories[key]) > max_length:
        histories[key].pop(1)

# detail 응답 생성
def text_response(client, model, messages):
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content