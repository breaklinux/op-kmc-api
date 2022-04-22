import configparser


def read_config(section, key):
    file = "config.ini"
    con = configparser.ConfigParser()
    con.read(file, encoding='utf-8-sig')
    sections = con.sections()
    return con.get(section, key)
