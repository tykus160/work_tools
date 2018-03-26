#
# Simple parser of isq files used by QA team
# to listings compatible with pyrcu.
#
# Usage: ./parser.py 'input_file' 'output_file'
#

from sys import argv
from datetime import datetime

# 
REQUIRED_ARGS = 3

MICROS_IN_MILLI = 1000
MILLIS_IN_SEC = MICROS_IN_MILLI
SECS_IN_MIN = 60

class KeyAction:
    def __init__(self, keyCode, timestamp):
        self.keyCode = KeyAction.parseKeyCode(keyCode)
        self.timestamp = KeyAction.parseTimestamp(timestamp)

    # Replace some of keycodes, leave rest as it is
    def parseKeyCode(keyCode):
        return {
            "epg"      : "guide",
            "tv/radio" : "tv",
            "rew"      : "rewind",
            "ffw"      : "ffwd",
            "reclist"  : "0x1f0",
            "i"        : "info",
            "rec"      : "record"
        }.get(keyCode, keyCode)

    # parse from format mins:secs.millis to milliseconds
    def parseTimestamp(timestamp):
        keyTime = datetime.strptime(timestamp, "%M:%S.%f")
        return int(keyTime.minute * SECS_IN_MIN * MILLIS_IN_SEC + keyTime.second * MILLIS_IN_SEC + keyTime.microsecond / MICROS_IN_MILLI)

    def __str__(self):
        return self.keyCode + ' ' + str(self.timestamp)

def readFile(input, output):
    file = open(input, 'r')
    lines = file.readlines()
    file.close()

    keynames = []
    timestamps = []

    for line in lines:
        if "key name" in line:
            keynames.append(line.split('=')[1].strip())
        elif "time" in line:
            timestamps.append(line.split('=')[1].strip())

    if len(keynames) == len(timestamps):
        file = open(output, 'w')
        for key, time in zip(keynames, timestamps):
            file.write(str(KeyAction(key, time)) + '\n')
        file.close()
    else:
        print("Input file corrupted")

if len(argv) == REQUIRED_ARGS:
    print("Parsing input " + argv[1] + " to output " + argv[2])
    readFile(argv[1], argv[2])
    print("It was a joy to help you!")
else:
    print("Usage: " + argv[0] + " 'input_file' 'output_file'")
