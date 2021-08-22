from selenium import webdriver # 파이썬 코드에 의해 조작되는 가상 웹 브라우져를 이용
from bs4 import BeautifulSoup
import math, csv, docx

doc = docx.Document() # word 파일로 저장
doc.save('example.docx')

driver = webdriver.Chrome('/usr/local/bin/chromedriver') # chrome driver 파일 다운로드 받고, 해당 디렉토리에 파일 저장해주기

target_link = [] # 세부적으로 접근해야 하는 link를 모두 저장할 list
for page_num in range(1, 6):
    URL = f'https://www.kpccoh.org/index.php?mid=sub02_01&search_target=title_content&search_keyword=%EC%82%AC%EB%8F%84%ED%96%89%EC%A0%84&page={page_num}&division=-18844&last_division=0'

    driver.get(URL)
    # delay = 3
    # driver.implicitly_wait(delay)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    href_lst = soup.select('#board_list > table > tbody > tr > .title > a')
    for href in href_lst:
        target_link.append(href['href'])

target_link.reverse() # 리스트 요소들을 역순으로 바꿔주기
for idx, link in enumerate(target_link): # 세부 페이지를 한 번씩 들어가서 데이터 scraping
    print(idx)
    
    URL = 'https://www.kpccoh.org' + link

    driver.get(URL)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    text_lst = soup.select('#content > div > div.board_read > div.read_body > div > p')

    for text in text_lst:
        para = doc.add_paragraph()
        run = para.add_run(text.text)
        doc.save('example.docx')