__author__ = 'Yonatan'

import mysql.connector

class connector:

    user = ''
    password = ''
    hostname = ''
    database_name = ''
    cnx = None

    def __init__(self,db_config):
        self.user = db_config['user']
        self.password = db_config['password']
        self.hostname = db_config['host']
        self.database_name = db_config['database']

    def connect(self):
        self.cnx = mysql.connector.connect(user = self.user,
                                           password = self.password,
                                           host = self.hostname,
                                           database = self.database_name)
        print "Connected to the database!"
    def insert(self,add,data):
        cursor = self.cnx.cursor()
        cursor.execute(add,data)
        self.cnx.commit()
        cursor.close()
    def if_exist(self,add,data):
        cursor = self.cnx.cursor()
        cursor.execute(add,data)
        exist = False
        arr = []
        for row in cursor:
            exist = True
            arr.append(row)
        self.cnx.commit()
        cursor.close()
        print arr
        return exist
    def close(self):
        self.cnx.close()