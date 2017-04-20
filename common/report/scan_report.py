# coding=utf-8
import os
import sys
import traceback
sys.path.append("../..")
reload(sys)
sys.setdefaultencoding('utf-8')
from jinja2 import Environment, FileSystemLoader
from jinja2.environment import Template
from common.exception.report_path_not_found import ReportPathNotFoundException
PATH = None
TEMPLATE_ENVIRONMENT = None


def get_environmnetpath():
    global PATH
    if PATH:
        return PATH
    else:
        PATH = os.path.dirname(os.path.abspath(__file__)) + "/../../source/"
    return PATH


def get_environmnet():
    global TEMPLATE_ENVIRONMENT
    if TEMPLATE_ENVIRONMENT:
        return TEMPLATE_ENVIRONMENT
    else:
        TEMPLATE_ENVIRONMENT = Environment(autoescape=False, loader=FileSystemLoader(os.path.join(get_environmnetpath(),
                                'templates')),trim_blocks=False)
    return TEMPLATE_ENVIRONMENT


def get_sickpoc_template():
    return get_environmnet().get_template("sicklepoc.html")


def get_plugindetail_template():
    return get_environmnet().get_template("plugindetail.html")


def save_sickpoc_report(filename, objects):
    try:
        path = "{}/{}.html".format(get_environmnetpath(), filename)
        save_template(path, get_sickpoc_template(), {'objects': objects})
        save_plugin_report(objects)
    except (ReportPathNotFoundException,TypeError), e:
        print traceback.format_exc()


def save_plugin_report(objects):
    try:
        for object in objects:
            plugindetails = {}
            index = object['index']
            vul_details = object['vuldetails']
            for vuldetail in vul_details:
                plugindetails['target'] = vuldetail['target']
                plugindetails['link'] = index
                plugindetails['name'] = vuldetail['pluginname']
                plugindetails['impversion'] = vuldetail['details']['plugin']['imp_version']
                plugindetails['level'] = vuldetail['details']['plugin']['type']['level']
                plugindetails['type'] = vuldetail['details']['plugin']['type']['fullchinesename']
                plugindetails['description'] = vuldetail['details']['plugin']['description']
                plugindetails['repair'] = vuldetail['details']['plugin']['repair']
                path = "{}/plugins/{}{}.html".format(get_environmnetpath(), plugindetails['link'], plugindetails['name'])
                save_template(path, get_plugindetail_template(), {'plugindetails': plugindetails})
    except Exception, e:
        print traceback.format_exc()


def save_template(path, template, args):
    if not path:
        raise ReportPathNotFoundException(path)
    if not isinstance(template, Template):
        raise TypeError("{}是一个{}object,而不是一个Template类型".format(template, type(template).__name__))
    if not isinstance(args, dict):
        raise TypeError("{}是一个{}object,而不是一个dict类型".format(args, type(args).__name__))
    with open(path, 'w') as files:
        html = template.render(args)
        files.write(html)