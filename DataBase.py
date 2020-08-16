import psycopg2


class DataBase:

    def __init__(self, host, user, password, db):
        self.connection = psycopg2.connect(dbname='warg_tst', user='django_user',
                        password='123456789', host='localhost')
        self.cursor = self.connection.cursor()

    def input(self, data):


    def __del__(self):
        self.cursor.close()
        self.connection.close()
