from ClovaX_Executor import CompletionExecutor
import json
import pandas as pd

def main():
    # api
    completion_executor = CompletionExecutor(
        host='https://clovastudio.stream.ntruss.com',
        api_key='NTA0MjU2MWZlZTcxNDJiY63IHRsuPbkmleZBGwzFCDyaHMUZtTU7D+D0PfCHfrjO',
        api_key_primary_val='2OJqSbHoUuBfEh0oRCoPrCDXRgT5TTElucAkTiXK',
        request_id='bd80a896-87c9-444e-8c71-de12be1d314d'
    )

    # json파일에서 클릭된 뉴스의 id를 조회 -> 해당 id에 속하는 뉴스 text 가져오기
    json_path = "news_crawling_sorted.json"
    id = 11
    news_crawling_json = pd.read_json(json_path, orient="records")
    news_text = news_crawling_json[news_crawling_json['id'] == id]['text'].values[0]

    # 요약 버튼 클릭하면 news_text에 입력되도록
    preset_text = [
        {"role":"system","content":"<명령문>\n당신은 뉴스 요약 어시스턴트입니다. 당신의 요약을 보는 고객은 금융 투자를 하고있는 만 65세 이상 고령층입니다. 고령층 고객들이 뉴스 기사를 보기 쉽게 핵심 내용을 추출하여 요약해야 합니다.\n예시와 지침을 참고하여 작업을 진행하세요.\n\n\n<예시>\n### 뉴스\n\"달러당 1300원까지는 '아직은 감내할 수 있을 정도'라는 안정감이 있다. 하지만 1400원이 넘어가면 원화값 방어가 가능할지에 대한 시장의 불안감이 급증한다.\" 외환당국의 한 고위 관계자는 16일 매일경제와 통화하며 이 같은 고민을 내비쳤다. 이날 오후 최상목 대통령실 경제수석은 대통령실 브리핑을 통해 \"한국과 미국 정상 간 포괄적 외환시장 안정화 협력에 대한 추가 논의가 있을 것\"이라고 언급했다. 그의 발언 직후 원화값은 수직 상승해 전일 종가 대비 5.7원 오른 달러당 1388.0원에 마무리했다. 원화값은 전일 1393.7원까지 떨어져 1400원 선 붕괴를 눈앞에 뒀었다.\n\n\n최 수석은 다음주 뉴욕에서 만나는 윤석열 대통령과 조 바이든 미국 대통령 간 통화스왑 논의가 있을 것인지 묻는 질문에 \"어떤 게 논의될지 정상들 간 만나보셔야 알 수 있는 상황이다. 양국 정상이 지난 5월 정상회담에서 외환시장에 대해 긴밀히 협의하기로 했고, 뉴욕에서 재무장관 회담도 예정된 만큼 이와 관련된 공통 관심사를 자연스럽게 논의할 것으로 예상한다\"고 원론적으로 말했다. 일단 외환당국은 통화스왑을 실질적으로 추진해야 할 상황은 아니라는 기류가 강하다. 지금은 주요 통화에 비해 달러 강세가 뚜렷할 뿐 한국의 달러 조달 역량이 위협받고 있지 않다는 이유에서다. 실제로 대표적 국가 신인도 지표인 한국 국채에 대한 신용부도스왑(CDS) 프리미엄은 15일 32bp로 전일 대비 변화가 없었고 아직 코로나19 사태 초기 수준인 50bp를 밑돌고 있다. 한 기획재정부 관계자는 \"한미 통화스왑 체결이 외환시장에 긍정적 요인이 될 수 있을 것이라는 점에는 공감한다\"면서도 \"현재 외화 유동성 등을 살펴봤을 때 통화스왑 체결이 당장 필요한 상황은 아닌 것으로 판단된다\"고 말했다.\n\n### 결과\n요약문 : 한국 원-달러 환율이 1400원에 가까워지면서 시장의 불안감이 커지고 있습니다. 최상목 경제수석은 한국과 미국 정상 간 외환시장 안정화 협력에 대한 논의가 있을 것이라고 밝혔습니다. 그의 발언 이후 원화 가치는 상승해 달러당 1388.0원으로 마감되었습니다. 외환당국은 현재 통화스왑 추진이 필요하지 않다고 보고 있으며, 한국의 달러 조달 능력이 안정적이라고 설명했습니다. 한국 국채 신용부도스왑(CDS) 프리미엄도 안정적인 수준을 유지하고 있습니다.\r\n\r\n금융 용어 :\r\n- 환율: 두 나라의 화폐 교환 비율을 말합니다. 예를 들어, 원-달러 환율이 1300원이라면 1달러를 사기 위해 1300원이 필요합니다.\r\n- 외환시장 안정화 협력: 국가 간 화폐 가치의 급격한 변동을 막기 위해 협력하는 것을 의미합니다.\r\n- 통화스왑: 두 나라가 서로의 통화를 일정 기간 교환하기로 약속하는 금융 계약입니다. 이를 통해 외환시장에 유동성을 공급할 수 있습니다.\r\n- 신용부도스왑(CDS) 프리미엄: 국가나 기업이 부도날 위험을 대비해 보험료처럼 지불하는 비용입니다. 이 프리미엄이 낮을수록 신용도가 높다는 의미입니다.\n\n\n\n<지침>\n아래 지침을 준수하여 주어진 뉴스를 분석하고 500자 내외로 요약하세요. 추가적으로 고령층이 어려워할 수 있는 금융 용어에 대해서는 따로 용어 정리를 진행해주세요.\n\r\n1. 주어진 텍스트의 전체적인 맥락과 주제를 파악합니다.\r\n2. 불필요한 세부사항은 제외하고 간결하고 명확한 문장으로 요약을 작성해야 하며, 문장간 연결성이 유지되는지 확인하세요.\r\n3. 요약문은 만 65세 이상 고령층에 전해집니다. 고령층은 뉴스기사의 내용을 어려워하는 경우가 있습니다. 쉽게 풀어서 작성해주세요.\r\n4. 용어 정리에 들어가는 용어는 반드시 요약문에도 포함이 되어 있어야 합니다.\r\n5. 위의 지침을 철저히 따라 고품질의 텍스트 요약을 제공합니다.\n\n\n<출력>\n### 요약문 :\n### 용어 정리 : "},
        {"role": "user", "content": f"다음 뉴스를 요약하고, 어려운 금융 용어를 설명하세요.\n\n# 뉴스 : {news_text}"}
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
    summary = completion_executor.full_response
    print(summary)

    dic = {"id" : id, "summary" : summary}
    with open('./summary_result.json', 'w', encoding = 'utf-8') as f:
        json.dump(dic, f, ensure_ascii = False, indent = 4)
    print('Json파일로 저장되었습니다')

if __name__ == '__main__':
    main()