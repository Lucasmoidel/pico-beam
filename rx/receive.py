from machine import ADC, Pin
import time
from math_func import *

rx = ADC(Pin(27))

VREF = 3.3
RES = 65535

samples = 50

base = 0
peak = 65535

packet_size_bytes = 5

threshold = 0

# Modes
# 1 - Standby
# 2 - Sync-mode
# 3 - Receive mode
    
mode = 1

print("Configuring Ambient Voltage - Samples:",samples)

for x in range(samples):
    base += rx.read_u16()
    time.sleep(0.01)

base = int(base/samples)
threshold = (peak-base)/2

print("Configured Ambient Voltage:",base)

clock = 0
warning_bit_rxed = False
bits_rxed = 0
packet_num = 0
data_rxed = [[]]
bits_wo_one = 0 # bits without 1
byte = ""

ontime = -1
timings = []
lasttime = -1

def get_ms():
    return time.time_ns() // 1000000

while True:
    volts = rx.read_u16()
    
    if mode == 1:
        #print(volts)
        if volts > threshold:
            mode = 2
            lasttime = get_ms()
            print("Starting Data Receive")
        #time.sleep(0.05)
        continue
    if mode == 2:
        #print("Im stupid idiot",get_ms()-lasttime)
        if get_ms()-lasttime > 2000:
            median_timing = median(timings)
            print(timings)
            print("Found Packet Timing:",median_timing)
            clock = median_timing / 1000
            mode = 3
        if volts > threshold and ontime == -1:
            ontime = get_ms()
        if volts < threshold and ontime != -1:
            cur_time = get_ms()
            dur = cur_time - ontime
            timings.append(dur)
            print("Cur",cur_time,"Start",ontime)
            print(dur)
            ontime = -1
            lasttime = cur_time
        continue
    if mode == 3:
        #print(volts)
        if volts > threshold and warning_bit_rxed == False:
            print("Begin Data Stream")
            warning_bit_rxed = True
            time.sleep(clock)
            continue
        if warning_bit_rxed == False:
            time.sleep(clock)
            continue
        cur_bit = 0
        if volts > threshold:
            cur_bit = 1
            bits_wo_one = 0
            #print("back to 0")
        else:
            bits_wo_one += 1
        #data_rxed[packet_num].append(cur_bit)
        byte += str(cur_bit)
        bits_rxed += 1
        #print(bits_wo_one)
        if bits_rxed % 8 == 0:
            data_rxed[packet_num].append(byte)
            byte = ""
        if bits_rxed == 8 and bits_wo_one == 8:
            print("Final Data Sent:",data_rxed)
            #data_rxed = data_rxed.pop(len(data_rxed)-1)
            #data_rxed[packet_num].append(byte)
            mode = 1
            for packet in data_rxed:
                print("Final Decoded Message",''.join([chr(int(b, 2)) for b in packet]))
        if bits_rxed == packet_size_bytes*8:
            bits_rxed = 0
            packet_num += 1
            data_rxed.append([])
            print(data_rxed)
            bits_wo_one = 0
        time.sleep(clock)
        continue
    