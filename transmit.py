from machine import Pin
import time

VERSION = 145 # set version number

laser = Pin(0, Pin.OUT) # init the laser pin

clock = 0.2;

def sync(x): # define sync function that takes in number of blinks
    for i in range(x):
        laser.value(0)
        time.sleep(clock)
        laser.value(1)
        time.sleep(clock)
    laser.value(0)
        
        
sync(5) # runs the sync function and makes the laser blink 4 times
laser.value(0)

time.sleep(3)

packet = "" # creates the packet variable

packet += '{0:08b}'.format(VERSION) # adds the version number to the packet
packet = "1001010111010100"
laser.value(1)
time.sleep(clock)
for i in packet:
    laser.value(int(i))
    time.sleep(clock)
    
laser.value(0)
print(packet)