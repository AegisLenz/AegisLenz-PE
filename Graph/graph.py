import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from function import prompt_files, load_prompt, print_response, text_response

# 환경 변수 로드 및 API 클라이언트 설정
load_dotenv()
api_key = os.getenv("OPEN_AI_SECRET_KEY")
client = OpenAI(api_key=api_key)

# 템플릿 파일 로드
template_content = load_prompt(prompt_files["graph"])  # 파일 내용을 읽어옴

logs = """"
[
    {
        "eventVersion": "1.09",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDA47CRYYD4YEGOHKGTD",
            "arn": "arn:aws:iam::891377205497:user/xtsmr",
            "accountId": "891377205497",
            "accessKeyId": "AKIA47CRYYD45SPKWWWZ",
            "userName": "xtsmr"
        },
        "eventTime": "2024-09-13T05:35:02Z",
        "eventSource": "iam.amazonaws.com",
        "eventName": "UpdateAssumeRolePolicy",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "Boto3/1.35.15 md/Botocore#1.35.15 ua/2.0 os/macos#24.0.0 md/arch#arm64 lang/python#3.12.4 md/pyimpl#CPython cfg/retry-mode#adaptive Botocore/1.35.15",
        "requestParameters": {
            "roleName": "testrole",
            "policyDocument": "{\"Version\": \"2012-10-17\", \"Statement\": [{\"Effect\": \"Allow\", \"Principal\": {\"AWS\": [\"arn:aws:iam::891377205497:root\", \"arn:aws:iam::891377205497:user/xtsmr\"]}, \"Action\": \"sts:AssumeRole\"}]}"
        },
        "responseElements": null,
        "requestID": "6c406b9d-86e2-4165-9dd8-48583504ef1b",
        "eventID": "3cf583bd-8c4f-424d-8e38-b66b73eb155b",
        "readOnly": false,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "891377205497",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "iam.amazonaws.com"
        },
        "mitreAttackTactics": "TA0003 - Persistence",
        "mitreAttackTechniques": "T1098 - Account Manipulation"
    },
    {
        "eventVersion": "1.09",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDA47CRYYD4YEGOHKGTD",
            "arn": "arn:aws:iam::891377205497:user/xtsmr",
            "accountId": "891377205497",
            "accessKeyId": "AKIA47CRYYD45SPKWWWZ",
            "userName": "xtsmr"
        },
        "eventTime": "2024-09-13T05:35:01Z",
        "eventSource": "iam.amazonaws.com",
        "eventName": "GetRole",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "Boto3/1.35.15 md/Botocore#1.35.15 ua/2.0 os/macos#24.0.0 md/arch#arm64 lang/python#3.12.4 md/pyimpl#CPython cfg/retry-mode#adaptive Botocore/1.35.15 Resource",
        "requestParameters": {
            "roleName": "testrole"
        },
        "responseElements": null,
        "requestID": "8611f46c-b7b8-4a6a-9386-3e7f1aa7e95d",
        "eventID": "ec24d282-8edc-430f-aa4b-fbd535492789",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "891377205497",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "iam.amazonaws.com"
        },
        "mitreAttackTactics": "TA0007 - Discovery",
        "mitreAttackTechniques": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.09",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDA47CRYYD4YEGOHKGTD",
            "arn": "arn:aws:iam::891377205497:user/xtsmr",
            "accountId": "891377205497",
            "accessKeyId": "AKIA47CRYYD45SPKWWWZ",
            "userName": "xtsmr"
        },
        "eventTime": "2024-09-13T05:35:00Z",
        "eventSource": "iam.amazonaws.com",
        "eventName": "UpdateAssumeRolePolicy",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "Boto3/1.35.15 md/Botocore#1.35.15 ua/2.0 os/macos#24.0.0 md/arch#arm64 lang/python#3.12.4 md/pyimpl#CPython cfg/retry-mode#adaptive Botocore/1.35.15",
        "errorCode": "UnmodifiableEntityException",
        "errorMessage": "Cannot perform the operation on the protected role 'AWSServiceRoleForTrustedAdvisor' - this role is only modifiable by AWS",
        "requestParameters": {
            "roleName": "AWSServiceRoleForTrustedAdvisor",
            "policyDocument": "{\"Version\": \"2012-10-17\", \"Statement\": [{\"Effect\": \"Allow\", \"Principal\": {\"Service\": \"trustedadvisor.amazonaws.com\", \"AWS\": \"arn:aws:iam::891377205497:user/xtsmr\"}, \"Action\": \"sts:AssumeRole\"}]}"
        },
        "responseElements": null,
        "requestID": "4969b644-2699-47e9-b65a-983c38bf8f6f",
        "eventID": "f6a51a5a-e2df-4f25-9f64-f3583ed1266f",
        "readOnly": false,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "891377205497",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "iam.amazonaws.com"
        },
        "mitreAttackTactics": "TA0003 - Persistence",
        "mitreAttackTechniques": "T1098 - Account Manipulation"
    },
    {
        "eventVersion": "1.09",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDA47CRYYD4YEGOHKGTD",
            "arn": "arn:aws:iam::891377205497:user/xtsmr",
            "accountId": "891377205497",
            "accessKeyId": "AKIA47CRYYD45SPKWWWZ",
            "userName": "xtsmr"
        },
        "eventTime": "2024-09-13T05:34:59Z",
        "eventSource": "iam.amazonaws.com",
        "eventName": "UpdateAssumeRolePolicy",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "Boto3/1.35.15 md/Botocore#1.35.15 ua/2.0 os/macos#24.0.0 md/arch#arm64 lang/python#3.12.4 md/pyimpl#CPython cfg/retry-mode#adaptive Botocore/1.35.15",
        "errorCode": "UnmodifiableEntityException",
        "errorMessage": "Cannot perform the operation on the protected role 'AWSServiceRoleForSupport' - this role is only modifiable by AWS",
        "requestParameters": {
            "roleName": "AWSServiceRoleForSupport",
            "policyDocument": "{\"Version\": \"2012-10-17\", \"Statement\": [{\"Effect\": \"Allow\", \"Principal\": {\"Service\": \"support.amazonaws.com\", \"AWS\": \"arn:aws:iam::891377205497:user/xtsmr\"}, \"Action\": \"sts:AssumeRole\"}]}"
        },
        "responseElements": null,
        "requestID": "8330ba25-c8df-41e0-848f-bf9f3eb9df16",
        "eventID": "63fc3467-9fab-4b40-b7ce-b8d2ba19d1b8",
        "readOnly": false,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "891377205497",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "iam.amazonaws.com"
        },
        "mitreAttackTactics": "TA0003 - Persistence",
        "mitreAttackTechniques": "T1098 - Account Manipulation"
    },
    {
        "eventVersion": "1.09",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDA47CRYYD4YEGOHKGTD",
            "arn": "arn:aws:iam::891377205497:user/xtsmr",
            "accountId": "891377205497",
            "accessKeyId": "AKIA47CRYYD45SPKWWWZ",
            "userName": "xtsmr"
        },
        "eventTime": "2024-09-13T05:34:59Z",
        "eventSource": "iam.amazonaws.com",
        "eventName": "GetRole",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "Boto3/1.35.15 md/Botocore#1.35.15 ua/2.0 os/macos#24.0.0 md/arch#arm64 lang/python#3.12.4 md/pyimpl#CPython cfg/retry-mode#adaptive Botocore/1.35.15 Resource",
        "requestParameters": {
            "roleName": "AWSServiceRoleForTrustedAdvisor"
        },
        "responseElements": null,
        "requestID": "de96d8f8-959e-45fa-8df2-b9d0e113f330",
        "eventID": "7cfa6bdf-f2f6-4f3c-acf0-222139477bca",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "891377205497",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "iam.amazonaws.com"
        },
        "mitreAttackTactics": "TA0007 - Discovery",
        "mitreAttackTechniques": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.09",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDA47CRYYD4YEGOHKGTD",
            "arn": "arn:aws:iam::891377205497:user/xtsmr",
            "accountId": "891377205497",
            "accessKeyId": "AKIA47CRYYD45SPKWWWZ",
            "userName": "xtsmr"
        },
        "eventTime": "2024-09-13T05:34:57Z",
        "eventSource": "iam.amazonaws.com",
        "eventName": "GetRole",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "Boto3/1.35.15 md/Botocore#1.35.15 ua/2.0 os/macos#24.0.0 md/arch#arm64 lang/python#3.12.4 md/pyimpl#CPython cfg/retry-mode#adaptive Botocore/1.35.15 Resource",
        "requestParameters": {
            "roleName": "AWSServiceRoleForSupport"
        },
        "responseElements": null,
        "requestID": "9d1f4ad3-82a0-4a3a-88e5-de681e4fd071",
        "eventID": "23c6dd4c-50ab-4dc7-a11c-7853a11fb39e",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "891377205497",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "iam.amazonaws.com"
        },
        "mitreAttackTactics": "TA0007 - Discovery",
        "mitreAttackTechniques": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.08",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDA47CRYYD4YEGOHKGTD",
            "arn": "arn:aws:iam::891377205497:user/xtsmr",
            "accountId": "891377205497",
            "accessKeyId": "AKIA47CRYYD45SPKWWWZ",
            "userName": "xtsmr"
        },
        "eventTime": "2024-09-13T05:34:55Z",
        "eventSource": "sts.amazonaws.com",
        "eventName": "GetCallerIdentity",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "Boto3/1.35.15 md/Botocore#1.35.15 ua/2.0 os/macos#24.0.0 md/arch#arm64 lang/python#3.12.4 md/pyimpl#CPython cfg/retry-mode#adaptive Botocore/1.35.15",
        "requestParameters": null,
        "responseElements": null,
        "requestID": "07755c64-75f6-4b58-b176-438bf435c019",
        "eventID": "af7f0afd-fbdf-4dfe-9fa4-c5d15705988a",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "891377205497",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "sts.amazonaws.com"
        },
        "mitreAttackTactics": "TA0007 - Discovery",
        "mitreAttackTechniques": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.09",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDA47CRYYD4YEGOHKGTD",
            "arn": "arn:aws:iam::891377205497:user/xtsmr",
            "accountId": "891377205497",
            "accessKeyId": "AKIA47CRYYD45SPKWWWZ",
            "userName": "xtsmr"
        },
        "eventTime": "2024-09-13T05:34:54Z",
        "eventSource": "iam.amazonaws.com",
        "eventName": "ListGroups",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "Boto3/1.35.15 md/Botocore#1.35.15 ua/2.0 os/macos#24.0.0 md/arch#arm64 lang/python#3.12.4 md/pyimpl#CPython cfg/retry-mode#adaptive Botocore/1.35.15",
        "requestParameters": null,
        "responseElements": null,
        "requestID": "caa14467-74ae-4483-ba9b-657f87aa0764",
        "eventID": "1720a451-e194-4df4-9bab-38322ec156de",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "891377205497",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "iam.amazonaws.com"
        },
        "mitreAttackTactics": "TA0007 - Discovery",
        "mitreAttackTechniques": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.09",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDA47CRYYD4YEGOHKGTD",
            "arn": "arn:aws:iam::891377205497:user/xtsmr",
            "accountId": "891377205497",
            "accessKeyId": "AKIA47CRYYD45SPKWWWZ",
            "userName": "xtsmr"
        },
        "eventTime": "2024-09-13T05:34:54Z",
        "eventSource": "iam.amazonaws.com",
        "eventName": "ListPolicies",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "Boto3/1.35.15 md/Botocore#1.35.15 ua/2.0 os/macos#24.0.0 md/arch#arm64 lang/python#3.12.4 md/pyimpl#CPython cfg/retry-mode#adaptive Botocore/1.35.15",
        "requestParameters": {
            "scope": "Local",
            "onlyAttached": false
        },
        "responseElements": null,
        "requestID": "6aade758-a046-48a6-befe-21ac1b2d6226",
        "eventID": "af6c99d3-0c3d-42a9-a697-165551bef6da",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "891377205497",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "iam.amazonaws.com"
        },
        "mitreAttackTactics": "TA0007 - Discovery",
        "mitreAttackTechniques": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.09",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDA47CRYYD4YEGOHKGTD",
            "arn": "arn:aws:iam::891377205497:user/xtsmr",
            "accountId": "891377205497",
            "accessKeyId": "AKIA47CRYYD45SPKWWWZ",
            "userName": "xtsmr"
        },
        "eventTime": "2024-09-13T05:34:53Z",
        "eventSource": "iam.amazonaws.com",
        "eventName": "ListRoles",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "Boto3/1.35.15 md/Botocore#1.35.15 ua/2.0 os/macos#24.0.0 md/arch#arm64 lang/python#3.12.4 md/pyimpl#CPython cfg/retry-mode#adaptive Botocore/1.35.15",
        "requestParameters": null,
        "responseElements": null,
        "requestID": "59df3c0f-ec78-40e5-819c-b9d068e25efd",
        "eventID": "b7a80793-a518-4edf-bfe0-9cd07e8859a7",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "891377205497",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "iam.amazonaws.com"
        },
        "mitreAttackTactics": "TA0007 - Discovery",
        "mitreAttackTechniques": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.09",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDA47CRYYD4YEGOHKGTD",
            "arn": "arn:aws:iam::891377205497:user/xtsmr",
            "accountId": "891377205497",
            "accessKeyId": "AKIA47CRYYD45SPKWWWZ",
            "userName": "xtsmr"
        },
        "eventTime": "2024-09-13T05:34:53Z",
        "eventSource": "iam.amazonaws.com",
        "eventName": "ListUsers",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "Boto3/1.35.15 md/Botocore#1.35.15 ua/2.0 os/macos#24.0.0 md/arch#arm64 lang/python#3.12.4 md/pyimpl#CPython cfg/retry-mode#adaptive Botocore/1.35.15",
        "requestParameters": null,
        "responseElements": null,
        "requestID": "44217c30-929e-4bb2-9d43-063b255ad538",
        "eventID": "e44e817f-33dd-42c4-8904-a37917b4ec2f",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "891377205497",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "iam.amazonaws.com"
        },
        "mitreAttackTactics": "TA0007 - Discovery",
        "mitreAttackTechniques": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.09",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDA47CRYYD4ZK4QW73V5",
            "arn": "arn:aws:iam::891377205497:user/lookupIam",
            "accountId": "891377205497",
            "accessKeyId": "AKIA47CRYYD4RRSTPACL",
            "userName": "lookupIam"
        },
        "eventTime": "2024-09-13T05:34:52Z",
        "eventSource": "iam.amazonaws.com",
        "eventName": "ListAttachedRolePolicies",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "APN/1.0 HashiCorp/1.0 Terraform/1.5.7 (+https://www.terraform.io) terraform-provider-aws/5.67.0 (+https://registry.terraform.io/providers/hashicorp/aws) m/C aws-sdk-go-v2/1.30.5 os/macos lang/go#1.22.6 md/GOOS#darwin md/GOARCH#arm64 api/iam#1.35.2",
        "requestParameters": {
            "roleName": "testrole"
        },
        "responseElements": null,
        "requestID": "ebaca5df-3c76-47d2-80be-5d683d8bbf1d",
        "eventID": "8945a98f-dd82-46de-9bd8-caf70a12789e",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "891377205497",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "iam.amazonaws.com"
        },
        "mitreAttackTactics": "TA0007 - Discovery",
        "mitreAttackTechniques": "T1087 - Account Discovery"
    }
]"""

# 템플릿에서 직접 변수 치환
template_content = template_content.format(**locals())

prompt_txt = {"graph": {"role": "system", "content": template_content}}

# Classify 프롬프트에 대해 응답 생성
report_response = text_response(client, "gpt-4o-mini", [prompt_txt["graph"]])

# '"""'와 'javascript'를 제외한 응답 생성
filtered_response = report_response.replace('"""', '').replace('javascript', '')

# 필터링된 응답 출력
print_response("그래프 데이터", filtered_response)

