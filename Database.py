import sqlite3


class DatabaseHands(object):
    def __init__(self, database):
        self.conn = sqlite3.connect(database)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS hands"
                         + "(id INTEGER PRIMARY KEY, first INTEGER,"
                         + "second INTEGER, third INTEGER)")
        self.conn.commit()

    def count(self):
        self.cur.execute("SELECT count(*) FROM hands")
        rows = self.cur.fetchone()
        return rows[0]

    def insert(self, hands):
        self.cur.executemany("INSERT INTO hands VALUES (NULL,?,?,?)", hands)
        self.conn.commit()

    # def view(self):
    #     self.cur.execute("SELECT * FROM hands")
    #     rows = self.cur.fetchall()
    #     return rows

    def search(self, id):
        self.cur.execute("SELECT * FROM hands WHERE id=?", (id,))
        row = self.cur.fetchone()
        return (row[1], row[2], row[3])

    def __del__(self):
        self.conn.close()


class DatabaseProbability(object):
    def __init__(self, database):
        self.conn = sqlite3.connect(database)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS probabilities"
                         + "(id INTEGER PRIMARY KEY, card INTEGER,"
                         + "win REAL, draw REAL, lose REAL)")
        self.conn.commit()

    def insert(self, probabilities):
        self.cur.executemany("INSERT INTO probabilities VALUES (NULL,?,?,?,?)",
                             probabilities)
        self.conn.commit()

    # def view(self):
    #     self.cur.execute("SELECT * FROM probabilities")
    #     rows = self.cur.fetchall()
    #     return rows

    def search(self, card):
        self.cur.execute("SELECT * FROM probabilities WHERE card=?", (card,))
        row = self.cur.fetchone()
        return (row[2], row[3], row[4])

    def __del__(self):
        self.conn.close()


class DatabaseGames(object):
    def __init__(self, database):
        self.conn = sqlite3.connect(database)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS games"
                         + "(id INTEGER PRIMARY KEY,"
                         + " card1 INTEGER, card2 INTEGER, card3 INTEGER,"
                         + " win REAL, draw REAL, lose REAL)")
        self.conn.commit()

    def count(self):
        self.cur.execute("SELECT count(*) FROM games")
        rows = self.cur.fetchone()
        return rows[0]

    def insert(self, card1, card2, card3, win, draw, lose):
        self.cur.execute("INSERT INTO games VALUES"
                         + " (NULL,?,?,?,?,?,?)",
                         (card1, card2, card3, win, draw, lose))
        self.conn.commit()

    def view(self):
        self.cur.execute("SELECT * FROM games")
        rows = self.cur.fetchall()
        return rows

    def search(self, card1="", card2="", card3=""):
        self.cur.execute("SELECT * FROM games WHERE"
                         + " card1=? AND card2=? AND card3=?",
                         (card1, card2, card3))
        row = self.cur.fetchone()
        return row

    def __del__(self):
        self.conn.close()
