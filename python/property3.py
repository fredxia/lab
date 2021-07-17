#!/usr/bin/python3

class A:
    def __init__(self, v):
        self.v = v

    @property
    def value(self):
        raise NotImplementedError("property 'value' not implemented")

class B(A):
    @property
    def value(self):
        return True

b = B(10)
print(b.value)

a = A(10)
print(a.value)
