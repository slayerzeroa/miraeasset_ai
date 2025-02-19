from ClovaX_Executor import CompletionExecutor
import json
import pandas as pd
import requests

def request_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Fail to retrieve data. Status code : {response.status_code}")

def main():
    # api
    completion_executor = CompletionExecutor(
        host='https://clovastudio.stream.ntruss.com',
        api_key='NTA0MjU2MWZlZTcxNDJiY63IHRsuPbkmleZBGwzFCDyaHMUZtTU7D+D0PfCHfrjO',
        api_key_primary_val='2OJqSbHoUuBfEh0oRCoPrCDXRgT5TTElucAkTiXK',
        request_id='08357cc3-9b13-4f29-b76c-31399d0f606b'
    )

    # customer_sentence랑 pb_sentence가 각각 고객 문장이랑 pb 문장
    customer_sentence = request_url("http://ajoufe.iptime.org:5556/customer")[2]["Description_Matching"]
    pb_sentence = request_url("http://ajoufe.iptime.org:5556/customer")[0]["Description"]

    # 매칭 이유 버튼 클릭하면 customer_sentence, pb_sentence에 입력되도록
    preset_text = [
        {"role":"system","content":"""
        <명령문>
        당신은 증권사의 개발자이고, 고령층 대상으로 PB-고객 매칭 알고리즘을 설계하려고 합니다. 이를 위해 고객과 PB의 데이터로 각 데이터 해당되는 문장들을 만들었었습니다.
        고객과 pb의 각 문장들을 임베딩한 후, 코사인 유사도를 통해서 고객에게 가장 유사한 pb를 추천해줬다고 가정해봅시다.
        당신은 고객에게 해당 pb를 추천한 이유를 설명해주어야 합니다. 이를 위해서 매칭된 고객과 pb의 문장을 활용해봅시다.

        <예시>
        매칭된 고객과 pb의 특징을 담은 문장이 아래와 같다고 가정해봅시다. 이 때 출력이 어떤식으로 이루어지는지 확인해보세요.

        #예시1
        ###input:
        customer_sentence = "이 고객은 75세 남자로, 서울 서초구에 거주하는 사업가입니다. 금융 지식 수준은 매우 높음이며, 중기투자를 선호하고, 위험 감수 성향은 보수적입니다. 선호하는 투자 유형은 부동산, 국내주식이며, 투자 금액은 1870529769원입니다. 과거 투자 경험은 낮음이며, 관심 있는 투자 주제는 블록체인, 부동산입니다. 포트폴리오 구성은 예/적금: 28.62%, 채권: 3.59%, 주식: 38.40%, 부동산: 13.31%, 펀드: 0.00% 입니다."
        pb_sentence = "이 PB는 57세 여자로, 서울 서초구에서 근무합니다. 전문 분야는 부동산이며, 선호하는 고객 그룹은 대기업 임원입니다. 관심 있는 투자 주제는 테크놀로지, 경제, 블록체인입니다."
        ###Chain-of-Thought:
        고객의 선호하는 투자 유형 중 부동산 있고, 이는 해당 PB의 전문 분야와 연결됩니다. 또한, 고객의 관심 있는 투자 주제에 블록체인이 있고, 이는 해당 PB의 관심있는 투자 주제와 일치합니다. 이러한 공통점에 착안하여 다음과 같이 추천 이유를 서술할 수 있습니다.
        ###output:
        고객님과 PB 모두 부동산에 대한 전문성과 관심이 있습니다. 이는 고객님께서 부동산 투자를 진행할 때 PB로부터 전문적인 조언을 받을 수 있음을 의미합니다. 
        고객님과 PB 모두 블록체인에 관심이 있습니다. 이는 두 분이 같은 주제에 대해 깊이 있는 대화를 나누고, 최신 투자 정보를 공유할 수 있는 좋은 기회가 될 것입니다. 또한, 고객님과 PB 모두 서울 서초구에 거주하여, 상담과 커뮤니케이션이 원활하게 이루어질 수 있습니다.

        #예시2
        ###input:
        customer_sentence = "이 고객은 70세 여자이며, 부산 해운대구에 거주하는 사업가입니다. 금융 지식 수준은 높음이며, 중기투자를 선호하고, 위험 감수 성향은 적극적입니다. 선호하는 투자 유형은 해외주식과 국내주식이며, 투자 금액은 15억원입니다. 과거 투자 경험은 높으며, 관심 있는 투자 주제는 테크놀로지와 2차전지입니다. 포트폴리오 구성은 예/적금: 5%, 채권: 20%, 주식: 50%, 부동산: 25%, 펀드: 0%입니다."
        pb_sentence = "이 PB는 44세 남자이며, 인천 연수구에서 근무합니다. 전문 분야는 국내주식이며, 선호하는 고객 그룹은 사업가입니다. 관심 있는 투자 주제는 반도체입니다."
        ###Chain-of-Thought:
        고객의 선호하는 투자 유형 중 국내주식이 있으며, 이는 해당 pb의 전문 분야와 연결됩니다. 또한, 고객의 직업은 사업가이며, 이는 해당 pb의 선호하는 고객 그룹에 속합니다. 고객의의 관심 있는 투자 주제인 테크놀로지와 2차전지는 pb의 관심 있는 투자 주제인 반도체와 간접적인 연관이 있습니다. 이러한 공통점에 착안해서 다음과 같은 추천 이유를 서술할 수 있습니다.
        ###output:
        고객님과 PB 모두 국내주식에 대한 전문성을 가지고 있어, 고객님의 투자 성향과 목표에 맞는 심도 있는 조언을 제공할 수 있습니다. 해당 PB는 사업가를 선호하는 고객 그룹으로 지정하고 있어, 고객님의 비즈니스 환경과 투자 요구를 잘 이해하고 있습니다.
        또한, 해당 PB는 반도체에 대한 깊은 관심을 가지고 있어, 고객님의 테크놀로지와 2차전지 투자에 대한 이해를 높이고, 관련 시장에서의 투자 기회를 파악하는 데 큰 도움이 될 것입니다. 이러한 전문성과 이해의 조합은 고객님의 투자 목표 달성에 큰 도움이 될 것입니다.

        #예시3:
        ###input:
        customer_sentence = "이 고객은 55세 여자이며, 대전 유성구에 거주하는 연구원입니다. 금융 지식 수준은 높음이며, 장기투자를 선호하고, 위험 감수 성향은 중립적입니다. 선호하는 투자 유형은 펀드, 국내주식이며, 투자 금액은 1억원입니다. 과거 투자 경험은 보통이며, 관심 있는 투자 주제는 과학기술, 교육입니다. 포트폴리오 구성은 예/적금: 15%, 채권: 25%, 주식: 40%, 펀드: 20%입니다."
        pb_sentence = "이 PB는 54세 여자이며, 서울 서초구에서 근무합니다. 전문 분야는 국내주식과 펀드이며, 선호하는 고객 그룹은 연구원입니다. 관심 있는 투자 주제는 테크놀로지, 교육입니다."
        ###Chain-of-Thought:
        고객의 선호하는 투자 유형은 펀드, 국내주식이며, 이는 해당 pb의 전문 분야와 일치합니다. 또한, 고객의 관심 있는 투자 주제는 과학기술과 교육이며, 이는 해당 pb의 관심사인 테크놀로지, 교육과 연결됩니다. 고객님과 해당 pb의 나이는 각각 55세와 54세로, 비슷한 나이대로 생각할 수 있습니다. 이러한 공통점에 착안해서 다음과 같은 추천 이유를 서술할 수 있습니다.
        ###output:
        고객님과 PB 모두 국내주식과 펀드에 대한 전문성을 가지고 있어, 더욱 심도 있는 조언을 제공할 수 있습니다. 두 분 모두 연구원이라는 직업군에 대한 깊은 이해를 가지고 있으며, 테크놀로지와 교육이라는 공통된 관심사를 공유하고 있습니다. 
        또한, 고객님과 PB는 나이가 비슷하여, 더 쉽게 공감하고 소통할 수 있습니다. 이러한 공통점은 고객님의 투자 목표를 달성하는 데 있어 PB의 지원이 매우 효과적일 것임을 나타냅니다.

        <조건>
        두 문장을 통해 해당 고객과 pb가 어떻게 매칭될 수 있었는지를 설명해야합니다. 아래와 같은 조건을 지키면서 줄글로 설명해보세요.
        - 고객의 문장과 pb의 문장을 재설명하면 안돼요. 당신이 해야될 일은 오직 '매칭 이유'를 설명하는 것입니다.
        - 고객과 pb의 차이를 언급하지 말아주세요. 억지로 간접적이라고 하면서 연결지어서도 안됩니다.
        - 주어진 customer_sentence, pb_sentence의 정보에서 벗어나는 말을 해서는 안됩니다.
        - 마무리는 멘트를 친절하게 한 문장 작성해주세요.
        """},
        {"role": "user", "content": f"customer_sentence:\n\{customer_sentence}\n\n\npb_sentence:\n\{pb_sentence}"}
    ]

    request_data = {
        'messages': preset_text,
        'topP': 0.8,
        'topK': 0,
        'maxTokens': 512,
        'temperature': 0.08,
        'repeatPenalty': 1.2,
        'stopBefore': [],
        'includeAiFilters': True,
        'seed': 0
    }
    completion_executor.execute(request_data)
    reason = completion_executor.full_response
    print(reason)

    dic = {"reason" : reason}
    with open('./summary_result.json', 'w', encoding = 'utf-8') as f:
        json.dump(dic, f, ensure_ascii = False, indent = 4)
    print('Json파일로 저장되었습니다')

if __name__ == '__main__':
    main()