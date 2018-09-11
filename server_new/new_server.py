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

server.bind(("192.168.1.114", 8888))
server.listen(5)

print("waiting for the client")

def checkValid(organisation_id,instrument,password,conn):
    organ_ins = Instrument.query.filter(Instrument.o_id==organisation_id)
    if instrument in [instrument.name for instrument in organ_ins]:
        password_hash = Instrument.query.filter(Instrument.o_id==organisation_id,Instrument.name==instrument).first().password_hash
        is_valid = check_password_hash(password_hash,password)
        if is_valid:
            conn.sendall('valid'.encode())
            return "valid"

        else:
            conn.sendall('wrong'.encode())
            return "wrong"

    else:
        conn.sendall('noExist'.encode())
        return "not exist"



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
            instrument = jsonFile['instrument']
            organisation_id = jsonFile['organisation_id']
            # targets = jsonFile['EIC']
            actual_end = datetime.strptime(actual_end, "%Y-%m-%d %H:%M:%S.%f")

            try:
                ##create Sample object
                sample = Sample(organisation_id,name, instrument, actual_start, actual_end)
            # Add to database
                db.session.add_all([sample])

                db.session.commit()
            except:
                print("failed store in database")
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
    print('Accept new connection from %s:%s...' % addr)
    connStream = context.wrap_socket(sock, server_side=True)
    try:
        while True:
            data = connStream.recv(1024).decode()
            if not data:
                continue
            else:
                data = json.loads(data)
                o_id = data['organisation_id']
                instrument = data['instrument']
                password = data['password']
                result = checkValid(o_id,instrument,password,connStream)

                if result != "valid":
                    connStream.close()
                    print ("client not valid")
                break
        print('receiving, please wait for a second ...')
        receiveFile(connStream)
        print('receive finished')

    except:
        connStream.close()
        print('The client %s:%s has been closed' % addr)


while True:
    conn, addr = server.accept()
    print("threads: " + str(threading.active_count()))

    # assign a new thread to deal with concurrency
    t = threading.Thread(target=connect, args=(conn, addr))
    t.start()


