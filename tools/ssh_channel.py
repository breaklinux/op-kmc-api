import paramiko


class sshChannelManager():
    def __init__(self, host, port, username):
        self.loginHost = host
        self.loginPort = port
        self.loginUser = username

    def sshClientPasswdChannel(self, password):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=self.loginHost, port=self.loginPort, username=self.loginUser, password=password)
        return ssh_client

    def sshClientPrivateKeyChannel(self, private_key_path):
        private_key = paramiko.RSAKey.from_private_key_file(private_key_path)  # "/home/remote_paramiko/id_rsa"
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=self.loginHost, port=self.loginPort, username=self.loginUser)
        return ssh_client

    def sshExecCommand(self, command, password, type="passwd", private_key_path=None):
        print("执行命令:{0}".format(command))
        if type == "passwd":
            ssh_client = self.sshClientPasswdChannel(password)
        else:
            ssh_client = self.sshClientPrivateKeyChannel(private_key_path)

        return self.commandResult(ssh_client, command)

    def commandResult(self, ssh_client, command):
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
