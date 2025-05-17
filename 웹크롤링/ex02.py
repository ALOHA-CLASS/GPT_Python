import urllib.request
url = "https://xn--pe5b27r.com/"

# URL 요청
res = urllib.request.urlopen(url)

# 응답 헤더
print("[ header 정보] ----------")
res_header = res.getheaders()
for s in res_header :
    print(s)

# 내용 출력
print("[ 내용 정보] ----------")
html = res.read().decode('utf-8')
print(html)
