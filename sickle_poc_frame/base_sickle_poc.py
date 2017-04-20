#coding=utf-8
'''
    SicklePoc基础父类
    功能说明
    只制作漏洞验证模块
    基础信息
    self.info = {'author':'bsmali4','name':'zabnix-2013-9-12','imp_version':'3.2-4.5','description':'zabbix前台注入,
    参考链接xxx','repair':'升级zabbix', 'type': BugType.sqlInject}
    self.option = {"url": "http://www.codersec.net","port": "80","user-agent":"Mozilla/5.0 (compatible; Googlebot/2.1"}
    self.result = {"target":"http://www.baidu.com","exit": "True","bugtype":"injection","description":[{"type":"injection","result":"username:admin|password:admin12345"},{"type":"xss","result":"xss?alert(1)"}]}
    sqlinject = '注入' hight
    xss = 'xss跨站脚本攻击' hight
    xxe = 'xml外部实体攻击' hight
    csrf = '跨站请求伪造' middle
    cors = '请求对象共享' hight
    jsonp = 'jsonp劫持' middle
    weakpwd = '弱密码' hight
    crlf = '回车键注入' low
    infoleak = '信息泄漏' hight
    cmdect = '命令执行' hight
    ddos = 'ddos漏洞' hight
    fileread = '任意文件读取,包含任意下载之类的' hight
    fileupload = '任意文件上传' hight
    fileinclude = '文件包含' hight
    other = '其它,包括越权之类的' middle

'''
import sys
sys.path.append("../..")
import argparse
import abc
import traceback
from abc import ABCMeta
from abc import abstractproperty
from abc import abstractmethod
from common.util.string_inject_dic import dicToString
from common.exception.sickle_poc_exception import SicklePocInfoWrong
from common.exception.sickle_poc_exception import SicklePocOptionsWrong


class BugLevel(object):
    HIGHT = 'hight'
    MIDDLE = 'middle'
    LOW = 'low'


class BugType(object):
    SQL_INJECT = {'fullname':'sqlinject', 'fullchinesename':'sql注入', 'level': BugLevel.HIGHT}
    XSS = {'fullname':'xss', 'fullchinesename':'xss跨站脚本攻击', 'level': BugLevel.HIGHT}
    XXE = {'fullname':'xxe', 'fullchinesename':'xml外部实体攻击', 'level': BugLevel.HIGHT}
    CSRF = {'fullname':'csrf', 'fullchinesename':'跨站请求伪造', 'level': BugLevel.MIDDLE}
    CORS = {'fullname':'cors', 'fullchinesename':'请求对象共享', 'level': BugLevel.MIDDLE}
    JSONP = {'fullname':'jsonp', 'fullchinesename':'jsonp跨域劫持劫持', 'level': BugLevel.MIDDLE}
    WEAK_PWD = {'fullname':'weakpwd', 'fullchinesename': '弱密码', 'level': BugLevel.HIGHT}
    CRLF = {'fullname':'crlf', 'fullchinesename': '回车键注入', 'level': BugLevel.MIDDLE}
    INFO_LEAK = {'fullname':'infoleak', 'fullchinesename': '信息泄漏', 'level': BugLevel.HIGHT}
    CMD_ECT = {'fullname':'cmdect', 'fullchinesename': '命令执行', 'level': BugLevel.HIGHT}
    DDOS = {'fullname':'ddos', 'fullchinesename': '命令执行', 'level': BugLevel.HIGHT}
    FILE_READ = {'fullname':'fileread', 'fullchinesename': '任意文件读取', 'level': BugLevel.HIGHT}
    FILE_UPLOAD = {'fullname':'fileupload', 'fullchinesename': '任意文件上传', 'level': BugLevel.HIGHT}
    FILE_INCLUDE = {'fullname':'fileinclude', 'fullchinesename': '文件包含', 'level': BugLevel.HIGHT}
    OTHER = {'fullname':'other', 'fullchinesename': '其它', 'level': BugLevel.MIDDLE}
    HIDDEN_DANGER = {'fullname':'hiddendanger', 'fullchinesename': '安全隐患', 'level': BugLevel.LOW}


class BaseSicklePoc(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.info = {"author": "bsmali4"}
        self.options = {}

    @abstractproperty
    def init_info(self):
        pass

    @abstractproperty
    def init_options(self):
        pass

    def get_info(self):
        return self.info

    def set_info(self, info):
        self.info = info

    def get_options(self):
        return self.options

    @abstractproperty
    def verify(self):
        pass

    def check_info(self, info):
        assert isinstance(info, dict), "传入的info不是一个dict类型"
        if not (info.has_key("author") and info.has_key("name") and info.has_key("imp_version")\
                and info.has_key("description") and info.has_key("repair") and info.has_key("type")):
            raise SicklePocInfoWrong(info)

    def check_options(self, options):
        assert isinstance(options, dict), "传入的options不是一个dict类型"
        if not (options.has_key("host") and options.has_key("port")):
            raise SicklePocOptionsWrong(options)

    def check_config(self):
        try:
            self.check_info(self.info)
            self.check_options(self.options)
        except (SicklePocInfoWrong,SicklePocOptionsWrong), e:
            print traceback.format_exc()

    @abstractproperty
    def help(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-t", "--target", required=False, action="store_true",
                            help="目标 eg:www.codersec.net")
        parser.add_argument("-p", "--port",  required=False, action="store_true",
                            help="端口 eg:80")
        parser.add_argument("--options", required=False, action="store_true",
                            help="特殊设置 eg:{\"username\":\"admin\"}")
        args = parser.parse_args()


def main(object):
    if len(sys.argv) <= 1:
        print "{} -h".format(sys.argv[0])
        exit()
    args = object.help()
    if args.info:
        print dicToString(object.info)
        exit()
    result = object.verify()
    print result