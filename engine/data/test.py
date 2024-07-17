import pandas as pd

import copy

import matplotlib.pyplot as plt
plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False

# 데이터 불러오기
df = pd.read_csv('./matching_system/data/seoul_citizen.csv')

test_df = copy.deepcopy(df)

# 데이터 전처리
# Nan 값 fill
test_df = test_df.fillna(0)

# 60대 이상
test_df = test_df[test_df['생년월일'] <= 1964]

pd.set_option('display.max_columns', None)

print(test_df)


plt.scatter(test_df['자치구명'], test_df['총자산평가금액'])
plt.xlabel('자치구명')
plt.ylabel('총자산평가금액')
plt.xticks(rotation=90)
plt.show()


# 여 == 1, 남 == 0
test_df['성별'] = test_df['성별'].astype('category').cat.codes
test_df['자치구명'] = test_df['자치구명'].astype('category').cat.codes

