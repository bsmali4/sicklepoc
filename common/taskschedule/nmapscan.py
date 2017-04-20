# coding=utf-8
import os
import re


def __checkLive(hostIp):
    cmd = "nmap -sP {}".format(hostIp)
    output = os.popen(cmd)
    tempResult = output.read()
    if "1 host up" in tempResult:
        return True
    elif "0 hosts up" in tempResult:
        return False


def __scanPortServiceByTcp(hostIp):
    portServices = []
    assert isinstance(hostIp, str)
    cmd = "nmap -PS {} -T4 -sS -host_timeout 600 -max-retries 1".format(hostIp)
    output = os.popen(cmd)
    tempResult = output.read()
    services = re.findall(r'[\d]{1,5}[\/]tcp\s+open\s+[\w\/\-]*', tempResult)
    for service in services:
        service = str(service)
        singleServices = re.split(r'\s*', service)
        singlePort = singleServices[0]
        singleService = singleServices[2]
        portServices.append({'port':singlePort, 'service': singleService})
    return portServices


def __scanPortServiceByUdp(hostIp):
    portServices = []
    assert isinstance(hostIp, str)
    cmd = "nmap -PU {} -T4 -sS -host_timeout 600 -max-retries 1".format(hostIp)
    output = os.popen(cmd)
    tempResult = output.read()
    services = re.findall(r'[\d]{1,5}[\/]tcp\s+open\s+[\w\/\-]*', tempResult)
    for service in services:
        service = str(service)
        singleServices = re.split(r'\s*', service)
        singlePort = singleServices[0]
        singleService = singleServices[2]
        portServices.append({'port':singlePort, 'service': singleService})
    return portServices


def scanSingleHostPortService(hostIp, checkLive = True):
    tempResult = []
    number = 0
    status = False
    if checkLive:
        status = __checkLive(hostIp)
    else:
        status = True
    while (status and tempResult == [] and number < 3):
        tempResult =__scanPortServiceByTcp(hostIp)
        number += 1
    return tempResult


def scanMultipleHostsPortServie(hostIps):
    livehostIps = []
    for hostIp in hostIps:
        if __checkLive(hostIp):
            livehostIps.append(hostIp)

    print livehostIps
    for livehostIp in livehostIps:
        scanSingleHostPortService(livehostIp)


