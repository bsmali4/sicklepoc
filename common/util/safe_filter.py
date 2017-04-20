# coding=utf-8


def check_traversal(name):
    if "../" not in name:
        return name
    name = name.replace("../","")
    name = check_traversal(name)
    return name
