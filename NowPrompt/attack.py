# -*- coding: utf-8 -*-
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
from function import dash_response, load_and_fill, prompt_files, load_prompt, save_history, generate_response, print_response, manage_history, text_response, generate_response_recom, load_json

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
base_query = f"AI 질의 : AWS 환경에서 발생한 공격이 MITRE ATTACK Tatic 중 {Tatic}일 때, 보안 관리자가 어떤 질문을 해야 하는지 추천 질문 만들어주세요. "

# 이전에 생성된 모든 질문을 누적할 리스트 초기화
previous_questions = []

# 변수 대입
histories["recom"] = [{"role": "system", "content": load_and_fill(prompt_files["recom"], prompt_files["recomVB"])}]
#prompt_txt["DB"] = {"role": "system", "content": load_and_fill(prompt_files["DB"], prompt_files["dbVB"])}

# 대화 진행 루프
while True:
    
    follow_up_question = generate_follow_up_question(client, base_query, previous_questions)
    
    histories["recom"].append({"role": "assistant", "content": follow_up_question})

    print(f"추천 질문 3가지 : {follow_up_question} ")

    question = input("\n 3가지 질문 중 하나를 선택하세요. : ")
    
    # 선택한 질문 넣어주기
    query = f"현재 날짜와 시간은 {current_datetime}입니다. 이 시간에 맞춰서 작업을 진행해주세요. 사용자 자연어 질문: {question} 답변은 반드시 json 형식으로 나옵니다."

    histories["recom"].append({"role": "user", "content": f"사용자가 선택한 자연어 질문: {question}"})

    # Classify 프롬프트에 대해 응답 생성
    classify_response = generate_response(client, "gpt-4o-mini", [prompt_txt["Classify"], {"role": "user", "content": question}])
    Dash_response = dash_response(client, "gpt-4o-mini", [prompt_txt["Dash"], {"role": "user", "content": question}])
    
    print(Dash_response, "\n")

    # classify_response에서 분류 결과 추출
    classify_data = json.loads(classify_response)
    print(classify_data, "\n")
    neededDetail = True
    if "sub_questions" in classify_data:
        final_responses = {}
        prior_answer = None
        prior_question = None

        for sub_question in classify_data["sub_questions"]:
            topic = sub_question["topics"]
            question = ""

            if prior_answer:
                #이전 질문에 대한 응답: {prior_return}
                question += f"\n 이전 질문: {prior_question}\n 이전 프롬프트의 응답: {prior_answer} \n 반드시 이전 응답 데이터를 반영해서 다음 질문을 해결하세요."
            
            question += sub_question["question"]
            print(topic, question)

            # 주제에 맞는 프롬프트 실행
            if topic in ["ES", "DB"]:
                prompt = []
                prompt.append(prompt_txt[topic])
                prompt.append({"role": "user", "content": question})
                sub_response = generate_response(client, "gpt-4o-mini", prompt)
            
            elif topic == "Normal": 
                sub_response = text_response(client, "gpt-4o-mini", [{"role": "user", "content": question}])
                neededDetail = False

            elif topic == "Policy":
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
                sub_response = text_response(client, "gpt-4o-mini", prompt)
                neededDetail = False

            if topic not in final_responses:
                final_responses[topic] = []
            if(topic in ['ES', 'DB']):
                final_responses[topic].append(json.loads(sub_response))
            else:
                final_responses[topic].append(sub_response)

            prior_question = sub_question['question']
            prior_answer = sub_response

        # 복합 질문 결과 출력
        print(json.dumps(final_responses, indent=2, ensure_ascii=False))

        if neededDetail:
            prompt = []
            prompt.append(prompt_txt["Detail"])
            prompt.append({"role": "user", "content":  f"{final_responses}"})

            #설명 응답 생성
            detail_response = text_response(client, "gpt-4o-mini" , prompt)
            print_response("Detail", detail_response)

    append_recom = "위 사용자가 선택한 질의와 응답을 참고해서 다시 추천 질문 세개를 만들어주세요. 이전과 절대 중복되지 않는 **다양한 주제**로 세 줄 질문을 생성해 주세요."
    histories["recom"].append({"role": "assistant", "content": append_recom})
    save_history(histories["recom"], history_files["recom"])


    

            
