import socket,threading,re,sys
from time import sleep

# 转发端口，ftp端口

ftp_server = {
    'ip':'111.111.111.111',
    'port':2333
}
server = {
    'ip':'222.222.222.222',
    'port':2334
}

# 被动端口
passive_port = 0
# 客户端数据
client_status = [None,None]

Step = 0
Finish = False
socket_1_send = [ "" , False ]
socket_1_return = [ "" , False ]

socket_2_send = [ "" , False ]
socket_2_return = [ b"" , False ]

def func_connect_main():
    global s1, client_status,Step,passive_port
    while True:
        client, host = s1.accept()
        # 判断是否为第1次请求
        if(client_status[1] == None):
            client_status[0], client_status[1] = client, host
            print("< 1 > ",host)

            # 处理<1>客户端请求
            accept_client_1 = threading.Thread(target = func_client_1_accept, kwargs = { 'client': client })
            return_client_1 = threading.Thread(target = func_client_1_return, kwargs = { 'client': client })
            accept_client_1.setDaemon(daemonic = True)
            return_client_1.setDaemon(daemonic = True)
            accept_client_1.start( )
            return_client_1.start( )
        else:

            client_2, host_2 = client, host
            print("< 2 >",host_2)

            # 处理<2>客户端请求
            accept_client_2 = threading.Thread(target = func_client_2_accept, kwargs = { 'client': client_2 })
            return_client_2 = threading.Thread(target = func_client_2_return, kwargs = { 'client': client_2 })

            # 开启线程处理被动端口的交互过程（进入请求文件状态）
            print("< 2 >",(ftp_server['ip'],passive_port))
            s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s3.connect((ftp_server['ip'], passive_port))

            accept_ftp_2 = threading.Thread(target = func_ftp_2_accept, kwargs = { 'socket_': s3 })
            send_ftp_2 = threading.Thread(target = func_ftp_2_send, kwargs = { 'socket_': s3})

            accept_client_2.setDaemon(daemonic = True)
            return_client_2.setDaemon(daemonic = True)
            accept_ftp_2.setDaemon(daemonic = True)
            send_ftp_2.setDaemon(daemonic = True)

            accept_client_2.start( )
            return_client_2.start( )
            accept_ftp_2.start( )
            send_ftp_2.start( )

            Step += 1

# <1> 接收户端发来的信息
def func_client_1_accept(client):
    global socket_1_send
    get_content = ""
    while True:
        get_content += client.recv(2048).decode('gbk')
        if(get_content.endswith("\x0d\x0a")):
            socket_1_send = [ get_content ,True]
            print("< 1 >",socket_1_send)
            get_content = ""

# <1> 将从ftp服务器的信息转发到客户端
def func_client_1_return(client):
    global socket_1_return
    while True:
        if (socket_1_return[ 1 ]):
            client.send(socket_1_return[ 0 ].encode('gbk'))
            socket_1_return = [ "", False ]

# <1> 将客户端发来的信息转发到ftp服务器
def func_ftp_1_send(socket_):
    global socket_1_send
    while True:
        if (socket_1_send[ 1 ]):
            socket_.send(socket_1_send[ 0 ].encode('gbk'))
            socket_1_send = [ "", False ]

# <1> 获取从ftp服务器得到的信息
def func_ftp_1_accept(socket_):
    global socket_1_return,passive_port,Step,Finish
    get_content = ""
    while True:
        get_content += socket_.recv(2048).decode('gbk')
        if(get_content.endswith("\x0d\x0a")):
            socket_1_return = [get_content, True]
            # 截取ftp开启的被动端口
            if (re.match(".*\(\|\|\|(\d.*)\|\)", get_content)):
                passive_port = int(re.search("\(\|\|\|(\d.*)\|\)", get_content).group(1))
            print("< 1 >", socket_1_return)

            if(get_content.split(" ")[0] == '150'):
                while (Step < 3):
                    pass

            # 由于ftp一旦向客户端发送Transfer starting时，当客户端再次连接首次访问端口，整个ftp交互就会关闭
            # 这里得对文件传输状态进行阻塞
            # 状态得到传输完成的信号，则取消阻塞
            if ("Transfer complete" in get_content):
                Finish = True
            get_content = ""

# <2>接收客户端发来的信息（passive）
def func_client_2_accept(client):
    global socket_2_send
    get_content = ""
    while True:
        get_content += client.recv(2048).decode('gbk')
        if(get_content.endswith("\x0d\x0a")):
            socket_2_send = [get_content, True]
            print("< 2 >",socket_2_send)
            get_content = ""
        else:
            print(get_content)

# <2>将从ftp服务器接收到的信息转回客户端（passive）
def func_client_2_return(client):
    global socket_2_return,Step
    while True:
        if(socket_2_return[ 1 ]):
            client.send(socket_2_return[0])
            socket_2_return = [b"",False]
            Step += 1

# <2>使用开启的被动端口与ftp服务器进行交互（passive）
def func_ftp_2_send(socket_):
    global socket_2_send
    while True:
        if(socket_2_send[ 1 ]):
            socket_.send(socket_2_send[ 0 ].encode('gbk'))
            socket_2_send = [ "" ,False]

def func_ftp_2_accept(socket_):
    global socket_2_return,Step
    get_content = b""
    cmp_content = b""
    while True:
        get_content += socket_.recv(65535)
        if(get_content == cmp_content and get_content != b""):
            socket_2_return = [get_content,True]
            print("< 2 >",socket_2_return)
            Step += 1
            get_content = b""
            cmp_content = b""
            continue
        cmp_content = get_content


def main():

    global s1,s2,s3

    # 监听转发端口
    s1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s1.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s1.bind(('0.0.0.0',server['port']))
    s1.listen(2)

    # 连接ftp服务器
    s2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s2.connect((ftp_server['ip'],ftp_server['port']))
    print("< 1 > ", (ftp_server[ 'ip' ], ftp_server[ 'port' ]))

    t_connect_main = threading.Thread(target = func_connect_main)

    accept_ftp_1 = threading.Thread(target = func_ftp_1_accept,kwargs = {"socket_":s2})
    send_ftp_1 = threading.Thread(target = func_ftp_1_send, kwargs = { "socket_": s2 })

    t_connect_main.setDaemon(daemonic = True)
    accept_ftp_1.setDaemon(daemonic = True)
    send_ftp_1.setDaemon(daemonic = True)

    t_connect_main.start()
    accept_ftp_1.start()
    send_ftp_1.start()

    while not Finish:
        try:
            sleep(1)
        except KeyboardInterrupt:
            s1.close( )
            s2.close( )
            exit(0)


    for wait in range(3, 0, -1):
        sys.stdout.write("\r````` [ " + str(wait) + " ]`````")
        sys.stdout.flush( )
        sleep(1)

    s1.close( )
    s2.close( )
    exit(0)


if __name__ == '__main__':
    main()
