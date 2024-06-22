from brping import Ping1D
import serial
import time

myPing = Ping1D()
myPing.connect_serial('COM8',115200)

if myPing.initialize() is False:
    print("Failed to initialize Ping")
    exit(1)

while True:
    data = myPing.get_distance()
    if data:
        print("Distance: %s\tConfidence: %s%%" % (data["distance"], data["confidence"]))
    else:
        print("Failed to get distance data")
    
    time.sleep(5)