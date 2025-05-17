import urllib.request
from bs4 import BeautifulSoup

# URL 요청
url = "https://entertain.daum.net/news/movie"
response = urllib.request.urlopen(url)
html = response.read().decode('utf-8')
# print(html)
# 파싱
soup = BeautifulSoup(html, 'html.parser')

# 헤드라인 추출
# headlines = soup.find_all("a", 
#                           attrs={
#                                 "data-tiara-layer": "right photo_tv photo",
#                                 "class": "link_txt"    
#                                 })

# 선택자를 이용하여 추출
# 선택자 기호
# id    : #
# class : .
headlines = soup.select('#mAside .link_txt')

# 반복 출력
for i, headlines in enumerate(headlines, 1):
    print("{}. {}".format(i, headlines.get_text() ))
