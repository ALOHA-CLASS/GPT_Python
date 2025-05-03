# 다중 조건문
# - 위에 나온 조건이 만족하지 않을 때, (if)
#   아래의 조건을 확인하고, (elif)
#   모두 만족하지 않으면 else 문을 실행한다.

score = input('성적 : ')
score = int(score)

if score >= 90:
    print('A 학점 입니다.')
elif score >= 80:
    print('B 학점 입니다.')
elif score >= 70:
    print('C 학점 입니다.')
elif score >= 60:
    print('D 학점 입니다.')
else:
    print('F 학점 입니다.')