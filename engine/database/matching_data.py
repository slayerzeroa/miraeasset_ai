import pandas as pd
from sentence_transformers import SentenceTransformer
import os
import urllib.parse as up
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.types import Integer, String, Float, Text
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import torch  # 올바른 PyTorch import 문


def generate_pb_info(pb_data):
    # 모든 정보를 한 문장으로 결합
    full_info = (
        f"PB는 {pb_data['Location']}에 거주하는 {pb_data['Age']}세 {pb_data['Gender']}입니다. "
        f"전문 분야는 {pb_data['Speciality']}입니다. "
        f"선호하는 고객 그룹은 {pb_data['Preferred_client_group']}입니다. "
        f"선호하는 투자 주제는 {pb_data['Preferred_Investment_Topics']}입니다. "
        f"리스크 성향은 {pb_data['Risk_Tolerance']}이며, 선호하는 투자 규모는 {pb_data['Preferred_Size']:,}원입니다."
    )
    
    return full_info

def generate_customer_info_for_pb(customer_data):
    # 모든 정보를 한 문장으로 결합
    full_info = (
        f"고객은 {customer_data['Location']}에 거주하는 {customer_data['Age']}세 {customer_data['Gender']}입니다. "
        f"직업은 {customer_data['Job']}이며, 투자 성향은 {customer_data['Investment_Horizon']}입니다. "
        f"선호하는 투자 주제는 {customer_data['Preferred_Investment_Topics']}이며, "
        f"리스크 성향은 {customer_data['Risk_Tolerance']}입니다. "
        f"선호하는 투자 유형은 {customer_data['Preferred_Investment_Types']}이고, "
        f"투자 금액은 {customer_data['Investment_Amount']:,}원입니다."
    )
    
    return full_info



def generate_customer_info(customer_data):
    # 모든 정보를 한 문장으로 결합
    full_info = (
        f"고객은 {customer_data['Location']}에 거주하는 {customer_data['Age']}세 {customer_data['Gender']}입니다. "
        f"직업은 {customer_data['Job']}이며, 금융 이해도는 {customer_data['Financial_Literacy_Level']}입니다. "
        f"투자 성향은 {customer_data['Investment_Horizon']}이며, 리스크 성향은 {customer_data['Risk_Tolerance']}입니다. "
        f"선호하는 투자 유형은 {customer_data['Preferred_Investment_Types']}입니다. "
        f"총 투자 금액은 {customer_data['Investment_Amount']}원입니다. "
        f"과거 투자 경험은 {customer_data['Past_Investment_Experience']} 수준입니다. "
        f"선호하는 투자 주제는 {customer_data['Preferred_Investment_Topics']}입니다. "
        f"포트폴리오는 다음과 같습니다: 채권 {customer_data['Portfolio_Bonds']}, 주식 {customer_data['Portfolio_Stocks']}, 부동산 {customer_data['Portfolio_House']}, 현금 {customer_data['Portfolio_Savings']}, 펀드 {customer_data['Portfolio_Funds']}입니다."
    )
    
    return full_info


def get_sentence_embedding(sentence: str):
    '''
    리스트 벡터를 문자열로 만드는 함수
    '''
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    embedding = model.encode(sentence)
    
    # 리스트 벡터를 문자열로 변환하면서 \n 제거
    embedding_str = ','.join(map(str, embedding))
    
    return embedding_str

def str2list(data):
    result = data[1:-1]
    return result

'''
Customer Data str to list
- Preferred_Investment_Types
- Preferred_Investment_Topics

PB Data str to list
- Speciality
- Preferred_client_group
- Preferred_Investment_Topics
'''

def load():
    customer_data = pd.read_csv('C:/Users/slaye/VscodeProjects/miraeasset-ai/engine/data/matching_customer_data.csv')
    pb_data = pd.read_csv('C:/Users/slaye/VscodeProjects/miraeasset-ai/engine/data/matching_pb_data.csv')

    customer_data['Preferred_Investment_Types'] = customer_data['Preferred_Investment_Types'].apply(lambda x: x[1:-1])
    customer_data['Preferred_Investment_Topics'] = customer_data['Preferred_Investment_Topics'].apply(lambda x: x[1:-1])
    pb_data['Speciality'] = pb_data['Speciality'].apply(lambda x: x[1:-1])
    pb_data['Preferred_client_group'] = pb_data['Preferred_client_group'].apply(lambda x: x[1:-1])
    pb_data['Preferred_Investment_Topics'] = pb_data['Preferred_Investment_Topics'].apply(lambda x: x[1:-1])

    customer_data.columns = ['index', 'Age', 'Gender', 'Location', 'Job', 'Financial_Literacy_Level', 'Investment_Horizon', 'Risk_Tolerance', 'Preferred_Investment_Types', 'Investment_Amount', 'Past_Investment_Experience', 'Preferred_Investment_Topics', 'Portfolio_Savings', 'Portfolio_Bonds', 'Portfolio_Stocks', 'Portfolio_House', 'Portfolio_Funds']

    return customer_data, pb_data


def make_customer_table(df):
    '''
    데이터베이스에 고객 테이블을 만드는 함수.
    '''
    print("Updating customer table to DataBase...")

    # Load environment variables
    load_dotenv()
    _GOGH_USER = os.environ.get("DB_USER")
    _GOGH_PASSWORD = os.environ.get("DB_PASSWORD")
    _GOGH_ADDRESS = os.environ.get("DB_ADDRESS")
    _GOGH_PORT = '3306'
    _GOGH_DB = os.environ.get("DB_NAME")
    _GOGH_URL = f'mysql+pymysql://{_GOGH_USER}:{up.quote_plus(_GOGH_PASSWORD)}@{_GOGH_ADDRESS}:{_GOGH_PORT}/{_GOGH_DB}?charset=utf8mb4'
    ENGINE = create_engine(_GOGH_URL, echo=False, pool_recycle=3600, poolclass=NullPool)

    # Define data types for columns
    dtype = {
        "Age": Integer(),
        "Gender": String(length=10),
        "Location": String(length=20),
        "Job": String(length=100),
        "Financial_Literacy_Level": Text(),
        "Investment_Horizon": Text(),
        "Risk_Tolerance": Text(),
        "Preferred_Investment_Types": Text(),
        "Investment_Amount": Integer(),
        "Past_Investment_Experience": Text(),
        "Preferred_Investment_Topics": Text(),
        "Portfolio_Savings": Float(),
        "Portfolio_Bonds": Float(),
        "Portfolio_Stocks": Float(),
        "Portfolio_House": Float(),
        "Portfolio_Funds": Float(),
        "Description": Text(),
        "Embedding": Text()
    }

    # Save dataframe to the database
    df.to_sql("customer", ENGINE, if_exists='append', index=False, dtype=dtype)
    print("Database update complete!")

def make_pb_table(df):
    '''
    데이터베이스에 고객 테이블을 만드는 함수.
    '''
    print("Updating pb table to DataBase...")

    # Load environment variables
    load_dotenv()
    _GOGH_USER = os.environ.get("DB_USER")
    _GOGH_PASSWORD = os.environ.get("DB_PASSWORD")
    _GOGH_ADDRESS = os.environ.get("DB_ADDRESS")
    _GOGH_PORT = '3306'
    _GOGH_DB = os.environ.get("DB_NAME")
    _GOGH_URL = f'mysql+pymysql://{_GOGH_USER}:{up.quote_plus(_GOGH_PASSWORD)}@{_GOGH_ADDRESS}:{_GOGH_PORT}/{_GOGH_DB}?charset=utf8mb4'
    ENGINE = create_engine(_GOGH_URL, echo=False, pool_recycle=3600, poolclass=NullPool)

    # Define data types for columns
    dtype = {
        "Age": Integer(),
        "Gender": String(length=10),
        "Location": String(length=200),
        "Speciality": Text(),
        "Preferred_client_group": Text(),
        "Preferred_Investment_Topics": Text(),
        "Risk_Tolerance": Text(),
        "Preferred_Size": Integer(),
        "Description": Text(),
        "Embedding": Text()
    }

    # Save dataframe to the database
    df.to_sql("pb", ENGINE, if_exists='append', index=False, dtype=dtype)
    print("Database update complete!")


def make_news_table(df):
    '''
    데이터베이스에 고객 테이블을 만드는 함수.
    '''
    print("Updating news table to DataBase...")

    # Load environment variables
    load_dotenv()
    _GOGH_USER = os.environ.get("DB_USER")
    _GOGH_PASSWORD = os.environ.get("DB_PASSWORD")
    _GOGH_ADDRESS = os.environ.get("DB_ADDRESS")
    _GOGH_PORT = '3306'
    _GOGH_DB = os.environ.get("DB_NAME")
    _GOGH_URL = f'mysql+pymysql://{_GOGH_USER}:{up.quote_plus(_GOGH_PASSWORD)}@{_GOGH_ADDRESS}:{_GOGH_PORT}/{_GOGH_DB}?charset=utf8mb4'
    ENGINE = create_engine(_GOGH_URL, echo=False, pool_recycle=3600, poolclass=NullPool)

    # Define data types for columns
    dtype = {
        "Keyword": Text(),
        "Title": Text(),
        "Text": Text(),
        "Url": Text(),
        "Date": Text(),
    }

    # Save dataframe to the database
    df.to_sql("news", ENGINE, if_exists='append', index=False, dtype=dtype)
    print("Database update complete!")





# 고객 설명과 임베딩 생성
def generate_data():
    customer_data, pb_data = load()
    customer_data['Description'] = customer_data.apply(generate_customer_info, axis=1)
    customer_data['Embedding'] = customer_data['Description'].apply(lambda x: get_sentence_embedding(x))
    customer_data['Description_Matching'] = customer_data.apply(generate_customer_info_for_pb, axis=1)
    customer_data['Embedding_Matching'] = customer_data['Description_Matching'].apply(lambda x: get_sentence_embedding(x))
    
    pb_data['Description'] = pb_data.apply(generate_pb_info, axis=1)
    pb_data['Embedding'] = pb_data['Description'].apply(lambda x: get_sentence_embedding(x))

    customer_data.to_csv('fix_embedding_matching_customer_data.csv', index=False)
    pb_data.to_csv('fix_embedding_matching_pb_data.csv', index=False)

    make_customer_table(customer_data.iloc[:, 1:])
    make_pb_table(pb_data.iloc[:, 1:])

pd.set_option('display.max_columns', None)
df = pd.read_json("C:/Users/slaye/VscodeProjects/miraeasset-ai/engine/data/news_crawling_sorted.json")
df = df.iloc[:, 1:]
df.columns = ['Keyword', 'Title', 'Text', 'Url', 'Date']
make_news_table(df)



# generate_data()

# # customer_data = pd.read_csv('engine/data/fix_embedding_matching_customer_data.csv')
# # pb_data = pd.read_csv('engine/data/fix_embedding_matching_pb_data.csv')

# # make_customer_table(customer_data.iloc[:, 1:])
# # make_pb_table(pb_data.iloc[:, 1:])

# # customer_data, pb_data = load()

# # pd.set_option('display.max_columns', None)
# # # print(customer_data)
# # print(pb_data)

# # pd.set_option('display.max_columns', None)

# # customer_data, pb_data = load()
# # # print(customer_data.head())
# # print(generate_customer_info(customer_data.iloc[0]))
# # print(generate_pb_info(pb_data.iloc[0]))
