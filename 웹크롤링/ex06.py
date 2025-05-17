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
print("----- 컨텐츠 추출 -----")
print("[[[ string 속성 ]]]")
print(type(bs.p.string), ':', bs.p.string)
print(type(bs.ul.string), ':', bs.ul.string)
print(type(bs.ul.li.string), ':', bs.ul.li.string)
print(type(bs.ul.li.strong.string), ':', bs.ul.li.strong.string)

print("[[[ text 속성 ]]]")
print(type(bs.p.text), ':', bs.p.text)
print(type(bs.ul.text), ':', bs.ul.text)
print(type(bs.ul.li.text), ':', bs.ul.li.text)
print(type(bs.ul.li.strong.text), ':', bs.ul.li.strong.text)

print("[[[ contents 속성 ]]]")
print(type(bs.p.contents), ':', bs.p.contents)
print(type(bs.ul.contents), ':', bs.ul.contents)
print(type(bs.ul.li.contents), ':', bs.ul.li.contents)
print(type(bs.ul.li.strong.contents), ':', bs.ul.li.strong.contents)
