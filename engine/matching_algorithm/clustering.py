import sklearn.cluster as cluster
from sklearn.mixture import GaussianMixture
from hmmlearn.hmm import GaussianHMM

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False


# 데이터 불러오기
df = pd.read_csv('./matching_system/data/seoul_citizen.csv')


# 데이터 전처리
# Nan 값 fill
df = df.fillna(0)



# 60대 이상
df = df[df['생년월일'] <= 1964]

# 여 == 1, 남 == 0
df['성별'] = df['성별'].astype('category').cat.codes


plt.scatter(df['자치구명'], df['총자산평가금액'])
plt.xlabel('자치구명')
plt.ylabel('총자산평가금액')
plt.xticks(rotation=90)
plt.show()


# # categorical -> numerical
# df['자치구명'] = df['자치구명'].astype('category').cat.codes


def initialise_model(model, params):
    for parameter, value in params.items():
        setattr(model, parameter, value)
    return model

pd.set_option('display.max_columns', None)

print(df)


test_df = df[['자치구명', '순자산평가금액', '성별', '카드소비금액']]

# # categorical -> numerical
# test_df['자치구명'] = test_df['자치구명'].astype('category').cat.codes




# # 데이터 클러스터링

# # GMM
# params = {'n_components':5, 'covariance_type': 'full', 'max_iter': 1000, 'n_init': 30,'init_params': 'kmeans', 'random_state':10, 'reg_covar': 1e-6, 'tol': 1e-3}
# gaussian = initialise_model(GaussianMixture(), params).fit(test_df)
# y_pred = gaussian.predict(test_df)

# test_df['cluster'] = y_pred

# test_df['자치구명'] = df['자치구명']

# plt.scatter(test_df['자치구명'], test_df['순자산평가금액'], c=test_df['cluster'])
# plt.xlabel('자치구명')
# plt.ylabel('순자산평가금액')
# plt.xticks(rotation=90)
# plt.show()


# # KMeans
# params = {'n_clusters':5, 'init': 'k-means++', 'n_init': 10, 'max_iter': 3000, 'random_state': 10}
# kmeans = initialise_model(cluster.KMeans(), params).fit(test_df)

# y_pred = kmeans.predict(test_df)

# test_df['cluster'] = y_pred

# test_df['자치구명'] = df['자치구명']

# plt.scatter(df['자치구명'], df['총자산평가금액'], c=df['cluster'])
# plt.xlabel('자치구명')
# plt.ylabel('순자산평가금액')
# plt.xticks(rotation=90)
# plt.show()