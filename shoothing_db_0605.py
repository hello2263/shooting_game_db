import pymysql

# db연결
db = pymysql.connect(host="shooting-db.cgb6v3f3cnyt.us-east-2.rds.amazonaws.com",
                     user="", password="", charset="utf8")

cursor = db.cursor(pymysql.cursors.DictCursor)

cursor.execute('USE shooting_db;')

# 삽입
# cursor.execute('INSERT INTO Level1(name, score) VALUES ("황도규", 700)')

# 출력
cursor.execute('SELECT * FROM Level1;')
value = cursor.fetchall()
print(value[0])





#갱신
# cursor.execut('UPDATE lang SET descriptiom = "ZHTML is for the form web" WHERE name = "HTML"')

#삭제
# cursor.execute('DELETE FROM lang WHERE name="Java"')

db.commit()
db.close()