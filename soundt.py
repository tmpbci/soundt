 
#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -*- mode: Python -*-

"""

Soundt
v0.1

LICENCE : CC
by Sam Neurohack 

"""

import traceback
import os
import time

from OSC3 import OSCServer, OSCClient, OSCMessage
import midi3
from sys import platform

myIP = "127.0.0.1"
myPort = 8085
print()
print("Soundt")

midi3.check()

#
# OSC
#

print()
print("OSC Server", myIP, ':', myPort)
oscserver = OSCServer((myIP, myPort))
oscserver.timeout = 0

# this method of reporting timeouts only works by convention
# that before calling handle_request() field .timed_out is 
# set to False
def handle_timeout(self):
    self.timed_out = True

# funny python's way to add a method to an instance of a class
import types
oscserver.handle_timeout = types.MethodType(handle_timeout, oscserver)

# RAW OSC Frame available ? 
def OSCframe():
    # clear timed_out flag
    oscserver.timed_out = False
    # handle all pending requests then return
    while not oscserver.timed_out:
        oscserver.handle_request()


# Properly close the system. Todo
def OSCstop():
    oscserver.close()


# default handler
def OSChandler(path, tags, args, source):

    oscaddress = ''.join(path.split("/"))
    print()
    print("Default OSC Handler got from " + str(source[0]),"OSC msg", path, "args", args)
    #print("OSC address", path)

    if len(args) > 0:
        #print("with args", args)
        pass

def OSCNote(path, tags, args, source):

    print("Got", path, args)
    note = args[0]


    if note == 1:

        if platform == 'darwin':
            os.system("afplay snare.wav")
        else:
            os.system("aplay snare.wav")


    if note == 2:
      
        if platform == 'darwin':
            os.system("afplay kick.wav")
        else:
            os.system("aplay kick.wav")


def Run():


    print("Running...")
    oscserver.addMsgHandler("default", OSChandler)
    oscserver.addMsgHandler("/note/on", OSCNote)

    
    try:
    
        while True:
    
            # OSC event
            OSCframe()
            time.sleep(0.01)


    except Exception:
        traceback.print_exc()
    
    finally:
    
        print ("soundt Stopping...")
        OSCstop()
    
    

if __name__ == '__main__':

    Run()