#!/usr/bin/env python

def tologs(data):
    f = open("logfile", "a")
    f.write(data)
    f.close