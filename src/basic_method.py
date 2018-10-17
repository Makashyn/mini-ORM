
import sqlite3
# import mysql.connector

class DBConnection():

    def __init__(self, **kwargs):
        if kwargs.get("adapter") == "psycorg2":
            try:
                connection_str = "dbname=" + kwargs.get("dbname") + " user=" + kwargs.get("user") + "" \
                                 " password=" + kwargs.get("password")
                self.connection = psycopg2.connect(connection_str)
            except ValueError:
                print("This is not valid parameters")
                raise
        if kwargs.get("adapter") == "mysql_connector":
            try:
                connection_str = "dbname=" + kwargs.get("dbname") + ", user=" + kwargs.get("user") + "" \
                                 ", password=" + kwargs.get("password")
                self.connection = connection.MySQLConnection(connection_str)
            except ValueError:
                print("This is not valid parameters")
                raise
        else:
            try:
                self.connection = sqlite3.connect(kwargs.get("dbname"))
            except ValueError:
                print("This is not valid parameters")
                raise

class Model():

    @classmethod
    def insert(cls, **kwargs):
        conn = sqlite3.connect('Test_db.sqlite')
        cursor = conn.cursor()
        name_params_str = ''
        value_str = ''
        for parameter_name, value in kwargs.items():
            if isinstance(value, str):
                value = "'" + str(value) + "'"
            name_params_str += str(parameter_name) + ","
            value_str += str(value) + ","
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

        if kwargs:
            query_string = "SELECT * from " + cls.__name__ + " WHERE "
            for argument_name, argument_value in kwargs.items():

                filter_dict = {
                    "__startwith": argument_name[:-len("__startwith")] + " LIKE '" + str(argument_value) + "%'", # left side of argument
                    "__gt": argument_name[:-len("__gt")] + " > " + str(argument_value),
                    "__lt": argument_name[:-len("__lt")] + " < " + str(argument_value),
                    "__gte": argument_name[:-len("__gte")] + " >= " + str(argument_value),
                    "__lte": argument_name[:-len("__lte")] + " <= " + str(argument_value)
                }

                if argument_name[-len("__startwith"):] == "__startwith":
                    query_string += filter_dict[argument_name[-len("__startwith"):]] #right side  of argument
                elif argument_name[-len("__gt"):] == "__gt":
                    query_string += filter_dict[argument_name[-len("__gt"):]]  # right side  of argument
                elif argument_name[-len("__lt"):] == "__lt":
                    query_string += filter_dict[argument_name[-len("__lt"):]]  # right side  of argument
                elif argument_name[-len("__gte"):] == "__gte":
                    query_string += filter_dict[argument_name[-len("__gte"):]]  # right side  of argument
                elif argument_name[-len("__lte"):] == "__lte":
                    query_string += filter_dict[argument_name[-len("__lte"):]]  # right side  of argument
                else:
                    print("This is not valid parameter for filter")
                    raise

                query_string += " and "

            query_string = query_string[:-4]
            try:
                cursor.execute(query_string)
            except:
                print("This is not valid name of column")
                raise

        data = cursor.fetchall()

        cursor.close()
        conn.close()
        return data

    @classmethod
    def update(cls, id=0, **kwargs):
        conn = sqlite3.connect('Test_db.sqlite')
        cursor = conn.cursor()
        value_str = ''
        for parameter_name, value in kwargs.items():
            if isinstance(value, str):
                value = "'" + str(value) + "'"
            value_str += str(parameter_name) + "=" + str(value) + ","
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


