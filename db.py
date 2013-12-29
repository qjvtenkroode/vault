import sqlite3
import ConfigParser
import os
import sys

class Database:
    _cfgfile = "vault.conf"
    _tables = ["vault"]
    _checkDbQuery = '''SELECT name FROM sqlite_master WHERE type='table';'''
    _createDbQuery = '''CREATE TABLE IF NOT EXISTS vault (id integer unique primary key autoincrement, name text, user text, password text, url text, tag text)'''

    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        configPath = os.path.join(os.path.dirname(sys.argv[0]), self._cfgfile)

        if not os.path.isfile(configPath):
            print "ERROR: no config file found in the application root"
            sys.exit(1)

        try:
            fp = open(configPath, "r")
            self.config.readfp(fp)
            fp.close()
        except IOError, e:
            print "ERROR: could not read config file: ", str(e)
            sys.exit(1)

        self.dbname = self.config.get("vault", "dbname")

        # get a db conn
        conn = self.getDbConn()
        # check if db's exists
        if self.checkDb(conn):
            print "INFO: databases ok!"
    
    def getDbConn(self):
        # generates and returns a db connection
        conn = sqlite3.connect(self.dbname)
        return conn

    def checkDb(self, conn):
        c = conn.cursor()
        c.execute(self._checkDbQuery)
        tables = c.fetchall()
        # check if all tables exist, otherwise rebuild missing tables
        if not all(e in [t[0] for t in tables] for e in self._tables):
            print "INFO: creating database..."
            self.createDb(conn)
        conn.close()
        return True

    def createDb(self, conn):
        c = conn.cursor()
        c.execute(self._createDbQuery)
        conn.commit()

if __name__ == "__main__":
    db = Database()
    #conn = db.getDbConn()
    #db.checkDb(conn)
