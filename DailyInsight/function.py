import os
import json

# 현재 파일의 절대 경로
current_file = os.path.abspath(__file__)

# 현재 파일이 있는 디렉토리의 상위 디렉토리를 가져옴
current_dir = os.path.dirname(current_file)  # 현재 파일 디렉토리
parent_dir = os.path.dirname(current_dir)    # 상위 디렉토리

# NowPrompt 및 Engineering 디렉토리 경로 설정
NowPrompt_dir = os.path.join(parent_dir, 'NowPrompt')
engineering_dir = os.path.join(NowPrompt_dir, 'Engineering')

# 파일 경로와 이름 정의
prompt_files = {
    "daily": os.path.join(engineering_dir, 'dailyinsight.txt')
}

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

# text 응답 생성
def text_response(client, model, messages):
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content

# 히스토리 파일 저장
def save_history(history, filename, append=False):
    """
    히스토리를 파일에 저장합니다.
    append=True일 경우 내용을 기존 파일에 추가합니다.
    """
    mode = "a" if append else "w"  # append 모드 설정
    try:
        with open(filename, mode, encoding="utf-8") as file:
            for entry in history:
                file.write(f"{entry['role']}: {entry['content']}\n")
        print(f"{filename}에 데이터 저장 완료.")
    except Exception as e:
        print(f"{filename} 저장 중 오류 발생: {e}")


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
