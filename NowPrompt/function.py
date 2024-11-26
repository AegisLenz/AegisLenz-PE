import os
import json

# 현재 스크립트 위치 기준으로 상대 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
engineering_dir = os.path.join(current_dir, 'Engineering')
variable_dir = os.path.join(current_dir, 'Variable')
sample_data_dir = os.path.join(current_dir, 'sample_data')

# 파일 경로와 이름 정의
prompt_files = {
    "Classify": os.path.join(engineering_dir, 'ClassifyPr.txt'),
    "ES": os.path.join(engineering_dir, 'onlyES.txt'),
    "DB": os.path.join(engineering_dir, 'onlyMDB.txt'),
    "Detail": os.path.join(engineering_dir, 'DetailPr.txt'),
    "Policy": os.path.join(engineering_dir, 'policy.txt'),
    "report":os.path.join(engineering_dir, 'reportPr.md'),
    "recom": os.path.join(engineering_dir, 'recomm.txt'),
    "reportVB" : os.path.join(variable_dir, 'report.txt'),
    "recomVB" : os.path.join(variable_dir, 'recom.txt')
}

# 추천 질문 생성
def generate_response_recom(client, model, messages):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        presence_penalty=1.5
    )
    return response.choices[0].message.content

def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {e}")
        return None
    
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

# text 응답 생성
def text_response(client, model, messages):
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content

# 변수 파일을 불러오고 템플릿 파일에 대입하는 함수
def load_and_fill(template_path, variables_path):
    # 변수 파일 읽기 및 실행
    variables = {}
    with open(variables_path, "r", encoding="utf-8") as file:
        exec(file.read(), variables)

    # 템플릿 파일 읽기
    with open(template_path, "r", encoding="utf-8") as template_file:
        content = template_file.read()

    # 자리 표시자를 변수 값으로 대체하여 반환
    return content.format(**variables)
