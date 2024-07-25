import requests
import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity

def request_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Fail to retrieve data. Status code : {response.status_code}")

def main():
    # 고객 데이터(첫 번째 데이터 기준)
    customer_data = request_url("http://ajoufe.iptime.org:5556/customer")[0]

    # 유튜브 데이터
    youtube_data = request_url("http://ajoufe.iptime.org:5556/youtube")

    cus_embedding = np.array([float(x) for x in customer_data['embedding'].split(',')]).reshape(1,-1)

    for item in youtube_data:
        item_embedding = np.array([float(x) for x in item['embedding'].split(',')]).reshape(1,-1)
        item['similarity'] = cosine_similarity(item_embedding, cus_embedding)[0][0]

    youtube_recommend_sorted = sorted(youtube_data, key = lambda x : x['similarity'], reverse = True)

    with open('./youtube_recommend_sorted.json', 'w', encoding = 'utf-8') as f:
        json.dump(youtube_recommend_sorted, f, ensure_ascii = False, indent = 4)
    print('Json파일로 저장되었습니다')

if __name__ == "__main__":
    main()