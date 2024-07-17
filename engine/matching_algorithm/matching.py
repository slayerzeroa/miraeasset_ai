from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd

from sentence_transformers import SentenceTransformer


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

def pb_customer_cosine_matching(pb:list, customer:list) -> list:
    '''
    PB와 Customer의 선호 Query를 비교하여 가장 유사한 매칭을 찾는 함수
    '''
    pb_vector = transformer_sentence_embedding(pb)
    customer_vector = transformer_sentence_embedding(customer)
    
    similarity_matrix = cosine_similarity(customer_vector, pb_vector)

    # 코사인 유사도 매트릭스를 통해 각 고객과 가장 유사한 PB를 찾기
    matches = []
    for customer_idx, customer_similarities in enumerate(similarity_matrix):
        pb_idx = np.argmax(customer_similarities)
        matches.append((customer_idx, pb_idx, customer_similarities[pb_idx]))

    return matches


def pb_customer_prefer(pb:list, customer:list) -> list:
    '''
    PB와 Customer의 선호 Query를 비교하여 선호도 벡터를 반환하는 함수
    '''
    pb_vector = transformer_sentence_embedding(pb)
    customer_vector = transformer_sentence_embedding(customer)

    similarity_matrix = cosine_similarity(customer_vector, pb_vector)
    
    customer_matrix = []
    pb_matrix = []
    for similarity in similarity_matrix:
        cosine_similarity_dict = {}
        for idx, sim in enumerate(similarity):
            cosine_similarity_dict[idx] = sim

        sorted_dict = sorted(cosine_similarity_dict.items(), key=lambda x: x[1], reverse=True)
        customer_matrix.append([idx for idx, sim in sorted_dict])
        pb_matrix.append([idx for idx, sim in sorted_dict])

    pb_matrix = (np.array(pb_matrix) + len(pb)).tolist()
    
    result = []
    result.extend(pb_matrix)
    result.extend(customer_matrix)
    return result




def transformer_sentence_embedding(sentence)->list:
    '''
    문장 임베딩하는 함수
    input: sentence (str or list)
    output: embeddings (np.array)
    '''
    if type(sentence) == str:
        sentence = [sentence] 
    model = SentenceTransformer('distiluse-base-multilingual-cased')
    embeddings = model.encode(sentence)
    return embeddings



# # 고객이 원하는 PB에 대한 인상들, 조건들을 그냥 문장으로 설명하면
# # -> 문장을 Transformer Sentence Embedding? -> 벡터화하고
# # PB쪽에서 설문 돌려서 벡터화

# customer = ['나이가 30대인 여성이고, 주소는 강동구이며, 직업은 은행원이고, 자산은 11552원이고, 가족 수는 3명이고, 성향은 1이고, 학력 대학교 졸업입니다.',
#             '나이가 42세인 남성이고, 주소는 송파구이며, 직업은 회사원이고, 자산은 42000원이고, 가족 수는 2명이고, 성향은 5이고, 학력은 1입니다.',
#             '나이가 52세인 남성이고, 주소는 강남구이며, 직업은 사업가이고, 자산은 1142000원이고, 가족 수는 6명이고, 성향은 2이고, 학력은 4입니다.']
# pb = ['나이가 50대인 남성이고, 주소는 강남구이며, 직업은 회사원이고, 자산은 760000원이고, 가족 수는 3명이고, 성향은 3이고, 학력은 3입니다.',
#       '나이가 30대인 여성이고, 주소는 강동구이며, 직업은 간호사이고, 자산은 11462원이고, 가족 수는 4명이고, 성향은 2이고, 학력은 3입니다.',
#       '나이가 20대인 여성이고, 주소는 강서구이며, 직업은 변호사이고, 자산은 1642662원이고, 가족 수는 2명이고, 성향은 1이고, 학력은 5입니다.']


# # 선호도 Matrix에서는 리스트를 절반으로 나누고 앞에 있는 것들이 PB의 Customer에 대한 선호도 리스트, 뒤에 있는 것들이 Customer의 PB에 대한 선호도 리스트
# matrix = pb_customer_prefer(customer, pb)
# print(matrix)

# # Matching 결과에서는 각 리스트에서 앞에 있는 것이 Customer, 뒤에 있는 것이 PB
# marriage = marriage_algo(matrix)
# print("Left: Customer의 번호 ", "Right: PB의 번호")
# print(marriage.stableMarriage())