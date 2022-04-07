#获取master、node系统资源，返回(CPU、内存、硬盘信息、资源上POD个数)

# 硬盘
def df(ssh_client):
    cmd1="df -hT | awk '{print $NF,$(NF-1)}' | sed '1d' |awk '{print $1}'" #获取硬盘占用率
    cmd2="df -hT | awk '{print $NF,$(NF-1)}' | sed '1d' |awk '{print $2}'" #获取磁盘名称
    stdin, dfout, stderr = ssh_client.exec_command(cmd1,get_pty=True)
    stdin, useout, stderr = ssh_client.exec_command(cmd2,get_pty=True)
    dflist = []
    uselist = []
    info = {}
    for df in dfout:
        dflist.append(df.replace('\n', ''))
    for use in useout:
        uselist.append(use.replace('\n', ''))
    for i, x in enumerate(dflist):
        info[dflist[i]] = uselist[i]
    info["remark"] = "硬盘及占用率"
    info["data"] = info
    return info

#内存
def mem(ssh_client):
    cmd="free -t | awk 'NR == 2 {print $3/$2*100}'"    #获取内存占用率
    stdin, useout, stderr = ssh_client.exec_command(cmd,get_pty=True)
    info = {}
    for usage in useout:
        info["usage"] = usage
    info["remark"] = "内存及占用率"
    info["data"] = info
    return info

#cpu
def cpu(ssh_client):
    cmd="top -b -n1 | fgrep \"Cpu(s)\" | tail -1 | awk -F'id,' '{split($1, vs, \",\"); v=vs[length(vs)]; sub(/\s+/, \"\", v);sub(/\s+/, \"\", v); printf \"%s\n\", 100-v; }'"
    stdin, useout, stderr = ssh_client.exec_command(cmd,get_pty=True)
    info = {}
    for usage in useout:
        info["usage"] = usage
    info["remark"] = "cpu使用率"
    info["data"] = info
    return info