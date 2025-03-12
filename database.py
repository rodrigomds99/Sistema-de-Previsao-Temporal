import sqlite3

class Database:
    def __init__(self):
        self.Connect_bd()
        self.Tables()

    def Connect_bd(self):
        self.conn = sqlite3.connect("Users.bd")
        self.cursor = self.conn.cursor()

    def Tables(self):
        self.Connect_bd()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            Username TEXT NOT NULL,
            Password TEXT NOT NULL
        )""")
