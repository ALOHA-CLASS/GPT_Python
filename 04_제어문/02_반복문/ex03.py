# 컬렉션 반복

# [] : 리스트
stars = ["마동석", "김태리", "박보검", "강하늘", "이정재"]
for star in stars:
    print(star)
print()
    
# () : 튜플
menu = ("라면", "샐러드", "돈까스", "제육볶음", "햄버거")
for food in menu:
    print('오늘 점심 메뉴는 : {}'.format( food ))
print()

# {} : 세트
mac_set = {"1955 버거", "고구마 프라이", "코카콜라"}
for item in mac_set:
    print("item : {}".format(item))
print()

# { "key" : "value" } : 딕셔너리
users = {
    "joeun1004" : "123456",
    "bogum93"   : "bogum1212",
    "admin"     : "admin2005"
}
for id, pw in users.items():
    print("아이디 : {}, 비밀번호 : {}".format( id, pw ))