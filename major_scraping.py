## 광주인공지능사관학교 Warm-up Project (Team - DOYA)
## 커리어넷에서 전공 관련된 정보들을 크롤링하자!
## 2020.09.09

import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import csv

major_link = [] # 각 전공 별로의 href를 할당하기 위한 list
major_big = []

for page in range(1, 53):
    URL = f'https://www.career.go.kr/cnet/front/base/major/FunivMajorList.do?pageIndex={page}' # 1~52 페이지까지 있는 커리어넷의 홈페이지 특성에 따라 URL 할당

    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    soup_section = soup.select('#view1 > ul > li')
    
    for data in soup_section:
        a_tag = data.select_one('a')['href'] 
        major_link.append(a_tag) # 1~52페이지까지 돌면서 각 전공들의 구체적인 내용들이 담겨 있는 href를 가지고 와서 major_link라는 리스트에 저장
        # len(major_link)는 516개 = 커리어넷에 있는 전공의 개수

major_dic = { # csv 파일에 넣기 위해서 dic를 만듦
    'major': "", 
    'major_describe': ""
}

for link in major_link: # 각 전공의 link에 들어가서 데이터들을 가져옴
    major_small = [] # 초기화

    URL = 'https://www.career.go.kr' + link

    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.select_one('#contents > #frm > .word_tit > h2').text
    detail = soup.select('#tab1 > .word_ul')
    
    for i in detail:
        major_small.append(i.text.replace('\n', '').replace('\r', '')) # 전공과 관련된 설명 부분들을 모두 모아서 major_small 이라는 작은 list에 저장
    
    major_dic['major'] = title # 전공 이름
    major_dic['major_describe'] = major_small # 전공 설명

    with open('careernet_major.csv', 'a', newline='') as csvfile: # for문이 한번 실행 될때마다 하나의 전공을 한 행씩 저장하는 csv 파일 생성
        fieldnames = ['major', 'major_describe']
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csv_writer.writerow(major_dic)
    
    print(111)