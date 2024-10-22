from openai import OpenAI
from dotenv import load_dotenv
import logging
import os, json

load_dotenv()
api_key = os.getenv("OPEN_AI_SECRET_KEY")
client_text = OpenAI(api_key = api_key)
client = OpenAI(api_key = api_key)
client_result = OpenAI(api_key = api_key)


with open("DetailPr.txt", "r", encoding="utf-8") as file:
    prompt_content_text = file.read()

with open("firstPT.txt", "r", encoding="utf-8") as file:
    prompt_content = file.read()

with open("ResultPr.txt", "r", encoding="utf-8") as file:
    prompt_content_result = file.read()

conversation_history_text = [{"role": "system", "content": prompt_content_text}]
conversation_history = [{"role": "system", "content": prompt_content}]
conversation_history_result = [{"role": "system", "content": prompt_content_result}]


def save_conversation_history_text():
    with open("conversation_history_text.txt", "w", encoding="utf-8") as file:
        for entry in conversation_history_text:
            file.write(f"{entry['role']}: {entry['content']}\n")

def save_conversation_history():
    with open("conversation_history.txt", "w", encoding="utf-8") as file:
        for entry in conversation_history:
            file.write(f"{entry['role']}: {entry['content']}\n")

def save_conversation_history_result():
    with open("conversation_history_result.txt", "w", encoding="utf-8") as file:
        for entry in conversation_history_result:
            file.write(f"{entry['role']}: {entry['content']}\n")

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


    response_text = client_text.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation_history_text
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation_history,
        response_format={"type":"json_object"}
    )
    response_result = client_result.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation_history_result
    )
    
    clean_answer_text = response_text.choices[0].message.content
    clean_answer = response.choices[0].message.content
    clean_answer_result = response_result.choices[0].message.content

    #clean_answer = answer.replace("", "").replace("'''", "").replace('"', '').strip()
    conversation_history_text.append({"role": "assistant", "content": clean_answer_text})
    conversation_history.append({"role": "assistant", "content": clean_answer})
    conversation_history_result.append({"role": "assistant", "content": clean_answer_result})

    #print(clean_answer)
    # 대화 기록을 파일에 저장
    save_conversation_history_text()
    save_conversation_history()
    save_conversation_history_result()

    print(clean_answer_text, "\n")

    try:
        response_json = json.loads(clean_answer)
        print(json.dumps(response_json, indent=4, ensure_ascii=False))
    except json.JSONDecodeError:
        print(clean_answer)

    print("\n", clean_answer_result)