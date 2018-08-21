import socket, ssl, threading
from datetime import datetime
import json
from monitor_system import db
from monitor_system.models import Sample, Instrument
from werkzeug.security import check_password_hash

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
# keyFiles = {'instrument1': '111', 'instrument2': '222', 'instrument3': '333'}


def checkValid(organisation_id,instrument,password,conn):
    organ_ins = Instrument.query.filter(Instrument.o_id==organisation_id)
    if instrument in [instrument.name for instrument in organ_ins]:
        password_hash = Instrument.query.filter(Instrument.o_id==organisation_id,Instrument.name==instrument).first().password_hash
        is_valid = check_password_hash(password_hash,password)
        # print (Instrument.query.filter(Instrument.o_id==organisation_id,Instrument.name==instrument))
        # if password_hash == Instrument.query.filter(Instrument.o_id==organisation_id,Instrument.name==instrument).first().password_hash:
        if is_valid:
            print ("valid")
            conn.sendall('valid'.encode())
        else:
            print ("wrong")
            conn.sendall('wrong'.encode())
    else:
        conn.sendall('noExist'.encode())


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
            organisation_id = jsonFile['organisation_id']
            # targets = jsonFile['EIC']
            actual_end = datetime.strptime(actual_end, "%Y-%m-%d %H:%M:%S.%f")

            ##create Sample object
            sample = Sample(organisation_id,name, instrument, actual_start, actual_end,length)

                # print("Created a null row at finish")
            # Add to database
            db.session.add_all([sample])


            db.session.commit()

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
            else:
                data = json.loads(data)
                o_id = data['organisation_id']
                instrument = data['instrument']
                password = data['password']
                result = checkValid(o_id,instrument,password,connstream)

                break
            # if reads 'username' flag then extract username
            # elif data.startswith('username'):
            #     username = data.split(':')[-1]
            #     checkUsername(username, connstream)
            # # if reads 'password' flag then extract password
            # elif data.startswith('password'):
            #     userpasswd = data.split(':')[-1]
            #     result = checkPassword(username, userpasswd, connstream)
            #     if result == 'valid':
            #         break

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


