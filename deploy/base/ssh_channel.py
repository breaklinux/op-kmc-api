import paramiko


class sshChannelManager():
    """
    1.封装连接ssh通道功能, 类初始化(连接地址,端口,用户名称)
    """
    def __init__(self, host, port, username):
        self.loginHost = host
        self.loginPort = port
        self.loginUser = username

    def sshClientPasswdChannel(self, password):
        """
        1.ssh 密码方式连接,返回连接对象.
        """
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=self.loginHost, port=self.loginPort, username=self.loginUser, password=password)
        return ssh_client

    def sshClientPrivateKeyChannel(self, private_key_path):
        """
        1.1.ssh 密钥方式连接,需要传入ssh 私钥key文件 返回连接对象.
        """
        private_key = paramiko.RSAKey.from_private_key_file(private_key_path)  # "/home/remote_paramiko/id_rsa"
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=self.loginHost, port=self.loginPort, username=self.loginUser)
        return ssh_client

    def sshExecCommand(self, command, password, type="passwd", private_key_path=None):
        """
        1.ssh 后执行操作命令.默认使用密码方式进行登录机器.
        2.支持通过密钥方式进行登录需要传递私钥的文件路径.
        """
        print("执行命令:{0}".format(command))
        if type == "passwd":
            ssh_client = self.sshClientPasswdChannel(password)
        else:
            ssh_client = self.sshClientPrivateKeyChannel(private_key_path)
        print(self.commandResult(ssh_client, command))
        return self.commandResult(ssh_client, command)

    def commandResult(self, ssh_client, command):
        """
        1.ssh后执行,执行命令格式处理返回.
        2.判断标准输出不为空读取执行命令返回信息.
        3.判断标准错误输出 不为空读取执行命令返回信息.
        """
        stdin, stdout, stderr = ssh_client.exec_command(command, get_pty=True)
        if not stdout is None:
            data = stdout.read()
            data = data.decode("utf-8")
            print("命令执行结果：" + str(data))
            return data

        if not stderr is None:
            data = stderr.read()
            data = data.decode("utf-8")
            print("命令执行错误：" + str(data))
            return data.read()

    def remoteHostScp(self, passwd, local_path, remote_path):
        """
        1.ssh方法拷贝本地文件到远程服务器上
        2.本地路径和远程服务器路径
        3.关闭连会话信息.
        """
        ssh_client = paramiko.Transport((self.loginHost, self.loginPort))
        ssh_client.connect(username=self.loginUser, password=passwd) # 登录远程服务器
        sftp = paramiko.SFTPClient.from_transport(ssh_client)  # sftp传输协议
        src = local_path
        des = remote_path
        try:
            sftp.put(src, des)
            return {"code": 0, "msg": "success", "info": "file upload success" }
        except Exception as e:
            ssh_client.close()
            return {"code": 0, "msg": "failure", "info": str(e)}
        finally:
            ssh_client.close()
