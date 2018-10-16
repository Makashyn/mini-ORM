
from tables import Table1

import sqlite3


class TablesRegister():


    def __init__(self):
        self.conn = sqlite3.connect('Test_db.sqlite')
        self.cursor = self.conn.cursor()

    def add(self, table):
        self.data = {}
        for i, j in table.__dict__.items():
            if i[0] != '_':
                self.data[i] = j
        self.table_name = table.__name__

    def migrate(self):
        self.cursor.execute("DROP TABLE IF EXISTS " + self.table_name)
        sql_query = 'CREATE TABLE ' + self.table_name + ' (id int auto_increment primary key'
        for i,j in self.data.items():
            sql_query += "," + i + " " + str(j)
        sql_query += ")"
        self.cursor.execute(sql_query)


if __name__ == '__main__':
    register = TablesRegister()
    register.add(Table1)
    register.migrate()



