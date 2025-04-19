'''
    커피 1잔을 300원
    자판기에 금액을 입력하고
    커피의 잔 수에 따라서 남은 금액을 출력하세요.
    
    1400원
    커피 1잔, 1100원
    커피 2잔, 800원
    커피 3잔, 500원
    커피 4잔, 200원
'''
money = input('입력 금액 : ')
money = int(money)

i = 0
while money >= 300 :
    money = money - 300     # 남은 금액
    i = i + 1               # 구입 잔수
    print('커피 {}잔, 잔돈 {}'.format(i, money))
    