
from connection import get_connection


class Model():

    @classmethod
    def insert(cls, **kwargs):
        db = get_connection()
        connection = db.connection
        name_params_list = []
        value_list = []
        for parameter_name, value in kwargs.items():
            if isinstance(value, str):
                value = "'" + str(value) + "'"
            name_params_list.append(str(parameter_name))
            value_list.append(str(value))
        value_str = ','.join(value_list)
        name_params_str = ','.join(name_params_list)
        db.execute("INSERT INTO " + cls.__name__ + " (" + name_params_str + ") VALUES (" + value_str + ")")
        connection.commit()

    @classmethod
    def select(cls,**kwargs):
        db = get_connection()
        connection = db.connection
        if not kwargs:
            db.execute("SELECT * from " + cls.__name__)
        if kwargs:
            query_string = "SELECT * from " + cls.__name__ + " WHERE "
            for argument_name, argument_value in kwargs.items():
                filter_column_name, filter_method = argument_name.split("__")
                filter_dict = {
                    "startwith": filter_column_name + " LIKE '" + str(argument_value) + "%'", # left side of argument
                    "gt": filter_column_name + " > " + str(argument_value),
                    "lt": filter_column_name + " < " + str(argument_value),
                    "gte": filter_column_name + " >= " + str(argument_value),
                    "lte": filter_column_name + " <= " + str(argument_value)
                }
                try:
                    query_string += filter_dict[filter_method] #right side  of argument
                except:
                    print("This is not valid parameters for filter")
                    raise
                query_string += " and "

            query_string = query_string[:-4]
            try:
                db.execute(query_string)
            except:
                print("This is not valid name of column")
                raise

        data = db.fetchall()
        return data

    @classmethod
    def update(cls, id=0, **kwargs):
        db = get_connection()
        connection = db.connection
        value_str = ''
        for parameter_name, value in kwargs.items():
            if isinstance(value, str):
                value = "'" + str(value) + "'"
            value_str += str(parameter_name) + "=" + str(value) + ","
        value_str = value_str[:-1]
        db.execute("UPDATE " + cls.__name__ + " SET " + value_str + " WHERE id=" + str(id))
        connection.commit()


    @classmethod
    def delete(cls, id):
        db = get_connection()
        connection = db.connection
        db.execute("DELETE FROM " + cls.__name__ + " WHERE id=" + str(id))
        connection.commit()
