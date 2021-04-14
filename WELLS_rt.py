# WELLS - MAIXduino NTP realtime update


import usocket as socket
import ustruct as struct
import network
import gc
import os
import lcd, image
import machine
from board import board_info
import utime
from Maix import GPIO
from Maix import I2S
from fpioa_manager import *



# Network Credentials
SSID = "YOUR WIFI HERE"
PWD = "YOUR PW HERE"


# (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60
NTP_DELTA = 3155673600

# The NTP host can be configured at runtime by doing: ntptime.host = 'myhost.org'
host = "pool.ntp.org"

# Variable for our current time
currTime = 0
def time():
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B

    s = socket.socket()

    # addr = socket.getaddrinfo('198.60.22.240', 123)[0][-1]
    addr = socket.getaddrinfo(host, 123)[0][-1]


    # create a DGRAM UDP socket with the specified port and address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    #s.connect(addr)

    try:
        s.settimeout(1)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
    finally:
        s.close()
    val = struct.unpack("!I", msg[40:44])[0]

    return val - NTP_DELTA

def settime():
    t = time()
    #rtc = machine.RTC()
    #rtc.init((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
    return t

def Realtime():
    t2 = utime.localtime(currTime)
    print("Current time is: ", t2[3],":",t2[4],":",t2[5]," on ",t2[1],"/",t2[2],"/",t2[0])


#iomap at MaixDuino for ESP32
fm.register(25,fm.fpioa.GPIOHS10)#cs
fm.register(8,fm.fpioa.GPIOHS11)#rst
fm.register(9,fm.fpioa.GPIOHS12)#rdy
fm.register(28,fm.fpioa.GPIOHS13)#mosi
fm.register(26,fm.fpioa.GPIOHS14)#miso
fm.register(27,fm.fpioa.GPIOHS15)#sclk


nic = network.ESP32_SPI(cs=fm.fpioa.GPIOHS10,rst=fm.fpioa.GPIOHS11,rdy=fm.fpioa.GPIOHS12,
mosi=fm.fpioa.GPIOHS13,miso=fm.fpioa.GPIOHS14,sclk=fm.fpioa.GPIOHS15)

wifi = nic.scan()
for v in wifi:
    print(v, end="\n")
print()

nic.isconnected()
nic.connect(SSID,PWD)
if nic.isconnected():
    print("Connection Successful")

print("Time before sync:")
Realtime()
currTime = settime()
print("Time after sync:")
Realtime()


