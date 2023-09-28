#Shamelessly combined from google and other stackoverflow like sites to form a single function

import platform
import socket
import re
import uuid
import json
import psutil
import logging
from windows_tools.installed_software import get_installed_software


def getSystemInfo():
    try:
        info = {}
        info['platform'] =platform.system()
        info['platform-release']=platform.release()
        info['platform-version']=platform.version()
        info['architecture']=platform.machine()
        info['hostname']=socket.gethostname()
        info['ip-address']=socket.gethostbyname(socket.gethostname())
        info['mac-address']=':'.join(re.findall('..', '%012x' % uuid.getnode()))
        info['processor']=platform.processor()
        info['ram']=str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
        return json.dumps(info)
    except Exception as e:
        logging.exception(e)


system_info = json.loads(getSystemInfo())

print("{:=^80}".format("VM Setup"))
print("Platform: {}".format(system_info['platform']))
print("Platform Version: {}".format(system_info['platform-version']))
print("Architecture: {}".format(system_info['architecture']))
print("Processor: {}".format(system_info['processor']))
print("Ram: {}".format(system_info['ram']))
print("{:-^80}".format("Software"))
for software in get_installed_software():
    print("Name: {}\n\tVersion: {}\n\tPublisher: {}".format(software['name'], software['version'], software['publisher']))
print("="*80)