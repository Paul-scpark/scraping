import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import csv

################################################
# 광주 인공지능 사관학교 news 제목과 링크 크롤링 #
################################################

### 크롤링 하려고 하는 '광주인공지능사관학교' 검색 시 나오는 뉴스 주소의 규칙을 찾아보자.
## 확인해보니 중간에 start= 값을 기준으로 1, 11, 21 형식과 같이 페이지가 넘어가면서 10 단위씩 증가하는 것을 볼 수 있었다.
## 따라서 10 단위로 변화하는 값을 for문과 f string으로 접근한다.
# https://search.naver.com/search.naver?&where=news&query=%EA%B4%91%EC%A3%BC%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5%EC%82%AC%EA%B4%80%ED%95%99%EA%B5%90&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so:r,p:all,a:all&mynews=0&cluster_rank=47&start=1&refresh_start=0
# https://search.naver.com/search.naver?&where=news&query=%EA%B4%91%EC%A3%BC%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5%EC%82%AC%EA%B4%80%ED%95%99%EA%B5%90&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so:r,p:all,a:all&mynews=0&cluster_rank=81&start=11&refresh_start=0
# https://search.naver.com/search.naver?&where=news&query=%EA%B4%91%EC%A3%BC%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5%EC%82%AC%EA%B4%80%ED%95%99%EA%B5%90&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so:r,p:all,a:all&mynews=0&cluster_rank=94&start=21&refresh_start=0

soup_objects = []

for start_num in range(1, 100, 10):
    URL = f'https://search.naver.com/search.naver?&where=news&query=%EA%B4%91%EC%A3%BC%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5%EC%82%AC%EA%B4%80%ED%95%99%EA%B5%90&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so:r,p:all,a:all&mynews=0&cluster_rank=104&start={start_num}&refresh_start=0'
    
    response = requests.get(URL) ## 1부터 10 단위로 증가하며, 마지막 91까지 돌아가면서 전체 URL 코드를 response에 할당
    soup_objects.append(BeautifulSoup(response.text, 'html.parser')) ## response로 할당된 값에서 html 형식의 웹 코드를 각각 soup_objects라는 리스트에 할당
    ### 여기까지 하면 1페이지 부터 10페이지까지 전체 html 웹 코드를 soup_objects라는 리스트에 넣은 상태.

### 그 다음으로는 우리가 가지고 오고 싶은 뉴스의 제목과 링크를 가져오도록 하자.
## 이렇게 하기 위해서는 전체 html 웹 코드에서 뉴스의 제목과 링크를 가리키고 있는 웹 코드를 불러와야 할 것.

for soup in soup_objects: 
    news_section = soup.select( # soup_objects의 각 웹 코드에 li 태그까지 접근한 웹 코드를 news_section으로 할당 (리스트로 저장됨)
        '#wrap > #container > #content > #main_pack > div.news.mynews.section._prs_nws > ul > li' # 링크 오타 주의할 것.
    )

    news_dic = { # 가지고 온 기사의 제목과 링크를 dict에 넣을 수 있도록 미리 만듦.
        'title': "", 
        'link': ""
    }

    for news in news_section: # 1페이지 부터 10페이지까지 li 태그로 접근한 웹 코드에 접근
        if isinstance(news, NavigableString):
            continue
        if isinstance(news, Tag):
            a_tag = news.select_one('dl > dt > a') # li 태그에 더 나아가서 dl > dt > a 까지 접근
            news_dic['title'] = a_tag['title'] # a 태그에서 title 부분(기사 제목)을 할당
            news_dic['link'] = a_tag['href'] # a 태그에서 href 부분(기사 링크)을 할당
            ### {'title': '코로나19 여파에도 인공지능 사업 ‘착착’', 'link': 'http://news.kbs.co.kr/news/view.do?ncd=4506654&ref=A'} 이런 형태로 dict에 모두 담겨 있음.
        
        with open('news0806.csv', 'a', newline='') as csvfile: # newline을 통해서 csv 파일에서 자동으로 한 줄씩 띄우는 것을 방지
            fieldnames = ['title', 'link']
            csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            csv_writer.writerow(news_dic)

            print(news_dic)

            ### 해결 해야 할 것.
            # 1. csv 파일 저장이 아직 익숙하지 못한 것 같다.
            # 2. for문이 계속 돌아가고 있어서 csv 파일 첫 행에 header를 넣고 싶은데 어떻게 넣을 수 있을까?
            # 3. open에서 newline과 같은 문법들을 잘 기억하자.