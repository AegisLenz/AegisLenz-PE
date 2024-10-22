from openai import OpenAI
from dotenv import load_dotenv
import logging
import os, json

load_dotenv()
api_key = os.getenv("OPEN_AI_SECRET_KEY")
client = OpenAI(api_key = api_key)

with open("prompt2.txt", "r", encoding="utf-8") as file:
    prompt_content = file.read()

conversation_history = [{"role": "system", "content": prompt_content}]

def save_conversation_history():
    with open("conversation_history.txt", "w", encoding="utf-8") as file:
        for entry in conversation_history:
            file.write(f"{entry['role']}: {entry['content']}\n")


while True:
    question = input("\n질문: ")
    query = f"사용자의 자연어 질문: {question} "
    conversation_history.append({"role": "user", "content": query})

    if len(conversation_history) > 10:
        conversation_history.pop(1)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation_history,
        #response_format={"type":"json_object"},
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "response_format",
                "schema": {
                    "type": "object",
                    "properties":{
                        "Detail": {"type": "string", "description":"Specific description of the response"},
                        "Dashboard": {"type": "array","items":{"type":"string"}, "description": "detail of Dashboard"},
                        "Elastic_query": {"type": "object", "description": "Elastic query for checking normal logs"},
                        "MongoDB_query": {"type": "object", "description": "MongoDB query for checking attack logs"}
                    },
                    "required": ["Detail","Dashboard"],
                    "additionalProperties": False
                },
                "strict": True      
            }
        }
    )
    
    clean_answer = response.choices[0].message.content
    #clean_answer = answer.replace("```", "").replace("'''", "").replace('"', '').strip()
    conversation_history.append({"role": "assistant", "content": clean_answer})
    #print(clean_answer)
    # 대화 기록을 파일에 저장
    save_conversation_history()

    try:
        response_json = json.loads(clean_answer)
        print(json.dumps(response_json, indent=4, ensure_ascii=False))
    except json.JSONDecodeError:
        print(clean_answer)
