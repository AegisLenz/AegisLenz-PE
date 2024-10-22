from openai import OpenAI
from dotenv import load_dotenv
import os, json

load_dotenv()
api_key = os.getenv("OPEN_AI_SECRET_KEY")
client = OpenAI(api_key = api_key)

with open("prompt.txt", "r", encoding="utf-8") as file:
    prompt_content = file.read()
with open("PromptDash.txt", "r", encoding="utf-8") as file:
    prompt_content_D = file.read()

conversation_history_ES = [{"role": "system", "content": prompt_content}]
conversation_history_D = [{"role": "system", "content": prompt_content_D}]


while True:
    question = input("질문: ")
    query = f"사용자의 자연어 질문: {question} 처음엔 반드시 설명 한 단락을 텍스트로 반환합니다."
    query_D = f"사용자의 자연어 질문: {question} 답변은 반드시 python list 형식만 반환합니다"

    conversation_history_ES.append({"role": "user", "content": query})
    conversation_history_D.append({"role": "user", "content": query_D})

    if len(conversation_history_ES) > 10:
        conversation_history_ES.pop(1)
    if len(conversation_history_D) > 10:
        conversation_history_ES.pop(1)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation_history_ES
    )

    response_D = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation_history_D
    )
    
    clean_answer = response.choices[0].message.content
    clean_answer_D = response_D.choices[0].message.content

    #clean_answer = answer.replace("```", "").replace("'''", "").replace('"', '').strip()
    conversation_history_ES.append({"role": "assistant", "content": clean_answer})
    conversation_history_D.append({"role": "assistant", "content": clean_answer_D})

    try:
        response_json = json.loads(clean_answer)
        print(json.dumps(response_json, indent=4))
    except json.JSONDecodeError:
        print(clean_answer)
    
    print("\n", clean_answer_D)
    
