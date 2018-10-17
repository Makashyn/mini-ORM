
from models import CharField, IntegerField
from basic_method import Model

class Table1(Model):

    name = CharField(default="asdf")
    age = IntegerField(default=1)

    def __str__(self):
        return str(self.name) + "  " + str(self.age)


