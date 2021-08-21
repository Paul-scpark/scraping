import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import csv

#################################################
# 네이버 영화 - 현재 상영 중인 영화 리뷰 가져오기 #
#################################################
### PART 1

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

movie_data = []

for movie in movie_list:
    a_tag = movie.select_one('.lst_dsc > .tit > a') # a 태그까지 접근한 것을 따로 a_tag 라는 변수에 할당
    movie_code = a_tag['href'][28:] # a 태그의 href에 있는 전체 링크에서 뒤에 code 번호에 해당하는 부분만 slicing
    movie_name = a_tag.get_text() # a 태그의 text인 영화 제목을 가져옴

    movie_dic = {
    'movie_code': movie_code, 
    'movie_name': movie_name
    }

    movie_data.append(movie_dic)

print(movie_data)

#################################################
# 네이버 영화 - 현재 상영 중인 영화 리뷰 가져오기 #
#################################################
### PART 2

### 우리가 가지고 오고 싶은 리뷰 부분의 network 부분에서 해당하는 cURL 링크를 copy 하고, trillworks 홈페이지에서 파이썬 코드로 가지고 옴.
for code in movie_data:
    code = code['movie_code'] # 영화 코드들을 code 라는 변수에 할당
    
    headers = {
        'authority': 'movie.naver.com',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Mobile Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'iframe',
        'referer': 'https://movie.naver.com/movie/bi/mi/point.nhn?code=189069',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': 'NNB=B6FX6KQ3ZL7F4; NRTK=ag#20s_gr#4_ma#2_si#2_en#2_sp#2; MM_NEW=1; NFS=2; MM_NOW_COACH=1; _fbp=fb.1.1595206974291.497284452; _ga=GA1.1.1836849414.1595206901; _ga_4BKHBFKFK0=GS1.1.1595206900.1.1.1595207054.60; nx_ssl=2; nid_inf=-1371309247; NID_AUT=Yjdzh3it3AQ3wyzYhhCxgJbxSYZgeGf4dD7SKxdwEpAxB1w08QCcT8v6a93UL3I/; NID_JKL=S12Hej+/XdG+5/Ay4Iwyvp4PMmVLDfiq6fCNZeCTKk8=; BMR=s=1596768551383&r=https%3A%2F%2Fm.blog.naver.com%2FPostView.nhn%3FblogId%3Ddesenyeo%26logNo%3D221752387817%26categoryNo%3D0%26proxyReferer%3Dhttps%3A%252F%252Fwww.google.com%252F&r2=https%3A%2F%2Fwww.google.com%2F; _naver_usersession_=IGa7pY9/NuwvL43xpxgYyA==; NID_SES=AAABhB8XIbyvanHma6ZnUfWhQrwJZRfhyElSEfGv/UWMS25hG7p7/6TibmZBzgpZPubHUrDTTnD44Giyss/FF/jL1DHDI0xymq/XrHhtQZc2t3XHHkVN7GbqDNd8RBudDI8FhAN8mNwOJSV4pHEXRIK2fUA5U6vY8m2BfeE6sHFsVNE8P6k759QaZeOernNVjYNIDWzLauKZ9oh4LmMu9vwK/J4GQkveXYmemyExysbSywdKjgaqDVI08QCRRSlFiYTPkKItqKfrRDisRzefkL1S//qY2bH044Q3+1OkOa4YYNEenCe3Gc+qzmdd7RUzbzWoYC3WBZM58S3C6NmN0EFmQK2W3x+QixBV8wkcljkETgXOz339nB5+F4oE+oP0+7SHwLlM5gTwDZ+ScvbWYs0j/zaRxYS9HfALRUK5EhN0HTd8/wn/cth2c2TQo5N4Nx8ky75x5zntKVcNij/NW4lrI53Gwi8tsNIloIF4ec2y6CBIUnsf8JBkX1Wo95S6b/JMA/C7nRof5LUpLeZwGGr8Za4=; page_uid=UyzaZwp0JXVssCShRZCssssss4G-289217; csrf_token=d1f1ee38-2536-49cf-9425-028bcada15fb',
    }

    params = (
        ('code', code), ## 여기서는 code 부분이 각 영화별로 수정이 되어야 하기 때문에 특정 code가 아닌 위에서 할당한 movie_dic에서의 code를 가지고 옴.
        ('type', 'after'),
        ('isActualPointWriteExecute', 'false'),
        ('isMileageSubscriptionAlready', 'false'),
        ('isMileageSubscriptionReject', 'false'),
    )

    response = requests.get('https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn', headers=headers, params=params)

    reveiew_soup = BeautifulSoup(response.text, 'html.parser') # 리뷰 부분이 담긴 웹 코드를 response로 불러왔고, 이를 html 코드로 담아옴.

    review_list = reveiew_soup.select( # 리뷰 부분부터 li 태그까지 접근한 코드를 review_list라는 리스트로 할당함.
        '.score_result > ul > li' # 각각의 li 태그에는 한 영화에 대한 10명의 네티즌들의 관람평이 적혀있음.
    )

    num = 0 # 규칙 특성상 #_filtered_ment_ 부분에서 0부터 1씩 늘어나는 부분을 f string 처리하기 위한 변수

    for review in review_list:
        score = review.select_one('.star_score > em').text # em 태그의 text에 담겨 있는 관람객의 평점을 score로 가지고 옴.

        ## 관람평의 길이에 따라서 한 번더 #_unfold_ment로 들어가는 경우가 있으므로 예외처리를 해줌.
        if review.select_one(f'.score_reple > p > #_filtered_ment_{num} > #_unfold_ment{num}') is None: # 짧은 경우
            netizen_review = review.select_one(f'.score_reple > p > #_filtered_ment_{num}').text.strip()
        elif review.select_one(f'.score_reple > p > #_filtered_ment_{num} > #_unfold_ment{num}'): # 긴 경우
            netizen_review = review.select_one(f'.score_reple > p > #_filtered_ment_{num} > #_unfold_ment{num} > a')['data-src'] # 긴 경우의 코드 접근

        num += 1

        print(score, netizen_review)