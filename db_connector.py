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
        return exist

    '''
        what2set is a function that tells you what command to give to the remote database: INSERT, UPDATE, DELETE.

        ** The Function what2set doesnt take the mountpoints array!!!
    '''

    def what2set(self,request,data,devices_arr=[]):
        exist = False
        need2delete = []
        exist_devices = []

        cursor = self.cnx.cursor()
        cursor.execute(request,data)

        for row in cursor:
            exist = True
            need2delete.append(row)
        if exist:
            if len(devices_arr) is 0:
                return "UPDATE"
            exist_devices.append([i[1] for i in need2delete])
            for device in need2delete:
                exist_devices.append(device[1])
            if len(list(set(exist_devices) - set(devices_arr))) > 0:
                return "DELETE"
        else:
            return "INSERT"

    def close(self):
        self.cnx.close()