사용자가 제공한 로그 데이터에 기반하여 공격 탐지 보고서를 작성해주세요.

- 공격으로 탐지된 근거: 사용자가 제공한 로그를 심층 분석하여, 공격을 입증할 수 있는 구체적인 로그 이벤트와 데이터를 기반으로 근거를 제시하세요. 공격에 사용된 구체적 방법이나 로그에서 감지된 이상 징후도 포함해 주세요.
- 공격 탐지 시간: {attack_time}
- 공격 유형 (Tactic, Technique): {attack_type}
- 공격 대상 (리소스들): 사용자가 제공한 로그의 resource 필드를 기반으로, 공격 대상이 되는 리소스를 구체적으로 나열하세요.

### 주의사항
1. 공격으로 탐지된 근거는 로그를 보고 과거에서 현재까지의 시간 순서로 정리해야 합니다. 반드시 과거가 가장 먼저 나오고, 현재는 가장 나중에 나와야 합니다
2. "stratus-red-team"은 offensive tool이므로, 해당 이름이 감지되면 공격 근거에서 제외해야합니다. 제외할 때는 "제외한다"는 표현 없이 자연스럽게 제외합니다.
3. "stratus-red-team"과 "offensive tool"은 보고서에 언급하지 말고 제외합니다.
4. 반드시, 공격 유형 필드엔, MITRE ATT&CK Cloud Matrix를 기반으로 {attack_type}에 대한 설명을 함께 작성해야 합니다. (예시: Tatic이 Execution이고, Technique이 User Execution인 경우, 
**Tactic**: Execution, ~한 공격 전술이다. 
**Technique**: User Execution, ~를 수행하는 공격이다."라는 자세한 설명 포함)


제공된 로그:
{logs}

보고서는 반드시 markdown 형식으로 작성하세요.