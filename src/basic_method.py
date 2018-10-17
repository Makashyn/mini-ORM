
import sqlite3
# import mysql.connector

class DBConnection():

    def __init__(self, **kwargs):
        if kwargs.get("adapter") == "psycorg2":
            try:
                connection_str = "dbname=" + kwargs.get("dbname") + " user=" + kwargs.get("user") + "" \
                                 " password=" + kwargs.get("password")
                self.connection = psycopg2.connect(connection_str)
                self.cursor = self.connection.cursor()
            except ValueError:
                print("This is not valid parameters")
                raise
        if kwargs.get("adapter") == "mysql_connector":
            try:
                connection_str = "dbname=" + kwargs.get("dbname") + ", user=" + kwargs.get("user") + "" \
                                 ", password=" + kwargs.get("password")
                self.connection = connection.MySQLConnection(connection_str)
                self.cursor = self.connection.cursor()
            except ValueError:
                print("This is not valid parameters")
                raise
        else:
            try:
                self.connection = sqlite3.connect(kwargs.get("dbname"))
                self.cursor = self.connection.cursor()
            except ValueError:
                print("This is not valid parameters")
                raise

    def __del__(self):
        self.cursor.close()
        self.connection.close()

class Model():

    @classmethod
    def insert(cls, **kwargs):
        db = DBConnection(dbname="Test_db.sqlite")
        name_params_str = ''
        value_str = ''
        for parameter_name, value in kwargs.items():
            if isinstance(value, str):
                value = "'" + str(value) + "'"
            name_params_str += str(parameter_name) + ","
            value_str += str(value) + ","
        value_str = value_str[:-1]
        name_params_str = name_params_str[:-1]
        db.cursor.execute("INSERT INTO "+ cls.__name__ + " (" + name_params_str + ") VALUES (" + value_str + ")")
        db.connection.commit()

    @classmethod
    def select(cls,**kwargs):
        db = DBConnection(dbname="Test_db.sqlite")
        if not kwargs:
            db.cursor.execute("SELECT * from " + cls.__name__)

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
                db.cursor.execute(query_string)
            except:
                print("This is not valid name of column")
                raise

        data = db.cursor.fetchall()

        db.cursor.close()
        return data

    @classmethod
    def update(cls, id=0, **kwargs):
        db = DBConnection(dbname="Test_db.sqlite")
        value_str = ''
        for parameter_name, value in kwargs.items():
            if isinstance(value, str):
                value = "'" + str(value) + "'"
            value_str += str(parameter_name) + "=" + str(value) + ","
        value_str = value_str[:-1]
        db.cursor.execute("UPDATE " + cls.__name__ + " SET " + value_str + " WHERE id=" + str(id))
        db.connection.commit()
        db.cursor.close()

    @classmethod
    def delete(cls, id):
        db = DBConnection(dbname="Test_db.sqlite")
        db.cursor.execute("DELETE FROM " + cls.__name__ + " WHERE id=" + str(id))
        db.connection.commit()
