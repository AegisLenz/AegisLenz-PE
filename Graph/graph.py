import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from function import prompt_files, load_prompt, print_response, generate_response

# 환경 변수 로드 및 API 클라이언트 설정
load_dotenv()
api_key = os.getenv("OPEN_AI_SECRET_KEY")
client = OpenAI(api_key=api_key)

# 템플릿 파일 로드
template_content = load_prompt(prompt_files["graph"])  # 파일 내용을 읽어옴

logs = """[
    {
        "eventVersion": "1.09",
        "eventVersion": "1.09",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDA47CRYYD4VWJGA4YTZ",
            "arn": "arn:aws:iam::891377205497:user/dwbcf",
            "accountId": "891377205497",
            "accessKeyId": "AKIA47CRYYD44ONNPRVY",
            "userName": "dwbcf"
        },
        "eventTime": "2024-09-13T05:37:25Z",
        "eventSource": "iam.amazonaws.com",
        "eventName": "UpdateAssumeRolePolicy",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "Boto3/1.35.15 md/Botocore#1.35.15 ua/2.0 os/macos#24.0.0 md/arch#arm64 lang/python#3.12.4 md/pyimpl#CPython cfg/retry-mode#adaptive Botocore/1.35.15",
        "userAgent": "Boto3/1.35.15 md/Botocore#1.35.15 ua/2.0 os/macos#24.0.0 md/arch#arm64 lang/python#3.12.4 md/pyimpl#CPython cfg/retry-mode#adaptive Botocore/1.35.15",
        "requestParameters": {
            "roleName": "testrole",
            "policyDocument": "{\"Version\": \"2012-10-17\", \"Statement\": [{\"Effect\": \"Allow\", \"Principal\": {\"AWS\": [\"arn:aws:iam::891377205497:root\", \"arn:aws:iam::891377205497:user/dwbcf\"]}, \"Action\": \"sts:AssumeRole\"}]}"
        },
        "responseElements": null,
        "requestID": "0800dc3f-006f-4511-927b-a8fe270fc906",
        "eventID": "275fe406-abba-46c3-9ef1-e0bf3fdbdd0b",
        "readOnly": false,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "891377205497",
        "recipientAccountId": "891377205497",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "iam.amazonaws.com"
            "clientProvidedHostHeader": "iam.amazonaws.com"
        },
        "mitreAttackTactics": "TA0003 - Persistence",
        "mitreAttackTechniques": "T1098 - Account Manipulation"
        "mitreAttackTactics": "TA0003 - Persistence",
        "mitreAttackTechniques": "T1098 - Account Manipulation"
    },
    {
        "eventVersion": "1.09",
        "eventVersion": "1.09",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDA47CRYYD4VWJGA4YTZ",
            "arn": "arn:aws:iam::891377205497:user/dwbcf",
            "accountId": "891377205497",
            "accessKeyId": "AKIA47CRYYD44ONNPRVY",
            "userName": "dwbcf"
        },
        "eventTime": "2024-09-13T05:37:24Z",
        "eventSource": "iam.amazonaws.com",
        "eventName": "GetRole",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "Boto3/1.35.15 md/Botocore#1.35.15 ua/2.0 os/macos#24.0.0 md/arch#arm64 lang/python#3.12.4 md/pyimpl#CPython cfg/retry-mode#adaptive Botocore/1.35.15 Resource",
        "userAgent": "Boto3/1.35.15 md/Botocore#1.35.15 ua/2.0 os/macos#24.0.0 md/arch#arm64 lang/python#3.12.4 md/pyimpl#CPython cfg/retry-mode#adaptive Botocore/1.35.15 Resource",
        "requestParameters": {
            "roleName": "testrole"
            "roleName": "testrole"
        },
        "responseElements": null,
        "requestID": "602bca20-42a1-4ed2-ba0c-097e23d1c71f",
        "eventID": "16d8d48b-1248-4035-b2f7-7895d0fd2304",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "891377205497",
        "recipientAccountId": "891377205497",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "iam.amazonaws.com"
            "clientProvidedHostHeader": "iam.amazonaws.com"
        },
        "mitreAttackTactics": "TA0007 - Discovery",
        "mitreAttackTechniques": "T1087 - Account Discovery"
        "mitreAttackTactics": "TA0007 - Discovery",
        "mitreAttackTechniques": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.09",
        "eventVersion": "1.09",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDA47CRYYD4VWJGA4YTZ",
            "arn": "arn:aws:iam::891377205497:user/dwbcf",
            "accountId": "891377205497",
            "accessKeyId": "AKIA47CRYYD44ONNPRVY",
            "userName": "dwbcf"
        },
        "eventTime": "2024-09-13T05:37:23Z",
        "eventSource": "iam.amazonaws.com",
        "eventName": "UpdateAssumeRolePolicy",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "Boto3/1.35.15 md/Botocore#1.35.15 ua/2.0 os/macos#24.0.0 md/arch#arm64 lang/python#3.12.4 md/pyimpl#CPython cfg/retry-mode#adaptive Botocore/1.35.15",
        "errorCode": "UnmodifiableEntityException",
        "errorMessage": "Cannot perform the operation on the protected role 'AWSServiceRoleForTrustedAdvisor' - this role is only modifiable by AWS",
        "userAgent": "Boto3/1.35.15 md/Botocore#1.35.15 ua/2.0 os/macos#24.0.0 md/arch#arm64 lang/python#3.12.4 md/pyimpl#CPython cfg/retry-mode#adaptive Botocore/1.35.15",
        "errorCode": "UnmodifiableEntityException",
        "errorMessage": "Cannot perform the operation on the protected role 'AWSServiceRoleForTrustedAdvisor' - this role is only modifiable by AWS",
        "requestParameters": {
            "roleName": "AWSServiceRoleForTrustedAdvisor",
            "policyDocument": "{\"Version\": \"2012-10-17\", \"Statement\": [{\"Effect\": \"Allow\", \"Principal\": {\"Service\": \"trustedadvisor.amazonaws.com\", \"AWS\": \"arn:aws:iam::891377205497:user/dwbcf\"}, \"Action\": \"sts:AssumeRole\"}]}"
        },
        "responseElements": null,
        "requestID": "a77480cc-ed28-4efa-99ac-4a1cc2dcc810",
        "eventID": "dbac0f68-9166-402f-bd4c-8fd7fbe90cab",
        "readOnly": false,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "891377205497",
        "recipientAccountId": "891377205497",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "iam.amazonaws.com"
            "clientProvidedHostHeader": "iam.amazonaws.com"
        },
        "mitreAttackTactics": "TA0003 - Persistence",
        "mitreAttackTechniques": "T1098 - Account Manipulation"
        "mitreAttackTactics": "TA0003 - Persistence",
        "mitreAttackTechniques": "T1098 - Account Manipulation"
    },
    {
        "eventVersion": "1.09",
        "eventVersion": "1.09",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDA47CRYYD4VWJGA4YTZ",
            "arn": "arn:aws:iam::891377205497:user/dwbcf",
            "accountId": "891377205497",
            "accessKeyId": "AKIA47CRYYD44ONNPRVY",
            "userName": "dwbcf"
        },
        "eventTime": "2024-09-13T05:37:22Z",
        "eventSource": "iam.amazonaws.com",
        "eventName": "GetRole",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "Boto3/1.35.15 md/Botocore#1.35.15 ua/2.0 os/macos#24.0.0 md/arch#arm64 lang/python#3.12.4 md/pyimpl#CPython cfg/retry-mode#adaptive Botocore/1.35.15 Resource",
        "userAgent": "Boto3/1.35.15 md/Botocore#1.35.15 ua/2.0 os/macos#24.0.0 md/arch#arm64 lang/python#3.12.4 md/pyimpl#CPython cfg/retry-mode#adaptive Botocore/1.35.15 Resource",
        "requestParameters": {
            "roleName": "AWSServiceRoleForTrustedAdvisor"
            "roleName": "AWSServiceRoleForTrustedAdvisor"
        },
        "responseElements": null,
        "requestID": "195b9024-0f42-4e87-8777-df50cce8e8e8",
        "eventID": "2cc50876-3e5f-441d-8608-fe4e951eebb5",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "891377205497",
        "recipientAccountId": "891377205497",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "iam.amazonaws.com"
            "clientProvidedHostHeader": "iam.amazonaws.com"
        },
        "mitreAttackTactics": "TA0007 - Discovery",
        "mitreAttackTechniques": "T1087 - Account Discovery"
        "mitreAttackTactics": "TA0007 - Discovery",
        "mitreAttackTechniques": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.09",
        "eventVersion": "1.09",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDA47CRYYD4VWJGA4YTZ",
            "arn": "arn:aws:iam::891377205497:user/dwbcf",
            "accountId": "891377205497",
            "accessKeyId": "AKIA47CRYYD44ONNPRVY",
            "userName": "dwbcf"
        },
        "eventTime": "2024-09-13T05:37:22Z",
        "eventSource": "iam.amazonaws.com",
        "eventName": "UpdateAssumeRolePolicy",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "Boto3/1.35.15 md/Botocore#1.35.15 ua/2.0 os/macos#24.0.0 md/arch#arm64 lang/python#3.12.4 md/pyimpl#CPython cfg/retry-mode#adaptive Botocore/1.35.15",
        "errorCode": "UnmodifiableEntityException",
        "errorMessage": "Cannot perform the operation on the protected role 'AWSServiceRoleForSupport' - this role is only modifiable by AWS",
        "requestParameters": {
            "roleName": "AWSServiceRoleForSupport",
            "policyDocument": "{\"Version\": \"2012-10-17\", \"Statement\": [{\"Effect\": \"Allow\", \"Principal\": {\"Service\": \"support.amazonaws.com\", \"AWS\": \"arn:aws:iam::891377205497:user/dwbcf\"}, \"Action\": \"sts:AssumeRole\"}]}"
        },
        "responseElements": null,
        "requestID": "fbdffe89-703c-4fe3-a3e7-c8b5c869007b",
        "eventID": "376601c1-7bfd-4cc9-bb10-4dfaea54ed98",
        "readOnly": false,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "891377205497",
        "recipientAccountId": "891377205497",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "iam.amazonaws.com"
            "clientProvidedHostHeader": "iam.amazonaws.com"
        },
        "mitreAttackTactics": "TA0003 - Persistence",
        "mitreAttackTechniques": "T1098 - Account Manipulation"
    },
    {
        "eventVersion": "1.09",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDA47CRYYD4VWJGA4YTZ",
            "arn": "arn:aws:iam::891377205497:user/dwbcf",
            "accountId": "891377205497",
            "accessKeyId": "AKIA47CRYYD44ONNPRVY",
            "userName": "dwbcf"
        },
        "eventTime": "2024-09-13T05:37:21Z",
        "eventSource": "iam.amazonaws.com",
        "eventName": "GetRole",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "Boto3/1.35.15 md/Botocore#1.35.15 ua/2.0 os/macos#24.0.0 md/arch#arm64 lang/python#3.12.4 md/pyimpl#CPython cfg/retry-mode#adaptive Botocore/1.35.15 Resource",
        "requestParameters": {
            "roleName": "AWSServiceRoleForSupport"
        },
        "responseElements": null,
        "requestID": "5048dae2-edc5-42c5-ad1a-9dedd4f96cb1",
        "eventID": "8d3af40f-eb5b-410f-8786-e5f15c14f04b",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "891377205497",
        "recipientAccountId": "891377205497",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "iam.amazonaws.com"
        },
        "mitreAttackTactics": "TA0007 - Discovery",
        "mitreAttackTechniques": "T1087 - Account Discovery"
        "mitreAttackTactics": "TA0007 - Discovery",
        "mitreAttackTechniques": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.08",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDA47CRYYD4VWJGA4YTZ",
            "arn": "arn:aws:iam::891377205497:user/dwbcf",
            "accountId": "891377205497",
            "accessKeyId": "AKIA47CRYYD44ONNPRVY",
            "userName": "dwbcf"
        },
        "eventTime": "2024-09-13T05:37:20Z",
        "eventSource": "sts.amazonaws.com",
        "eventName": "GetCallerIdentity",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "Boto3/1.35.15 md/Botocore#1.35.15 ua/2.0 os/macos#24.0.0 md/arch#arm64 lang/python#3.12.4 md/pyimpl#CPython cfg/retry-mode#adaptive Botocore/1.35.15",
        "requestParameters": null,
        "userAgent": "Boto3/1.35.15 md/Botocore#1.35.15 ua/2.0 os/macos#24.0.0 md/arch#arm64 lang/python#3.12.4 md/pyimpl#CPython cfg/retry-mode#adaptive Botocore/1.35.15",
        "requestParameters": null,
        "responseElements": null,
        "requestID": "fa4780fe-3c31-428f-88de-25776675a486",
        "eventID": "0e470741-7aae-4bbe-ac46-d9838d76f98c",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "891377205497",
        "recipientAccountId": "891377205497",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "sts.amazonaws.com"
        },
        "mitreAttackTactics": "TA0007 - Discovery",
        "mitreAttackTechniques": "T1087 - Account Discovery"
        "mitreAttackTactics": "TA0007 - Discovery",
        "mitreAttackTechniques": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.09",
        "eventVersion": "1.09",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDA47CRYYD4VWJGA4YTZ",
            "arn": "arn:aws:iam::891377205497:user/dwbcf",
            "accountId": "891377205497",
            "accessKeyId": "AKIA47CRYYD44ONNPRVY",
            "userName": "dwbcf"
        },
        "eventTime": "2024-09-13T05:37:18Z",
        "eventSource": "iam.amazonaws.com",
        "eventName": "ListGroups",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "Boto3/1.35.15 md/Botocore#1.35.15 ua/2.0 os/macos#24.0.0 md/arch#arm64 lang/python#3.12.4 md/pyimpl#CPython cfg/retry-mode#adaptive Botocore/1.35.15",
        "requestParameters": null,
        "responseElements": null,
        "requestID": "a6666796-88b7-402d-9234-4e185db9e043",
        "eventID": "5ac818ea-9221-43fe-a608-ec869433c169",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "891377205497",
        "recipientAccountId": "891377205497",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "iam.amazonaws.com"
            "clientProvidedHostHeader": "iam.amazonaws.com"
        },
        "mitreAttackTactics": "TA0007 - Discovery",
        "mitreAttackTechniques": "T1087 - Account Discovery"
        "mitreAttackTactics": "TA0007 - Discovery",
        "mitreAttackTechniques": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.09",
        "eventVersion": "1.09",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDA47CRYYD4VWJGA4YTZ",
            "arn": "arn:aws:iam::891377205497:user/dwbcf",
            "accountId": "891377205497",
            "accessKeyId": "AKIA47CRYYD44ONNPRVY",
            "userName": "dwbcf"
        },
        "eventTime": "2024-09-13T05:37:18Z",
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
        "requestID": "94e314de-4721-41aa-a342-bb380969996c",
        "eventID": "683f073b-6ced-45c7-b8d5-2df338e494d1",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "891377205497",
        "recipientAccountId": "891377205497",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "iam.amazonaws.com"
            "clientProvidedHostHeader": "iam.amazonaws.com"
        },
        "mitreAttackTactics": "TA0007 - Discovery",
        "mitreAttackTechniques": "T1087 - Account Discovery"
        "mitreAttackTactics": "TA0007 - Discovery",
        "mitreAttackTechniques": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.09",
        "eventVersion": "1.09",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDA47CRYYD4VWJGA4YTZ",
            "arn": "arn:aws:iam::891377205497:user/dwbcf",
            "accountId": "891377205497",
            "accessKeyId": "AKIA47CRYYD44ONNPRVY",
            "userName": "dwbcf"
        },
        "eventTime": "2024-09-13T05:37:17Z",
        "eventSource": "iam.amazonaws.com",
        "eventName": "ListRoles",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "Boto3/1.35.15 md/Botocore#1.35.15 ua/2.0 os/macos#24.0.0 md/arch#arm64 lang/python#3.12.4 md/pyimpl#CPython cfg/retry-mode#adaptive Botocore/1.35.15",
        "requestParameters": null,
        "userAgent": "Boto3/1.35.15 md/Botocore#1.35.15 ua/2.0 os/macos#24.0.0 md/arch#arm64 lang/python#3.12.4 md/pyimpl#CPython cfg/retry-mode#adaptive Botocore/1.35.15",
        "requestParameters": null,
        "responseElements": null,
        "requestID": "f8f0cd9d-ebc1-4661-a72e-a2b2b00f6d2a",
        "eventID": "362cbd95-280a-4bb7-9d23-80078225d60a",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "891377205497",
        "recipientAccountId": "891377205497",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "iam.amazonaws.com"
            "clientProvidedHostHeader": "iam.amazonaws.com"
        },
        "mitreAttackTactics": "TA0007 - Discovery",
        "mitreAttackTechniques": "T1087 - Account Discovery"
        "mitreAttackTactics": "TA0007 - Discovery",
        "mitreAttackTechniques": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.09",
        "eventVersion": "1.09",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDA47CRYYD4VWJGA4YTZ",
            "arn": "arn:aws:iam::891377205497:user/dwbcf",
            "accountId": "891377205497",
            "accessKeyId": "AKIA47CRYYD44ONNPRVY",
            "userName": "dwbcf"
        },
        "eventTime": "2024-09-13T05:37:17Z",
        "eventSource": "iam.amazonaws.com",
        "eventName": "ListUsers",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "Boto3/1.35.15 md/Botocore#1.35.15 ua/2.0 os/macos#24.0.0 md/arch#arm64 lang/python#3.12.4 md/pyimpl#CPython cfg/retry-mode#adaptive Botocore/1.35.15",
        "requestParameters": null,
        "responseElements": null,
        "requestID": "3b8e5b2a-739f-463a-8195-cd1f6b27f301",
        "eventID": "633bb346-aaed-4955-bbd5-97aad7d46f17",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "891377205497",
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
        "eventTime": "2024-09-13T05:37:16Z",
        "eventSource": "iam.amazonaws.com",
        "eventName": "ListAttachedRolePolicies",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "APN/1.0 HashiCorp/1.0 Terraform/1.5.7 (+https://www.terraform.io) terraform-provider-aws/5.67.0 (+https://registry.terraform.io/providers/hashicorp/aws) m/C aws-sdk-go-v2/1.30.5 os/macos lang/go#1.22.6 md/GOOS#darwin md/GOARCH#arm64 api/iam#1.35.2",
        "requestParameters": {
            "roleName": "testrole"
        },
        "responseElements": null,
        "requestID": "c3a4e69c-bd27-4aba-8cca-f38e0d7dd0a7",
        "eventID": "5e291ecf-23b4-424f-b1a0-b91db608ba4a",
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
report_response = generate_response(client, "gpt-4o-mini", [prompt_txt["graph"]])
print_response("그래프 데이터", report_response)

# '"""'와 'javascript'를 제외한 응답 생성
filtered_response = report_response.replace('"""', '').replace('javascript', '')

# 필터링된 응답 출력
print_response("그래프 데이터", filtered_response)

