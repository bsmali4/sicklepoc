# coding=utf-8


class ReportPathNotFoundException(Exception):
    def __init__(self, path=None):
        Exception.__init__(self, "保存报告路径不能为空")