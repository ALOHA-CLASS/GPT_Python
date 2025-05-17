from bs4 import BeautifulSoup

html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset='utf-8'>
        <title>Test BeautifulSoup</title>
    </head>
    <body>
        <p id="first">First paragraph</p>
        <p class="myp">Second paragraph</p>
        <p id="third" class="myp">Third paragraph</p>
        <div id="container" class="box">Content in a div</div>
        
        <button class="btn">Button 1</button>
        <button class="btn">Button 2</button>
        <button class="btn">Button 3</button>
    </body>
    </html>
"""

# BeatifulSoup 객체 생성
bs = BeautifulSoup(html, 'html.parser')

# id 속성으로 선택
print('id="first" 인 p 태그 선택')
print(bs.find('p', id="first"))

# class 속성으로 선택
print('class="myp" 인 첫 번째 p 태그 선택')
print(bs.find('p', class_="myp"))

# class 속성으로 여러개 선택
buttons = bs.find_all('button', class_="btn")
print('class="btn" 인 여러 태그 선택')
for idx, btn in enumerate(buttons, 1) :
    print("{} : {}".format(idx, btn.get_text() ))
    
    
# id 와 class 를 동시에 선택
print('id="third" 이고, class="myp" 인 p 태그 선택')
print(bs.find('p', attrs={"id": "third", "class": "myp"}))

# id 로 div 태그 선택
print('id="container" 인 div 태그 선택')
div = bs.find('div', id="container")
print(div)