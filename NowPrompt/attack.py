# -*- coding: utf-8 -*-
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
from function import load_and_fill, prompt_files, load_prompt, save_history, generate_response, print_response, manage_history, text_response, generate_response_recom, load_json

# 환경 변수 로드 및 API 클라이언트 설정
load_dotenv()
api_key = os.getenv("OPEN_AI_SECRET_KEY")
client = OpenAI(api_key=api_key)

# 현재 날짜와 시간을 문자열로 가져오기
current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 추천 질문 생성 함수 (중복 방지, 한 번에 세개씩)
def generate_follow_up_question(client, prompt, previous_questions):
    # 중복 방지 지시사항 추가
    
    prompt_text  = f"{prompt}\n 이전과 중복되지 않는 세 줄 질문을 생성해 주세요. 출력은 반드시 세개의 간단한 질문으로만 주세요."

    while True:
        
        
        # 모델로부터 응답 생성 (3가지 질문을 하나의 응답으로 받음)
        response = generate_response_recom(client, "gpt-4o-mini", histories["recom"])
        histories["recom"].append({"role": "user", "content": prompt_text })

        # 생성된 질문을 줄 단위로 나눔
        new_questions = response.splitlines()

        # 중복되지 않는 질문만 선택
        unique_questions = [question.strip() for question in new_questions if question.strip() and question not in previous_questions]

        # 중복되지 않는 질문을 모두 반환
        if unique_questions:
            # 중복되지 않는 질문을 previous_questions에 누적하여 저장하고, 하나의 문자열로 조합해서 반환
            previous_questions.extend(unique_questions[:3])
            return '\n'.join([f'{question}' for question in unique_questions[:3]])


# recom용
history_files = {name: f"history_{name}.txt" for name in prompt_files}
histories = {name: [{"role": "system", "content": load_prompt(path)}] for name, path in prompt_files.items()}

prompt_txt = {name: {"role": "system", "content": load_prompt(path)} for name, path in prompt_files.items()}

Tatic = "Execution"
base_query = f"AI 질의 : AWS 환경에서 발생한 공격이 MITRE ATTACK Tatic 중 {Tatic}일 때, 보안 관리자가 어떤 질문을 해야 하는지 추천 질문 만들어줘 "

# 이전에 생성된 모든 질문을 누적할 리스트 초기화
previous_questions = []

# 변수 대입
histories["recom"] = [{"role": "system", "content": load_and_fill(prompt_files["recom"], prompt_files["recomVB"])}]
prompt_txt["DB"] = {"role": "system", "content": load_and_fill(prompt_files["DB"], prompt_files["dbVB"])}

# 대화 진행 루프

while True:
    
    follow_up_question = generate_follow_up_question(client, base_query, previous_questions)
    
    histories["recom"].append({"role": "assistant", "content": follow_up_question})

    print(f"추천 질문 3가지 : {follow_up_question} ")

    question = input("\n 3가지 질문 중 하나를 선택하세요. : ")

    # 선택한 질문 넣어주기
    query = f"현재 날짜와 시간은 {current_datetime}입니다. 이 시간에 맞춰서 작업을 진행해주세요. 사용자의 자연어 질문: {question} 답변은 반드시 json 형식으로 나옵니다."

    histories["recom"].append({"role": "user", "content": query})

    # Classify 프롬프트에 대해 응답 생성
    classify_response = generate_response(client, "gpt-4o-mini", [prompt_txt["Classify"], {"role": "user", "content": query}])

    print(classify_response, "\n")

    # classify_response에서 분류 결과 추출
    classify_data = json.loads(classify_response)

    # 'topics' 키의 값을 직접 가져와 확인
    classification_result = classify_data.get("topics")  # 'topics'가 단일 값
    
    # 분류 결과에 따른 프롬프트 설정

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

        histories["recom"].append({"role": "assistant", "content": f"응답:{detail_response}"})
    
    elif classification_result == "Normal": # 3개의 주제에 해당하지 않는 질문
        normal_response = text_response(client, "gpt-4o-mini", [{"role": "user", "content": question}])
        histories["recom"].append({"role": "assistant", "content": f"응답:{normal_response}"})
        print(normal_response) 
        continue        

    elif classification_result == "Policy":
        policy = {}
       #original_policy = policy.get("original_policy")
        original_policy = load_json(prompt_files["ExistingPolicy"])
        least_privilege_policy = load_json(prompt_files["ChangedPolicy"])

       #least_privilege_policy = policy.get("least_privilege_policy")
        prompt = []
        policy_prompt_content = prompt_txt["Policy"]["content"].format(
            original_policy=json.dumps(original_policy, indent=2), 
            least_privilege_policy=json.dumps(least_privilege_policy, indent=2)
        )
        prompt.append({"role": "system", "content": policy_prompt_content})
        prompt.append({"role": "user", "content": question})
        policy_answer = text_response(client, "gpt-4o-mini", prompt)
        print(policy_answer)
        
        histories["recom"].append({"role": "assistant", "content": policy_answer})

    append_recom = "위 사용자 질의와 응답을 참고해서 다시 추천 질문 세개를 만들어줘"
    histories["recom"].append({"role": "assistant", "content": append_recom})
    save_history(histories["recom"], history_files["recom"])

            
