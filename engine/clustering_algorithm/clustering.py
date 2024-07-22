import sklearn.cluster as cluster
from sklearn.mixture import GaussianMixture
from hmmlearn.hmm import GaussianHMM

import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

import copy

import matplotlib.pyplot as plt
plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False


# 데이터 불러오기
df = pd.read_csv('./engine/data/seoul_citizen.csv')


# 데이터 전처리
# Nan 값 fill
df = df.fillna(0)



# 60대 이상
df = df[df['생년월일'] <= 1964]

# 여 == 1, 남 == 0
df['성별'] = df['성별'].astype('category').cat.codes

# # categorical -> numerical
# df['자치구명'] = df['자치구명'].astype('category').cat.codes

# # EDA
# plt.scatter(df['자치구명'], df['가구_순자산평가금액'])
# plt.xlabel('자치구명')
# plt.ylabel('총자산평가금액')
# plt.xticks(rotation=90)
# plt.show()


def initialise_model(model, params):
    for parameter, value in params.items():
        setattr(model, parameter, value)
    return model

pd.set_option('display.max_columns', None)

print(df)



'''
1. 인지욕구 - 연령과 주관적 건강 상태
2. 가용자원 -  배우자 및 자녀 유무, 가구총소득, 고용 상태, 가구순자산, 현재 거주하고 있는 주거의 자가 여부
3. 소인특성 - 성별과 교육수준


가구총소득, 가구순자산 (로그변환)
'''

# 원하는 Feature만 추출 (독립변수)
test_df = df[['생년월일', '1인가구여부', '가구_추정연소득', '직업군', '가구_순자산평가금액', '자가거주여부', '성별']]


test_df['가구_추정연소득'] = np.log(test_df['가구_추정연소득'])
test_df['가구_순자산평가금액'] = np.log(test_df['가구_순자산평가금액'])

x = test_df.values
scaler = StandardScaler()
x = scaler.fit_transform(x)




'''
주성분 개수 설정

# for i in range(2, len(test_df.columns)):
#     pca = PCA(n_components=i) # 주성분을 몇개로 할지 결정
#     pca.fit_transform(x)
#     print(f"n_components:{i}", sum(pca.explained_variance_ratio_))

n_components:2 0.4975591653399979
n_components:3 0.6708352306191852
n_components:4 0.8359416432160702
n_components:5 0.9453835332913266
n_components:6 1.0

-> 주성분 4개로 설정
'''
pca = PCA(n_components=4)
printcipalComponents = pca.fit_transform(x)
principalDf = pd.DataFrame(data=printcipalComponents)

visualize_df = copy.deepcopy(test_df)

# 데이터 클러스터링
# PCA GMM
params = {'n_components':3, 'covariance_type': 'full', 'max_iter': 1000, 'n_init': 30,'init_params': 'kmeans', 'random_state':10, 'reg_covar': 1e-6, 'tol': 1e-3}
gaussian = initialise_model(GaussianMixture(), params).fit(principalDf)
y_pred = gaussian.predict(principalDf)

visualize_df['cluster'] = y_pred


visualize_df['자치구명'] = df['자치구명']
print(visualize_df['cluster'].value_counts())
# 자치구명
scatter = plt.scatter(visualize_df['자치구명'], visualize_df['가구_순자산평가금액'], c=visualize_df['cluster'])
plt.title('PCA GMM Clustering')
plt.xlabel('자치구명')
plt.ylabel('순자산평가금액')
plt.xticks(rotation=90)
plt.legend(handles=scatter.legend_elements()[0], labels=set(y_pred), title="Cluster")
plt.show()


# cluster 결과 비율 확인


# No PCA GMM
params = {'n_components':3, 'covariance_type': 'full', 'max_iter': 1000, 'n_init': 30,'init_params': 'kmeans', 'random_state':10, 'reg_covar': 1e-6, 'tol': 1e-3}
gaussian = initialise_model(GaussianMixture(), params).fit(test_df)
y_pred = gaussian.predict(test_df)

visualize_df['cluster'] = y_pred
print(visualize_df['cluster'].value_counts())

scatter = plt.scatter(visualize_df['자치구명'], visualize_df['가구_순자산평가금액'], c=visualize_df['cluster'])
plt.title('GMM Clustering')
plt.xlabel('자치구명')
plt.ylabel('순자산평가금액')
plt.xticks(rotation=90)
plt.legend(handles=scatter.legend_elements()[0], labels=set(y_pred), title="Cluster")
plt.show()


# KMeans
params = {'n_clusters':3, 'init': 'k-means++', 'n_init': 10, 'max_iter': 3000, 'random_state': 10}
kmeans = initialise_model(cluster.KMeans(), params).fit(test_df)

y_pred = kmeans.predict(test_df)
visualize_df['cluster'] = y_pred
print(visualize_df['cluster'].value_counts())

scatter = plt.scatter(visualize_df['자치구명'], visualize_df['가구_순자산평가금액'], c=visualize_df['cluster'])
plt.title('KMeans Clustering')
plt.xlabel('자치구명')
plt.ylabel('순자산평가금액')
plt.xticks(rotation=90)
plt.legend(handles=scatter.legend_elements()[0], labels=set(y_pred), title="Cluster")
plt.show()



# PCA KMeans
params = {'n_clusters':3, 'init': 'k-means++', 'n_init': 10, 'max_iter': 3000, 'random_state': 10}
kmeans = initialise_model(cluster.KMeans(), params).fit(principalDf)

y_pred = kmeans.predict(principalDf)
visualize_df['cluster'] = y_pred
print(visualize_df['cluster'].value_counts())

scatter = plt.scatter(visualize_df['자치구명'], visualize_df['가구_순자산평가금액'], c=visualize_df['cluster'])
plt.title('PCA KMeans Clustering')
plt.xlabel('자치구명')
plt.ylabel('순자산평가금액')
plt.xticks(rotation=90)
plt.legend(handles=scatter.legend_elements()[0], labels=set(y_pred), title="Cluster")
plt.show()