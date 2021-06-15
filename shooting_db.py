import pymysql

# 데이터 베이스 연결
# host = 아마존 RDS를 통해 SQL로 접속
# shooting_db를 사용 172.16.200.101
# 무조건 맨 처음 실행해줘야 하는 기본 함수이다
def db_connecting(id, key):
    global db, cursor
    db = pymysql.connect(host="localhost",
                         user=id, password=key)
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute('USE shooting;')
    if (cursor.execute("show status like 'Threads_connected';") == 1):
        print('shooting_db Connected')


# 데이터 삽입
# level로 테이블 선정
# name과 score 삽입 후
# score 내림차순으로 정렬
# 게임이 끝났을때 점수를 DB에 삽입하고 db_printing 함수와 같이 쓰인다
def db_inserting(level, name, score):
    cursor.execute("SELECT * FROM Level" + str(level) + " ORDER BY id DESC LIMIT 1")
    if ((cursor.execute("SELECT * FROM Level" + str(level) + " ORDER BY id DESC LIMIT 1")) == 0):
        final_id = 1
    else:
        final_id = cursor.fetchone()['id']
        final_id += 1
    data_loc = "INSERT INTO Level" + str(level) + "(id, name, score) "
    data_value = "VALUES ('" + str(final_id) +"', '" + str(name) + "', " + str(score) + ')'
    cursor.execute(data_loc + data_value)
    db.commit()
    if ((cursor.execute("show status like 'Handler_write'"))==1):
        print("data_insert Success")



# 데이터 검색
# level로 테이블 선택 후 name에 제일 최고점수를 출력
# 그 테이블 안에 등수도 출력
# 주로 자신의 최고 순위와 점수를 알고 싶을때 사용한다
def db_searching(level, name):
    cursor.execute("SELECT * FROM Level" + str(level) +" WHERE NAME = '" + str(name) +
                   "' ORDER BY id DESC LIMIT 1")
    final_id = cursor.fetchone()['id']
    rank = {}
    count = 1
    cursor.execute('SELECT * FROM Level' + str(level) + ' ORDER BY SCORE DESC')
    for i in cursor.fetchall():
        rank[i['id']] = count
        count += 1
    cursor.execute('SELECT MAX(SCORE) FROM Level' + str(level) + " GROUP BY NAME HAVING NAME = '"
                   +str(name)+"'")
    max_score = cursor.fetchall()[0]['MAX(SCORE)']
    print(name, "님의 최고 점수는", max_score, '점이며')
    print(rank.get(final_id), "위 입니다")



# 데이터 출력
# level로 플레이한 단계와 이름을 입력하면
# 현재 가장 최근 플레이한 점수와 순위가 나온다
# 이 말은 게임을 플레이하고 나서 게임이 종료되었을 때 실행시키면
# 그 게임의 점수와 순위가 나온다
def db_printing(level, name):
    cursor.execute("SELECT * FROM Level" + str(level) + " WHERE NAME = '" + str(name) +
                   "' ORDER BY id DESC LIMIT 1")
    final_id = cursor.fetchone()['id']
    rank = {}
    count = 1
    cursor.execute('SELECT * FROM Level' + str(level) + ' ORDER BY SCORE DESC')
    for i in cursor.fetchall():
        rank[i['id']] = count
        count += 1
    cursor.execute('SELECT SCORE FROM Level' + str(level) + " WHERE ID = " + str(final_id) +
                   " GROUP BY NAME HAVING NAME = '" + str(name) + "'")
    now_score = cursor.fetchall()[0]['SCORE']
    print(name, "님의 현재 점수는", now_score, '점이며')
    print(rank.get(final_id), "위 입니다")




# 테이블 생성
# level에 따른 테이블 생성
# 기본키는 id이며 name과 score 존재한다
def create_table(level):
    table = '''
        CREATE TABLE Level'''+ str(level) + ''' (
            id int(10) NOT NULL PRIMARY KEY,
            name varchar(255) NOT NULL,
            score int(10) NOT NULL
        )
        '''
    cursor.execute(table)
    db.commit()
    print("table Created")



# 테이블 삭제
# level에 따른 테이블 삭제
# 안에 있는 모든 데이터들이 삭제 된다
def delete_table(level):
    cursor.execute("DROP TABLE Level"+str(level))
    db.commit()
    print("table Deleted")


# 테이블 전체 조회
def printing_data(level):
    cursor.execute("SELECT * FROM Level" + str(level))
    #print(cursor.fetchall())
    return cursor.fetchall()

def printing_table():
    cursor.execute("SHOW TABLES")
    print(cursor.fetchall())

# 데이터 베이스 연결 해제
def db_disconnecting():
    db.close()

# db_connecting(db_user, db_password)       # db접속 항시 켜놓아야함

# create_table(2)                         # 테이블(level) 생성
# db_inserting(1, '황도규', 2000)          # 점수 삽입(level, name, score)
# db_printing(1, '황도규')                 # 최근 게임의 점수, 순위 출력 (level, name)
# db_searching(1, '황도규')                # 해당 난이도의 자신의 최고 점수 및 순위 출력 (level, name)
# data = printing_data(1)                        # 테이블(level)내 모든 데이터 출력
# print(data[0]['name'])
# printing_table()                        # 테이블 목록 출력
# delete_table(1)                         # 테이블(level) 삭제
# db.close()                                # db탈출 마지막에 꼭 있어야함




### db_connecting으로 DB와 연결
### 게임이 클리어 된 후에 db_insterting 으로 DB에 해당 게임의 점수와 이름 삽입
### 게임 후 결과창에는 db_printing 으로 금방 플레이한 게임의 점수와 순위 출력
### 순위 조회창에서는 db_searching 으로 자신의 최고 점수와 순위 출력
### db.close() 로 DB의 사용을 중지3