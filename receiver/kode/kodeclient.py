#!/usr/bin/env python

import http.client
import sys

#get http server ip
http_server = sys.argv[1]
#create a connection
conn = http.client.HTTPConnection(http_server, 8080)

while 1:

    conn.request('GET', 'dummy.html')

    #get response from server
    rsp = conn.getresponse()
    
    #print server response and data
    print(rsp.status, rsp.reason)
    data_received = rsp.read()
    print(data_received)
    
    break
    
conn.close()
