# 20명을 5명씩 4개조로 만들기 - shuffle() 함수 사용

import random

list = [
        '정국','뷔','지민','리사','제니','카리나','장원영','안유진','태용',
        '이병헌','송강호','전도연','김태리','박서준','한소희','정해인',
        '아이린','최수영','신현지','김조은'
        ]


random.shuffle(list)

# 리스트 슬라이싱 - 5명씩 쪼개기
# team1 = list[0:5]           # 0 1 2 3 4
# team2 = list[5:10]          # 5 6 7 8 9
# team3 = list[10:15]         # 10 11 12 13 14
# team4 = list[15:20]         # 15 16 17 18 19
# team_list = [team1, team2, team3, team4]

# 리스트 내포를 사용하여 5명씩 쪼개기
team_list = [ list[i:i+5] for i in range(0, 20, 5) ]

# enumerate
for team in enumerate( team_list, 1):
    print('{}조 : {}'.format(team[0], team[1]))

