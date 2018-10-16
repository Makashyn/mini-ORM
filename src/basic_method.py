
import sqlite3

class Model():
    @classmethod
    def insert(cls,**kwargs):
        conn = sqlite3.connect('Test_db.sqlite')
        cursor = conn.cursor()
        name_params_str = ''
        value_str = ''
        for i, j in kwargs.items():
            if isinstance(j, str):
                j = "'" + str(j) + "'"
            name_params_str += str(i) + ","
            value_str += str(j) + ","
        value_str = value_str[:-1]
        name_params_str = name_params_str[:-1]
        cursor.execute("INSERT INTO "+ cls.__name__ + " (" + name_params_str + ") VALUES (" + value_str + ")")
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def select(cls,**kwargs):
        conn = sqlite3.connect('Test_db.sqlite')
        cursor = conn.cursor()
        if not kwargs:
            cursor.execute("SELECT * from " + cls.__name__)

        if kwargs.get('name__startwith'):
            cursor.execute("SELECT * from " + cls.__name__ + " WHERE name LIKE '" + kwargs.get("name__startwith") + "%'")

        data = cursor.fetchone()

        cursor.close()
        conn.close()
        return data

    @classmethod
    def update(cls, id=0, **kwargs):
        conn = sqlite3.connect('Test_db.sqlite')
        cursor = conn.cursor()
        value_str = ''
        for i, j in kwargs.items():
            if isinstance(j, str):
                j = "'" + str(j) + "'"
            value_str += str(i) + "=" + str(j) + ","
        value_str = value_str[:-1]
        cursor.execute("UPDATE " + cls.__name__ + " SET " + value_str + " WHERE id=" + str(id))
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def delete(cls, id):
        conn = sqlite3.connect('Test_db.sqlite')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM " + cls.__name__ + " WHERE id=" + str(id))
        conn.commit()
        cursor.close()
        conn.close()