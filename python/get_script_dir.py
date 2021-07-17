#!/usr/bin/python

import os

def get_script_dir():
    script_dir = os.path.dirname(__file__)
    if script_dir.startswith("/"):
        return script_dir
    return os.getcwd() + "/" + script_dir

print get_script_dir()
