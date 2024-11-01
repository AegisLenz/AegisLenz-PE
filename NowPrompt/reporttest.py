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
    "report": os.path.join(engineering_dir, 'reportPr.txt')
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

# 응답 생성 및 출력
def generate_response(client, model, messages):
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content

# 응답 출력
def print_response(target_prompt, clean_answer):
    try:
        response_json = json.loads(clean_answer)
        print(f"{target_prompt}:\n", json.dumps(response_json, indent=4, ensure_ascii=False))
    except json.JSONDecodeError:
        print(f"{target_prompt}:\n", clean_answer)

# 히스토리 파일 저장 함수
def save_history(history, filename):
    with open(filename, "w", encoding="utf-8") as file:
        for entry in history:
            file.write(f"{entry['role']}: {entry['content']}\n")

# 히스토리 관리 함수
def manage_history(histories, key, max_length=10):
    if len(histories[key]) > max_length:
        # 오래된 항목 제거
        histories[key].pop(1)


# 프롬프트와 히스토리 초기화
histories = {name: [{"role": "system", "content": load_prompt(path)}] for name, path in prompt_files.items()}


attack_time =  "2024년 09월 18일 07:20 KST"
attack_type = "Exfiltration, Exfiltration Over Alternative Protocol" 
user_json_logs = '''
[
    {
        "eventVersion": "1.10",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDA5FCD6JGVWEKBUQ246",
            "arn": "arn:aws:iam::904233109931:user/user2",
            "accountId": "904233109931",
            "accessKeyId": "AKIA5FCD6JGV37C7ZMBY",
            "userName": "user2"
        },
        "eventTime": "2024-09-18T07:11:42Z",
        "eventSource": "s3.amazonaws.com",
        "eventName": "PutBucketPolicy",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "58.123.207.197",
        "userAgent": "[stratus-red-team_fc75fb55-eebc-451a-b796-c82e8a8d9304]",
        "requestParameters": {
            "bucketPolicy": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {
                            "AWS": "arn:aws:iam::193672423079:root"
                        },
                        "Action": [
                            "s3:GetObject",
                            "s3:GetBucketLocation",
                            "s3:ListBucket"
                        ],
                        "Resource": [
                            "arn:aws:s3:::stratus-red-team-bdbp-mduodsdrms/*",
                            "arn:aws:s3:::stratus-red-team-bdbp-mduodsdrms"
                        ]
                    }
                ]
            },
            "bucketName": "stratus-red-team-bdbp-mduodsdrms",
            "Host": "stratus-red-team-bdbp-mduodsdrms.s3.us-east-1.amazonaws.com",
            "policy": ""
        },
        "responseElements": null,
        "additionalEventData": {
            "SignatureVersion": "SigV4",
            "CipherSuite": "TLS_AES_128_GCM_SHA256",
            "bytesTransferredIn": 416,
            "AuthenticationMethod": "AuthHeader",
            "x-amz-id-2": "rLdeqGEXKtNiv6xX6aVdrB0PETweRjTqnGGB/fK8UALfZsdT0IJgxGD6qb+eIXLjhqU12bOolnw=",
            "bytesTransferredOut": 0
        },
        "requestID": "B8P6HW7P6J5E80BQ",
        "eventID": "a17db0df-2089-4366-9a4f-06b08ee22dc5",
        "readOnly": false,
        "resources": [
            {
                "accountId": "904233109931",
                "type": "AWS::S3::Bucket",
                "ARN": "arn:aws:s3:::stratus-red-team-bdbp-mduodsdrms"
            }
        ],
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "904233109931",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "stratus-red-team-bdbp-mduodsdrms.s3.us-east-1.amazonaws.com"
        }
    }
]
'''

# 동적 값을 삽입하여 최종 프롬프트 구성
prompt_text = histories["report"][0]['content']
report_prompt = prompt_text.format(
    attack_time=attack_time,
    attack_type=attack_type,
    logs=user_json_logs
)
# 사용자 질문 추가 (Classify 프롬프트에 대해 질문을 보냄)
histories["report"].append({"role": "user", "content": report_prompt})

# Classify 프롬프트에 대해 응답 생성
report_response = generate_response(client, "gpt-4o-mini", histories["report"])
print_response("생성된 공격 탐지 보고서", report_response)

histories["report"].append({"role": "assistant", "content": report_response})
save_history(histories["report"], history_files["report"])


    


