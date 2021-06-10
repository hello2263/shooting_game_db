import pymysql

db_user = ""
db_password = ""

# 데이터 베이스 연결
# host = 아마존 RDS를 통해 SQL로 접속
# shooting_db를 사용
def db_connecting(id, key):
    global db, cursor
    db = pymysql.connect(host="shooting-db.cgb6v3f3cnyt.us-east-2.rds.amazonaws.com",
                         user=id, password=key, charset="utf8")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute('USE shooting_db;')
    if (cursor.execute("show status like 'Threads_connected';") == 1):
        print('shooting_db Connected')



# 데이터 삽입
# level로 테이블 선정
# name과 score 삽입 후
# score 내림차순으로 정렬
def db_inserting(level, name, score):
    cursor.execute("SELECT * FROM Level2 ORDER BY id DESC LIMIT 1")
    final_id = cursor.fetchone()['id']
    final_id += 1
    data_loc = "INSERT INTO Level" + str(level) + "(id, name, score) "
    data_value = "VALUES ('" + str(final_id) +"', '" + str(name) + "', " + str(score) + ')'
    cursor.execute(data_loc + data_value)
    db.commit()
    if ((cursor.execute("show status like 'Handler_write'"))==1):
        print("data_insert Success")



#데이터 검색
#level로 테이블 선택 후 name에 제일 최고점수를 출력
#그 테이블 안에 등수도 출력
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
    max = cursor.fetchall()[0]['MAX(SCORE)']
    print(name, "님의 최고 점수는", max, '점이며')
    print(rank.get(final_id), "위 입니다")


#테이블 생성
#level에 따른 테이블 생성
#기본키는 id이며 name과 score 존재
def create_table(level):
    table = '''
        CREATE TABLE Level2'''+ str(level) + ''' (
            id int(10) NOT NULL PRIMARY KEY,
            name varchar(255) NOT NULL,
            score int(10) NOT NULL
        )
        '''
    cursor.execute(table)
    db.commit()
    print("table Created")


db_connecting(db_user, db_password) #DB에 접속할 ID와 패스워드
create_table(3)                     #3에 해당하는 Level 테이블 생성
db_inserting(2, '이세현', 3000)      #Level2 테이블에 이세현 3000점 삽입
db_searching(2, '황도규')            #Level2 테이블에서 황도규의 최고 점수와 최고 순위 출력
db.close()

