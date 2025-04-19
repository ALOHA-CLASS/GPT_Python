# range() 함수
# : 범위를 생성하는 함수
# * 구조        : range( 초기값, 종료값+1, 증감치 )

# range(5)      : 0 1 2 3 4
# range(1, 11)  : 1 2 3 4 5 6 7 8 9 10
# range(1,10,2) : 1 3 5 7 9

# 1~10 까지 반복하여 출력
for n in range(1, 11):
    print(n, end=" ")
print()

# 단을 입력받아서 구구단 출력
dan = input("단  : ")
dan = int(dan)
for n in range(1, 10):
    print('{} x {} = {}'.format(dan, n, dan*n))
