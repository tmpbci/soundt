#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Midi3 light version for soundt
v0.7.0

Midi Handler : 

- Hook to the MIDI host
- Enumerate connected midi devices and spawn a process/device to handle incoming events

by Sam Neurohack 
from /team/laser


"""


import time

import rtmidi
from rtmidi.midiutil import open_midiinput 
from threading import Thread
from rtmidi.midiconstants import (CHANNEL_PRESSURE, CONTROLLER_CHANGE, NOTE_ON, NOTE_OFF,
                                  PITCH_BEND, POLY_PRESSURE, PROGRAM_CHANGE)
import mido
from mido import MidiFile
import traceback
import weakref
import sys
from sys import platform
import os

from queue import Queue


print()
#print('midi3')
#print('Midi startup...')


midiname = ["Name"] * 16
midiport = [rtmidi.MidiOut() for i in range(16) ]

OutDevice = [] 
InDevice = []

# max 16 midi port array 

midinputsname = ["Name"] * 16
midinputsqueue = [Queue() for i in range(16) ]
midinputs = []




BhorealPort, Midi1Port, Midi2Port, VirtualPort, MPort = -1,-1,-1, -1, -1
VirtualName = "LaunchPad Mini"
Mser = False

# Myxolidian 3 notes chords list
Myxo = [(59,51,54),(49,52,56),(49,52,56),(51,54,57),(52,56,59),(52,56,59),(54,57,48),(57,49,52)]
MidInsNumber = 0


clock = mido.Message(type="clock")

start = mido.Message(type ="start")
stop = mido.Message(type ="stop")
ccontinue = mido.Message(type ="continue")
reset = mido.Message(type ="reset")
songpos = mido.Message(type ="songpos")

#mode = "maxwell"

'''
print("clock",clock)
print("start",start)
print("continue", ccontinue)
print("reset",reset)
print("sonpos",songpos)
'''

try:
    input = raw_input
except NameError:
    # Python 3
    StandardError = Exception


STATUS_MAP = {
    'noteon': NOTE_ON,
    'noteoff': NOTE_OFF,
    'programchange': PROGRAM_CHANGE,
    'controllerchange': CONTROLLER_CHANGE,
    'pitchbend': PITCH_BEND,
    'polypressure': POLY_PRESSURE,
    'channelpressure': CHANNEL_PRESSURE
}



notes = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
def midi2note(midinote):

    print("midinote",midinote, "note", notes[midinote%12]+str(round(midinote/12)))
    return notes[midinote%12]+str(round(midinote/12))


#
# MIDI Startup and handling
#
      
mqueue  = Queue()
inqueue = Queue()

#
# Events from Generic MIDI Handling
#

def MidinProcess(inqueue, portname):

    inqueue_get = inqueue.get

    while True:
        time.sleep(0.001)
        msg = inqueue_get()
        print()
        print("Generic from", portname,"msg : ", msg)
        
        # Note On
        if msg[0]==NOTE_ON:

            MidiChannel = msg[0]-144
            MidiNote = msg[1]
            MidiVel = msg[2]
            print ("NOTE ON :", MidiNote, 'velocity :', MidiVel, "Channel", MidiChannel)
        
        
            if MidiNote < 63 and MidiVel >0:
        
                if platform == 'darwin':
                    os.system("afplay snare.wav")
                else:
                    os.system("aplay snare.wav")
        
        
            if MidiNote > 62 and MidiVel >0:
              
                if platform == 'darwin':
                    os.system("afplay kick.wav")
                else:
                    os.system("aplay kick.wav")
        
                    
                
        # Note Off
        if msg[0]==NOTE_OFF:
            print ("NOTE OFF :", MidiNote, 'velocity :', MidiVel, "Channel", MidiChannel)

                
        # Midi CC message          
        if msg[0] == CONTROLLER_CHANGE:
            print("CC :", msg[1], msg[2])


        # other midi message  
        if msg[0] != NOTE_OFF and  msg[0] != NOTE_ON and msg[0] != CONTROLLER_CHANGE:
            pass



       
# Generic call back : new msg forwarded to queue 
class AddQueue(object):
    def __init__(self, portname, port):
        self.portname = portname
        self.port = port
        #print("AddQueue", port)
        self._wallclock = time.time()

    def __call__(self, event, data=None):
        message, deltatime = event
        self._wallclock += deltatime
        #print("inqueue : [%s] @%0.6f %r" % ( self.portname, self._wallclock, message))
        message.append(deltatime)
        midinputsqueue[self.port].put(message)


#    
# MIDI OUT Handling
#


class OutObject():

    _instances = set()
    counter = 0

    def __init__(self, name, kind, port):

        self.name = name
        self.kind = kind
        self.port = port
        
        self._instances.add(weakref.ref(self))
        OutObject.counter += 1

        print(self.name, "kind", self.kind, "port", self.port)

    @classmethod
    def getinstances(cls):
        dead = set()
        for ref in cls._instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.add(ref)
        cls._instances -= dead

    def __del__(self):
        OutObject.counter -= 1



def OutConfig():
    global midiout, MidInsNumber
    
    # 
    if len(OutDevice) == 0:
        print("")
        print("MIDIout...")
        print("List and attach to available devices on host with IN port :")
    
        # Display list of available midi IN devices on the host, create and start an OUT instance to talk to each of these Midi IN devices 
        midiout = rtmidi.MidiOut()
        available_ports = midiout.get_ports()
    
        for port, name in enumerate(available_ports):
    
            midiname[port]=name
            midiport[port].open_port(port)
            #print()
            #print("New OutDevice [%i] %s" % (port, name))

            OutDevice.append(OutObject(name, "generic", port))
    
        #print("")      
        print(len(OutDevice), "Out devices")
        #ListOutDevice()
        MidInsNumber = len(OutDevice)+1

def ListOutDevice():

    for item in OutObject.getinstances():

        print(item.name)

def FindOutDevice(name):

    port = -1
    for item in OutObject.getinstances():
        #print("searching", name, "in", item.name)
        if name == item.name:
            #print('found port',item.port)
            port = item.port
    return port


def DelOutDevice(name):

    Outnumber = Findest(name)
    print('deleting OutDevice', name)

    if Outnumber != -1:
        print('found OutDevice', Outnumber)
        delattr(OutObject, str(name))
        print("OutDevice", Outnumber,"was removed")
    else:
        print("OutDevice was not found")



#    
# MIDI IN Handling 
# Create processing thread and queue for each device
#

class InObject():

    _instances = set()
    counter = 0

    def __init__(self, name, kind, port, rtmidi):

        self.name = name
        self.kind = kind
        self.port = port
        self.rtmidi = rtmidi
        self.queue = Queue()
        
        self._instances.add(weakref.ref(self))
        InObject.counter += 1

        #print("Adding InDevice name", self.name, "kind", self.kind, "port", self.port,"rtmidi", self.rtmidi, "Queue", self.queue)

    @classmethod
    def getinstances(cls):
        dead = set()
        for ref in cls._instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.add(ref)
        cls._instances -= dead

    def __del__(self):
        InObject.counter -= 1


def InConfig():

    print("")
    print("MIDIin...")
    print("List and attach to available devices on host with OUT port :")

    if platform == 'darwin':
        mido.set_backend('mido.backends.rtmidi/MACOSX_CORE')

    genericnumber = 0

    for port, name in enumerate(mido.get_input_names()):


        outport = FindOutDevice(name)
        midinputsname[port]=name
        
        #print("name",name, "Port",port, "Outport", outport)
        

        try:
            #print (name, name.find("RtMidi output"))
            if name.find("RtMidi output") > -1:
                print("No thread started for device", name)
            else:
                portin = object
                port_name = ""
                portin, port_name = open_midiinput(outport)
                #midinputs.append(portin)
                InDevice.append(InObject(name, "generic", outport, portin))
                
                thread = Thread(target=MidinProcess, args=(midinputsqueue[port],port_name))
                thread.setDaemon(True)
                thread.start() 

                print("Thread launch for midi port", port, "portname", port_name)
                #midinputs[port].set_callback(AddQueue(name),midinputsqueue[port])
                #midinputs[port].set_callback(AddQueue(name))
                #genericnumber += 1
                InDevice[port].rtmidi.set_callback(AddQueue(name,port))

        except Exception:
            traceback.print_exc()
                    
    #print("")      
    print(InObject.counter, "In devices")
    #ListInDevice()


def ListInDevice():

    for item in InObject.getinstances():

        print(item.name)

def FindInDevice(name):

    port = -1
    for item in InObject.getinstances():
        #print("searching", name, "in", item.name)
        if name in item.name:
            #print('found port',item.port)
            port = item.port
    return port


def DelInDevice(name):

    Innumber = Findest(name)
    print('deleting InDevice', name)

    if Innumber != -1:
        print('found InDevice', Innumber)
        delattr(InObject, str(name))
        print("InDevice", Innumber,"was removed")
    else:
        print("InDevice was not found")



def End():
    global midiout
    
    #midiin.close_port()
    midiout.close_port()
  
    #del virtual
    if launchpad.Here != -1:
        del launchpad.Here
    if bhoreal.Here  != -1:
        del bhoreal.Here
    if LPD8.Here  != -1:
        del LPD8.Here


def listdevice(number):
	
	return midiname[number]
	
def check():

    OutConfig()
    InConfig()
    
    #return listdevice(255)

	