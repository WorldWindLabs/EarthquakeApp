#!/usr/bin/python3

import time
import http.client, urllib.parse  # http and url libs used for HTTP POSTs
import socket  # socket used to get host name/IP
from struct import *
import random
import sys
import os

#################
## Phant Stuff ##
#################
#server = "10.193.20.17"  # base URL of your feed
# server = "24.237.235.227"
server = "127.0.0.1"
port = 5000

publicKey = "ppkZO7k2gvu2RWqbjdj4u2re9m8"  # public key, everyone can see this
privateKey = "n1v2byvwPKtZV0z2GeG9tGw3Y6B"  # private key, only you should know
fields = ["timestamp", "x", "y", "z"]  # Your feed's data fields

######################
## I/O Stuff & Misc ##
######################

##########
## Loop ##
##########


# Our first job is to create the data set. Should turn into
# something like "light=1234&switch=0&name=raspberrypi"

logline = {}
ts_old = 0
count_old = 0
last_mtime = 0

data = {}

socket.setdefaulttimeout(10)


raw_value = "{0:0{1}x}".format(random.randint(0,0xffffffffffff),12)
print (raw_value)

line = bytearray.fromhex(raw_value)

(x, y, z) = unpack('>hhh', line)  # Not sure of endian direction

nT = 100000

x = (x / 15000) * nT
y = (y / 15000) * nT
z = (z / 15000) * nT

x = round(x, 2)
y = round(y, 2)
z = round(z, 2)

print(x, y, z)
# exit()

data[fields[0]] = 0
data[fields[1]] = x
data[fields[2]] = y
data[fields[3]] = z

params = urllib.parse.urlencode(data)
# Now we need to set up our headers:
headers = {}  # start with an empty set
# These are static, should be there every time:
headers["Content-Type"] = "application/x-www-form-urlencoded"
headers["Connection"] = "close"
headers["Content-Length"] = len(params)  # length of data
headers["Phant-Private-Key"] = privateKey  # private key header

# Now we initiate a connection, and post the data

try:

    c = http.client.HTTPConnection(server, port)
    # Here's the magic, our reqeust format is POST, we want
    # to send the data to data.sparkfun.com/input/PUBLIC_KEY.txt
    # and include both our data (params) and headers
    c.request("POST", "/input/" + publicKey + ".txt", params, headers)
    r = c.getresponse()  # Get the server's response and print it

    print(r.read(), r.status, r.reason)

except Exception as err:

    print("Got error in transmit: ", err)
    pass


