import mysql.connector


class SaveData():
    def __init__(self, host = "127.0.0.1", user = "root", password = "123456789", database = "rank_player_cshot"):
        self.host = host 
        self.user = user
        self.password = password
        self.database = database
        self.conn = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database=self.database
        )
        self.cursor = self.conn.cursor()
    def Table(self):                      #ساخت جدول برای ثبت اطلاعات
        self.cursor.execute('''
    CREATE TABLE IF NOT EXISTS leaderboard (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        point BIGINT
    )
    ''')
    def Register(self, name, point=0):     #ثبت کردن اطلاعات بازیکن
        self.cursor.execute('''
            INSERT INTO leaderboard (name, point)
            VALUES (%s, %s)
        ''', (name, point))
        self.conn.commit()
    def repeatName(self, name, point):    #اگر اسم تکراری باشد امتیاز گرفته شده را اضافه میکند به امتیاز قبلی
        self.cursor.execute('SELECT * FROM leaderboard')
        users = self.cursor.fetchall()
        for user in users:
            if user[1] == name:
                CurrentScore = user[2]
                newScore = CurrentScore + point
                self.cursor.execute('''
                UPDATE leaderboard
                SET point = %s
                WHERE name = %s '''
                , (newScore, name))
                self.conn.commit()



if __name__ == "__main__":
    P1 = SaveData()
    P1.Table()
    P1.Register("saeed",36)
    P1.repeatName("saeed",100)
    


    