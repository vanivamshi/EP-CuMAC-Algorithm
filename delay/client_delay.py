# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 12:36:05 2021

@author: vamshi
"""

# generate constant public and private key


# frequent communications - full hash, less communications - truncated hash (75% length of full hash)
# light-weight node and less communications - truncated hash (50% length of full hash)


### UDP client

import socket
import os
import hashlib
import timeit
import time
import math

# increase in data rate decreases transmission delay
# We'll limit ourself to a 40KB/sec maximum send rate
maxSendRateBytesPerSecond = (30*1024)
M = 0.608  #number of levels a single symbol can take - for C = 30*1024, B = 180kHz

def ConvertSecondsToBytes(numSeconds):
   return numSeconds*maxSendRateBytesPerSecond

def ConvertBytesToSeconds(numBytes):
   return float(numBytes)/maxSendRateBytesPerSecond


# at the schedule specified by (maxSendRateBytesPerSecond)
bytesAheadOfSchedule = 0

prevTime = None


message1 = 'Lorem Ipsum text'
message2 = 'Lorem Ipsum text'
message3 = 'Lorem Ipsum text'
message4 = 'Lorem Ipsum text'

# calculate hash
msg_hash = hashlib.sha256(message1).hexdigest()

#truncated_mac = (hashlib.sha256('Lorem Ipsum text').hexdigest())[:32] # truncate mac
# truncate to get last 128 characters
#l = len(str1)
#print(str1[l - 128:])

# message to be sent has to be sent in 'bytesTo Send'
serverAddressPort   = ("127.0.0.1", 20001)
bufferSize          = 1024

#noise = 

def calc_delay(signal):
   rate = 0.18 * ( float(signal) + 46 ) / 70    # bandwidth = 0.18M, tx power signals = 46 dBm and 23 dBm,divide by difference (gain) of 70dBm
   return(rate)

rate_cmd = 'iwconfig wlan0 rate %sM" % calc_delay(signal)'
os.system(rate_cmd)


# fragment message
frag = input('Input number of fragments = ')
m = []
h = []
t = []
e = []
s = []

# split bytesToSend to 4 fragments and store in msg[]
length = len(message1)
n = length/frag

m.append(message1)
m.append(message2)
m.append(message3)
m.append(message4)


#i = 0
#while (i<frag) :
#    m.append(message1[i*n:(i+1)*n])
#    i = i + 1


# fragment hash
# split bytesToSend to 4 fragments and store in msg[]
length = len(hashlib.sha256(message1).hexdigest())
n = length/frag

i = 0
while (i<frag) :
    h.append(msg_hash[i*n:(i+1)*n])
    i = i + 1


def prepend(list, str):
      
    # Using format()
    str += '{0}'
    list = [str.format(i) for i in list]
    return(list)

str = '0x'
h = prepend(h, str)
#print(h)
#an_integer = int(h, 16)
#h = hex(an_integer)


#for i in range(0, len(h)):
#    h[i] = hex(h[i])

h = [0x103ca96c06a1ce798f08f8ef, 0xf0dfb0ccdb567d48b285b23d, 0x0cd773454667a3c2fa5f1b58, 0xd9cdf2329bd9979730bfaaff]
#h = [0x103ca96c06a1, 0xce798f08f8ef, 0xf0dfb0ccdb56, 0x7d48b285b23d,
#     0x0cd773454667, 0xa3c2fa5f1b58, 0xd9cdf2329bd9, 0x979730bfaaff]


# calculate tags from hash fragments
t.append(h[0])
t.append(h[1]^h[0])
t.append(h[2]^h[1]^h[0])
t.append(h[3]^h[2]^h[1]^h[0])

#t.append(h[4]^h[3]^h[2]^h[1])
#t.append(h[5]^h[4]^h[3]^h[2])
#t.append(h[6]^h[5]^h[4]^h[3])
#t.append(h[7]^h[6]^h[5]^h[4])


t = ['5025095778980253837715634415',
 '69599189387669389377364904658',
 '73101831266818452109753733514',
 '16704449815391399881558850421']

#t = ['17852726511265', '244388578262606', '51241487443224', '92162015205157',
#     '87110493460451', '37944078578772', '12716486784219', '247730686880793']


# append message, tag and signature
e = [x + y for x, y in zip(m, t)]


# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

i = 0
# send packets
while (i == 0):
    
    now = time.time()
    if (prevTime != None):
        bytesAheadOfSchedule -= ConvertSecondsToBytes(now-prevTime)

    prevTime = now

    numBytesSent = UDPClientSocket.sendto(e[0], serverAddressPort)
    # 1
    start = timeit.default_timer()
    UDPClientSocket.sendto(e[0], serverAddressPort)
    #get reply
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    stop = timeit.default_timer()

    if (numBytesSent > 0):
      bytesAheadOfSchedule += numBytesSent
      if (bytesAheadOfSchedule > 0):
         time.sleep(ConvertBytesToSeconds(bytesAheadOfSchedule))
         
    ss = stop - start
    print(ss)
    if (ss > 1.5):
        print("High transmission delay. Vary parameters")
        #if time greater than permitted value, vary parameters and transmit next packet
        maxSendRateBytesPerSecond = 2*(180**3)*math.log(2*M*1.02, 2) # increase M by 10%

    # 2
    start = timeit.default_timer()
    UDPClientSocket.sendto(e[1], serverAddressPort)
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    stop = timeit.default_timer()
    
    if (numBytesSent > 0):
      bytesAheadOfSchedule += numBytesSent
      if (bytesAheadOfSchedule > 0):
         time.sleep(ConvertBytesToSeconds(bytesAheadOfSchedule))

    ss = stop - start
    print(ss)
    if (ss > 1.5):
        print("High transmission delay. Vary parameters")
        maxSendRateBytesPerSecond = 2*(180**3)*math.log(2*M*1.02, 2) # increase M by 10%

    # 3
    start = timeit.default_timer()
    UDPClientSocket.sendto(e[2], serverAddressPort)
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    stop = timeit.default_timer()

    if (numBytesSent > 0):
      bytesAheadOfSchedule += numBytesSent
      if (bytesAheadOfSchedule > 0):
         time.sleep(ConvertBytesToSeconds(bytesAheadOfSchedule))

    ss = stop - start
    print(ss)
    if (ss > 1.5):
        print("High transmission delay. Vary parameters")
        maxSendRateBytesPerSecond = 2*(180**3)*math.log(2*M*1.02, 2) # increase M by 10%

    # 4
    start = timeit.default_timer()
    UDPClientSocket.sendto(e[3], serverAddressPort)
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    stop = timeit.default_timer()

    if (numBytesSent > 0):
      bytesAheadOfSchedule += numBytesSent
      if (bytesAheadOfSchedule > 0):
         time.sleep(ConvertBytesToSeconds(bytesAheadOfSchedule))

    ss = stop - start
    print(ss)
    if (ss > 1.5):
        print("High transmission delay. Vary parameters")
        maxSendRateBytesPerSecond = 2*(180**3)*math.log(2*M*1.02, 2) # increase M by 10%

    i = i + 1
    

msgFromServer = UDPClientSocket.recvfrom(bufferSize)
msg = "Message from Server {}".format(msgFromServer[0])
print(msg)


# sinr (dB) = 10 log((PS-PN)/PN)   --> PS = output power, PN = output power - input power
# jitter = average of end to end delays
# RSSI = transmission power at receiver

# C(bps) = 2B * log2 (2M) (Nyquist), M = number of levels a single symbol can take on
# for C = 30*1024 and B = 180kHz -> M = 0.530