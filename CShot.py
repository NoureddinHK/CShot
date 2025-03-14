import mysql.connector


class SaveData():
    def __init__(self, host = "127.0.0.1", user = "root", password = 123456789, database = "Project_Ap"):
        self.host = host 
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None
        