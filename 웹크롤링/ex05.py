# pip install BeautifulSoup4 lxml
from bs4 import BeautifulSoup

html = """
    <html>
        <head>
            <meta charset='utf-8'>
            <title>Test BeautifulSoup</title>
        </head>
        <body>
            <p align="center">P태그의 컨텐트</p>
            <img src="https://알클.com/img/logo.png" width="300">
            <ul>
                <li>테스트1<strong>강조</strong></li>
                <li>테스트2</li>
                <li>테스트3</li>
            </ul>
        </body>
    </html>
    """
bs = BeautifulSoup( html, 'html.parser' )
print(type(bs.title), ':', bs.title)                # title 태그
print(type(bs.title.name), ':', bs.title.name)      # title 태그명
print(type(bs.title.string), ':', bs.title.string)  # title 태그 컨텐츠

print('-'*100)

print(type(bs.p['align']), ':', bs.p['align'])
print(type(bs.img['src']), ':', bs.img['src'])
print(type(bs.img.attrs), ':', bs.img.attrs)
print(type(bs.img.attrs.get('src')), ':', bs.img.attrs.get('src'))
print(type(bs.img.attrs.get('width')), ':', bs.img.attrs.get('width'))

