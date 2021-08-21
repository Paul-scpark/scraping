from selenium import webdriver # 파이썬 코드에 의해 조작되는 가상 웹 브라우져를 이용
from bs4 import BeautifulSoup
import math
import csv

driver = webdriver.Chrome(r'C:\Users\psc85\OneDrive\바탕 화면\1120_hisnet_data\chromedriver.exe')

url = 'https://hisnet.handong.edu/login/login.php'
driver.get(url)
delay = 3
driver.implicitly_wait(delay)

## 히즈넷 로그인
idBox = driver.find_element_by_xpath('''//*[@id=\"loginBoxBg\"]/table[2]/tbody/tr/td[5]/form/table/tbody/tr[3]/td/table/tbody/tr/td[1]/table/tbody/tr[1]/td[2]/span/input''')
idBox.send_keys('ID') # 히즈넷 아이디 입력하기
idBox = driver.find_element_by_xpath('''//*[@id=\"loginBoxBg\"]/table[2]/tbody/tr/td[5]/form/table/tbody/tr[3]/td/table/tbody/tr/td[1]/table/tbody/tr[3]/td[2]/input''')
idBox.send_keys('PASSWORD') # 히즈넷 비밀번호 입력하기
driver.find_element_by_xpath('''//*[@id=\"loginBoxBg\"]/table[2]/tbody/tr/td[5]/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/input''').click()


## 히즈넷 '일반공지'로 들어가서 모든 글들의 링크 저장하기
contents_link_list = [] # 글들의 링크들을 저장할 list 정의
for page in range(1, 81): # 1~80 페이지까지 접근
    driver.get(f'https://hisnet.handong.edu//myboard/list.php?Page={page}&Board=NB0001')
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    for num in range(17, 32): # 접근한 페이지에서 글들을 읽어오기(공지글 제외)
        contents = soup.select_one(f'body > table:nth-child(12) > tbody > tr:nth-child(2) > td > table > tbody > tr > td:nth-child(3) > table > tbody > tr:nth-child(3) > td > table > tbody > tr:nth-child(1) > td > table > tbody > tr:nth-child({num}) > td:nth-child(2) > a')
        contents_link_list.append(contents['href'])

## csv 파일에 저장할 데이터를 위한 dic 생성
hisnet_dic = {
    'contents': ""
}

## 저장한 링크들에 하나씩 접근해서 데이터 가져오기
for link in contents_link_list:
    URL = 'https://hisnet.handong.edu/myboard/' + link
    driver.get(URL)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    text = soup.select_one('body > table:nth-child(12) > tbody > tr:nth-child(2) > td > table > tbody > tr > td:nth-child(3) > table > tbody > tr:nth-child(3) > td > table:nth-child(5) > tbody > tr:nth-child(1) > td > table > tbody')
    hisnet_dic['contents'] = text.get_text().replace('\n', '')
    print(text.get_text().replace('\n', ''))

    # csv 파일로 데이터 저장
    # with open('hisnet_data.csv', 'a', newline = '', encoding = 'utf-8') as csvfile:
    #     fieldnames = ['contents']
    #     csv_writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    #     csv_writer.writerow(hisnet_dic)
