#!/usr/bin/python3

Flag_Is_Last_Token = 0x0001
Flag_Is_Optional = 0x0002

class A:
    def __init__(self, v):
        self.v = v
        self.flags = 0

    @property
    def is_last_keyword(self):
        return self.flags & Flag_Is_Last_Token

    @is_last_keyword.setter
    def is_last_keyword(self, is_last):
        if is_last:
            self.flags |= Flag_Is_Last_Token
        else:
            self.flags &= ~Flag_Is_Last_Token

    @property
    def is_optional(self):
        return self.flags & Flag_Is_Optional

    @is_optional.setter
    def is_optional(self, optional):
        if optional:
            self.flags |= Flag_Is_Optional
        else:
            self.flags &= ~Flag_Is_Optional

    @property
    def segment_id(self):
        return self.flags >> 8

    @segment_id.setter
    def segment_id(self, seg_id):
        self.flags = (seg_id << 8) | (self.flags & 0x000000FF)

a = A(123)
a.is_last_keyword = True
a.is_optional = True
a.segment_id = 9999

print(a.is_last_keyword)
print(a.is_optional)
print(a.segment_id)

a.is_last_keyword = False
a.is_optional = False
a.segment_id = 2222

print(a.is_last_keyword)
print(a.is_optional)
print(a.segment_id)

