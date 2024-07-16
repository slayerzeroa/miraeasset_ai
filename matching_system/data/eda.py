import pandas as pd
from sentence_transformers import SentenceTransformer
# 워드클라우드
from wordcloud import WordCloud


df = pd.read_csv('./matching_system/data/survey_result.csv')
print(df)