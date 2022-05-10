# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 12:36:05 2021

@author: vamshi
"""

### UDP client

import socket
import os
import hashlib

# Initialise messages to be sent
message1 = 'abcdefghijkl'
message2 = 'abcdefghijkl'
message3 = 'abcdefghijkl'
message4 = 'abcdefghijkl'

# calculate hash for each message
msg_hash1 = hashlib.sha384(message1).hexdigest()
msg_hash2 = hashlib.sha384(message2).hexdigest()
msg_hash3 = hashlib.sha384(message3).hexdigest()
msg_hash4 = hashlib.sha384(message4).hexdigest()

# set buffer size and port
serverAddressPort   = ("127.0.0.1", 20001)
bufferSize          = 1024


# set transmission rate to simulate NB-IoT performance
def calc_delay(signal):
   rate = 0.18 * ( float(signal) + 46 ) / 70    # bandwidth = 0.18M, tx power signals = 46 dBm and 23 dBm,divide by difference (gain) of 70dBm
   return(rate)

rate_cmd = 'iwconfig wlan0 rate %sM" % calc_delay(signal)'
os.system(rate_cmd)


#frag = input('Input number of fragments = ')
frag = 4
m = []
h1 = []
h2 = []
h3 = []
h4 = []
t = []
e = []


# add messages in message list
m.append(message1)
m.append(message2)
m.append(message3)
m.append(message4)


# fragment hash
# split hash of messages to 4 fragments and store in h1, h2, h3 and h4
length = len(hashlib.sha384(message1).hexdigest())
n = length/frag

i = 0
while (i<frag) :
    h1.append(msg_hash1[i*n:(i+1)*n])
    h2.append(msg_hash2[i*n:(i+1)*n])
    h3.append(msg_hash3[i*n:(i+1)*n])
    h4.append(msg_hash4[i*n:(i+1)*n])
    i = i + 1


# hashes are in hexadecimal. as fragmented hashes do not have 0x before them, prepend 0x
def prepend(list, str):
      
    # Using format()
    str += '{0}'
    list = [str.format(i) for i in list]
    return(list)

str = '0x'
h1 = prepend(h1, str)
h2 = prepend(h2, str)
h3 = prepend(h3, str)
h4 = prepend(h4, str)


# h1, h2, h3, h4 are of type string. convert to hex
#an_integer = int(h, 16)
#h = hex(an_integer)


#for i in range(0, len(h)):
#    h[i] = hex(h[i])

# even after executing the above lines, hashes are of type string. so, hashes we redeclared as follows
h1 = [0x103ca96c06a1ce798f08f8ef, 0xf0dfb0ccdb567d48b285b23d, 0x0cd773454667a3c2fa5f1b58, 0xd9cdf2329bd9979730bfaaff]
h2 = [0x103ca96c06a1ce798f08f8ef, 0xf0dfb0ccdb567d48b285b23d, 0x0cd773454667a3c2fa5f1b58, 0xd9cdf2329bd9979730bfaaff]
h3 = [0x103ca96c06a1ce798f08f8ef, 0xf0dfb0ccdb567d48b285b23d, 0x0cd773454667a3c2fa5f1b58, 0xd9cdf2329bd9979730bfaaff]
h4 = [0x103ca96c06a1ce798f08f8ef, 0xf0dfb0ccdb567d48b285b23d, 0x0cd773454667a3c2fa5f1b58, 0xd9cdf2329bd9979730bfaaff]


# calculate tags from hash fragments
t.append(h1[0])
t.append(h1[1]^h2[0])
t.append(h1[2]^h2[1]^h3[0])
t.append(h1[3]^h2[2]^h3[1]^h4[0])

# to append tag along with message, tag has to be converted from hex to string
# but this process prints int equivalent of hex in str format. so, t was redeclared with original values as a string
t = ['5025095778980253837715634415',
 '69599189387669389377364904658',
 '73101831266818452109753733514',
 '16704449815391399881558850421']


# append each message with their tag
e = [x + y for x, y in zip(m, t)]


# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


# send packets
# each packet is sent. after a reply is received from receiver, next packet is sent
UDPClientSocket.sendto(e[0], serverAddressPort)
msgFromServer = UDPClientSocket.recvfrom(bufferSize)
msg = "Message from Server {}".format(msgFromServer[0])
print(msg)

UDPClientSocket.sendto(e[1], serverAddressPort)
msgFromServer = UDPClientSocket.recvfrom(bufferSize)
msg = "Message from Server {}".format(msgFromServer[0])
print(msg)

UDPClientSocket.sendto(e[2], serverAddressPort)
msgFromServer = UDPClientSocket.recvfrom(bufferSize)
msg = "Message from Server {}".format(msgFromServer[0])
print(msg)

UDPClientSocket.sendto(e[3], serverAddressPort)
msgFromServer = UDPClientSocket.recvfrom(bufferSize)
msg = "Message from Server {}".format(msgFromServer[0])
print(msg)
