import socket, ssl, threading
from datetime import datetime
import json
from models import db, Instrument, Sample

import pymysql
pymysql.install_as_MySQLdb()


# create SSL socket layer
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
# create socket
server = socket.socket()
# bind address and port

server.bind(("127.0.0.1", 8080))
# listen request
server.listen(5)

print("waiting for the client")
# Administrator can modify this dict to add or remove new client
keyFiles = {'instrument1': '111', 'instrument2': '222', 'instrument3': '333'}


# check username
def checkUsername(organisation_id,insturment,conn):
    if organisation_id in keyFiles:
        conn.sendall('valid'.encode())
    else:
        conn.sendall('invalid'.encode())


# check password
def checkPassword(username,password,conn):
    if keyFiles[username] == password:
        conn.sendall('valid'.encode())
        return 'valid'
    else:
        conn.sendall('invalid'.encode())
        return 'invalid'


def receiveFile(conn):
    s = 'jsonfile'
    while True:
        data = conn.recv(1024).decode()
        # If meet 'finish' flag, then open the json file and extract information
        if data == 'finish':
            print('reach the end of file')
            with open('./' + s + '.json', 'r') as f:
                jsonFile = json.load(f)
            f.close()
            name = jsonFile['file name']
            actual_start = jsonFile['actual start time']
            actual_end = jsonFile['actual end time']
            start = jsonFile['start time']
            end = jsonFile['end time']
            length = jsonFile['length']
            instrument = jsonFile['instrument']
            # targets = jsonFile['EIC']
            actual_end = datetime.strptime(actual_end, "%Y-%m-%d %H:%M:%S.%f")

            db.create_all()
            # print ("created")
            # print (type(instrument))
            ## if the instrument does not exist in DB, then create Instrument object and add
            instrument_exist = False
            all_instruments = Instrument.query.all()
            for ins in all_instruments:
                if(ins.name == instrument):
                    instrument_exist = True
                    print ("instrument exists")

            if not instrument_exist:
                print ("not exist")
                ins = Instrument(instrument)
                # print ("created Instrument object")
                db.session.add_all([ins])
                db.session.commit()

            ##create Sample object
            sample = Sample(name, instrument, actual_start, actual_end, start, end, length)

                # print("Created a null row at finish")
            # Add to database
            db.session.add_all([sample])


            db.session.commit()

            # Check with a query, this prints out all the puppies!
            print(Instrument.query.all())

            #create Organisation Object

        # If meet 'begin to send' flag, then create a new json file
        elif data == 'begin to send':
            print('create file')
            with open('./' + s + '.json', 'w') as f:
                pass
        # if meet 'file_name' flag, then set new json file's name
        elif data[0:9] == 'file_name':
            s = data[9:]
        # Otherwise stream is the content of json file
        else:
            with open('./' + s + '.json', 'a') as f:
                f.write(data)


def connect(sock, addr):
    try:
        print('Accept new connection from %s:%s...' % addr)
        connstream = context.wrap_socket(sock, server_side=True)

        while True:
            data = connstream.recv(1024).decode()

            if not data:
                continue
            # if reads 'username' flag then extract username
            elif data.startswith('username'):
                username = data.split(':')[-1]
                checkUsername(username, connstream)
            # if reads 'password' flag then extract password
            elif data.startswith('password'):
                userpasswd = data.split(':')[-1]
                result = checkPassword(username, userpasswd, connstream)
                if result == 'valid':
                    break

        print('receiving, please wait for a second ...')

        receiveFile(connstream)

        print('receive finished')
    except ConnectionResetError:

        print('The client %s:%s has been closed' % addr)


while True:
    conn, addr = server.accept()
    # assign a new thread to deal with concurrency
    t = threading.Thread(target=connect, args=(conn, addr))
    t.start()


