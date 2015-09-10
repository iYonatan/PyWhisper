__author__ = 'Yonatan'

from db_connector import connector
from system import *

######################## database connection ########################

db_config = {
      'user': 'sql287864',
      'password': 'jA2*cS1%',
      'host': 'sql2.freesqldatabase.com',
      'database': 'sql287864',
    }
db_con = connector(db_config)
db_con.connect()
user_id = 0

######################## System Information ########################

proc = cpu()
exist = "SELECT user_id FROM cpu WHERE user_id= %s"
exist_data = (user_id,)
if not db_con.if_exist(exist,exist_data):
    add_cpu = ("INSERT INTO cpu "
                "(user_id,Brand, num_proccess)"
                "VALUES (%s, %s, %s)")
    cpu_data = (user_id,proc.name,proc.num_proccess)
    db_con.insert(add_cpu,cpu_data)



memo = memory()
exist = "SELECT user_id FROM memory WHERE user_id= %s"
exist_data = (user_id,)
if not db_con.if_exist(exist,exist_data):
    add_memo = "UPDATE memory SET total= %s WHERE user_id=%s"
    memo_data = (memo.total,user_id)
    db_con.insert(add_memo,memo_data)



disk = disk()
add_disk = "SELECT user_id,device,mountpoint FROM disk WHERE user_id=%s"
data = (user_id,)
op = db_con.what2set(add_disk,data,disk.devices)

if op is "INSERT":
    for d in range(len(disk.devices)):
        if not db_con.if_exist(add_disk,data):
             add_disk = ("INSERT INTO disk"
                         "(user_id,os_name,device,mountpoint,fstype,total)"
                         "VALUES (%s,%s,%s,%s,%s,%s)")
             disk_data = (user_id,disk.os_name,disk.devices[d],disk.mountpoint[d],disk.fstype[d],disk.total[d])
             db_con.insert(add_disk,disk_data)

elif op is "UPDATE":
    print "UPDATE"
else:
    print "REMOVE"

# net = network()
# print net.ipconfig

######################## Closed Vars ##############################
db_con.close()