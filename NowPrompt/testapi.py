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
    "Classify": os.path.join(engineering_dir, 'ClassifyPr.txt'),
    "Dash": os.path.join(engineering_dir, 'DashbPr.txt'),
    "onlyES": os.path.join(engineering_dir, 'onlyES.txt'),
    "onlyDB": os.path.join(engineering_dir, 'onlyMDB.txt'),
    "Detail": os.path.join(engineering_dir, 'DetailPr.txt'),
    "policy": os.path.join(engineering_dir, 'policy.txt')
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

# 프롬프트와 히스토리 초기화
histories = {name: [{"role": "system", "content": load_prompt(path)}] for name, path in prompt_files.items()}

# 대화 진행 루프
while True:
    question = input("\n질문: ")
    query = f"사용자의 자연어 질문: {question} 답변은 반드시 json 형식으로 나옵니다."

    # 사용자 질문 추가 (Classify 프롬프트에 대해 질문을 보냄)
    histories["Classify"].append({"role": "user", "content": query})

    # Classify 프롬프트에 대해 응답 생성
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=histories["Classify"],
        response_format={"type": "json_object"}
    )
    classify_response = response.choices[0].message.content
    print(classify_response, "\n")

    # classify_response에서 분류 결과 추출
    try:
        classify_data = json.loads(classify_response)
        classification_results = classify_data.get("topics", [])  # 'topics'에 여러 분류 값이 포함됨

        for classification_result in classification_results:
            # 분류 결과에 따른 프롬프트 설정
            if classification_result == "onlyES":
                target_prompt = "onlyES"
            elif classification_result == "onlyMDB":
                target_prompt = "onlyDB"
            elif classification_result == "DashbPr":
                target_prompt = "Dash"
            elif classification_result == "policy":
                target_prompt = "policy"
            else:
                target_prompt = "None"  # 예외 처리 시 기본값

            # 각 프롬프트에 사용자 질문 추가 및 응답 생성
            histories[target_prompt].append({"role": "user", "content": query})
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=histories[target_prompt],
                response_format={"type": "json_object"}
            )
            clean_answer = response.choices[0].message.content

            # onlyES와 onlyDB 응답을 저장하고 Detail 프롬프트 호출 추가
            if target_prompt == "onlyES":
                onlyES_response = clean_answer
                # Detail 프롬프트에도 저장
                histories["Detail"].append({"role": "user", "content": f"{query}\nES 응답: {onlyES_response}"})

            elif target_prompt == "onlyDB":
                onlyDB_response = clean_answer
                # Detail 프롬프트에도 저장
                histories["Detail"].append({"role": "user", "content": f"{query}\nDB 응답: {onlyDB_response}"})

            # Detail 프롬프트 호출 및 응답 생성
            if target_prompt in ["onlyES", "onlyDB"]:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=histories["Detail"],
                    response_format={"type": "json_object"}
                )
                detail_answer = response.choices[0].message.content
                histories["Detail"].append({"role": "assistant", "content": detail_answer})
                

            # 히스토리 관리 (최대 10개 유지)
            if len(histories[target_prompt]) > 10:
                histories[target_prompt].pop(1)
            histories[target_prompt].append({"role": "assistant", "content": clean_answer})

            # 응답 출력
            try:
                response_json = json.loads(clean_answer)
                print(f"{target_prompt}:\n", json.dumps(response_json, indent=4, ensure_ascii=False))
            except json.JSONDecodeError:
                print(f"{target_prompt}:\n", clean_answer)
            
            # Detail 응답 출력
            if target_prompt in ["onlyES", "onlyDB"]:
                try:
                    response_json = json.loads(detail_answer)
                    print("Detail:\n", json.dumps(response_json, indent=4, ensure_ascii=False))
                except json.JSONDecodeError:
                    print("Detail:\n", detail_answer)

            # 히스토리 저장
            save_history(histories[target_prompt], history_files[target_prompt])
            save_history(histories["Detail"], history_files["Detail"])


    except json.JSONDecodeError:
        print("Classify 응답이 JSON 형식이 아닙니다:", classify_response)
