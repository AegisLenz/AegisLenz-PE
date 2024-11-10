# -*- coding: utf-8 -*-
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
from function import load_and_fill, prompt_files, load_prompt, save_history, generate_response, print_response, manage_history, text_response, generate_response_recom

# 환경 변수 로드 및 API 클라이언트 설정
load_dotenv()
api_key = os.getenv("OPEN_AI_SECRET_KEY")
client = OpenAI(api_key=api_key)

history_files = {name: f"history_{name}.txt" for name in prompt_files}

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

# 프롬프트와 히스토리 초기화
histories = {name: [{"role": "system", "content": load_prompt(path)}] for name, path in prompt_files.items()}

Tatic = "Execution"
base_query = f"AI 질의 : AWS 환경에서 발생한 공격이 MITRE ATTACK Tatic 중 {Tatic}일 때, 보안 관리자가 어떤 질문을 해야 하는지 추천 질문 만들어줘 "

# 이전에 생성된 모든 질문을 누적할 리스트 초기화
previous_questions = []

# 변수 대입
histories["recom"] = [{"role": "system", "content": load_and_fill(prompt_files["recom"], prompt_files["recomVB"])}]
histories["DB"] = [{"role": "system", "content": load_and_fill(prompt_files["DB"], prompt_files["dbVB"])}]



while True:
    
    follow_up_question = generate_follow_up_question(client, base_query, previous_questions)
    
    histories["recom"].append({"role": "assistant", "content": follow_up_question})

    print(f"추천 질문 3가지 : {follow_up_question} ")

    user_input = input("\n 3가지 질문 중 하나를 선택하세요. : ")

    # 선택한 질문 넣어주기
    user_query = f"현재 날짜와 시간은 {current_datetime}입니다. 이 시간에 맞춰서 작업을 진행해주세요. 사용자의 자연어 질문: {user_input} 답변은 반드시 json 형식으로 나옵니다."

    # 사용자 질문 추가 (Classify 프롬프트에 대해 질문을 보냄)
    histories["Classify"].append({"role": "user", "content": user_query})
    histories["recom"].append({"role": "user", "content": user_query})

    # Classify 프롬프트에 대해 응답 생성
    classify_response = generate_response(client, "gpt-4o-mini", histories["Classify"])

    print(classify_response, "\n")
    histories["Classify"].append({"role": "assistant", "content": classify_response})  

    # classify_response에서 분류 결과 추출
    classify_data = json.loads(classify_response)

    # 'topics' 키의 값을 직접 가져와 확인
    classification_result = classify_data.get("topics")  # 'topics'가 단일 값으로 가정
    
    # 분류 결과에 따른 프롬프트 설정

    # Detail 프롬프트 호출 및 응답 생성
    if classification_result in ["ES", "DB"]:
        
        target_prompt = classification_result
        # 각 프롬프트에 사용자 질문 추가 및 응답 생성
        histories[target_prompt].append({"role": "user", "content": user_query})
        clean_answer = generate_response(client, "gpt-4o-mini", histories[target_prompt])

        # 응답 출력 (target 프롬프트)
        print_response(target_prompt, clean_answer)
        manage_history(histories, target_prompt)
        histories[target_prompt].append({"role": "assistant", "content": clean_answer})

        if target_prompt in ["ES", "DB"]:
            histories["Detail"].append({"role": "user", "content": f"{user_query}\n{target_prompt} 응답: {clean_answer}"})
            #응답 생성
            detail_response = text_response(client, "gpt-4o-mini" , histories["Detail"])
            # 응답 출력
            print_response("Detail", detail_response)

            # 히스토리 관리 (최대 10개 유지) - Detail
            manage_history(histories, "Detail")

            histories["Detail"].append({"role": "assistant", "content": detail_response})
            histories["recom"].append({"role": "assistant", "content": f"응답:{detail_response}"})
    
    elif classification_result == "Normal": # 3개의 주제에 해당하지 않는 질문
        normal_response = text_response(client, "gpt-4o-mini", [{"role": "user", "content": user_input}])
        histories["recom"].append({"role": "assistant", "content": f"응답:{normal_response}"})
        print(normal_response) 
        continue        

    elif classification_result == "Policy":
        
        target_prompt = classification_result
        histories[target_prompt].append({"role": "user", "content": user_input})
        policy_answer = text_response(client, "gpt-4o-mini", histories[target_prompt]) 

        # 응답 출력 (target 프롬프트)
        print_response(target_prompt, policy_answer)
        manage_history(histories, target_prompt)

        histories[target_prompt].append({"role": "assistant", "content": policy_answer})
        histories["recom"].append({"role": "assistant", "content": policy_answer})

    append_recom = "위 사용자 질의와 응답을 참고해서 다시 추천 질문 세개를 만들어줘"
    histories["recom"].append({"role": "assistant", "content": append_recom})


    # 히스토리 저장
    save_history(histories[target_prompt], history_files[target_prompt])
    save_history(histories["Detail"], history_files["Detail"])
    save_history(histories["Classify"], history_files["Classify"])
    save_history(histories["recom"], history_files["recom"])

            
