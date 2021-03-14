# DQV5-Script

------

DQV5 scripts for pentest and ctf.



## FakeFTP

------

### ftpzf.py

一个很简单的 “畸形ftp” 脚本，可以支持形如 `ftp://user:pass@xxx.xxx.xxx.xxx:[port],127.0.0.1:80/evil.txt` 结构的ftp请求。

具体参考：[畸形ftp简单分析](https://morblog.cc/posts/60343/?t=1615684110173)

参数格式：

- ftp_server = {'ip':'[ftp服务器IP]','port':'[ftp服务器端口]'}
- server = {'ip':'[监听服务器IP]','port':'[监听服务器端口]'}

例子：

例如请求 `ftp://user:pass@10.10.10.1:2333,hahahahha:200/ha.txt` ，那么先起一个 **ftp服务器** ，设其 `ip:port = 20.20.20.2:21` ，那么得将 `server` 改为 `{'ip':'127.0.0.1','port':2333}`，将 `ftp_server` 改为 `{'ip':'20.20.20.2','port':21}` 即可。



## Other

------

### zf.py

这是一个很简单的转发脚本，由于一般都用 **socat** ，基本没啥用了。

参数格式：

- python3 zf.py [端口] [生成文件名] [获取内容类型] [是否进行解码]

具体参数有点忘了，大伙们看一下源码好了，简单的一批，没啥技术含量的。



## phpevil

------

### base_convert.py

基于 **base_convert函数** 的字符拼接。

### fuck.py

基于 **一次异或的非字母数字** 的字符拼接。

### truefuck.py

基于形如 **jsfuck** 的字符拼接。

### math.py

基于 **数字以及运算符** 的字符拼接。



## PHP

------

### soap_post.php

简单使用 **soapClient** 构造 **crlf** 的 **post** 请求，挺老的了，这个可以直接在 [ctfbox](https://github.com/way29/ctfbox) 里边有。

### soap_upload.php

简单使用 **soapClient** 构造的 **crlf** 的 **文件上传** 请求，直接在 **ctfbox** 里边用就好了。



## python

------

### redisbrute.py

这个是用来简单爆破 **redis** 密码的。

参数格式：

- host = 目标地址
- listenHost = 本机地址
- listenPorts = 监听端口范围
- threadNum = 开启的线程数
- passList = [filePath/List] 密码字典，可以是文件路径或纯列表
- waitTime = 每次爆破间隔(redis密码爆破需要许些时间监听端口判断是否成功认证)

具体使用，参考脚本里边的调用就好了。

### redisreshell.py

这个是使用 **redis主从复制** 执行命令的脚本，可以支持**单次命令执行** 、 **伪交互式执行** 以及简单弹个 **伪交互式shell** (伪交互式shell接收脚本脚本源码来自 longlone)。

参数格式：

- host = 目标地址
- masterHost = 主机地址
- autPass = redis认证密码
- expFileName = 写入的so文件名称
- command = 执行一次的命令(仅交互模式=False,reshell={}时有用)
- interactive = 是否启动伪交互式shell
- reshell = 伪交互式反弹shell(若不为{}则使用，仅支持Linux)

具体使用参考脚本函数调用吧。
