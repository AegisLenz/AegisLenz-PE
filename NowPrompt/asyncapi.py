import os
import json
import asyncio
import aiofiles  # 비동기 파일 I/O 라이브러리
from dotenv import load_dotenv
#from openai import OpenAI
from openai import AsyncOpenAI  # 비동기 OpenAI 클라이언트 사용

# 환경 변수 로드 및 API 클라이언트 설정
load_dotenv()
api_key = os.getenv("OPEN_AI_SECRET_KEY")
client = AsyncOpenAI(api_key=api_key)

# 현재 스크립트 위치 기준으로 상대 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
engineering_dir = os.path.join(current_dir, 'Engineering')

# 파일 경로와 이름 정의
prompt_files = {
    "Classify": os.path.join(engineering_dir, 'ClassifyPr.txt'),
    "Dash": os.path.join(engineering_dir, 'DashbPr.txt'),
    "ES": os.path.join(engineering_dir, 'onlyES.txt'),
    "DB": os.path.join(engineering_dir, 'onlyMDB.txt'),
    "Detail": os.path.join(engineering_dir, 'DetailPr.txt'),
    "policy": os.path.join(engineering_dir, 'policy.txt')
}
history_files = {name: f"history_{name}.txt" for name in prompt_files}

# 비동기 프롬프트 파일 읽기
async def load_prompt(file_path):
    async with aiofiles.open(file_path, "r", encoding="utf-8") as file:
        return await file.read()

# 비동기 히스토리 파일 저장
async def save_history(history, filename):
    async with aiofiles.open(filename, "w", encoding="utf-8") as file:
        for entry in history:
            await file.write(f"{entry['role']}: {entry['content']}\n")

# 프롬프트와 히스토리 초기화
async def initialize_histories():
    return {name: [{"role": "system", "content": await load_prompt(path)}] for name, path in prompt_files.items()}

# 비동기 응답 생성 및 출력
async def generate_response(client, model, messages):
    response = await client.chat.completions.create(
        model=model,
        messages=messages,
        response_format={"type": "json_object"}
    )
    return response.choices[0].message.content

# 비동기 응답 출력
async def print_response(target_prompt, clean_answer):
    try:
        response_json = json.loads(clean_answer)
        print(f"{target_prompt}:\n", json.dumps(response_json, indent=4, ensure_ascii=False))
    except json.JSONDecodeError:
        print(f"{target_prompt}:\n", clean_answer)

# 비동기 히스토리 파일 저장 함수
async def save_history(history, filename):
    async with aiofiles.open(filename, "w", encoding="utf-8") as file:
        for entry in history:
            await file.write(f"{entry['role']}: {entry['content']}\n")

# 비동기 히스토리 관리 함수
async def manage_history(histories, key, max_length=10):
    if len(histories[key]) > max_length:
        # 오래된 항목 제거
        histories[key].pop(1)

# 메인 함수 정의
async def main():
    histories = await initialize_histories()
    # 대화 진행 루프
    while True:
        question = input("\n질문: ")
        query = f"사용자의 자연어 질문: {question} 답변은 반드시 json 형식으로 나옵니다."

        # 사용자 질문 추가 (Classify 프롬프트에 대해 질문을 보냄)
        histories["Classify"].append({"role": "user", "content": query})

        # Classify 프롬프트에 대해 응답 생성
        classify_response = await generate_response(client, "gpt-4o-mini", histories["Classify"])
        print(classify_response, "\n")

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
            elif classification_result == "Dash":
                target_prompt = "Dash"
            elif classification_result == "policy":
                target_prompt = "policy"
            else:
                target_prompt = "None"  # 기본값

            histories[target_prompt].append({"role": "user", "content": query})
            
            # (비동기) 각 프롬프트에 사용자 질문 추가 및 응답 생성
            clean_answer_task = asyncio.create_task(generate_response(client, "gpt-4o-mini", histories[target_prompt]))

            
            # ES와 DB 응답을 저장하고 Detail 프롬프트 호출 추가
            if target_prompt == "ES":
                clean_answer = await clean_answer_task
                ES_response = clean_answer
                # Detail 프롬프트에도 저장
                histories["Detail"].append({"role": "user", "content": f"{query}\nES 응답: {ES_response}"})

            elif target_prompt == "DB":
                clean_answer = await clean_answer_task
                DB_response = clean_answer
                # Detail 프롬프트에도 저장
                histories["Detail"].append({"role": "user", "content": f"{query}\nDB 응답: {DB_response}"})
            
            # 비동기 응답 출력 target_prompt
            await print_response(target_prompt, clean_answer) # clean_answer를 await로 가져옴

            # (비동기) 히스토리 관리 호출
            await manage_history(histories, target_prompt)

            histories[target_prompt].append({"role": "assistant", "content": clean_answer})
            
            # Detail 응답 출력
            if target_prompt in ["ES", "DB"]:
                
                histories["Detail"].append({"role": "user", "content": query})

                # (비동기) 사용자 detail 질문 추가 및 응답 생성
                detail_answer = await generate_response(client, "gpt-4o-mini", histories["Detail"])  # await 사용                
        
                # 비동기 응답 출력
                await print_response("Detail", detail_answer) # detail_answer를 await으로 가져옴
        
                # (비동기) 히스토리 관리 호출
                await manage_history(histories, "Detail")

                histories["Detail"].append({"role": "assistant", "content": detail_answer}) 

            
            # Dash 응답 출력
            if target_prompt in ["ES", "DB","policy"]:
                   
                histories["Dash"].append({"role": "user", "content": query})
                
                # (비동기) 사용자 대시보드 질문 추가 및 응답 생성
                dash_answer = await generate_response(client, "gpt-4o-mini", histories["Dash"]) #await 사용
        
                # 비동기 응답 출력
                await print_response("Dash", dash_answer) #dash_answer를 await으로 가져옴

                # (비동기) 히스토리 관리 호출
                await manage_history(histories, "Dash")

                histories["Dash"].append({"role": "assistant", "content": dash_answer}) 

            # 비동기 히스토리 저장 호출
            await save_history(histories[target_prompt], history_files[target_prompt])
            await save_history(histories["Dash"], history_files["Dash"])
            await save_history(histories["Detail"], history_files["Detail"])
                            
        except json.JSONDecodeError:
            print("Classify 응답이 JSON 형식이 아닙니다:", classify_response)

# 프로그램 실행
if __name__ == "__main__":
    asyncio.run(main())
