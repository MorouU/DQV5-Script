import socket,threading,re
from sys import argv
from base64 import b64decode
from urllib.parse import unquote_plus
from os import popen, path
from time import time, sleep



def Exec( cmd ):
    with popen(cmd,"r") as p:
        result = p.read()
    return result

def socket_listen(port:int = 3333):
    global s,m,w
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            s.setblocking(False)
            s.settimeout(5)
            s.bind(('0.0.0.0', port))
            s.listen(1)
            m = ""
            get_content = ""
            connection, addres = s.accept()
            print(connection,addres)
            while True:
                try:
                    get_content = connection.recv(65535).decode('utf8')
                    if(get_content != ""):
                        w = True
                        m = get_content
                        while w:
                            sleep(.25)
                        get_content = ""
                    else:
                        s.shutdown(socket.SHUT_RDWR)
                        s.close()
                        break
                except socket.timeout:
                    s.shutdown(socket.SHUT_RDWR)
                    s.close()
                    break
        except Exception as e:
            print(e)
            sleep(.25)

def data_decode(data:str,decoder:str):

    if(decoder == ""):
        return data
    if(decoder == "b64"):
        return b64decode(data.encode()).decode()
    if(decoder == "url"):
        return unquote_plus(data)

def method_http_url(decoder:str = "",file:str=""):
    global s, m,w
    try:
        while True:
            if (m != ""):
                text = re.findall("(GET \/(\S+) HTTP\/)", data_decode(data = m, decoder = decoder))[ 0 ][ 1 ]
                if (file == ""):
                    file = str(time( )) + '.txt'
                with open(file, "a") as f:
                    f.write(text)
                m = ""
                w = False
    except KeyboardInterrupt:
        print("bye")
        exit(0)

def method_orgin(decoder:str = "",file:str=""):
    global s,m
    try:
        while True:
            if(m != ""):
                text = data_decode(data = m,decoder = decoder)
                if(file == ""):
                    file = str(time()) + '.txt'
                with open(file,"a") as f:
                    f.write(text)
                m = ""
                w = False
    except KeyboardInterrupt:
        s.close()
        print("bye")
        exit(0)

def main(port:int = 3333,file:str ="",decoder:str = "",method:str = "orgin"):
    global m,s,t
    m = ""
    w = False
    t = threading.Thread(target = socket_listen,kwargs = {"port":port})
    t.setDaemon(daemonic = True)
    t.start()

    if(method == "orgin"):
        method_orgin(decoder = decoder,file = file)
    if(method == "url"):
        method_http_url(decoder = decoder,file = file)

if __name__ == '__main__':
    if(len(argv) == 2 and argv[1] == "-h"):
        print(f"{path.basename(argv[0])} <PORT[default=3333]> <FILEPATH[default=`time_ns().txt`]> <METHOD[default=orgin|url]> <DECODER[default=|b64|url]>")
        exit(1)

    port = 3333
    file = ""
    method = "orgin"
    decoder = ""

    try:
        port = int(argv[1])
        file = argv[2]
        method = argv[3]
        decoder = argv[4]
    except IndexError:
        pass

    main(port = port,file = file,method = method,decoder = decoder)
