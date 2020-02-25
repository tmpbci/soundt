Soundt v0.1

Loosely play wav files from OSC and Midi commands. It should run on Linux (aplay) and OS X (afplay). Soundt will spawn a thread for each connected midi instrument to handle incoming messages.

Kick :

/note/on 1 or a midi note <63

Snare :
/note/on 2 or a midi note >62


# To modify/expand :

Midi events : search Midinprocess() in midi3.py


OSC events  : /note/on goes to OSCNote() everything else to the default Handler. Read the code for more.


# Install

sudo apt install python3-pip 

pip3 install python-rtmidi (you may need first : sudo apt install libasound2-dev, sudo apt install libjack-dev)

pip3 install mido


# Run

Launch/connect your midi "instruments" first. 

python3 soundt.py



