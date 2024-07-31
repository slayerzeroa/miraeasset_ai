from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import requests
from .matching_reason import *

# from sentence_transformers import SentenceTransformer


class marriage_algo():
    '''
    Stable Marriage Algorithm
    두 그룹 모두 가장 최선의 선택을 하는 경우에 안정적인 결과를 보장하는 알고리즘

    input: prefer matrix
    output: stable matching result
    '''
    def __init__(self, prefer):
        self.prefer = prefer
        self.N = len(prefer)//2
        self.wPartner = None
        self.mFree = None
        self.freeCount = None

    def wPrefersM1OverM(self, w, m, m1):
        for i in range(self.N):
            if (self.prefer[w][i] == m1):
                return True
            if (self.prefer[w][i] == m):
                return False


    def stableMarriage(self):
        self.wPartner = [-1 for _ in range(self.N)]
        self.mFree = [False for _ in range(self.N)]
        self.freeCount = self.N
        while (self.freeCount > 0):
            m = 0
            while (m < self.N):
                if (self.mFree[m] == False):
                    break
                m += 1
            i = 0
            while i < self.N and self.mFree[m] == False:
                w = self.prefer[m][i]
                if (self.wPartner[w - self.N] == -1):
                    self.wPartner[w - self.N] = m
                    self.mFree[m] = True
                    self.freeCount -= 1
    
                else: 

                    m1 = self.wPartner[w - self.N]

                    if (self.wPrefersM1OverM(w, m, m1) == False):
                        self.wPartner[w - self.N] = m
                        self.mFree[m] = True
                        self.mFree[m1] = False
                i += 1
        
        result = []
        for i in range(self.N):
            result.append([i + self.N, self.wPartner[i]])

        return result


# # Driver Code
# prefer = [[4, 5, 7, 6], [5, 7, 6, 4],
#           [4, 5, 6, 7], [5, 6, 4, 7],
#           [1, 0, 2, 3], [2, 1, 0, 3],
#           [3, 1, 2, 0], [2, 1, 3, 0]]

# marriage = marriage_algo(prefer)
# print("Left: Woman ", "Right: Man")
# print(marriage.stableMarriage())




# customer: [age, sex, address, job, asset, family_size, tendency, education]
# pb: 선호하는[age, sex, address, job, asset, family_size, tendency, education]

# def pb_customer_cosine_matching(pb:list, customer:list) -> list:
#     '''
#     PB와 Customer의 선호 Query를 비교하여 가장 유사한 매칭을 찾는 함수
#     '''
#     pb_vector = transformer_sentence_embedding(pb)
#     customer_vector = transformer_sentence_embedding(customer)
    
#     similarity_matrix = cosine_similarity(customer_vector, pb_vector)

#     # 코사인 유사도 매트릭스를 통해 각 고객과 가장 유사한 PB를 찾기
#     matches = []
#     for customer_idx, customer_similarities in enumerate(similarity_matrix):
#         pb_idx = np.argmax(customer_similarities)
#         matches.append((customer_idx, pb_idx, customer_similarities[pb_idx]))

#     return matches

def str2list(string:str) -> list:
    '''
    문자열을 리스트로 변환하는 함수
    '''
    return string.split(',')


def pb_customer_cosine_matching(pb_json:list, customer_json:list, rank:int=4) -> list:
    '''
    PB와 Customer의 선호 Query를 비교하여 가장 유사한 매칭을 찾는 함수
    rank는 상위 몇개를 뽑을지 선택
    input: pb_json, customer_json, rank
    output: matches (customer_idx, pb_idx, similarity)
    '''

    # PB 정보
    pb_vector = []
    pb_rating = []
    for pb in pb_json:
        pb_vector.append(list(map(float, str2list(pb['Embedding']))))
        pb_rating.append(float(pb['Rating']))
    # pb 별점
    pb_rating = np.array(pb_rating)

    customer_vector = [list(map(float, str2list(customer_json['Embedding'])))]

    similarity_matrix = cosine_similarity(customer_vector, pb_vector)
    # print(similarity_matrix)

    # 유사도 매트릭스에 별점을 곱하여 가중치 부여
    similarity_matrix = similarity_matrix * pb_rating

    # 코사인 유사도 매트릭스를 통해 각 고객과 가장 유사한 PB를 찾기
    matches = []
    for customer_idx, customer_similarities in enumerate(similarity_matrix):
        top_pb_indices = np.argsort(customer_similarities)[-rank:][::-1]  # 상위 4개의 인덱스
        for pb_idx in top_pb_indices:
            matches.append((customer_idx, pb_idx, customer_similarities[pb_idx]))

    return matches

pb_json = requests.get('http://ajoufe.iptime.org:5556/pb').json()
customer_json = requests.get('http://ajoufe.iptime.org:5556/customer').json()

customer_json = customer_json[2]

pb_vector = []
for pb in pb_json:
    pb_vector.append(list(map(float, str2list(pb['Embedding']))))

customer_vector = [list(map(float, str2list(customer_json['Embedding'])))]

import asyncio
import aiohttp

async def get_pb_data(matches):
    async def fetch_pb_data(session, match):
        part = pb_json[match[1] - 1]
        customer_sentence = customer_json['Description_Matching']
        pb_sentence = pb_json[match[1] - 1]['Description']
        reason = get_matching_reason(customer_sentence, pb_sentence)
        part['Reason'] = reason
        return part

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_pb_data(session, match) for match in matches]
        pb_data = await asyncio.gather(*tasks)

    pb_data = pd.DataFrame(pb_data)
    return pb_data

# def get_pb_data(matches):
#     pb_data = []
#     for match in matches:
#         part = pb_json[match[1]-1]
#         customer_sentence = customer_json['Description_Matching']
#         pb_sentence = pb_json[match[1]-1]['Description']
#         reason = get_matching_reason(customer_sentence, pb_sentence)
#         part['Reason'] = reason
#         pb_data.append(part)
        
#     pb_data = pd.DataFrame(pb_data)
#     return pb_data

def test_get_pb_data():
    matches = pb_customer_cosine_matching(pb_json, customer_json)
    print(get_pb_data(matches))
    return get_pb_data(matches)


async def async_get_pb_data():
    matches = pb_customer_cosine_matching(pb_json, customer_json)
    pb_data = await get_pb_data(matches)
    return pb_data

# asyncio.run(main())

# print(test_get_pb_data())

# print(pb_customer_cosine_matching(pb_json, customer_json))
# print(get_pb_data(pb_customer_cosine_matching(pb_json, customer_json)))

# def pb_customer_prefer(pb:list, customer:list) -> list:
#     '''
#     PB와 Customer의 선호 Query를 비교하여 선호도 벡터를 반환하는 함수
#     '''
#     pb_vector = transformer_sentence_embedding(pb)
#     customer_vector = transformer_sentence_embedding(customer)

#     similarity_matrix = cosine_similarity(customer_vector, pb_vector)
    
#     customer_matrix = []
#     pb_matrix = []
#     for similarity in similarity_matrix:
#         cosine_similarity_dict = {}
#         for idx, sim in enumerate(similarity):
#             cosine_similarity_dict[idx] = sim

#         sorted_dict = sorted(cosine_similarity_dict.items(), key=lambda x: x[1], reverse=True)
#         customer_matrix.append([idx for idx, sim in sorted_dict])
#         pb_matrix.append([idx for idx, sim in sorted_dict])

#     pb_matrix = (np.array(pb_matrix) + len(pb)).tolist()
    
#     result = []
#     result.extend(pb_matrix)
#     result.extend(customer_matrix)
#     return result




# def transformer_sentence_embedding(sentence)->list:
#     '''
#     문장 임베딩하는 함수
#     input: sentence (str or list)
#     output: embeddings (np.array)
#     '''
#     if type(sentence) == str:
#         sentence = [sentence] 
#     model = SentenceTransformer('distiluse-base-multilingual-cased')
#     embeddings = model.encode(sentence)
#     return embeddings


# def test():
#     customer = ['나이가 30대인 여성이고, 주소는 강동구이며, 직업은 은행원이고, 자산은 11552원이고, 가족 수는 3명이고, 성향은 1이고, 학력 대학교 졸업입니다.',
#                 '나이가 42세인 남성이고, 주소는 송파구이며, 직업은 회사원이고, 자산은 42000원이고, 가족 수는 2명이고, 성향은 5이고, 학력은 1입니다.',
#                 '나이가 52세인 남성이고, 주소는 강남구이며, 직업은 사업가이고, 자산은 1142000원이고, 가족 수는 6명이고, 성향은 2이고, 학력은 4입니다.']
#     pb = ['나이가 50대인 남성이고, 주소는 강남구이며, 직업은 회사원이고, 자산은 760000원이고, 가족 수는 3명이고, 성향은 3이고, 학력은 3입니다.',
#         '나이가 30대인 여성이고, 주소는 강동구이며, 직업은 간호사이고, 자산은 11462원이고, 가족 수는 4명이고, 성향은 2이고, 학력은 3입니다.',
#         '나이가 20대인 여성이고, 주소는 강서구이며, 직업은 변호사이고, 자산은 1642662원이고, 가족 수는 2명이고, 성향은 1이고, 학력은 5입니다.']
    
#     prefer = pb_customer_prefer(pb, customer)
#     marriage = marriage_algo(prefer)

#     # 인덱스 맞추기
#     result = []
#     for match in marriage.stableMarriage():
#         match[0] -= len(customer)
#         result.append(match)

#     # PB, Customer의 노드 ID 생성
#     pb_ids = [i for i in range(len(pb))]
#     customer_ids = [i for i in range(len(customer))]

#     connections = result

#     return pb_ids, customer_ids, connections


# # 고객이 원하는 PB에 대한 인상들, 조건들을 그냥 문장으로 설명하면
# # -> 문장을 Transformer Sentence Embedding? -> 벡터화하고
# # PB쪽에서 설문 돌려서 벡터화



# # 선호도 Matrix에서는 리스트를 절반으로 나누고 앞에 있는 것들이 PB의 Customer에 대한 선호도 리스트, 뒤에 있는 것들이 Customer의 PB에 대한 선호도 리스트
# matrix = pb_customer_prefer(customer, pb)
# print(matrix)

# # Matching 결과에서는 각 리스트에서 앞에 있는 것이 Customer, 뒤에 있는 것이 PB
# marriage = marriage_algo(matrix)
# print("Left: Customer의 번호 ", "Right: PB의 번호")
# print(marriage.stableMarriage())