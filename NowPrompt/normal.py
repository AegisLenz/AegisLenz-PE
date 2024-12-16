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
    classify_data = json.loads(classify_response)
    print(classify_data, "\n")

    if "sub_questions" in classify_data:
        final_responses = {}
        prior_answer = None
        prior_question = None

        for sub_question in classify_data["sub_questions"]:
            topic = sub_question["topics"]
            question = ""

            if prior_answer:
                question += f"\n 이전 질문: {prior_question}\n 이전 응답 데이터: {prior_answer} \n 반드시 이전 응답 데이터를 반영해서 다음 질문을 해결하세요."
            
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

        prompt = []
        prompt.append(prompt_txt["Detail"])
        prompt.append({"role": "user", "content":  f"{final_responses}"})

        #설명 응답 생성
        detail_response = text_response(client, "gpt-4o-mini" , prompt)
        print_response("Detail", detail_response)

    #Dash_response = generate_response(client, "gpt-4o-mini", [prompt_txt["Dash"], {"role": "user", "content": query}])
    #print(Dash_response, "\n")  