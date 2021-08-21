import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import csv

#################################################
# 네이버 영화 - 현재 상영 중인 영화 리뷰 가져오기 #
#################################################

### 크롤링 하려고 하는 네이버 영화에 있는 현재 상영 중인 영화 링크의 규칙을 찾아보자.
## 확인해보니 마지막에 code= 이후의 값이 각 영화 별로 고유의 코드로 할당되어 있는 것을 볼 수 있다.
# https://movie.naver.com/movie/bi/mi/basic.nhn?code=189069
# https://movie.naver.com/movie/bi/mi/basic.nhn?code=188909
# https://movie.naver.com/movie/bi/mi/basic.nhn?code=185917

URL = 'https://movie.naver.com/movie/running/current.nhn'
response = requests.get(URL) # 네이버 영화 - 현재 상영 중 메인 페이지 가져오기

soup = BeautifulSoup(response.text, 'html.parser') # html 웹 코드로 불러오기

movie_list = soup.select( # html 웹 코드에 li 태그까지 접근 - 웹 코드들을 각각 리스트에 저장함.
    '#wrap > #container > #content > .article > .obj_section > .lst_wrap > ul > li'
)

movie_dic = {
    'movie_code': "", 
    'movie_name': ""
}

for movie in movie_list:
    a_tag = movie.select_one('.lst_dsc > .tit > a') # a 태그까지 접근한 것을 따로 a_tag 라는 변수에 할당
    movie_dic['movie_code'] = a_tag['href'][28:] # a 태그의 href에 있는 전체 링크에서 뒤에 code 번호에 해당하는 부분만 slicing
    movie_dic['movie_name'] = a_tag.get_text() # a 태그의 text인 영화 제목을 가져옴

    with open('movie_first0806.csv', 'a', newline='') as csvfile:
        fieldnames = ['movie_code', 'movie_name']
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csv_writer.writerow(movie_dic)

    print(movie_dic)