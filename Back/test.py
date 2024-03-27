import json
import customtkinter as ctk
import ttkbootstrap as btrp

class params:
    def __init__(self):
        self.d = dict()

class algorithm:
    def __init__(self):
        self.p = params()


class alg1(algorithm):
    pass

class alg2(algorithm):
    pass

a1 = alg1()
a2 = alg2()

a1.p.d[int] = 5
print(a1.p.d, a2.p.d)
