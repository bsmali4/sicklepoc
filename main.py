# coding=utf-8
import argparse
import sys
sys.path.append("../..")
from common.taskschedule import task_schedule
from common.util import load_plugin
from common.exception.sickle_poc_exception import TargetsError
from common.exception.sickle_poc_exception import PluginsError
from common.exception.sickle_poc_exception import PluginsNotFound
from common.exception.sickle_poc_exception import LevelError
from common.exception.sickle_poc_exception import TargetsRepeat
from plugins import plugin_config

def print_logo():
    logo = '''
                             .       .
                            / `.   .' "
                    .---.  <    > <    >  .---.
                    |    \  \ - ~ ~ - /  /    |
         _____          ..-~             ~-..-~
        |     |   \~~~\.'                    `./~~~/
       ---------   \__/                        \__/
      .'  O    \     /               /       \  "
     (_____,    `._.'               |         }  \/~~~/
      `----.          /       }     |        /    \__/
            `-.      |       /      |       /      `. ,~~|
                ~-.__|      /_ - ~ ^|      /- _      `..-'
                     |     /        |     /     ~-.     `-. _  _  _
                     |_____|        |_____|         ~ - . _ _ _ _ _>

            '''
    title = '''
                 _      _    _
             ___(_) ___| | _| | ___ _ __   ___   ___
            / __| |/ __| |/ / |/ _ \ '_ \ / _ \ / __|   email:root@codersec.net
            \__ \ | (__|   <| |  __/ |_) | (_) | (__
            |___/_|\___|_|\_\_|\___| .__/ \___/ \___|   author:b5mali4
                                   |_|
            '''
    print logo
    print title

def help():
    parser = argparse.ArgumentParser()
    parser.add_argument("--targets", required=False, help="扫描目标 eg:www.codersec.net,root.codersec.net")
    parser.add_argument("--plugins", required=False, help="插件 eg:zabbix, structs")
    parser.add_argument("--files", required=False, help="扫描目标文件 eg:b5mali4.txt")
    parser.add_argument("--level", type=int, default=1, help = "等级 eg:1-4")
    parser.add_argument("--options", required=False, help="poc扫描配置, 比如需要提供登录之后的cookie eg:"
                                                              "{\"Cookie\":\"JSESSIONID=E485B11E73DCB\"}")
    parser.add_argument("--list", action="store_true", help="列出所有可以利用的插件模块", default=False)
    parser.add_argument("--debug", default=True, help="debug模式，可以看到扫描详情")
    args = parser.parse_args()
    return args


def list_modles(args):
    if args.list:
        plugin_config.get_modles()
        exit()


def get_parserdata(args):
    try:
        list_modles(args)
        debug = parser_debug(args)
        targets = parser_targets(args)
        plugins = parser_plugins(args)
        level = parser_level(args)
    except (TargetsError, PluginsError, LevelError, TargetsRepeat), e:
        print e
        exit()
    return targets, plugins, level, debug


def parser_debug(args):
    if args.debug and args.debug == "False":
        return False
    return True


def parser_level(args):
    if not (args.level and isinstance(args.level, int) and args.level > 0 and args.level < 5):
        raise LevelError()
    return args.level


def parser_plugins(args):
    if not args.plugins:
        raise PluginsError
    return string_list(args.plugins)


def parser_targets(args):
    if not args.targets and not args.files:
        raise TargetsError()
    if args.targets and args.files:
        raise TargetsRepeat()
    if args.targets:
        return string_list(args.targets)
    elif args.files:
        return file_list(args.files)


def file_list(file_name):
    files = None
    result = []
    try:
        files = open(file_name)
        result = files.readlines()
        result = [str(line).replace("\n","") for line in result]
    except IOError, e:
        print str(e)
        exit()
    finally:
        if files:
            files.close()
            del files
    return result

def string_list(string):
    if not isinstance(string, str):
        raise TypeError("string_list函数必须要传入一个str类型的参数")
    temp_strings = string.split(",")
    result_string = []
    for temp_string in temp_strings:
        if str(temp_string).strip() != "":
            result_string.append(temp_string)
    return result_string

if __name__ == "__main__":
    print_logo()
    if len(sys.argv) <= 1:
        print "{} -h".format(sys.argv[0])
        exit()
    args = help()
    targets, plugins, level, debug = get_parserdata(args)
    try:
        task_schedule.main(targets, load_plugin.load_plugins(plugins), level, debug)
    except PluginsNotFound, e:
        print str(e)
        exit()