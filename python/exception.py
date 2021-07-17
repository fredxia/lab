#!/usr/bin/python3

class MyException(Exception):
    def __init__(self, int_value):
        self.value = int_value

    def __str__(self):
        return "My error is %s" % self.value

class Exception2(MyException):
    def __init__(self, float_value):
        super().__init__(int(float_value))
        
def func():
    raise Exception2(100.23)

func()

