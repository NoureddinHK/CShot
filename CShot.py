import mysql.connector


class SaveData():
    def __init__(self, host = "127.0.0.1", user = "root", password = "123456789", database = "rank_player_cshot"):
        self.host = host 
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None
    def connectToDatabase(self):
        self.conn = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database=self.database
        )
        self.cursor = self.conn.cursor()
        print("3*9")
    def Table(self):
        self.cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        point BIGINT
    )
    ''')
    def Register(self, name, point=0):
        self.cursor.execute('''
            INSERT INTO users (name, point)
            VALUES (%s, %s)
        ''', (name, point))
        self.conn.commit()




if __name__ == "__main__":
    db = SaveData()
    db.connectToDatabase()
    db.Table()
    db.Register("amin","66")
    print(True)


    