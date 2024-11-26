import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from function import load_and_fill, prompt_files, load_prompt, save_history, print_response, manage_history, text_response

# 환경 변수 로드 및 API 클라이언트 설정
load_dotenv()
api_key = os.getenv("OPEN_AI_SECRET_KEY")
client = OpenAI(api_key=api_key)

# 템플릿 파일 로드
template_content = load_prompt(prompt_files["report"])  # 파일 내용을 읽어옴

Field = input("\n양식: ")

attack_time =  "2024년 09월 21일 08:20 KST"
attack_type = "Execution, Command and Scripting Interpreter" 
logs = """ 
[
    {
        "eventVersion": "1.10",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDAQ52DOPIP4PJDL3L6Y",
            "arn": "arn:aws:iam::064029096479:user/attack_user_03",
            "accountId": "064029096479",
            "accessKeyId": "AKIAQ52DOPIPU3YLJCES",
            "userName": "attack_user_03"
        },
        "eventTime": "2024-09-21T07:53:28Z",
        "eventSource": "ec2.amazonaws.com",
        "eventName": "DescribeInstances",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "stratus-red-team_fb117e45-c7c5-4c7b-9fbc-b73aad12dc50",
        "requestParameters": {
            "instancesSet": {
                "items": [
                    {
                        "instanceId": "i-01c646c4b28fcf780"
                    }
                ]
            },
            "filterSet": {}
        },
        "responseElements": null,
        "requestID": "b9a909fa-3419-4638-9edc-f9f29c956957",
        "eventID": "12f8d90e-0537-47ae-a3c1-6cac4844af56",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "064029096479",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "ec2.us-east-1.amazonaws.com"
        },
        "mitreAttackTactic": "TA0007 - Discovery",
        "mitreAttackTechnique": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.10",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDAQ52DOPIP4PJDL3L6Y",
            "arn": "arn:aws:iam::064029096479:user/attack_user_03",
            "accountId": "064029096479",
            "accessKeyId": "AKIAQ52DOPIPU3YLJCES",
            "userName": "attack_user_03"
        },
        "eventTime": "2024-09-21T07:53:27Z",
        "eventSource": "ec2.amazonaws.com",
        "eventName": "DescribeInstances",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "stratus-red-team_fb117e45-c7c5-4c7b-9fbc-b73aad12dc50",
        "requestParameters": {
            "instancesSet": {
                "items": [
                    {
                        "instanceId": "i-01c646c4b28fcf780"
                    }
                ]
            },
            "filterSet": {}
        },
        "responseElements": null,
        "requestID": "591c45b2-e85e-4641-b906-100b5888f00b",
        "eventID": "bc3cba93-63d5-4107-b5c9-f97d83cbf82d",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "064029096479",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "ec2.us-east-1.amazonaws.com"
        },
        "mitreAttackTactic": "TA0007 - Discovery",
        "mitreAttackTechnique": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.10",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDAQ52DOPIP4PJDL3L6Y",
            "arn": "arn:aws:iam::064029096479:user/attack_user_03",
            "accountId": "064029096479",
            "accessKeyId": "AKIAQ52DOPIPU3YLJCES",
            "userName": "attack_user_03"
        },
        "eventTime": "2024-09-21T07:53:25Z",
        "eventSource": "ec2.amazonaws.com",
        "eventName": "DescribeInstances",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "stratus-red-team_fb117e45-c7c5-4c7b-9fbc-b73aad12dc50",
        "requestParameters": {
            "instancesSet": {
                "items": [
                    {
                        "instanceId": "i-01c646c4b28fcf780"
                    }
                ]
            },
            "filterSet": {}
        },
        "responseElements": null,
        "requestID": "13ef1cb2-bdbc-4fc9-a226-6202a3c411cd",
        "eventID": "0dbd729a-da07-4fc3-a937-8fddd6530a1e",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "064029096479",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "ec2.us-east-1.amazonaws.com"
        },
        "mitreAttackTactic": "TA0007 - Discovery",
        "mitreAttackTechnique": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.10",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDAQ52DOPIP4PJDL3L6Y",
            "arn": "arn:aws:iam::064029096479:user/attack_user_03",
            "accountId": "064029096479",
            "accessKeyId": "AKIAQ52DOPIPU3YLJCES",
            "userName": "attack_user_03"
        },
        "eventTime": "2024-09-21T07:53:24Z",
        "eventSource": "ec2.amazonaws.com",
        "eventName": "DescribeInstances",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "stratus-red-team_fb117e45-c7c5-4c7b-9fbc-b73aad12dc50",
        "requestParameters": {
            "instancesSet": {
                "items": [
                    {
                        "instanceId": "i-01c646c4b28fcf780"
                    }
                ]
            },
            "filterSet": {}
        },
        "responseElements": null,
        "requestID": "2ab8fac7-ffd5-4f72-8c1a-938788b71922",
        "eventID": "0012b809-9c2d-496b-a7f8-55eb9caec7b2",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "064029096479",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "ec2.us-east-1.amazonaws.com"
        },
        "mitreAttackTactic": "TA0007 - Discovery",
        "mitreAttackTechnique": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.10",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDAQ52DOPIP4PJDL3L6Y",
            "arn": "arn:aws:iam::064029096479:user/attack_user_03",
            "accountId": "064029096479",
            "accessKeyId": "AKIAQ52DOPIPU3YLJCES",
            "userName": "attack_user_03"
        },
        "eventTime": "2024-09-21T07:53:23Z",
        "eventSource": "ec2.amazonaws.com",
        "eventName": "ModifyInstanceAttribute",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "stratus-red-team_fb117e45-c7c5-4c7b-9fbc-b73aad12dc50",
        "requestParameters": {
            "instanceId": "i-01c646c4b28fcf780",
            "userData": "<sensitiveDataRemoved>"
        },
        "responseElements": {
            "requestId": "53634e3e-d74a-4701-94fe-02d683d2860d",
            "_return": true
        },
        "requestID": "53634e3e-d74a-4701-94fe-02d683d2860d",
        "eventID": "2ad63cce-5063-4fa2-8e7a-be877cff2354",
        "readOnly": false,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "064029096479",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "ec2.us-east-1.amazonaws.com"
        },
        "mitreAttackTactic": "TA0008 - Execution",
        "mitreAttackTechnique": "T1059 - Command and Scripting Interpreter"
    },
    {
        "eventVersion": "1.10",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDAQ52DOPIP4PJDL3L6Y",
            "arn": "arn:aws:iam::064029096479:user/attack_user_03",
            "accountId": "064029096479",
            "accessKeyId": "AKIAQ52DOPIPU3YLJCES",
            "userName": "attack_user_03"
        },
        "eventTime": "2024-09-21T07:53:23Z",
        "eventSource": "ec2.amazonaws.com",
        "eventName": "StartInstances",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "stratus-red-team_fb117e45-c7c5-4c7b-9fbc-b73aad12dc50",
        "requestParameters": {
            "instancesSet": {
                "items": [
                    {
                        "instanceId": "i-01c646c4b28fcf780"
                    }
                ]
            }
        },
        "responseElements": {
            "requestId": "9c6bc22d-416e-4259-8592-225d6e8bf7de",
            "instancesSet": {
                "items": [
                    {
                        "instanceId": "i-01c646c4b28fcf780",
                        "currentState": {
                            "code": 0,
                            "name": "pending"
                        },
                        "previousState": {
                            "code": 80,
                            "name": "stopped"
                        }
                    }
                ]
            }
        },
        "requestID": "9c6bc22d-416e-4259-8592-225d6e8bf7de",
        "eventID": "b9516b17-0866-4e4a-a869-d48a4572b5fd",
        "readOnly": false,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "064029096479",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "ec2.us-east-1.amazonaws.com"
        },
        "mitreAttackTactic": "TA0008 - Execution",
        "mitreAttackTechnique": "T1484 - Domain Policy Modification"
    },
    {
        "eventVersion": "1.10",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDAQ52DOPIP4PJDL3L6Y",
            "arn": "arn:aws:iam::064029096479:user/attack_user_03",
            "accountId": "064029096479",
            "accessKeyId": "AKIAQ52DOPIPU3YLJCES",
            "userName": "attack_user_03"
        },
        "eventTime": "2024-09-21T07:53:22Z",
        "eventSource": "ec2.amazonaws.com",
        "eventName": "DescribeInstances",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "stratus-red-team_fb117e45-c7c5-4c7b-9fbc-b73aad12dc50",
        "requestParameters": {
            "instancesSet": {
                "items": [
                    {
                        "instanceId": "i-01c646c4b28fcf780"
                    }
                ]
            },
            "filterSet": {}
        },
        "responseElements": null,
        "requestID": "738673fc-e2ee-472a-86f1-12484e0fb32b",
        "eventID": "3b693878-8df3-41aa-b1b4-54365830a1fd",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "064029096479",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "ec2.us-east-1.amazonaws.com"
        },
        "mitreAttackTactic": "TA0007 - Discovery",
        "mitreAttackTechnique": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.10",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDAQ52DOPIP4PJDL3L6Y",
            "arn": "arn:aws:iam::064029096479:user/attack_user_03",
            "accountId": "064029096479",
            "accessKeyId": "AKIAQ52DOPIPU3YLJCES",
            "userName": "attack_user_03"
        },
        "eventTime": "2024-09-21T07:53:20Z",
        "eventSource": "ec2.amazonaws.com",
        "eventName": "DescribeInstances",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "stratus-red-team_fb117e45-c7c5-4c7b-9fbc-b73aad12dc50",
        "requestParameters": {
            "instancesSet": {
                "items": [
                    {
                        "instanceId": "i-01c646c4b28fcf780"
                    }
                ]
            },
            "filterSet": {}
        },
        "responseElements": null,
        "requestID": "ac77a8d2-5f1a-4fa4-9aee-3c95e695ac6a",
        "eventID": "fcaf49fd-d7ab-4f54-afb7-70d853552232",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "064029096479",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "ec2.us-east-1.amazonaws.com"
        },
        "mitreAttackTactic": "TA0007 - Discovery",
        "mitreAttackTechnique": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.10",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDAQ52DOPIP4PJDL3L6Y",
            "arn": "arn:aws:iam::064029096479:user/attack_user_03",
            "accountId": "064029096479",
            "accessKeyId": "AKIAQ52DOPIPU3YLJCES",
            "userName": "attack_user_03"
        },
        "eventTime": "2024-09-21T07:53:18Z",
        "eventSource": "ec2.amazonaws.com",
        "eventName": "DescribeInstances",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "stratus-red-team_fb117e45-c7c5-4c7b-9fbc-b73aad12dc50",
        "requestParameters": {
            "instancesSet": {
                "items": [
                    {
                        "instanceId": "i-01c646c4b28fcf780"
                    }
                ]
            },
            "filterSet": {}
        },
        "responseElements": null,
        "requestID": "af994d29-2e33-4ae9-a0e0-2208812f0572",
        "eventID": "fe2bbd28-4502-4fb3-b3db-702ba6f24c3e",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "064029096479",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "ec2.us-east-1.amazonaws.com"
        },
        "mitreAttackTactic": "TA0007 - Discovery",
        "mitreAttackTechnique": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.10",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDAQ52DOPIP4PJDL3L6Y",
            "arn": "arn:aws:iam::064029096479:user/attack_user_03",
            "accountId": "064029096479",
            "accessKeyId": "AKIAQ52DOPIPU3YLJCES",
            "userName": "attack_user_03"
        },
        "eventTime": "2024-09-21T07:53:17Z",
        "eventSource": "ec2.amazonaws.com",
        "eventName": "DescribeInstances",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "stratus-red-team_fb117e45-c7c5-4c7b-9fbc-b73aad12dc50",
        "requestParameters": {
            "instancesSet": {
                "items": [
                    {
                        "instanceId": "i-01c646c4b28fcf780"
                    }
                ]
            },
            "filterSet": {}
        },
        "responseElements": null,
        "requestID": "6fbfdcd7-b837-4e2c-b997-5c93f6bcecd2",
        "eventID": "74c254a4-877f-48b1-baa3-a45350bd58cc",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "064029096479",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "ec2.us-east-1.amazonaws.com"
        },
        "mitreAttackTactic": "TA0007 - Discovery",
        "mitreAttackTechnique": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.10",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDAQ52DOPIP4PJDL3L6Y",
            "arn": "arn:aws:iam::064029096479:user/attack_user_03",
            "accountId": "064029096479",
            "accessKeyId": "AKIAQ52DOPIPU3YLJCES",
            "userName": "attack_user_03"
        },
        "eventTime": "2024-09-21T07:53:15Z",
        "eventSource": "ec2.amazonaws.com",
        "eventName": "DescribeInstances",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "stratus-red-team_fb117e45-c7c5-4c7b-9fbc-b73aad12dc50",
        "requestParameters": {
            "instancesSet": {
                "items": [
                    {
                        "instanceId": "i-01c646c4b28fcf780"
                    }
                ]
            },
            "filterSet": {}
        },
        "responseElements": null,
        "requestID": "3366ebed-0881-4f98-a5b3-48e8da0cbbba",
        "eventID": "761fb3a8-db86-4b12-9ab1-14936370042a",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "064029096479",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "ec2.us-east-1.amazonaws.com"
        },
        "mitreAttackTactic": "TA0007 - Discovery",
        "mitreAttackTechnique": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.10",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDAQ52DOPIP4PJDL3L6Y",
            "arn": "arn:aws:iam::064029096479:user/attack_user_03",
            "accountId": "064029096479",
            "accessKeyId": "AKIAQ52DOPIPU3YLJCES",
            "userName": "attack_user_03"
        },
        "eventTime": "2024-09-21T07:53:14Z",
        "eventSource": "ec2.amazonaws.com",
        "eventName": "DescribeInstances",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "stratus-red-team_fb117e45-c7c5-4c7b-9fbc-b73aad12dc50",
        "requestParameters": {
            "instancesSet": {
                "items": [
                    {
                        "instanceId": "i-01c646c4b28fcf780"
                    }
                ]
            },
            "filterSet": {}
        },
        "responseElements": null,
        "requestID": "19b163ab-71dc-4cbf-8f8a-05acc92a8c95",
        "eventID": "f942bcad-3a96-4198-a2af-48ad17be9663",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "064029096479",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "ec2.us-east-1.amazonaws.com"
        },
        "mitreAttackTactic": "TA0007 - Discovery",
        "mitreAttackTechnique": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.10",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDAQ52DOPIP4PJDL3L6Y",
            "arn": "arn:aws:iam::064029096479:user/attack_user_03",
            "accountId": "064029096479",
            "accessKeyId": "AKIAQ52DOPIPU3YLJCES",
            "userName": "attack_user_03"
        },
        "eventTime": "2024-09-21T07:53:11Z",
        "eventSource": "ec2.amazonaws.com",
        "eventName": "DescribeInstances",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "stratus-red-team_fb117e45-c7c5-4c7b-9fbc-b73aad12dc50",
        "requestParameters": {
            "instancesSet": {
                "items": [
                    {
                        "instanceId": "i-01c646c4b28fcf780"
                    }
                ]
            },
            "filterSet": {}
        },
        "responseElements": null,
        "requestID": "c246a2ed-29ee-4602-9e41-83e73c067235",
        "eventID": "bca1a8f8-e285-437a-abbf-a4d4c0fdf569",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "064029096479",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "ec2.us-east-1.amazonaws.com"
        },
        "mitreAttackTactic": "TA0007 - Discovery",
        "mitreAttackTechnique": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.10",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDAQ52DOPIP4PJDL3L6Y",
            "arn": "arn:aws:iam::064029096479:user/attack_user_03",
            "accountId": "064029096479",
            "accessKeyId": "AKIAQ52DOPIPU3YLJCES",
            "userName": "attack_user_03"
        },
        "eventTime": "2024-09-21T07:53:09Z",
        "eventSource": "ec2.amazonaws.com",
        "eventName": "DescribeInstances",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "stratus-red-team_fb117e45-c7c5-4c7b-9fbc-b73aad12dc50",
        "requestParameters": {
            "instancesSet": {
                "items": [
                    {
                        "instanceId": "i-01c646c4b28fcf780"
                    }
                ]
            },
            "filterSet": {}
        },
        "responseElements": null,
        "requestID": "5453822c-2a0b-40f1-8ad7-6ace5c793086",
        "eventID": "6399a829-6d33-49e6-8e16-d679a52e3349",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "064029096479",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "ec2.us-east-1.amazonaws.com"
        },
        "mitreAttackTactic": "TA0007 - Discovery",
        "mitreAttackTechnique": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.10",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDAQ52DOPIP4PJDL3L6Y",
            "arn": "arn:aws:iam::064029096479:user/attack_user_03",
            "accountId": "064029096479",
            "accessKeyId": "AKIAQ52DOPIPU3YLJCES",
            "userName": "attack_user_03"
        },
        "eventTime": "2024-09-21T07:53:07Z",
        "eventSource": "ec2.amazonaws.com",
        "eventName": "DescribeInstances",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "stratus-red-team_fb117e45-c7c5-4c7b-9fbc-b73aad12dc50",
        "requestParameters": {
            "instancesSet": {
                "items": [
                    {
                        "instanceId": "i-01c646c4b28fcf780"
                    }
                ]
            },
            "filterSet": {}
        },
        "responseElements": null,
        "requestID": "95019e49-aafc-4b3d-ada3-ee3133b3e696",
        "eventID": "83ba63bc-574a-41e6-9bd6-d2768c955e70",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "064029096479",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "ec2.us-east-1.amazonaws.com"
        },
        "mitreAttackTactic": "TA0007 - Discovery",
        "mitreAttackTechnique": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.10",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDAQ52DOPIP4PJDL3L6Y",
            "arn": "arn:aws:iam::064029096479:user/attack_user_03",
            "accountId": "064029096479",
            "accessKeyId": "AKIAQ52DOPIPU3YLJCES",
            "userName": "attack_user_03"
        },
        "eventTime": "2024-09-21T07:53:05Z",
        "eventSource": "ec2.amazonaws.com",
        "eventName": "DescribeInstances",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "stratus-red-team_fb117e45-c7c5-4c7b-9fbc-b73aad12dc50",
        "requestParameters": {
            "instancesSet": {
                "items": [
                    {
                        "instanceId": "i-01c646c4b28fcf780"
                    }
                ]
            },
            "filterSet": {}
        },
        "responseElements": null,
        "requestID": "e57dedfa-a345-4818-b57c-d2dbc85e01ed",
        "eventID": "80d2787b-445d-4b73-8323-d9ec25a13654",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "064029096479",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "ec2.us-east-1.amazonaws.com"
        },
        "mitreAttackTactic": "TA0007 - Discovery",
        "mitreAttackTechnique": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.10",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDAQ52DOPIP4PJDL3L6Y",
            "arn": "arn:aws:iam::064029096479:user/attack_user_03",
            "accountId": "064029096479",
            "accessKeyId": "AKIAQ52DOPIPU3YLJCES",
            "userName": "attack_user_03"
        },
        "eventTime": "2024-09-21T07:53:04Z",
        "eventSource": "ec2.amazonaws.com",
        "eventName": "DescribeInstances",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "stratus-red-team_fb117e45-c7c5-4c7b-9fbc-b73aad12dc50",
        "requestParameters": {
            "instancesSet": {
                "items": [
                    {
                        "instanceId": "i-01c646c4b28fcf780"
                    }
                ]
            },
            "filterSet": {}
        },
        "responseElements": null,
        "requestID": "ea5f9923-8dbc-4435-a7ca-c75ec64c783f",
        "eventID": "dd59ec32-22d6-4eeb-9c10-d93dd2d2baea",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "064029096479",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "ec2.us-east-1.amazonaws.com"
        },
        "mitreAttackTactic": "TA0007 - Discovery",
        "mitreAttackTechnique": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.10",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDAQ52DOPIP4PJDL3L6Y",
            "arn": "arn:aws:iam::064029096479:user/attack_user_03",
            "accountId": "064029096479",
            "accessKeyId": "AKIAQ52DOPIPU3YLJCES",
            "userName": "attack_user_03"
        },
        "eventTime": "2024-09-21T07:53:02Z",
        "eventSource": "ec2.amazonaws.com",
        "eventName": "DescribeInstances",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "stratus-red-team_fb117e45-c7c5-4c7b-9fbc-b73aad12dc50",
        "requestParameters": {
            "instancesSet": {
                "items": [
                    {
                        "instanceId": "i-01c646c4b28fcf780"
                    }
                ]
            },
            "filterSet": {}
        },
        "responseElements": null,
        "requestID": "95ba8bb7-9320-4b70-8214-ba3066505ae7",
        "eventID": "fe580727-4ebe-4d52-aeb2-e8d14f7779f7",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "064029096479",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "ec2.us-east-1.amazonaws.com"
        },
        "mitreAttackTactic": "TA0007 - Discovery",
        "mitreAttackTechnique": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.10",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDAQ52DOPIP4PJDL3L6Y",
            "arn": "arn:aws:iam::064029096479:user/attack_user_03",
            "accountId": "064029096479",
            "accessKeyId": "AKIAQ52DOPIPU3YLJCES",
            "userName": "attack_user_03"
        },
        "eventTime": "2024-09-21T07:53:00Z",
        "eventSource": "ec2.amazonaws.com",
        "eventName": "DescribeInstances",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "stratus-red-team_fb117e45-c7c5-4c7b-9fbc-b73aad12dc50",
        "requestParameters": {
            "instancesSet": {
                "items": [
                    {
                        "instanceId": "i-01c646c4b28fcf780"
                    }
                ]
            },
            "filterSet": {}
        },
        "responseElements": null,
        "requestID": "604ceb8a-f763-4dcc-9e46-d8f12647e29d",
        "eventID": "5e0ed2d5-fc00-4098-aadd-6508f25d17e7",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "064029096479",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "ec2.us-east-1.amazonaws.com"
        },
        "mitreAttackTactic": "TA0007 - Discovery",
        "mitreAttackTechnique": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.10",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDAQ52DOPIP4PJDL3L6Y",
            "arn": "arn:aws:iam::064029096479:user/attack_user_03",
            "accountId": "064029096479",
            "accessKeyId": "AKIAQ52DOPIPU3YLJCES",
            "userName": "attack_user_03"
        },
        "eventTime": "2024-09-21T07:52:58Z",
        "eventSource": "ec2.amazonaws.com",
        "eventName": "DescribeInstances",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "stratus-red-team_fb117e45-c7c5-4c7b-9fbc-b73aad12dc50",
        "requestParameters": {
            "instancesSet": {
                "items": [
                    {
                        "instanceId": "i-01c646c4b28fcf780"
                    }
                ]
            },
            "filterSet": {}
        },
        "responseElements": null,
        "requestID": "cfd93cdd-0d62-43ee-b5ad-482b59892843",
        "eventID": "3ed750d7-7ccc-41ca-8136-9fe16053b9aa",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "064029096479",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "ec2.us-east-1.amazonaws.com"
        },
        "mitreAttackTactic": "TA0007 - Discovery",
        "mitreAttackTechnique": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.10",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDAQ52DOPIP4PJDL3L6Y",
            "arn": "arn:aws:iam::064029096479:user/attack_user_03",
            "accountId": "064029096479",
            "accessKeyId": "AKIAQ52DOPIPU3YLJCES",
            "userName": "attack_user_03"
        },
        "eventTime": "2024-09-21T07:52:57Z",
        "eventSource": "ec2.amazonaws.com",
        "eventName": "DescribeInstances",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "stratus-red-team_fb117e45-c7c5-4c7b-9fbc-b73aad12dc50",
        "requestParameters": {
            "instancesSet": {
                "items": [
                    {
                        "instanceId": "i-01c646c4b28fcf780"
                    }
                ]
            },
            "filterSet": {}
        },
        "responseElements": null,
        "requestID": "ff2b9d62-5a91-4b23-a313-ea072c26f674",
        "eventID": "1f19c6c5-bb91-4eea-809b-5c516c2054fc",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "064029096479",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "ec2.us-east-1.amazonaws.com"
        },
        "mitreAttackTactic": "TA0007 - Discovery",
        "mitreAttackTechnique": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.10",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDAQ52DOPIP4PJDL3L6Y",
            "arn": "arn:aws:iam::064029096479:user/attack_user_03",
            "accountId": "064029096479",
            "accessKeyId": "AKIAQ52DOPIPU3YLJCES",
            "userName": "attack_user_03"
        },
        "eventTime": "2024-09-21T07:52:55Z",
        "eventSource": "ec2.amazonaws.com",
        "eventName": "DescribeInstances",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "stratus-red-team_fb117e45-c7c5-4c7b-9fbc-b73aad12dc50",
        "requestParameters": {
            "instancesSet": {
                "items": [
                    {
                        "instanceId": "i-01c646c4b28fcf780"
                    }
                ]
            },
            "filterSet": {}
        },
        "responseElements": null,
        "requestID": "64abe5ef-6eb3-40bb-8c68-bb4441277a67",
        "eventID": "7719a437-1475-4711-ae9a-5ae1961e154d",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "064029096479",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "ec2.us-east-1.amazonaws.com"
        },
        "mitreAttackTactic": "TA0007 - Discovery",
        "mitreAttackTechnique": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.10",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDAQ52DOPIP4PJDL3L6Y",
            "arn": "arn:aws:iam::064029096479:user/attack_user_03",
            "accountId": "064029096479",
            "accessKeyId": "AKIAQ52DOPIPU3YLJCES",
            "userName": "attack_user_03"
        },
        "eventTime": "2024-09-21T07:52:54Z",
        "eventSource": "ec2.amazonaws.com",
        "eventName": "DescribeInstances",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "stratus-red-team_fb117e45-c7c5-4c7b-9fbc-b73aad12dc50",
        "requestParameters": {
            "instancesSet": {
                "items": [
                    {
                        "instanceId": "i-01c646c4b28fcf780"
                    }
                ]
            },
            "filterSet": {}
        },
        "responseElements": null,
        "requestID": "841a37a4-f30e-4b61-8b31-b013251029dc",
        "eventID": "90a176fd-e3e4-47e5-946f-4737fb2700eb",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "064029096479",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "ec2.us-east-1.amazonaws.com"
        },
        "mitreAttackTactic": "TA0007 - Discovery",
        "mitreAttackTechnique": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.10",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDAQ52DOPIP4PJDL3L6Y",
            "arn": "arn:aws:iam::064029096479:user/attack_user_03",
            "accountId": "064029096479",
            "accessKeyId": "AKIAQ52DOPIPU3YLJCES",
            "userName": "attack_user_03"
        },
        "eventTime": "2024-09-21T07:52:52Z",
        "eventSource": "ec2.amazonaws.com",
        "eventName": "DescribeInstances",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "stratus-red-team_fb117e45-c7c5-4c7b-9fbc-b73aad12dc50",
        "requestParameters": {
            "instancesSet": {
                "items": [
                    {
                        "instanceId": "i-01c646c4b28fcf780"
                    }
                ]
            },
            "filterSet": {}
        },
        "responseElements": null,
        "requestID": "e7c54934-d551-4de3-b910-558f49ab1229",
        "eventID": "4d3d214e-2ca4-4d31-b800-2f9c6cbd56d1",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "064029096479",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "ec2.us-east-1.amazonaws.com"
        },
        "mitreAttackTactic": "TA0007 - Discovery",
        "mitreAttackTechnique": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.10",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDAQ52DOPIP4PJDL3L6Y",
            "arn": "arn:aws:iam::064029096479:user/attack_user_03",
            "accountId": "064029096479",
            "accessKeyId": "AKIAQ52DOPIPU3YLJCES",
            "userName": "attack_user_03"
        },
        "eventTime": "2024-09-21T07:52:51Z",
        "eventSource": "ec2.amazonaws.com",
        "eventName": "DescribeInstances",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "stratus-red-team_fb117e45-c7c5-4c7b-9fbc-b73aad12dc50",
        "requestParameters": {
            "instancesSet": {
                "items": [
                    {
                        "instanceId": "i-01c646c4b28fcf780"
                    }
                ]
            },
            "filterSet": {}
        },
        "responseElements": null,
        "requestID": "9fd798a6-f3a8-40a7-ba02-deba00576bc2",
        "eventID": "d880d1a6-f431-41d2-bac5-59354d65130c",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "064029096479",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "ec2.us-east-1.amazonaws.com"
        },
        "mitreAttackTactic": "TA0007 - Discovery",
        "mitreAttackTechnique": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.10",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDAQ52DOPIP4PJDL3L6Y",
            "arn": "arn:aws:iam::064029096479:user/attack_user_03",
            "accountId": "064029096479",
            "accessKeyId": "AKIAQ52DOPIPU3YLJCES",
            "userName": "attack_user_03"
        },
        "eventTime": "2024-09-21T07:52:49Z",
        "eventSource": "ec2.amazonaws.com",
        "eventName": "DescribeInstances",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "stratus-red-team_fb117e45-c7c5-4c7b-9fbc-b73aad12dc50",
        "requestParameters": {
            "instancesSet": {
                "items": [
                    {
                        "instanceId": "i-01c646c4b28fcf780"
                    }
                ]
            },
            "filterSet": {}
        },
        "responseElements": null,
        "requestID": "fec6ede2-de3d-4b48-a7af-00c0e8b3a480",
        "eventID": "84c144a4-7a8b-4500-9533-3ab9a6ab20ef",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "064029096479",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "ec2.us-east-1.amazonaws.com"
        },
        "mitreAttackTactic": "TA0007 - Discovery",
        "mitreAttackTechnique": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.10",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDAQ52DOPIP4PJDL3L6Y",
            "arn": "arn:aws:iam::064029096479:user/attack_user_03",
            "accountId": "064029096479",
            "accessKeyId": "AKIAQ52DOPIPU3YLJCES",
            "userName": "attack_user_03"
        },
        "eventTime": "2024-09-21T07:52:48Z",
        "eventSource": "ec2.amazonaws.com",
        "eventName": "StopInstances",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "stratus-red-team_fb117e45-c7c5-4c7b-9fbc-b73aad12dc50",
        "requestParameters": {
            "instancesSet": {
                "items": [
                    {
                        "instanceId": "i-01c646c4b28fcf780"
                    }
                ]
            },
            "force": true
        },
        "responseElements": {
            "requestId": "712cf79c-509f-479e-8ee3-223f909f2641",
            "instancesSet": {
                "items": [
                    {
                        "instanceId": "i-01c646c4b28fcf780",
                        "currentState": {
                            "code": 64,
                            "name": "stopping"
                        },
                        "previousState": {
                            "code": 16,
                            "name": "running"
                        }
                    }
                ]
            }
        },
        "requestID": "712cf79c-509f-479e-8ee3-223f909f2641",
        "eventID": "1e3fc212-3b1a-4582-8aa8-8c1fb5f5d022",
        "readOnly": false,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "064029096479",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "ec2.us-east-1.amazonaws.com"
        },
        "mitreAttackTactic": "TA0008 - Execution",
        "mitreAttackTechnique": "T1489 - Service Stop"
    },
    {
        "eventVersion": "1.10",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDAQ52DOPIP4PJDL3L6Y",
            "arn": "arn:aws:iam::064029096479:user/attack_user_03",
            "accountId": "064029096479",
            "accessKeyId": "AKIAQ52DOPIPU3YLJCES",
            "userName": "attack_user_03"
        },
        "eventTime": "2024-09-21T07:52:48Z",
        "eventSource": "ec2.amazonaws.com",
        "eventName": "DescribeInstances",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "stratus-red-team_fb117e45-c7c5-4c7b-9fbc-b73aad12dc50",
        "requestParameters": {
            "instancesSet": {
                "items": [
                    {
                        "instanceId": "i-01c646c4b28fcf780"
                    }
                ]
            },
            "filterSet": {}
        },
        "responseElements": null,
        "requestID": "b1f2f36c-ce24-4720-b439-7cc9413f67d8",
        "eventID": "adc9a093-f990-4096-b788-4c804833c71f",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "064029096479",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "ec2.us-east-1.amazonaws.com"
        },
        "mitreAttackTactic": "TA0007 - Discovery",
        "mitreAttackTechnique": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.10",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDAQ52DOPIP4PJDL3L6Y",
            "arn": "arn:aws:iam::064029096479:user/attack_user_03",
            "accountId": "064029096479",
            "accessKeyId": "AKIAQ52DOPIPU3YLJCES",
            "userName": "attack_user_03"
        },
        "eventTime": "2024-09-21T07:52:47Z",
        "eventSource": "ec2.amazonaws.com",
        "eventName": "DescribeAccountAttributes",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "stratus-red-team_976f5613-2e73-48ca-a929-2226131cd100",
        "requestParameters": {
            "accountAttributeNameSet": {},
            "filterSet": {}
        },
        "responseElements": null,
        "requestID": "1b0e96b8-22da-44bc-a433-73abe47ad00d",
        "eventID": "1f97c652-6d44-4107-99ad-5cdde806be56",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "064029096479",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "ec2.us-east-1.amazonaws.com"
        },
        "mitreAttackTactic": "TA0007 - Discovery",
        "mitreAttackTechnique": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.10",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDAQ52DOPIP4PJDL3L6Y",
            "arn": "arn:aws:iam::064029096479:user/attack_user_03",
            "accountId": "064029096479",
            "accessKeyId": "AKIAQ52DOPIPU3YLJCES",
            "userName": "attack_user_03"
        },
        "eventTime": "2024-09-21T07:52:46Z",
        "eventSource": "ec2.amazonaws.com",
        "eventName": "StopInstances",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "aws-cli/2.17.46 md/awscrt#0.21.2 ua/2.0 os/macos#24.1.0 md/arch#arm64 lang/python#3.11.10 md/pyimpl#CPython cfg/retry-mode#standard md/installer#source md/prompt#off md/command#ec2.stop-instances",
        "errorCode": "Client.IncorrectInstanceState",
        "errorMessage": "This instance 'i-0bb0ccfd03ce061a4' is not in a state from which it can be stopped.",
        "requestParameters": {
            "instancesSet": {
                "items": [
                    {
                        "instanceId": "i-0bb0ccfd03ce061a4"
                    },
                    {
                        "instanceId": "i-01c646c4b28fcf780"
                    }
                ]
            },
            "force": true
        },
        "responseElements": null,
        "requestID": "87376cb0-081b-4001-9d94-95dae87217c8",
        "eventID": "60a8c9c2-c6d8-45da-8e69-fe598e6ea601",
        "readOnly": false,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "064029096479",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "ec2.us-east-1.amazonaws.com"
        },
        "mitreAttackTactic": "TA0008 - Execution",
        "mitreAttackTechnique": "T1489 - Service Stop"
    },
    {
        "eventVersion": "1.10",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDAQ52DOPIP4PJDL3L6Y",
            "arn": "arn:aws:iam::064029096479:user/attack_user_03",
            "accountId": "064029096479",
            "accessKeyId": "AKIAQ52DOPIPU3YLJCES",
            "userName": "attack_user_03"
        },
        "eventTime": "2024-09-21T07:52:44Z",
        "eventSource": "ec2.amazonaws.com",
        "eventName": "DescribeInstances",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "aws-cli/2.17.46 md/awscrt#0.21.2 ua/2.0 os/macos#24.1.0 md/arch#arm64 lang/python#3.11.10 md/pyimpl#CPython cfg/retry-mode#standard md/installer#source md/prompt#off md/command#ec2.describe-instances",
        "requestParameters": {
            "instancesSet": {},
            "filterSet": {
                "items": [
                    {
                        "name": "tag:StratusRedTeam",
                        "valueSet": {
                            "items": [
                                {
                                    "value": "true"
                                }
                            ]
                        }
                    }
                ]
            }
        },
        "responseElements": null,
        "requestID": "418b4122-6732-4cc2-9d7c-0606307ad3eb",
        "eventID": "713be9c1-48e9-4c5b-a706-aba86f281435",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "064029096479",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "ec2.us-east-1.amazonaws.com"
        },
        "mitreAttackTactic": "TA0007 - Discovery",
        "mitreAttackTechnique": "T1087 - Account Discovery"
    },
    {
        "eventVersion": "1.08",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDAQ52DOPIP4PJDL3L6Y",
            "arn": "arn:aws:iam::064029096479:user/attack_user_03",
            "accountId": "064029096479",
            "accessKeyId": "AKIAQ52DOPIPU3YLJCES",
            "userName": "attack_user_03"
        },
        "eventTime": "2024-09-21T07:52:43Z",
        "eventSource": "sts.amazonaws.com",
        "eventName": "GetCallerIdentity",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "211.212.221.147",
        "userAgent": "aws-cli/2.17.46 md/awscrt#0.21.2 ua/2.0 os/macos#24.1.0 md/arch#arm64 lang/python#3.11.10 md/pyimpl#CPython cfg/retry-mode#standard md/installer#source md/prompt#off md/command#sts.get-caller-identity",
        "requestParameters": null,
        "responseElements": null,
        "requestID": "5f7884b9-4311-4336-a1e9-247f62ff2578",
        "eventID": "dcd72d42-af62-4a3a-90d2-258a2d8d4e42",
        "readOnly": true,
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "recipientAccountId": "064029096479",
        "eventCategory": "Management",
        "tlsDetails": {
            "tlsVersion": "TLSv1.3",
            "cipherSuite": "TLS_AES_128_GCM_SHA256",
            "clientProvidedHostHeader": "sts.us-east-1.amazonaws.com"
        },
        "mitreAttackTactic": "TA0007 - Discovery",
        "mitreAttackTechnique": "T1087 - Account Discovery"
    }
]
"""

# 템플릿에서 직접 변수 치환
template_content = template_content.format(**locals())

prompt_txt = {"report": {"role": "system", "content": template_content}}

# Classify 프롬프트에 대해 응답 생성
report_response = text_response(client, "gpt-4o-mini", [prompt_txt["report"]])
print_response("생성된 공격 탐지 보고서", report_response)


