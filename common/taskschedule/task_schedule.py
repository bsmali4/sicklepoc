# coding=utf-8
import traceback
import os
import sys
sys.path.append("../..")
import multiprocessing
import hashlib
import pickle
import gevent
from gevent.event import Event
from gevent import monkey
monkey.patch_socket()
from common import config
from common.util import load_plugin
from common.taskschedule import nmapscan
from common.report import scan_report
from common.exception.sickle_poc_exception import LevelError
from common.util import crypto


def main(targets, plugins, level, debug):
    delete_cache()
    if not (isinstance(level, int) and level > 0 and level < 5):
        raise LevelError()
    level = config.get_cpu_count() * level
    scan(targets, plugins, int(level), debug)


def scan(targets, plugins, level, debug):
    canceled = False
    jobqueue = multiprocessing.JoinableQueue()
    create_process(level, jobqueue, plugins, debug)
    add_job(targets, jobqueue)
    try:
        jobqueue.join()
    except KeyboardInterrupt, e:
        canceled = True
    finally:
        save_report()


def add_job(targets, jobqueue):
    for target in targets:
        jobqueue.put(target)


def create_process(level, jobqueue, plugins, debug):
    for _ in range(level):
        process = multiprocessing.Process(target=worker, args=(jobqueue, plugins, debug))
        process.daemon = True
        process.start()


def worker(jobqueue, plugins, debug):
    while True:
        try:
            target = jobqueue.get()
            gevent_scan_task(target, plugins, debug)
        except Exception, e:
            print traceback.format_exc()
        finally:
            jobqueue.task_done()


def gevent_scan_task(target, plugins, debug):
    evt = Event()
    pool = []
    scanmodle = ScanModle(target, plugins, debug)
    pool.append(gevent.spawn(scanmodle.scan_port(evt)))
    pool.append(gevent.spawn(scanmodle.scan_plugins(evt)))
    for port in scanmodle.get_ports():
        pool.append(gevent.spawn(scanmodle.scan_plugins(evt, port)))
    gevent.joinall(pool)
    save_cache(scanmodle)


def save_cache(object):
    try:
        filepath = "{}/taskschedule/cache.data".format(config.getplugspath())
        output = open(filepath, 'a')
        tempresult = {'index': crypto.md5_encrypt(object.get_host_ip()), 'host': object.get_host_ip(), 'portservices': object.get_port_services(),
                      'vuldetails': object.get_results()}
        pickle.dump(tempresult, output)
    except Exception, e:
        print traceback.format_exc()


def restore_cache():
    data = []
    filepath = "{}/taskschedule/cache.data".format(config.getplugspath())
    if not os.path.exists(filepath):
        return
    pkl_file = open(filepath, 'rb')
    while True:
        try:
            tempdata = pickle.load(pkl_file)
            data.append(tempdata)
        except EOFError, e:
            break
    return data


def save_report(fileName='sicklepoc'):
    scan_report.save_sickpoc_report(fileName, restore_cache())


def delete_cache():
    filepath = "{}/taskschedule/cache.data".format(config.getplugspath())
    if os.path.exists(filepath):
        os.remove(filepath)

class ScanModle(object):
    def __init__(self, hostip, plugins, debug):
        global results
        self.__debug = debug
        self.__host_ip = hostip
        self.__ports = []
        self.__plugins = plugins
        self.__port_services = []
        self.__results = []

    def get_results(self):
        return self.__results

    def set_results(self, results):
        self.__results = results

    def get_port_services(self):
        return self.__port_services

    def set_port_services(self, portservices):
        self.__port_services = portservices

    def get_ports(self):
        return self.__ports

    def set_ports(self, ports):
        self.__ports = ports

    def get_host_ip(self):
        return self.__host_ip

    def set_host_ip(self, hostip):
        self.__host_ip = hostip

    def get_plugins(self):
        return self.__plugins

    def set_plugins(self, plugins):
        self.__plugins = plugins

    def scan_port(self, evt):
        port_services = nmapscan.scanSingleHostPortService(self.__host_ip)
        for single_port_service in port_services:
            self.__ports.append(int(single_port_service['port'].replace("/tcp", "").replace("/udp", "")))
        self.__port_services = port_services
        evt.set()

    def scan_plugins(self, evt, port=None):
        evt.wait()
        for plugin in self.__plugins:
            plugin.options['host'] = self.__host_ip
            if port:
                plugin.options['port'] = port
            result = plugin.verify(False)
            if self.__debug:
                print result
            if result['status'] == True and self.__results.count(result) == 0:
                self.__results.append(result)