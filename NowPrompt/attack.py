# -*- coding: utf-8 -*-
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
    "ES": os.path.join(engineering_dir, 'onlyES.txt'),
    "DB": os.path.join(engineering_dir, 'onlyMDB.txt'),
    "Detail": os.path.join(engineering_dir, 'DetailPr.txt'),
    "Policy": os.path.join(engineering_dir, 'policy.txt'),
    "recom": os.path.join(engineering_dir, 'recomm.txt')
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

# 추천 질문 생성
def generate_response_recom(client, model, messages):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        presence_penalty=1.5
    )
    return response.choices[0].message.content

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

# 프롬프트와 히스토리 초기화
histories = {name: [{"role": "system", "content": load_prompt(path)}] for name, path in prompt_files.items()}

Tatic = "Execution"
base_query = f"AI 질의 : AWS 환경에서 발생한 공격이 MITRE ATTACK Tatic 중 {Tatic}일 때, 보안 관리자가 어떤 질문을 해야 하는지 추천 질문 만들어줘 "

report_text = ''' 
 ### 공격 탐지 보고서

- **공격 탐지 시간**: 2024년 09월 21일 08:20 KST
- **공격 유형 (Tactic, Technique)**: Execution, Command and Scripting Interpreter
- **공격 대상 (리소스들)**: EC2 인스턴스 (ID: i-01c646c4b28fcf780)

#### 공격 근거
로그 분석을 통해 몇 가지 이벤트가 감지되었으며, 이는 명확한 공격 징후로 해석됩니다. 다음은 세부 사항입니다:

1. **DescribeInstances 이벤트**:
   - 다수의 DescribeInstances 요청이 발생하고, 이는 특정 EC2 인스턴스에 대한 정보를 조회하는데 사용되었습니다.
   - 이벤트 발생 시간은 2024년 09월 21일 07:58:27, 07:58:25, 07:58:24 등으로 반복적으로 감지되었습니다. 이러한 빈번한 요청은 계정의 정보 수집을 나타내며, 공격자가 인프라를 스캐닝하는 악의적인 행위로 해석될 수 있습니다.

2. **StartInstances 이벤트**:
   - 2024년 09월 21일 07:58:24에 특별한 요청을 통해 EC2 인스턴스 (ID: i-01c646c4b28fcf780)를 시작하는 이벤트가 기록되었습니다. 이 이벤트는 서비스의 잠재적 중단을 초래할 수 있으며, 권한 없이 인스턴스를 시작하는 것도 공격 시나리오로 볼 수 있습니다.

3. **ModifyInstanceAttribute 이벤트**:
   - 같은 시간대에 발생한 ModifyInstanceAttribute 이벤트는 인스턴스의 사용자 데이터를 수정하는 작업을 내포하고 있습니다. 이는 인스턴스에 악성 스크립트를 주입할 수 있는 가능성을 나 타냅니다(사용자 데이터는 인스턴스 시작 시 실행되는 스크립트).

4. **StopInstances 이벤트**:
   - 2024년 09월 21일 07:58:08에 발생한 StopInstances 이벤트는 EC2 인스턴스를 중지하는 요 청을 실행하였습니다. 이 조치는 서비스 중단을 초래할 수 있으며, 공격자가 시스템을 제어하기 위한 행위로 판단될 수 있습니다.

이러한 이벤트들은 모두 동일한 사용자인 "attack_user_05"에 의해 발생하였으며, 이 사용자는  여러 작업을 통해 해당 EC2 인스턴스를 조작하고 정보를 수집하려는 의도가 분명합니다. 따라서 사용자의 활동은 공격자로 판단됩니다.

이상 징후를 바탕으로, 공격자가 보안 허점을 이용하여 EC2 인스턴스에 대한 통제를 시도하고 있다는 것을 강력히 시사합니다. 추가적인 조치와 모니터링이 필요합니다.
'''

attack_logs = '''

'''

# 이전에 생성된 모든 질문을 누적할 리스트 초기화
previous_questions = []

# 동적 값을 삽입하여 최종 프롬프트 구성
prompt_text = histories["recom"][0]['content']
report_prompt = prompt_text.format(
    Tatic=Tatic,
    report=report_text,
    logs=attack_logs
)



while True:
    
    follow_up_question = generate_follow_up_question(client, base_query, previous_questions)
    
    histories["recom"].append({"role": "assistant", "content": follow_up_question})

    print(f"추천 질문 3가지 : {follow_up_question} ")

    user_input = input("\n 3가지 질문 중 하나를 선택하세요. : ")

    # 선택한 질문 넣어주기
    user_query = f"사용자의 자연어 질문: {user_input} 답변은 반드시 json 형식으로 나옵니다."

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

            
