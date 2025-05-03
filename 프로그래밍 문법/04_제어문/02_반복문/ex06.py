# 가위바위보 게임
import random
choices = ["가위","바위","보"]
win = True

while win:
    computer = random.choice(choices)  # 리스트 요소 중 하나를 랜덤 선택
    user = input("가위, 바위, 보 중 하나를 입력해주세요 : ")
    print("컴퓨터 : {}".format(computer))
    print("사용자 : {}".format(user))

    win1 = (user == "가위" and computer == "보")
    win2 = (user == "바위" and computer == "가위")
    win3 = (user == "보" and computer == "바위")

    if user == computer:
        win = True
        print("비겼습니다!")
    elif win1 or win2 or win3:
        win = True
        print("이겼습니다!")
    else:
        win = False
        print("졌습니다!")