import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
from function import load_and_fill, prompt_files, load_prompt, save_history, generate_response, print_response, manage_history, text_response, load_json

# 환경 변수 로드 및 API 클라이언트 설정
load_dotenv()
api_key = os.getenv("OPEN_AI_SECRET_KEY")
client = OpenAI(api_key=api_key)


# 현재 날짜와 시간을 문자열로 가져오기
current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#history_files = {name: f"history_{name}.txt" for name in prompt_files}   
window = []
prompt_txt = {name: {"role": "system", "content": load_prompt(path)} for name, path in prompt_files.items()}

# 변수 대입
#prompt_txt["DB"] = {"role": "system", "content": load_and_fill(prompt_files["DB"], prompt_files["dbVB"])}

# 대화 진행 루프
while True:
    question = input("\n질문: ")
    query = f"현재 날짜와 시간은 {current_datetime}입니다. 이 시간에 맞춰서 작업을 진행해주세요. 사용자의 자연어 질문: {question} 답변은 반드시 json 형식으로 나옵니다."

    # Classify 프롬프트에 대해 응답 생성
    classify_response = generate_response(client, "gpt-4o-mini", [prompt_txt["Classify"], {"role": "user", "content": query}])
    print(classify_response, "\n")  

    # classify_response에서 분류 결과 추출
    classify_data = json.loads(classify_response)
    classification_result = classify_data.get("topics")  # 'topics'가 단일 값

    # Detail 프롬프트 호출 및 응답 생성
    if classification_result in ["ES", "DB"]:
        # 각 프롬프트에 사용자 질문 추가 및 응답 생성
        prompt = []
        prompt.append(prompt_txt[classification_result])
        prompt.append({"role": "user", "content": query})
        clean_answer = generate_response(client, "gpt-4o-mini", prompt)

        # json 응답 출력 (target 프롬프트)
        print_response(classification_result, clean_answer)

        prompt = []
        prompt.append(prompt_txt["Detail"])
        prompt.append({"role": "user", "content":  f"{query}\n{classification_result} 응답: {clean_answer}"})

        #설명 응답 생성
        detail_response = text_response(client, "gpt-4o-mini" , prompt)
        print_response("Detail", detail_response)

    elif classification_result == "Normal": # 3개의 주제에 해당하지 않는 질문
        normal_response = text_response(client, "gpt-4o-mini", [{"role": "user", "content": question}])
        print(normal_response) 

    elif classification_result == "Policy":
        
        policy = {}

        basedir = os.path.dirname(os.path.abspath(__file__)) 
        existing_policy_path = os.path.join(basedir, 'sample_data', 'Existing_policy.json')
        changed_policy_path = os.path.join(basedir, 'sample_data', 'Changed_policy.json')
        original_policy = load_json(existing_policy_path)
        least_privilege_policy = load_json(changed_policy_path)
       
        prompt = []
        policy_prompt_content = prompt_txt["Policy"]["content"].format(
            original_policy=json.dumps(original_policy, indent=2), 
            least_privilege_policy=json.dumps(least_privilege_policy, indent=2)
        )
        prompt.append({"role": "system", "content": policy_prompt_content})
        prompt.append({"role": "user", "content": question})
        policy_answer = text_response(client, "gpt-4o-mini", prompt)
        print(policy_answer)

