from selenium import webdriver
from tqdm import tqdm_notebook
from bs4 import BeautifulSoup, NavigableString, Tag
import pandas as pd
import numpy as np
import time, requests, csv

i = 0

# 넷플릭스 영화의 장르별 크롤링을 위해 코드를 가지고 옴
codes = [11714, 34399, 839338, 72404, 1365, 7442, 
         7424, 783, 67673, 6548, 5763, 8711, 8883, 1492, 8933]

driver = webdriver.Chrome('chromedriver')

for code in codes:
    url = f'https://www.netflix.com/kr/browse/genre/{code}'
    driver.get(url)
    
    # url의 웹 페이지를 가져오기
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    
    # 각 영화들의 a 태그 내용들을 list 형태로 불러와서 movies로 저장
    movies = soup.select('#appMountPoint > .basicLayout.browseTitlesGallery.dark > .nm-collections-page > .nm-collections-container > .nm-collections-row > div > ul > li > a') 
    
    movie_list = []
    for movie in movies: # 각 a 태그 내용들로 접근하기
        # a 태그에서 href를 가지고 와서 'title/'을 기점으로 나눠서 뒤에 있는 각 영화들의 코드들을 가져오기
        movie_code = movie['href'].split('title/')[1] 
        
        URL = f'https://www.netflix.com/kr/title/{movie_code}'
        driver.get(URL)
        
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        
        # 넷플릭스 페이지에 접근하여 각 컨텐츠의 제목과 줄거리, 장르 등의 데이터를 가져오기
        mains = soup.select('#section-hero > div.hero-container > div.info-container > div.details-container')
        details = soup.select('#section-more-details')

        for main in mains: 
            title = (main.select_one('.title-info > h1').get_text()) # 영화들의 제목
            try:
                summary = (main.select_one('div > div.title-info-synopsis-talent > div.title-info-synopsis').get_text()) # 영화들의 줄거리
            except:
                continue
        
        for detail in details: 
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
        print(i)

        if i < 10: print(movie_dict)

        # movie_list.append(movie_dict)

        with open('final_netflix.csv', 'a', newline='', encoding='utf8') as csvfile: # newline을 통해서 csv 파일에서 자동으로 한 줄씩 띄우는 것을 방지
            fieldnames = ['title', 'summary', 'genre', 'feature']
            csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            csv_writer.writerow(movie_dict)
