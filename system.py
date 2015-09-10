__author__ = 'Yonatan'

import psutil, subprocess
from ctypes import *
from cpuinfo import cpuinfo
from _winreg import *

def bytes2human(n):
    symbols = ('KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n

def bytes2mega(n):
    mb = 1 << 20
    value = float(n) / mb
    return round(value,2)

class cpu:
    name = ''
    utilization = ''
    num_proccess = 0
    def __init__(self):
        info = cpuinfo.get_cpu_info()
        self.name = info['brand']
        self.num_proccess = psutil.cpu_count()
        self.utilization = self.utilization_update()
    def utilization_update(self):
        return int(round(psutil.cpu_percent(interval=0.9)))

    def end(self):
        pass

class memory:
    total = ''
    available = ''
    precent = ''
    used = ''
    free = ''
    def __init__(self):
        (total,available,precent,used, free) = psutil.virtual_memory()
        self.total = total
        self.available = available
        self.precent = int(precent)
        self.used = used
        self.free = free
    def end(self):
        pass

class disk:

    #   ---------------> Computer Devices <---------------  #

    devices = [] # Contains the computer's devices. Such as: C:\\, D:\\ ...
    mountpoint = [] # Where the devices are located (devices path).
    fstype = [] # Is a string which varies depending on the platform.
    device_type = [] # Fixed devices (Hardware...) or Removable devices (DVD, DiskOnKey...).
    os_name = '' # Operation system name. Windows 10, Windows 8.1, Windows 8 ...

    #   ---------------> Devices Information <---------------  #

    total = [] # Total disk space.
    used = [] # Used space.
    free = [] # Free space.
    percent = [] # percent of used disk.

    def __init__(self):
        self.devices = [disk.device for disk in psutil.disk_partitions()]
        self.mountpoint = [disk.mountpoint for disk in psutil.disk_partitions()]
        self.fstype = [disk.fstype for disk in psutil.disk_partitions()]
        self.device_type = [self.GetDriveType(path) for path in self.devices]
        self.os_name = self.get_os_name()
        for path in self.mountpoint:
            self.total.append(bytes2mega(psutil.disk_usage(path).total))
            self.used.append(bytes2human(psutil.disk_usage(path).used))
            self.free.append(bytes2human(psutil.disk_usage(path).free))
            self.percent.append(str(psutil.disk_usage(path).percent)+'%')

    def GetDriveType(self,path):
        type_dict = {0: 'Unknown drive',
                     1: 'Path is invalid',
                     2: 'Removable drive',
                     3: 'Fixed drive',
                     4: 'Remote drive',
                     5: 'CD-ROM',
                     6: 'RAM-Disk'}
        type = windll.Kernel32.GetDriveTypeA(path)
        return type_dict[type]

    def get_os_name(self):
        root_dict = {
                 "HKEY_CLASSES_ROOT": HKEY_CLASSES_ROOT,
                 "HKEY_CURRENT_USER" : HKEY_CURRENT_USER,
                 "HKEY_LOCAL_MACHINE" : HKEY_LOCAL_MACHINE,
                 "HKEY_USERS" : HKEY_USERS,
                 "HKEY_CURRENT_CONFIG" : HKEY_CURRENT_CONFIG
                }
        root = root_dict['HKEY_LOCAL_MACHINE']
        path = 'SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion'
        key_hdl = CreateKey(root,path)
        num_subkeys, num_values, last_modified = QueryInfoKey(key_hdl)

        for i in range(num_values):
            v_name, v_data, d_type = EnumValue(key_hdl,i)
            if v_name == 'ProductName': return v_data

    def end(self):
        pass

class network:
    ipconfig = {}
    def __init__(self):
        cmd = ["ipconfig","/all"]
        log = open('log.txt','w')
        proc = subprocess.Popen(cmd,0,None,None,log,log)
        proc.wait()

        ip_values = {}
        titles = []

        log = open('log.txt', 'r')
        for line in log.readlines():
            if line.find('adapter') > -1:
                titles.append(line.strip())

        #First dict Keys decleration
        for t in titles:
            self.ipconfig[t] = None

        log = open('log.txt', 'r')
        log = log.read().split('\n')

        # Taking the title's data from ipconfig
        for i in range(len(log)-3):
            if log[i] is '':
                i+=1
                if log[i] in [t for t in titles]:
                    cat = log[i]
                    i+=1
                    if log[i] is '':
                         i+=1
                         while log[i] != '':
                             line = log[i].split("\n")
                             for l in line:
                                 y = l.split(":", 1)
                                 y[0] = y[0].replace('.','').strip()
                                 ip_values[y[0]] = y[1]
                             i+=1
                         self.ipconfig[cat] = ip_values
                         ip_values = {}
    def end(self):
        pass