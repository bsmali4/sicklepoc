#coding=utf-8
import sys
import argparse
sys.path.append("../..")
import requests
from sickle_poc_frame import base_sickle_poc


class SicklePoc(base_sickle_poc.BaseSicklePoc):
    def __init__(self):
        super(SicklePoc, self).__init__()
        self.init_info()
        self.init_options()
        super(SicklePoc, self).check_config()

    def init_info(self):
        self.info = super(SicklePoc, self).get_info()
        name = "tomcat2016-9-20"
        imp_version = "所有版本"
        description = "tomcat配置不当,可以写任意session,参考链接<a href='http://chenjc.blog.51cto.com/9122508/1434858'>" \
                      "chenjc.blog.51cto.com/9122508/1434858</a>"
        repair = "删除servlets/servlet/SessionExample"
        type = base_sickle_poc.BugType.HIDDEN_DANGER
        temp_info = {"repair":repair, "name":"tomcat2016-9-20", "type": type, "description":description, "imp_version": imp_version}
        self.info = dict(self.info, **temp_info)

    def init_options(self):
        self.options = {'port': 8080, 'host': '', 'headers': {}, }

    def verify(self, use_parser=True):
        result = {}
        result['target'] = ""
        result['info'] = ""
        result['error'] = []
        result['details'] = ""
        result['status'] = False
        result['details'] = {}
        result['pluginname'] = self.info['name']
        args = (use_parser == True and self.help() or argparse.Namespace(target=None, port=None, headers=None))
        target = (args.target == None and self.options['host'] or args.target)
        port = (args.port == None and self.options['port'] or args.port)
        headers = (args.headers == None and self.options['headers'] or args.headers)
        if port != 443:
            target = "http://" + target + ":" + str(port)
        else:
            target = "https://" + target
        target_url = target + "/examples/servlets/servlet/SessionExample"
        result['target'] = target_url
        req = None
        try:
            req = requests.get(target_url, timeout = 5, headers = headers)
            res_html = req.content
            if "Sessions Example" in res_html:
                info = "tomcat存在任意session操作漏洞"
                result['status'] = True
                result['info'] = info
                result['details']['plugin'] = self.info
        except Exception, e:
            if result['error'].count(str(e)) == 0:
                result['error'].append(str(e))
        finally:
            if req is not None:
                req.close()
                del req
        return result

    def help(self):
        parser = argparse.ArgumentParser(description='插件帮助文档')
        parser.add_argument("-t", "--target", type = str, required=False, help="目标,不需要带http:// eg:www.codersec.net")
        parser.add_argument("-p", "--port", required=False, type = int,
                            help="端口 eg:8080 ")
        parser.add_argument("--headers", required=False, type = str,
                            help="特殊设置 eg:{\"user-agent\":\"Mozilla/5.0 (compatible; Googlebot/2.1\"}")
        parser.add_argument("-i", "--info", required=False, action="store_true",
                            help="插件详细信息")
        args = parser.parse_args()
        return args

if __name__ == "__main__":
    base_sickle_poc.main(SicklePoc())