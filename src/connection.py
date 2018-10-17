
from abc import ABCMeta, abstractmethod, abstractproperty
import sqlite3
# import mysql.connector
from settings import DATABASE

class DBConnection():
    __metaclass__ = ABCMeta


    @abstractmethod
    def execute():
        ''' Create sql query '''

    @abstractmethod
    def fetchall():
        ''' Get all row from table'''

class MySQLDBConnection(DBConnection):
    def __init__(self, **kwargs):
        self._dbname = kwargs.get('dbname')
        self._user = kwargs.get('user')
        self._password = kwargs.get('password')
        self.connection = connection.MySQLConnection("dbname=" + self._dbname + ", user=" + self._user + ", password=" + self._password)
        self._cursor = self.connection.cursor()

    def execute(self, query):
        self._cursor.execute(query)

    def fetchall(self):
        return self._cursor.fetchall()

class SQLiteDBConnection(DBConnection):
    def __init__(self, **kwargs):
        self._dbname = kwargs.get('dbname')
        self.connection = sqlite3.connect(self._dbname)
        self._cursor = self.connection.cursor()

    def execute(self, query):
        self._cursor.execute(query)

    def fetchall(self):
        return self._cursor.fetchall()

def get_connection():
    connection = None
    try:
        if DATABASE['ENGINE'].lower() == "sqlite3":
                connection = SQLiteDBConnection(dbname=DATABASE['NAME'])
        elif DATABASE['ENGINE'].lower() == 'mysql':
                connection = MySQLDBConnection(dbname=DATABASE['NAME'], user=DATABASE['user'], password=DATABASE['password'])
    except ValueError:
        print("Your settings file isn't correct")
        raise
    return connection


