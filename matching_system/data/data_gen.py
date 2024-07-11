import pandas as pd
import numpy as np
from faker import Faker

average_assets = {
    "의사": 3000000,
    "치과의사": 2800000,
    "약사": 1200000,
    "변호사": 2500000,
    "엔지니어": 1800000,
    "금융 분석가": 2300000,
    "투자 은행가": 4000000,
    "경영 컨설턴트": 2700000,
    "경영진": 5000000,
    "데이터 과학자": 2000000,
    "항공기 조종사": 2400000,
    "치과 위생사": 1500000,
    "대학 교수": 1800000,
    "건축가": 1700000,
    "연예인": 6000000,
    "프로 운동선수": 7000000,
    "부동산 개발자": 4500000,
    "기업가": 8000000,
    "의료 관리자": 2600000,
    "금융 관리자": 2700000,
    "마케팅 관리자": 1900000,
    "광고 임원": 2100000,
    "상업 파일럿": 2200000,
    "판사": 2800000,
    "보험 전문가": 1600000,
    "재무 계획사": 2000000,
    "IT 관리자": 2300000,
    "프로젝트 관리자": 1800000,
    "인공지능 연구자": 2200000,
    "생명 과학 연구자": 2000000
    "이외 직업": 8000
}


# 자산 데이터 생성 함수 (정규분포 기반)
def generate_asset(job):
    mean, std_dev = asset_stats.get(job, asset_stats['이외 직업'])
    asset_value = np.random.normal(mean, std_dev)
    return max(0, int(asset_value))  # 자산 값이 0 이하가 되지 않도록 설정

fake = Faker('ko-KR')

test_data = [(fake.name(), fake.pyint(min_value=60, max_value=90), fake.address(), fake.job()) for i in range(300)]

test_df = pd.DataFrame(test_data)
test_df.columns = ['name', 'age', 'address', 'job']

# 자산 데이터 생성 및 추가
test_df['asset'] = test_df['job'].apply(generate_asset)

test_df.to_csv('./matching_system/data/test_data.csv', index=False)