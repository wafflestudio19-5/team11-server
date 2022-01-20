import csv
import requests

def f(filename, year, season):
    # 2022 - 1
    f = open(filename, 'r', encoding='utf-8')
    rdr = csv.reader(f)

    index, dict = 0, {}

    field = ['교과구분', '개설대학', '개설학과', '이수과정', '학년', '교과목번호', '강좌번호', '교과목명', '부제명', '학점', '강의', '실습', '수업교시', '수업형태', '강의실(동-호)(#연건, *평창)', '주담당교수', '장바구니신청', '정원', '수강신청인원', '비고', '강의언어', '개설상태']
    for i in field:
        dict[i] = set()

    field_ = ['대학-학과', '장소-시간']
    for i in field_:
        dict[i] = set()

    for line in rdr:

        if index <= 2:
            pass
        else:
            for i in range(len(field)):
                dict[field[i]].add(line[i])

            dict['대학-학과'].add((line[1], line[2]))
            dict['장소-시간'].add((len(line[12].split('/')), len(line[14].split('/'))))

        #print(content)
        index += 1


    f.close()
    return dict

def mergeDict(x, y):
    for i in x:
        x[i] |= y[i]
    return x


d = f("강좌검색.csv", 2022, 1)
d = mergeDict(f("강좌검색 (1).csv", 2021, 2), d)
d = mergeDict(f("강좌검색 (2).csv", 2021, 1), d)
d = mergeDict(f("강좌검색 (4).csv", 2020, 2), d)
d = mergeDict(f("강좌검색 (5).csv", 2020, 1), d)
d = mergeDict(f("강좌검색 (6).csv", 2019, 2), d)
d = mergeDict(f("강좌검색 (7).csv", 2019, 1), d)
d = mergeDict(f("강좌검색 (8).csv", 2018, 2), d)
d = mergeDict(f("강좌검색 (9).csv", 2018, 1), d)
#print(s)

print(d['학년'])
print(d['이수과정'])
print(d['장소-시간'])
print()

'''
dict = {}

for i in d['대학-학과']:
    if i[0] not in dict:
        dict[i[0]] = set()
    dict[i[0]].add(i[1])

for i in dict:
    print(i, dict[i])
'''