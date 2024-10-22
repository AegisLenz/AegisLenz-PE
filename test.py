import asyncio
import aiofiles
from openai import OpenAI
from dotenv import load_dotenv
import logging
import os, json

load_dotenv()
api_key = os.getenv("OPEN_AI_SECRET_KEY")
client_text = OpenAI(api_key=api_key)
client = OpenAI(api_key=api_key)
client_result = OpenAI(api_key=api_key)

# 비동기로 파일 읽기
async def read_file_async(file_path):
    async with aiofiles.open(file_path, "r", encoding="utf-8") as file:
        return await file.read()

# 비동기로 파일 쓰기
async def write_file_async(file_path, content_list):
    async with aiofiles.open(file_path, "w", encoding="utf-8") as file:
        for entry in content_list:
            await file.write(f"{entry['role']}: {entry['content']}\n")

# 비동기로 파일 읽기
async def initialize_conversation_histories():
    global prompt_content_text, prompt_content, prompt_content_result
    prompt_content_text, prompt_content, prompt_content_result = await asyncio.gather(
        read_file_async("DetailPr.txt"),
        read_file_async("firstPT.txt"),
        read_file_async("ResultPr.txt")
    )

conversation_history_text = []
conversation_history = []
conversation_history_result = []

# 비동기로 대화 기록 저장
async def save_conversation_history_text():
    await write_file_async("conversation_history_text.txt", conversation_history_text)

async def save_conversation_history():
    await write_file_async("conversation_history.txt", conversation_history)

async def save_conversation_history_result():
    await write_file_async("conversation_history_result.txt", conversation_history_result)

# API 호출 비동기 처리 및 병렬 실행
async def get_responses(query_text, query, query_result):
    response_text_task = asyncio.to_thread(client_text.chat.completions.create,
        model="gpt-4o-mini",
        messages=conversation_history_text
    )
    response_task = asyncio.to_thread(client.chat.completions.create,
        model="gpt-4o-mini",
        messages=conversation_history,
        response_format={"type": "json_object"}
    )
    response_result_task = asyncio.to_thread(client_result.chat.completions.create,
        model="gpt-4o-mini",
        messages=conversation_history_result
    )

    # 세 가지 API 호출을 동시에 실행 (병렬 처리)
    response_text, response, response_result = await asyncio.gather(
        response_text_task, response_task, response_result_task
    )

    return response_text, response, response_result

async def main():
    # 비동기로 파일 읽기
    await initialize_conversation_histories()

    conversation_history_text.append({"role": "system", "content": prompt_content_text})
    conversation_history.append({"role": "system", "content": prompt_content})
    conversation_history_result.append({"role": "system", "content": prompt_content_result})

    while True:
        question = input("\n질문: ")
        query_text = f"사용자의 자연어 질문: {question} 답변은 반드시 텍스트만 반환하고, 한 단락만 반환합니다."
        query = f"사용자의 자연어 질문: {question} 답변은 json 형식으로 나옵니다."
        query_result = f"사용자의 자연어 질문: {question} 답변은 반드시 텍스트만 반환합니다."

        conversation_history_text.append({"role": "user", "content": query_text})
        conversation_history.append({"role": "user", "content": query})
        conversation_history_result.append({"role": "user", "content": query_result})

        if len(conversation_history_text) > 10:
            conversation_history_text.pop(1)
        if len(conversation_history) > 10:
            conversation_history.pop(1)
        if len(conversation_history_result) > 10:
            conversation_history_result.pop(1)

        # 비동기 API 호출 병렬 처리
        response_text, response, response_result = await get_responses(query_text, query, query_result)

        clean_answer_text = response_text.choices[0].message.content
        clean_answer = response.choices[0].message.content
        clean_answer_result = response_result.choices[0].message.content

        conversation_history_text.append({"role": "assistant", "content": clean_answer_text})
        conversation_history.append({"role": "assistant", "content": clean_answer})
        conversation_history_result.append({"role": "assistant", "content": clean_answer_result})

        # 비동기로 대화 기록을 파일에 저장 (병렬로 처리)
        await asyncio.gather(
            save_conversation_history_text(),
            save_conversation_history(),
            save_conversation_history_result()
        )

        # 비동기 print 처리
        print(clean_answer_text, "\n")

        try:
            response_json = json.loads(clean_answer)
            print(json.dumps(response_json, indent=4, ensure_ascii=False))
        except json.JSONDecodeError:
            print(clean_answer)

        print("\n", clean_answer_result)

# 비동기 루프 실행
if __name__ == "__main__":
    asyncio.run(main())
