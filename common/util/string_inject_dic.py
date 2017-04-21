# coding=utf-8

import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def str_inject_dic(dic, string):
    assert isinstance(dic, dict) and isinstance(string, basestring), "dic 不是 dict or string 不是 " \
                                                                    "basestring"
    tempDic = json.loads(string)
    for tempKey, tempValue in tempDic.items():
        dic[str(tempKey)] = str(tempValue)
    return dic


def string_to_dic(string):
    tempdic = json.loads(string)
    dic = {}
    for key, value in tempdic.items():
        dic[str(key)] = str(value)
    return dic


def dic_to_string(dic):
    assert isinstance(dic, dict)
    return json.dumps(dic, ensure_ascii=False)

