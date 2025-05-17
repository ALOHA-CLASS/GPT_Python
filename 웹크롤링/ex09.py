import ssl
import urllib.request
from bs4 import BeautifulSoup

# URL 요청하여 HTML 가져오기
url = "https://www.cgv.co.kr/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}
# SSL 인증 무시
# 낮은 DH 키도 허용하는 보안 설정
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
context.set_ciphers("DEFAULT:@SECLEVEL=1")  # 핵심 부분

req = urllib.request.Request(url, headers=headers)
response = urllib.request.urlopen(req, context=context)
html = response.read().decode('utf-8')

# bs 객체 생성
soup = BeautifulSoup(html, "html.parser")

# 선택자를 사용하여 영화 제목 지정
movie_list = soup.select('#movieChart_list .movieName')

# 영화 제목 리스트 출력
if movie_list:
    for i, movie_name in enumerate(movie_list, 1):
        print("{}. {}".format(i, movie_name.get_text() ))
else:
    print('영화 제목이 HTML 에 없습니다.')
