import mysql.connector


class SaveData():
    def __init__(self, host = "localhost", user = "root", password = "123456789", database = "`rank_player_cshot"):
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
    def Table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS rank (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                point INT NOT NULL
        )
        ''')
    def Register(self, name, point=0):
        self.cursor.execute('''
        INSERT INTO rank (name, point) VALUES (%s, %s)
        ''', (name, point))
        self.conn.commit()




if __name__ == "__main__":
    db = SaveData()
    db.connectToDatabase()
    db.Table()
    db.Register("Ali", 25)


    