# This code is used for monitoring d file and coverting to mzml file and get stats
# use watchdog to monitor folder
from watchdog.observers import Observer
from watchdog.events import *
import time
import os
from os.path import join, getsize
import pymzml
import json
import socket, ssl
import datetime
import configparser
import time

# read config file
config = configparser.ConfigParser()

config.read('config.ini')
# read server's address and port number
address = config.get('section3', 'address')
port = config.getint('section3', 'port')
# the folder being monitored, put raw files into this path
A_path = config.get('section2', 'file_path')
# the path of msconvert eg. msconvert.exe
msconvert_path = config.get('section2', 'msconvert_path')
# the name of instrument
instrument = config.get('section1', 'instrument')
# the username and password used to validate
# username = config.get('section1','username')
password = config.get('section1', 'password')
organisation_id = config.get('section1', 'organisation_id')

# create a new socket
client = socket.socket()
# load the self-signed crtificate
client = ssl.wrap_socket(client, ca_certs="cert.pem", cert_reqs=ssl.CERT_REQUIRED)

address = socket.gethostbyname(address.strip())
print(address)
# connect to the server
client.connect((address, port))

info = {'organisation_id': organisation_id, 'instrument': instrument, 'password': password}
info = json.dumps(info)
print(info)
client.sendall(info.encode())
recv_msg = client.recv(1024).decode()
if recv_msg == 'valid':
    print('connected!')
elif recv_msg == 'wrong':
    print('wrong password!')
    time.sleep(5)
    exit()
elif recv_msg == 'noExist':
    print('instrument does not exist!')
    time.sleep(5)
    exit()


# send json file to the server
def sendFile(file_path, name):
    msg = 'file_name' + name
    client.send(msg.encode())
    # set a flag before sending the file
    client.send('begin to send'.encode())
    print('Sending the file from ' + file_path)
    with open(file_path, 'r') as f:
        for data in f:
            client.send(data.encode())

        client.send('finish'.encode())
        print('Finish !')


# monitor folder
class FileEventHandler(FileSystemEventHandler):

    def __init__(self):
        FileSystemEventHandler.__init__(self)

    # get the size of a folder
    def getdirsize(self, dir):
        size = 0
        for root, dirs, files in os.walk(dir):
            size += sum([getsize(join(root, name)) for name in files])
        return size

    def produceJson(self, mzmlName, actual_end_time, actual_start_time):
        jfile_path = A_path
        jfile_pathname = jfile_path + "\\" + mzmlName.split('.')[0] + ".json"
        f = open(jfile_pathname, 'a')
        f.close

        js = {}  # create a empty dict for json data
        js['file name'] = mzmlName

        mzmlpath = jfile_path + "\\" + mzmlName
        msrun = pymzml.run.Reader(mzmlpath, obo_version='3.71.0')
        times = msrun['TIC'].mz

        intensities = msrun['TIC'].i
        length = max(times) - min(times)
        delta_time = datetime.timedelta(seconds=length)
        js['actual start time'] = str(actual_start_time)
        js['actual end time'] = str(actual_end_time)
        js['start time'] = min(times)
        js['end time'] = max(times)
        js['length'] = length
        js['instrument'] = instrument
        js['organisation_id'] = organisation_id

        msrun = pymzml.run.Reader(mzmlpath, obo_version='3.71.0')
        js_final = json.dumps(js)
        file = open(jfile_pathname, 'w')
        file.write(js_final)
        file.close()
        sendFile(jfile_pathname, mzmlName.split('.')[0])

    # when new files/folders come in
    def on_created(self, event):
        # print "log file %s changed!" % event.src_path
        s = event.src_path
        if s.endswith('.d'):
            actual_start_time = datetime.datetime.now()
            convertname = s.replace("\\", "\\\\")
            size_list = []
            while True:
                foldersize = self.getdirsize(s)
                size_list.append(foldersize)
                print(size_list)

                if len(size_list) > 2:

                    if size_list[len(size_list) - 1] == size_list[len(size_list) - 3]:
                        print("size of folder doesn't change")
                        actual_end_time = datetime.datetime.now()  # get the actual end time of generating mzML
                        break
                # every 30 sec
                time.sleep(30)

            # put mzml file in the file that contain this code file
            cmd = msconvert_path + ' ' + convertname + ' -o ' + A_path
            print(cmd)
            print(convertname)
            os.system(cmd)

            dName = convertname.split("\\")[len(convertname.split("\\")) - 1]
            mzmlName = dName.replace(".d", ".mzML")
            print(mzmlName)
            # wait for json file produced
            time.sleep(5)
            # when convert to mzml, produce json file
            # self.produceJson("pbQC009.mzML")#change it to mzmlName
            self.produceJson(mzmlName, actual_end_time, actual_start_time)


if __name__ == "__main__":
    observer = Observer()
    event_handler = FileEventHandler()
    print('waiting for files')
    observer.schedule(event_handler, A_path, True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
