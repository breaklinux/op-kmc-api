import json
from ldap3 import Server, Connection, HASHED_SHA, ALL
from ldap3.utils.hashed import hashed
from ldap3 import ALL_ATTRIBUTES
import uuid
import random
from django.conf import settings
import ldap
LDAP = settings.LDAP

class MyLdapOps(object):
    def __init__(self):
        self.ldap_host = LDAP.get("server")
        self.ldap_port = LDAP.get("port", 389)
        self.base = LDAP.get("base")
        self.check_names = True
        self.lazy = False
        self.receive_timeout = 30
        self.use_ssl: False
        self.ldap_obj = None
        self.connect_timeout = 15
        # 连接LDAP固定参数

    def ldapConnect(self, ldap_name, ldap_passwd):
        self.ldap_name = ldap_name
        self.ldap_passwd = ldap_passwd
        ldap_url = "{}:{}".format(self.ldap_host, self.ldap_port)
        server = Server(ldap_url, get_info=ALL)
        conn = Connection(server, self.ldap_name, self.ldap_passwd)
        conn.bind()
        self.ldap_obj = conn
        return self.ldap_obj

        # 查询lDAP用户 默认输入 * 查询所有用户
    def ldapSearch(self, user='*'):
        search_parameters = {'search_base': self.base,
                             'search_filter': '(cn={})'.format(user)}
        self.ldap_obj.search(**search_parameters, attributes=ALL_ATTRIBUTES)
        search_list = self.ldap_obj.response
        try:
            user_list = []
            for i in search_list:
                user_map = {"code": 0, "status": True, "data": "LDAP查询成功"}
                username_tmp = i['raw_dn'].decode()
                tmp_user = i['raw_attributes']
                user_map["username"] = username_tmp.split(",")[0].split('=')[1]
                user_map["password"] = tmp_user['userPassword'][0].decode()
                user_map["name"] = tmp_user['givenName'][0].decode()
                user_map["mail"] = tmp_user["mail"][0].decode()
                user_list.append(user_map)

            if not user_list:
                data = 'there is no {userName} '.format(userName=user)
                user_list = {"code": 0, "message": "查询无该用户存在", "data": data, "status": False}
            return user_list
        except Exception as e:
            print(e)
            return {"code": 1, "message": "LDAP出现异常", "data": str(e), "status": False}

    def login(self, username, password):
        try:
            user = f"cn={username},{self.base}"
            conn = self.ldapConnect(user, password)
            print(conn.result.get("result"))
            if conn.result.get("result") == 0 and conn.result.get("description") == "success":
                return {"code": 0, "message": "LDAP登陆验证成功", "data": conn.result.get("description"), "user": username,"status": True}
            else:
                err_msg = 'LDAP 认证失败,请检查账号名称或者密码'
                return {"code": 1, "message": err_msg, "data": conn.result.get("description"), "user": username, "status": False}
        except Exception as e:
            err_msg = f'LDAP失败信息:{e}'
            return {"code": 1, "message": "连接失败", "data": err_msg, "user": username, "status": False}

    # 通过随机数生成LDAP密码
    def ldapRendomPassword(self):
        seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        sa = []
        for i in range(16):
            sa.append(random.choice(seed))
        password = ''.join(sa)
        return password

    # 添加LDAP用户.
    def ldapAdd(self, username, password, name, mail=None):
        if mail is None:
            mail = '{}@163.com'.format(username)
        # passwd = self.ldapRendomPassword()
        # hashed_password = hashed(HASHED_SHA, passwd)
        # hashed_password = hashed_password.replace('sha', 'SHA')  # 将sha 替换为 SHA
        dn = 'cn={},ou=user,dc=ops,dc=com'.format(username)
        uid = uuid.uuid1().int
        obj_class = ['top', 'shadowAccount', 'posixAccount', 'inetOrgPerson']
        data = {'cn': username,
                'uid': username,
                'uidNumber': uid,
                'gidNumber': 0,
                'givenName': name,
                'homeDirectory': '/home/{}'.format(username),
                'loginShell': username,
                'sn': username,
                'mail': mail,
                'shadowExpire': 99999,
                'shadowFlag': 0,
                'shadowInactive': 99999,
                'shadowLastChange': 12011,
                'shadowMax': 99999,
                'shadowMin': 0,
                'shadowWarning': 0,
                'userPassword': password
                }
        ret = self.ldapConnect(dn, obj_class, data)
        if ret:
            print(username, passwd)
            # self.ldap_mail(mail, username, passwd)
            return {"code": 0, "username": username, "passwd": passwd,  "user": name, "mail": mail, "message": "账号添加成功", "status": True}
        return {"code": 1, "username": username, "passwd": "账号已存在", "user": name, "mail": mail, "message": "账号已存在", "status": False}

    # 删除LDAP用户
    def ldapDel(self, username):
        dn = "cn={},ou=user,dc=ops,dc=com".format(username)
        ret = self.ldap_obj.delete(dn)
        if ret:
            return {"code": 0, "message": "删除成功", "username": username, "status": True}
        else:
            return {"code": 1, "message": "删除失败", "username": username,  "status": False}

class newLdap:
    def __init__(self):
        self.server = LDAP.get("server")
        self.port = LDAP.get("port")
        self.rules = LDAP.get("rules")
        self.admin_dn = LDAP.get("admin_dc")
        self.password = LDAP.get("admin_passwd")
        self.base_dn = LDAP.get("base")

    def valid_user(self, username, password):
        try:
            conn = ldap.initialize("ldap://{0}:{1}".format(self.server, self.port), bytes_mode=False)
            conn.simple_bind_s(self.admin_dn, self.password)
            search_filter = f'({self.rules}={username})'
            ldap_result_id = conn.search(self.base_dn, ldap.SCOPE_SUBTREE, search_filter, None)
            result_type, result_data = conn.result(ldap_result_id, 0)
            if result_type == ldap.RES_SEARCH_ENTRY:
                conn.simple_bind_s(result_data[0][0], password)
                return {"code": 0, "message": "LDAP登陆验证成功", "user": username, "status": True }
            else:
                err_msg = 'LDAP 认证失败,请检查账号名称或者密码'
                return {"code": 1, "message": err_msg,  "user": username, "status": False}
                # return False, None
        except Exception as error:
            args = error.args
            print(args)
            return {"code": 1, "message": '未知错误', "data": str(args), "user": username, "status": False}
