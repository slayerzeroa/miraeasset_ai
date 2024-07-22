from matching import marriage_algo, pb_customer_prefer, pb_customer_cosine_matching
import streamlit as st
import visualize as vis


pb = ['나이가 50대인 남성이고, 주소는 강남구이며, 직업은 회사원이고, 자산은 760000원이고, 가족 수는 3명이고, 성향은 3이고, 학력은 3입니다.',
      '나이가 30대인 여성이고, 주소는 강동구이며, 직업은 간호사이고, 자산은 11462원이고, 가족 수는 4명이고, 성향은 2이고, 학력은 3입니다.',
      '나이가 20대인 여성이고, 주소는 강서구이며, 직업은 변호사이고, 자산은 1642662원이고, 가족 수는 2명이고, 성향은 1이고, 학력은 5입니다.']
customer = ['나이가 30대인 여성이고, 주소는 강동구이며, 직업은 은행원이고, 자산은 11552원이고, 가족 수는 3명이고, 성향은 1이고, 학력 대학교 졸업입니다.',
            '나이가 42세인 남성이고, 주소는 송파구이며, 직업은 회사원이고, 자산은 42000원이고, 가족 수는 2명이고, 성향은 5이고, 학력은 1입니다.',
            '나이가 52세인 남성이고, 주소는 강남구이며, 직업은 사업가이고, 자산은 172000원이고, 가족 수는 6명이고, 성향은 2이고, 학력은 4입니다.']

'''
1. 문장 similarity말고 다른 feature(별점)를 이용해서 prefer scoring
2. 한 customer에 대해 여러 pb가 붙게
'''




# 선호도 Matrix에서는 리스트를 절반으로 나누고 앞에 있는 것들이 PB의 Customer에 대한 선호도 리스트, 뒤에 있는 것들이 Customer의 PB에 대한 선호도 리스트
prefer = pb_customer_prefer(pb, customer)
print('prefer matrix:', prefer)

# Matching 결과에서는 각 리스트에서 앞에 있는 것이 Customer, 뒤에 있는 것이 PB
marriage = marriage_algo(prefer)


# 인덱스 맞추기
result = []
for match in marriage.stableMarriage():
    match[0] -= len(customer)
    result.append(match)


# print("Left: Customer의 번호 ", "Right: PB의 번호")
print("connection:", result)


# PB, Customer의 노드 ID 생성
pb_ids = [i for i in range(len(pb))]
customer_ids = [i for i in range(len(customer))]

connections = result


# # 시각화
# vis.draw_graph_streamlit(customer_ids, pb_ids, connections)