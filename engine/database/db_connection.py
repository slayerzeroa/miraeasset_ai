import os
import urllib.parse as up
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.types import Integer, String, Float, Text
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import torch  # 올바른 PyTorch import 문

# GPU 사용 확인
def check_gpu_availability():
    if torch.cuda.is_available():
        print("GPU is available!")
        return torch.device('cuda')
    else:
        print("GPU is not available, using CPU instead.")
        return torch.device('cpu')

# GPU 장치 설정
device = check_gpu_availability()

def make_table(df, table_name):
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
        "CustomerID": Integer(),
        "Age": Integer(),
        "Gender": String(length=10),
        "Location": String(length=20),
        "Occupation": String(length=50),
        "Financial_Literacy_Level": String(length=20),
        "Investment_Horizon": String(length=50),
        "Risk_Tolerance": String(length=50),
        "Preferred_Investment_Types": String(length=50),
        "Investment_Amount": Integer(),
        "Past_Investment_Experience": String(length=50),
        "Preferred_Investment_Topics": String(length=50),
        "Savings_Account": Float(),
        "Bonds": Float(),
        "Stocks": Float(),
        "description": Text(),
        "embedding": Text()
    }

    # Save dataframe to the database
    df.to_sql(table_name, ENGINE, if_exists='append', index=False, dtype=dtype)
    print("Database update complete!")

def update_youtube_table(df):
    '''
    데이터베이스에 youtube table을 업데이트하는 함수.
    '''
    print("Updating expressions to DataBase...")

    load_dotenv()
    _GOGH_USER = os.environ.get("DB_USER")
    _GOGH_PASSWORD = os.environ.get("DB_PASSWORD")
    _GOGH_ADDRESS = os.environ.get("DB_ADDRESS")
    _GOGH_PORT = '3306'
    _GOGH_DB = os.environ.get("DB_NAME")
    _GOGH_URL = f'mysql+pymysql://{_GOGH_USER}:{up.quote_plus(_GOGH_PASSWORD)}@{_GOGH_ADDRESS}:{_GOGH_PORT}/{_GOGH_DB}?charset=utf8mb4'
    _GOGH_TABLE_NAME = 'expressions'
    ENGINE = create_engine(_GOGH_URL, echo=False, pool_recycle=3600, poolclass=NullPool)

    df.to_sql(_GOGH_TABLE_NAME, ENGINE, if_exists='append', index=False)
    print("initializing done!")

def get_sentence_embedding(sentence: str):
    '''
    리스트 벡터를 문자열로 만드는 함수
    '''
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2').to(device)
    embedding = model.encode(sentence)
    
    # 리스트 벡터를 문자열로 변환하면서 \n 제거
    embedding_str = ','.join(map(str, embedding))
    
    return embedding_str

def transfrom_string_to_vector(str_vector:str):
    '''
    문자열 벡터를 리스트 벡터로 변환하는 함수
    '''
    return [float(x) for x in str_vector.split()]

# 고객 특징 설명 글 생성
def generate_customer_description(customer_data):
    description = (
        f"이 고객은 {customer_data['Location']}에 거주하는 {customer_data['Age']}세의 {customer_data['Gender']}입니다. "
        f"현재 직업은 {customer_data['Occupation']}이며, 금융 이해도는 {customer_data['Financial_Literacy_Level']} 수준입니다. "
        f"투자 기간은 {customer_data['Investment_Horizon']}으로, 위험 감수 성향은 {customer_data['Risk_Tolerance']}입니다. "
        f"주로 선호하는 투자 유형은 {customer_data['Preferred_Investment_Types']}이며, 현재 투자 가능한 금액은 {customer_data['Investment_Amount']}만원입니다. "
        f"과거 투자 경험은 {customer_data['Past_Investment_Experience']} 수준이며, 선호하는 투자 주제는 {customer_data['Preferred_Investment_Topics']}입니다. "
        f"현재 자산 구성 비율은 저축 계좌에 {customer_data['Savings_Account']*100}%, 채권에 {customer_data['Bonds']*100}%, 주식에 {customer_data['Stocks']*100}%로 분포되어 있습니다."
    )
    return description

# 고객 설명과 임베딩 생성
def generate_customer_data(df):
    # 모델 불러오기 및 GPU 설정
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2').to(device)
    
    df['description'] = df.apply(generate_customer_description, axis=1)
    df['embedding'] = df['description'].apply(lambda x: get_sentence_embedding(x))
    df = df[df.columns[1:]]
    return df



'''유튜브 데이터베이스 업데이트'''
df = pd.read_csv('./engine/data/youtube_data.csv')
df = df.drop(df.columns[0], axis=1)
df['embedding'] = df['embedding'].apply(lambda x: x[1:-1])
print(df)
make_table(df, 'youtube')


# # pd.set_option('display.max_columns', None)
# '''고객 데이터베이스 업데이트'''
# df = pd.read_csv('./engine/data/customer_data.csv') 
# df = generate_customer_data(df)
# print(df)

# make_table(df, 'customer')