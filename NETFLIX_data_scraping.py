## 개요
# 2020.08.25
# 광주 인공지능사관학교 - 추천 알고리즘 및 NLP 관련 미니 프로젝트(김준태 강사님)
# PART1 - 데이터 크롤링

## 서비스 목표
# 사용자의 취향에 맞는 영화를 컨텐츠 기반 필터링 알고리즘을 이용하여 추천해주도록 한다.
# 이를 위하여 넷플릭스 데이터를 사용한다.
# 이 코드는 '넷플릭스 데이터를 크롤링' 하는 코드

import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import csv

i = 0

# 넷플릭스 영화의 장르별 크롤링을 위해 코드를 가지고 옴
codes = [11714, 34399, 839338, 72404, 1365, 7442, 
         7424, 783, 67673, 6548, 5763, 8711, 8883, 1492, 8933]

for code in codes: # 각 코드별로 돌아가면서 모든 데이터들 크롤링
    url = f'https://www.netflix.com/kr/browse/genre/{code}'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    movies = (soup.select( # 각 영화들의 a 태그 내용들을 list 형태로 불러와서 movies로 저장
        '''#appMountPoint > div > div.nm-collections-page > 
        div.nm-collections-container > div > .nm-collections-row > .nm-content-horizontal-row > ul > li > a''')
    )

    movie_list = []

    for movie in movies: # 각 a 태그 내용들로 접근 = 리스트 벗겨주기

        cookies = {
            'nfvdid': 'BQFmAAEBEMBeegIovbtH7I3zmWiinXlA-6_KAQmtgtu44QRYahdb7ppzBVnDt97TUjePO72wlVvz86ZOISCXX70TJuXmKEQss-lYsOml7APEo6d8UZF1eg%3D%3D',
            'memclid': '3bb94aec-9966-4e7e-8816-a7d4d5561b15',
            'flwssn': 'e9a5ad72-a32b-423b-8d80-bfe828426b2d',
            'clSharedContext': '9353b96c-3e40-4c8f-b18d-3645cbcc6e79',
            'SecureNetflixId': 'v%3D2%26mac%3DAQEAEQABABR4DU4Dc-awWU6TblOXy26zbuYMm2SmS3c.%26dt%3D1598459637127',
            'NetflixId': 'v%3D2%26ct%3DBQAOAAEBELXyGn_k6Abmm_qSPlw2cPmBEP2__CMQ2HOj625gI2gv9h9cD89h7DlRW6j8sSwh6mGnL4dHizwOoL1xJ7PmSv9rl8qREm_snhlvr-OIOY_S5Noxdrv5Cd6ef5ovfjZ1rP7ZdJRC_oalJ3vZhbpoItj9eOzbik0j69d_q_doWFK2Y2WNzo9-cm4KuqC2KRi-da6kXx5FdJcUFq6qH6SkUV6nSv8Zjh-H_xurML1xsvuSQ3u-9bzdeJHhHSpAVjOUjWxrHSHgzTZzdTyxynETMW_oRQIM3wFnG3YdK_g3YzG7xeiOuVnATD3YTgHCso-AkL0lCmnLmWKSZvggDXFT30BfTSZWVKZA-4Dy5wSshON96SxxKK9-D9stCkUcXmoCnVUT%26bt%3Ddev%26mac%3DAQEAEAABABTPJb6RZm6MmXJImscDALJnYWPWLQzt-1c.',
            'cL': '1598460729811%7C159845963963576889%7C159845963942151729%7C%7C29%7Cundefined',
        }

        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://www.netflix.com/kr/browse/genre/34399',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        }

        movie_code = movie['href'].split('title/')[1] # a 태그에서 href를 가지고 와서 'title/'을 기점으로 나눠서 뒤에 있는 각 영화들의 코드들을 가져오기

        response = requests.get(f'https://www.netflix.com/kr/title/{movie_code}', headers=headers, cookies=cookies)
        soup = BeautifulSoup(response.text, 'html.parser')

        mains = soup.select('#section-hero > div.hero-container > div.info-container > div.details-container')
        details = soup.select('#section-more-details')

        for main in mains: 
            title = (main.select_one('.title-info > h1').get_text()) # 영화들의 제목
            summary = (main.select_one('div > div.title-info-synopsis-talent > div.title-info-synopsis').get_text()) # 영화들의 줄거리
        
        for detail in details: # 영화들의 
            genre = detail.select_one('div.more-details-container > div.more-details-cell.cell-genres > div.more-details-item-container').get_text() # 영화들의 장르
            
            if detail.select_one('div.more-details-container > div.more-details-cell.cell-mood-tag > div.more-details-item-container') == None: # 예외처리
                pass
            else: # 영화들의 특징
                feature = detail.select_one('div.more-details-container > div.more-details-cell.cell-mood-tag > div.more-details-item-container').get_text()
        
        movie_dict = {
            'title': title,
            'summary': summary,
            'genre': genre,
            'feature': feature
        }

        i += 1

        # 데이터 나오는 것 확인
        # print(i)
        # print(movie_dict)

        # movie_list.append(movie_dict)

        with open('final_netflix.csv', 'a', newline='', encoding='utf8') as csvfile: # newline을 통해서 csv 파일에서 자동으로 한 줄씩 띄우는 것을 방지
            fieldnames = ['title', 'summary', 'genre', 'feature']
            csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            csv_writer.writerow(movie_dict)