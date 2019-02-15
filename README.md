
#centos7.4自动化服务器配置

具体配置项目如下：
1、	服务器IP地址、网关、子网掩码、DNS
2、	yum云源
3、	kernel
4、	yum安装第三方软件（vim、pip、gcc….）
5、	pip安装第三方软件（numpy、psutil、gevent….）

程序部署方法：

1、将整个安装程序包InstallScript复制到待安装机器根目录。
2、进入待安装机器根目录下InstallScript目录，修改CONFIG.py配置信息（文件路径:file_path、IP:IPADDR、网关:GATEWAY）。
3、若需要将安装反馈信息发送到指定邮箱需进入待安装机器根目录下InstallScript/SendEmail目录，
   将自己的邮箱地址添加到Email_config.py中receiver列表，同时修改EmailHelper.py中如下信息即可。
   sender = 'XXXX'      # 发送账户
   smtpserver = 'XXXX'  # 邮箱服务器
   username = 'XXXX'    # 用户名
   password = 'XXXX'    # 授权码
4、修改完以上配置后进入到待安装机器根目录下InstallScript目录，执行：python InstallSysConfig.py 即可开启自动化配置程序。
5、静心等待程序执行完，程序审理执行完之后会在待安装机器根目录下生成一个installLog.txt文件，里面学习记载了此次安装的反
   馈信息，若您配置了邮箱地址，待系统配置成功后会将完整的反馈信息发送到您指定的邮箱，等待查收即可。
