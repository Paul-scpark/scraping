from selenium import webdriver # 파이썬 코드에 의해 조작되는 가상 웹 브라우져를 이용
from bs4 import BeautifulSoup
import math, csv, docx

doc = docx.Document() # word 파일로 저장
doc.save('example.docx')

driver = webdriver.Chrome('/usr/local/bin/chromedriver') # chrome driver 파일 다운로드 받고, 해당 디렉토리에 파일 저장해주기

target_link = [] # 세부적으로 접근해야 하는 link를 모두 저장할 list
for page_num in range(1, 4):
    URL = f'https://www.denverdoulos.org/?c=sermon/9&p={page_num}'

    driver.get(URL)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    link_lst = soup.select('#bbslist > table > tbody > tr > td.sbj > a')

    for link in link_lst:
        target_link.append(link['href'])

target_link.reverse() # 리스트 요소들을 역순으로 바꿔주기
for idx, link in enumerate(target_link):
    URL = 'https://www.denverdoulos.org' + link

    driver.get(URL)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.select_one('#bbsview > div.viewbox > div.subject').text

    if len(soup.select('#vContent > p')) != 0:
        for contents in soup.select('#vContent > p'):
            content_text = contents.text
    elif len(soup.select('#vContent > p')) == 0:
        content_text = soup.select_one('#vContent').text
 
    para = doc.add_paragraph()
    run = para.add_run(title)
    run = para.add_run(content_text)
    doc.save('example.docx')
    
    # if idx == 2: break

    print(idx)