
from tables import Table1
from basic_method import DBConnection

import sqlite3


class TablesRegister(DBConnection):


    def __init__(self):
        DBConnection.__init__(self, dbname="Test_db.sqlite")
        self.cursor = self.connection.cursor()

    def add(self, table):
        self.data = {}
        for parameter_name, value in table.__dict__.items():
            if parameter_name[0] != '_':
                self.data[parameter_name] = value
        self.table_name = table.__name__

    def migrate(self):
        self.cursor.execute("DROP TABLE IF EXISTS " + self.table_name)
        sql_query = 'CREATE TABLE ' + self.table_name + ' (id int auto_increment primary key'
        for parameter_name, value in self.data.items():
            sql_query += "," + parameter_name + " " + str(value)
        sql_query += ")"
        self.cursor.execute(sql_query)


if __name__ == '__main__':
    register = TablesRegister()
    register.add(Table1)
    register.migrate()



