

class CharField():

    def __init__(self, null=False, default=None):
        self.type = "VARCHAR"
        self.null = null
        self.default = default
        null_str = ''
        if not self.null:
            null_str = "NOT NULL"

        default_str = ''
        if self.default:
            default_str = 'DEFAULT ' + str(self.default)
        self.data_str = self.type + " " + null_str +  " " + default_str

    def __str__(self):
        return self.data_str


class IntegerField():

    def __init__(self, default=None):
        self.type = 'INT'
        self.default = default

        default_str = ''
        if self.default:
            default_str = 'DEFAULT ' + str(self.default)
        self.data_str = self.type + " " + default_str

    def __str__(self):
        return self.data_str

