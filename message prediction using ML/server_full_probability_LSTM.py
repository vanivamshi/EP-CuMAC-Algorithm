# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

### UDP server

import socket
import os
import hashlib
import random

frag = 4

# Compare strings
def comp_str(x,y):
    z = x
    ch=0
    if len(x)==len(y):
        for i in range (len(x)):
            if x[i]!=y[i]:
                print("Strings are not equal. They do not match by " + str(len(x)-i) + " characters")
                ch=1
                break
        if(ch==0):
            print("Strings are equal")
    else:
        print("String lengths are not equal. All tag bits not received")
        z = y
        z = y.ljust(64-len(y) + len(y), '0')
        for i in range (len(z)):
            if (x[i]==z[i]):
                continue
            
            else:#if (z[i]!=y[i]):# and z[i]==0):
                print("Strings match by " + str(100*i/len(x)) + "%")
                print(len(z),i)
                ch=1
                break
        

# Deep learning - predict missing values or when message is not verified

import tensorflow as tf
from tensorflow.keras.layers import Dense, LSTM, Dropout, RepeatVector, TimeDistributed, Flatten
from tensorflow.keras.models import Sequential

import numpy as np

## LSTM
def viz_polymonial(X,y,N):
    X = X.reshape(4,1,1)
    y = y.reshape(4,1,1)

    model = Sequential([
                        LSTM(4, input_shape=(1,1)),
                        Dropout(0.2),
                        RepeatVector(4),
                        LSTM(20, return_sequences=True),
                        Dropout(0.2),
                        TimeDistributed(Dense(1)),
                        Flatten(),
                        #Dense(1, activation='softmax')
                        ])
    
    X_val = np.array([5])
    y_val = np.array([37])
    
    X_val = X_val.reshape(1,1,1)
    y_val = y_val.reshape(1,1,1)
    
    X_test = np.array([N])    
    X_test = X_test.reshape(1,1,1)
    
    model.fit(X, y, epochs=10, batch_size=1, verbose=2, validation_data=(X_val, y_val))
    
    model.compile(loss='mae', optimizer='adam')
    
    pred = model.predict(np.array([X_test]).reshape(1,1,1))
    print(pred)
    return



# shuffle tag list
seed = 0.1
def myfunction():
  return seed

t = [1, 2, 3, 4]
random.shuffle(t, myfunction)
print(t)

seed = seed + 0.1


# message used = 'abcdefghijkl'
#frag = 4


# set IP, port and buffer size
localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 1024

# set transmission rate to simulate NB-IoT performance
def calc_delay(signal):
   rate = 0.18 * ( float(signal) + 46 ) / 40    # bandwidth = 0.18M, rx power signals = 46 dBm and 23 dBm,divide by difference (gain) of 40dBm
   return(rate)

rate_cmd = 'iwconfig wlan0 rate %sM" % calc_delay(signal)'
os.system(rate_cmd)


# declare message to be sent to sender upon receiving a packet
msgFromServer       = "Hello UDP Client"
bytesToSend         = str.encode(msgFromServer)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort)) 

print("UDP listening")
 

cipher_array = []
tag1 = []
tag2 = []
tag3 = []
tag4 = []
h = []
c = []


# Listen for incoming datagrams - full authentication
i = 0
while(i<frag):

    # seperate message-tag packet from client address
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    cipher = bytesAddressPair[0]
    address = bytesAddressPair[1]    
    
    # seperate message from message-tag, store message in list 'c', calculate hash of message
    msg = cipher[0:2] #[0:16]
    c.append(msg) #c.append(cipher[12:])
    hsh = hashlib.sha256(msg).hexdigest()

    # calculate length of each fragment and divide hash into 4 fragments. store in h
    n = len(hsh)/4
    
    j = 0
    while (j<4) :
        h.append(hsh[j*n:(j+1)*n])
        j = j + 1


    # store the hashes in tags
    # tag1 = [h1[0],h1[1],h1[2],h1[3]]
    tag2.append(h[0+i])

    # tag2 = [h2[0],h2[1],h2[2],h2[3]]
    try:
        tag3.append(h[4+i])
    except IndexError:
        pass

    # tag3 = [h3[0],h3[1],h3[2],h3[3]]
    try:
        tag4.append(h[8+i])
    except IndexError:
        pass

    # tag4 = [h4[0],h4[1],h4[2],h4[3]]
    try:
        tag1.append(h[12+i])
    except IndexError:
        pass
    
    # Sending a reply to client
    UDPServerSocket.sendto(bytesToSend, address)
    i = i + 1



# verify tags with the cipher of each message stored in list 'c'
# as tags are in str, they have to be converted using hex(). as the resulting output is also str, tag values were individually declared    

# check lengths of tags to see if all of them have been received

# tag1[0]
if(len(tag1) == 1):
    if (hashlib.sha256(c[0]).hexdigest() == "d682ed4ca4d989c1"):  # sha 256
    #if (c[0] == "103ca96c06a1ce798f08f8ef"):  # sha 384
        print("message 1 verified")
    else:
        print("message 1 not verified")
        # use AI to predict value
        viz_polymonial(np.array([2,3,4]).reshape(-1,1),np.array([c[1],c[2],c[3]]),1)
else:
    print("message 1 not received")
    comp_str(hashlib.sha256(c[0]).hexdigest(),"d682ed4ca4d989c1")
    # predict correctness of values with probability


# tag2[0]^tag1[1]
if(len(tag4) == 2):
    if (hashlib.sha256(c[1]).hexdigest() == "d682ed4ca4d989c1" + "34ec94f1551e1ec5"):  # sha 256
    #if (c[1] == "103ca96c06a1ce798f08f8ef" + "f0dfb0ccdb567d48b285b23d"):  # sha 384
        print("message 2 verified")
    else:
        print("message 2 not verified")
        viz_polymonial(np.array([1,2,3]).reshape(-1,1),np.array([c[0],c[1],c[2]]),4)
else:
    print("message 2 not received")
    comp_str(hashlib.sha256(c[1]).hexdigest(),"d682ed4ca4d989c1" + "34ec94f1551e1ec5")


# tag3[0]^tag2[1]^tag1[2]
if(len(tag3) == 3):
    if (hashlib.sha256(c[2]).hexdigest() == "d682ed4ca4d989c1" + "34ec94f1551e1ec5" + "80dd6d5a6ecde9f3"):  # sha 256
    #if (c[2] == "103ca96c06a1ce798f08f8ef" + "f0dfb0ccdb567d48b285b23d" + "0cd773454667a3c2fa5f1b58"):  # sha 384
        print("message 3 verified")
    else:
        print("message 3 not verified")
        viz_polymonial(np.array([1,2,4]).reshape(-1,1),np.array([c[0],c[1],c[3]]),3)
else:
    print("message 3 not received")
    comp_str(hashlib.sha256(c[2]).hexdigest(),"d682ed4ca4d989c1" + "34ec94f1551e1ec5" + "80dd6d5a6ecde9f3")


# tag4[0]^tag3[1]^tag2[2]^tag1[3]
if(len(tag2) == 4):
    if (hashlib.sha256(c[3]).hexdigest() == "d682ed4ca4d989c1" + "34ec94f1551e1ec5" + "80dd6d5a6ecde9f3" + "d35e6e4a717fbde4"):  # sha 256
    #if (c[3] == "103ca96c06a1ce798f08f8ef" + "f0dfb0ccdb567d48b285b23d" + "0cd773454667a3c2fa5f1b58" + "d9cdf2329bd9979730bfaaff):  # sha 384
        print("message 4 verified")
    else:
        print("message 4 not verified")
        viz_polymonial(np.array([1,3,4]).reshape(-1,1),np.array([c[0],c[2],c[3]]),2)
else:
    print("message 4 not received")
    comp_str(hashlib.sha256(c[3]).hexdigest(),"d682ed4ca4d989c1" + "34ec94f1551e1ec5" + "80dd6d5a6ecde9f3" + "d35e6e4a717fbde4")

