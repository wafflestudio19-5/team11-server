import csv
import requests

def f(filename, year, season):
    # 2022 - 1
    f = open(filename, 'r', encoding='utf-8')
    rdr = csv.reader(f)

    index = 0
    label =  ['교과구분', '개설대학', '개설학과', '이수과정', '학년', '교과목번호', '강좌번호', '교과목명', '부제명', '학점', '강의', '실습', '수업교시', '수업형태', '강의실(동-호)(#연건, *평창)', '주담당교수', '장바구니신청', '정원', '수강신청인원', '비고', '강의언어', '개설상태']
    for line in rdr:
        if index <= 2:
            pass
        else:
            dict_line = {}
            for i, j in zip(label, line):
                dict_line[i] = j

            data = {}

            data['subject_name'] = dict_line['교과목명'] #string
            data['professor'] = dict_line['주담당교수'] #string
            data['subject_code'] = dict_line['교과목번호'] #string
            data['year'] = year #int
            data['season'] = season #int
            data['college'] = dict_line['개설대학']
            data['department'] = dict_line['개설학과']

            data['grade'] = 0
            for i in range(10):
                if str(i) in dict_line['학년']:
                    data['grade'] = i
                    break

            LevelCode = {"학사": 1, "학석사통합": 2, "석사": 3, "석박사통합": 4, "박사": 5,
                         1: "학사", 2: "학석사통합", 3: "석사", 4: "석박사통합", 5: "박사"}

            data['level'] = LevelCode[dict_line['이수과정']]

            data['credit'] = int(dict_line['학점'])


            CategoryCode = {'교양': 1, '전선': 2, '전필': 3, '교직': 4, '대학원': 5, '논문': 6, '일선': 7, '공통': 8,
                            1: '교양', 2: '전선', 3: '전필', 4: '교직', 5: '대학원', 6: '논문', 7: '일선', 8: '공통'}

            data['category'] = CategoryCode[dict_line['교과구분']]

            data['number'] = int(dict_line['강좌번호'])

            data['detail'] = line[19]

            data['language'] = line[20]

            data['location'] = line[14]
            data['time'] = line[12]


            x = requests.put(url="http://127.0.0.1:8000/api/v1/lecture/", data=data)
            if x.status_code == 404:
                x = requests.post(url="http://127.0.0.1:8000/api/v1/lecture/", data=data)

            print("{0}년 {1}학기 {2}번 강의 status code: {3}".format(year, season, index, x.status_code))

            if x.status_code != 200:
                print(data)
                return False

        #print(content)
        index += 1
        #if index > 10:
        #    break


    f.close()
    return True


#f("강좌검색.csv", 2022, 1)
#f("강좌검색 (1).csv", 2021, 2)
#f("강좌검색 (2).csv", 2021, 1)
#f("강좌검색 (4).csv", 2020, 2)
list_ = [("강좌검색 (5).csv", 2020, 1), ("강좌검색 (6).csv", 2019, 2), ("강좌검색 (7).csv", 2019, 1), ("강좌검색 (8).csv", 2018, 2), ("강좌검색 (9).csv", 2018, 1)]
for i in list_:
    if not f(*i):
        break