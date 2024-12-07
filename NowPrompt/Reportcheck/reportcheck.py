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
template_content = load_prompt(prompt_files["check"])  # 파일 내용을 읽어옴

totalreport = ''' # 공격 탐지 보고서

## 공격시간
2024년 09월 21일 08:20 KST

## 공격 탐지 근거
2024년 09월 21일 07:52:44부터 2024년 09월 21일 07:52:48까지의 로그에서 다음과 같은 이벤트가 감지되었습니다:

1. **DescribeInstances** 이벤트 (T1087 - Account Discovery)
   - **이벤트시간**: 2024-09-21T07:52:44Z
   - **사용자**: attack_user_03가 인스턴스 정보를 검색하는 요청을 여러 번 하였습니다.
   - **IP 주소**: 211.212.221.147
   - **로그 이벤트 총횟수**: 15회

2. **StopInstances** 이벤트 (T1489 - Service Stop)
   - **이벤트시간**: 2024-09-21T07:52:48Z 
   - **사용자**: attack_user_03가 인스턴스를 중지시키려는 시도를 하였습니다.
   - **IP 주소**: 211.212.221.147

이 사건은 여러 차례의 인스턴스 정보 검색과 인스턴스 중지 시도로 구성되어 있으며, 이는 내부 시스템의 탐색과 통제를 시도하는 공격 행위로 보입니다.

## 공격 유형
- **Tactic**: Execution
  - Execution은 공격자가 특정 스크립트나 명령어를 실행하여 시스템 내에서 추가적인 악성 행위를 수행하는 공격 전술이다.

- **Technique**: Command and Scripting Interpreter (T1059)
  - Command and Scripting Interpreter는 공격자가 시스템에서 명령어나 스크립트를 실행하는 공격으로, 이 경우 AWS 환경에서 API 호출을 통해  인스턴스를 중지시키려는 시도가 포함된다.

## 결론
이상적인 보안 환경을 유지하기 위해, 사용자는 다음과 같은 조치를 강화해야 합니다:

1. **접근 제어 강화**: IAM 사용자에게 최소 권한 원칙을 적용하고, 불필요한 권한을 제거합니다.
2. **로그 모니터링 및 경고 시스템 구축**: AWS CloudTrail 같은 로그 서비스를 활용하여 비정상적인 활동을 신속하게 탐지하고 대응합니다.     
3. **보안 교육**: 모든 사용자에게 클라우드 보안 인식 교육을 실시하여 의심스러운 행동이나 이벤트를 보고하도록 교육합니다.

적절한 방어 수칙을 마련하여 유사한 공격을 예방할 수 있도록 해야 합니다.

# 공격 탐지 보고서

## 공격시간
- **2024년 09월 21일 08:20 KST**

## 공격 탐지 근거
2024년 09월 13일 05:33:49 UTC에 IAM 사용자 "smtpk"에 의해 `UpdateAssumeRolePolicy` 이벤트가 발생하였습니다. 이 이벤트는 `testrole` 롤의  정책을 수정하려는 시도로, Policy Document를 통해 Policy의 Principal을 수정하려고 했습니다. 이로 인해 IAM 리소스를 변경하려는 의도가 명확 해 보입니다.

또한, 동일한 사용자가 `GetRole`과 `UpdateAssumeRolePolicy`를 여러 차례 호출하였으며, 이 과정에서 두 개의 `UnmodifiableEntityException` 오류가 발생했습니다. 이는 사용자가 보호된 역할을 수정하려 하는 시도를 나타냅니다.

- 주요 활동:
  - **Event Name**: UpdateAssumeRolePolicy
  - **Event Time**: 2024-09-13T05:33:49Z
  - **Source IP Address**: 211.212.221.147
  - **User Agent**: Boto3/1.35.15 md/Botocore#1.35.15
  - **Error Message**: Cannot perform the operation on the protected role 'AWSServiceRoleForTrustedAdvisor' - this role is only modifiable by AWS.

이 정보는 해당 사용자에 의해 관리자 권한 상승을 위한 활동이 수반된 것으로 해석될 수 있습니다.

## 공격자 정보
- **사용자 이름**: smtpk
- **Principal ID**: AIDA47CRYYD4WJZ3OBVPB
- **ARN**: arn:aws:iam::891377205497:user/smtpk
- **IP 주소**: 211.212.221.147
- **사용자 에이전트**: Boto3/1.35.15 md/Botocore#1.35.15

---

### 결론
이번 공격 탐지는 IAM 사용자의 불법적인 권한 상승 시도를 나타내며, 이는 계정 조작 및 권한 상승 전술이 포함된 활동입니다. 해당 사용자의 행 동을 모니터링하고, 추가적인 보안 조치가 필요합니다.

**권장사항**:
1. IAM 사용자 `smtpk`에 대한 감사 로그 및 활동을 면밀히 검토하십시오.
2. 사용자 권한을 재평가하고, 필요 없는 권한을 제한하십시오.
3. 추가적인 보안 정책 및 여러 계정 간의 분리된 권한 구조를 구현하여 피해를 방지하십시오.
4. 지속적인 보안 모니터링 및 이상 징후 탐지 시스템을 강화하십시오.

# 공격 탐지 보고서

### 1. 공격시간
- **발생시간**: 2024-09-21 08:20 KST

### 2. 공격 탐지 근거
- **로그 이벤트 분석**:
  1. **이벤트명**: TerminateInstances (2024-09-20 02:15:59 UTC)
     - **사용자 정보**: "assumed-role"을 통해 EC2 인스턴스를 종료하는 요청이 발생함.
     - **IP 주소**: 35.153.160.118
     - **결과**: 인스턴스 ID:i-0db6ddcaaacb323b4에 대해 "shutting-down" 상태로 변경됨.
     - **MITRE ATT&CK**:
       - **Tactic**: Impact, 이는 시스템이나 서비스의 중단 또는 파괴를 목표로 하는 공격 전술이다.
       - **Technique**: Service Stop, 서비스의 중단을 수행하는 공격이다.

  2. **이벤트명**: 여러 DescribeInstances 및 RunInstances에서 user1 계정이 다음 행동을 취함:
     - 인스턴스를 조회하고 새로운 인스턴스를 생성하기 위해 AWS API를 호출하여 IAM 역할을 주거나 변경하는 등의 행위가 지속적으로 발생함.  공격자는 사용자 권한을 상승시키기 위해 여러 인스턴스를 조작하고 있다는 흐름이 감지됨.

### 3. 공격자 정보
- **사용자 정보**: `user1` (IAM 사용자)
- **계정 ID**: `891377266362`
- **IP 주소**: 1.233.83.215
- **사용자 에이전트**: aws-cli/2.17.42 등의 툴을 사용

### 결론
이 공격의 패턴은 사용자 권한을 이용해 인스턴스를 조작하고 서비스에 중단을 야기할 수 있는 행위가 포함되어 있습니다. 사용자 1(user1)이 다양한 AWS 자원에 대해 접근 및 조작을 시도하는 로그가 확인되었습니다.

#### 권장 사항
1. 사용자의 IAM 권한 검토 및 필요한 최소 권한 원칙을 적용하여 권한을 제한해야 합니다.
2. 사용자 접근 로그를 지속적으로 모니터링하고, 비정상적인 행동에 대한 경각심을 유지해야 합니다.
3. 활성화된 MFA(다단계 인증)를 모든 사용자에게 적용하여 보안성을 높여야 합니다.'''

# 템플릿에서 직접 변수 치환
template_content = template_content.format(**locals())

prompt_txt = {"check": {"role": "system", "content": template_content}}

# Classify 프롬프트에 대해 응답 생성
report_response = text_response(client, "gpt-4o-mini", [prompt_txt["check"]])
print_response("Reportcheck 데이터", report_response)


