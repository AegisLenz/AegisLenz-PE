import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from function import prompt_files, load_prompt, save_history, generate_response, print_response, manage_history, text_response

# 환경 변수 로드 및 API 클라이언트 설정
load_dotenv()
api_key = os.getenv("OPEN_AI_SECRET_KEY")
client = OpenAI(api_key=api_key)

history_files = {name: f"history_{name}.txt" for name in prompt_files}   

# 프롬프트와 히스토리 초기화
histories = {name: [{"role": "system", "content": load_prompt(path)}] for name, path in prompt_files.items()}

# 대화 진행 루프
while True:
    question = input("\n질문: ")
    query = f"사용자의 자연어 질문: {question} 답변은 반드시 json 형식으로 나옵니다."

    # 사용자 질문 추가 (Classify 프롬프트에 대해 질문을 보냄)

    # Classify 프롬프트에 대해 응답 생성
    classify_response = generate_response(client, "gpt-4o-mini", [histories["Classify"][0], {"role": "user", "content": query}])

    print(classify_response, "\n")  

    # classify_response에서 분류 결과 추출
    classify_data = json.loads(classify_response)

    # 'topics' 키의 값을 직접 가져와 확인
    classification_result = classify_data.get("topics")  # 'topics'가 단일 값으로 가정
    
    # 분류 결과에 따른 프롬프트 설정

    # Detail 프롬프트 호출 및 응답 생성
    if classification_result in ["ES", "DB"]:
        # 각 프롬프트에 사용자 질문 추가 및 응답 생성
        histories[classification_result].append({"role": "user", "content": query})
        clean_answer = generate_response(client, "gpt-4o-mini", histories[classification_result])

        # 응답 출력 (target 프롬프트)
        print_response(classification_result, clean_answer)
        manage_history(histories, classification_result)

        histories[classification_result].append({"role": "assistant", "content": clean_answer})

        # Detail 프롬프트에도 저장
        histories["Detail"].append({"role": "user", "content": f"{query}\n{classification_result} 응답: {clean_answer}"})
        
        #응답 생성
        detail_response = text_response(client, "gpt-4o-mini" , histories["Detail"])
        # 응답 출력
        print_response("Detail", detail_response)

        # 히스토리 관리 (최대 10개 유지) - Detail
        manage_history(histories, "Detail")

        histories["Detail"].append({"role": "assistant", "content": detail_response})
    elif classification_result == "Normal": # 3개의 주제에 해당하지 않는 질문
        normal_response = text_response(client, "gpt-4o-mini", [{"role": "user", "content": question}])
        print(normal_response) 
        continue

    elif classification_result == "Policy":
        classification_result = classification_result
        histories[classification_result].append({"role": "user", "content": question})
        policy_answer = text_response(client, "gpt-4o-mini", histories[classification_result]) 

        # 응답 출력 (target 프롬프트)
        print_response(classification_result, policy_answer)

        # 히스토리 관리 (최대 10개 유지)
        manage_history(histories, classification_result)

        histories[classification_result].append({"role": "assistant", "content": policy_answer}) 

    # 히스토리 저장
    #save_history(histories[classification_result], history_files[classification_result])
    #save_history(histories["Detail"], history_files["Detail"])
    #save_history(histories["Classify"], history_files["Classify"])
