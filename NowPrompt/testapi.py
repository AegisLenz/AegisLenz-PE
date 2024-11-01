import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

# 환경 변수 로드 및 API 클라이언트 설정
load_dotenv()
api_key = os.getenv("OPEN_AI_SECRET_KEY")
client = OpenAI(api_key=api_key)

# 현재 스크립트 위치 기준으로 상대 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
engineering_dir = os.path.join(current_dir, 'Engineering')

# 파일 경로와 이름 정의
prompt_files = {
    "Classify": os.path.join(engineering_dir, 'ClassifyPr.txt'),
    "ES": os.path.join(engineering_dir, 'onlyES.txt'),
    "DB": os.path.join(engineering_dir, 'onlyMDB.txt'),
    "Detail": os.path.join(engineering_dir, 'DetailPr.txt'),
    "Policy": os.path.join(engineering_dir, 'policy.txt')
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

class Detail(BaseModel):
    explanation: str

# detail 응답 생성
def detail_summary(client, model, messages):
    completion = client.beta.chat.completions.parse(
        model=model,
        messages= messages,
        response_format=Detail,
    )
    return completion.choices[0].message.parsed


# 프롬프트와 히스토리 초기화
histories = {name: [{"role": "system", "content": load_prompt(path)}] for name, path in prompt_files.items()}

# 대화 진행 루프
while True:
    question = input("\n질문: ")
    query = f"사용자의 자연어 질문: {question} 답변은 반드시 json 형식으로 나옵니다."

    # 사용자 질문 추가 (Classify 프롬프트에 대해 질문을 보냄)
    histories["Classify"].append({"role": "user", "content": query})

    # Classify 프롬프트에 대해 응답 생성
    classify_response = generate_response(client, "gpt-4o-mini", histories["Classify"])

    print(classify_response, "\n")
    histories["Classify"].append({"role": "assistant", "content": classify_response})  


    # classify_response에서 분류 결과 추출
    try:
        classify_data = json.loads(classify_response)

        # 'topics' 키의 값을 직접 가져와 확인
        classification_result = classify_data.get("topics")  # 'topics'가 단일 값으로 가정
        
        # 분류 결과에 따른 프롬프트 설정
        if classification_result == "ES":
            target_prompt = "ES"
        elif classification_result == "DB":
            target_prompt = "DB"
        elif classification_result == "Policy":
            target_prompt = "Policy"
        else:
            target_prompt = "None"  # 기본값

        # 각 프롬프트에 사용자 질문 추가 및 응답 생성
        histories[target_prompt].append({"role": "user", "content": query})

        clean_answer = generate_response(client, "gpt-4o-mini", histories[target_prompt])

        # ES와 DB 응답을 저장하고 Detail 프롬프트 호출 추가
        if target_prompt == "ES":
            ES_response = clean_answer
            # Detail 프롬프트에도 저장
            histories["Detail"].append({"role": "user", "content": f"{query}\nES 응답: {ES_response}"})

        elif target_prompt == "DB":
            DB_response = clean_answer
            # Detail 프롬프트에도 저장
            histories["Detail"].append({"role": "user", "content": f"{query}\nDB 응답: {DB_response}"})

        # 응답 출력 (target 프롬프트)
        print_response(target_prompt, clean_answer)
    
        # 히스토리 관리 (최대 10개 유지)
        manage_history(histories, target_prompt)

        histories[target_prompt].append({"role": "assistant", "content": clean_answer})
        
        # Detail 프롬프트 호출 및 응답 생성
        if target_prompt in ["ES", "DB"]:
            
            #응답 생성
            detail_response = detail_summary(client, "gpt-4o-mini" , histories["Detail"])
            Explanation = detail_response.explanation
            # 응답 출력
            print("Detail설명")
            print(Explanation)
            
            # 히스토리 관리 (최대 10개 유지) - Detail
            manage_history(histories, "Detail")

            histories["Detail"].append({"role": "assistant", "content": Explanation})  

        # 히스토리 저장
        save_history(histories[target_prompt], history_files[target_prompt])
        save_history(histories["Detail"], history_files["Detail"])
        save_history(histories["Classify"], history_files["Classify"])
       
    except json.JSONDecodeError:
        print("Classify 응답이 JSON 형식이 아닙니다:", classify_response)


