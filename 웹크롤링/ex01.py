import urllib.request
# URL 요청
res = urllib.request.urlopen("https://www.naver.com/")

# 응답 읽기
html = res.read().decode("utf-8")

# 출력
print(html)
