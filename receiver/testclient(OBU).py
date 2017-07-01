import http.client
import ssl 


if __name__ == '__main__':

	conn = http.client.HTTPConnection('localhost', 8080)
	conn.request("GET", "/")
	r1 = conn.getresponse()
	print(r1.status, r1.reason)
	print(r1.read())


	#~ conn = http.client.HTTPSConnection("www.python.org")
	#~ conn.request("GET", "/")
	#~ r1 = conn.getresponse()
	#~ print(r1.status, r1.reason)

#~ conn = http.client.HTTPConnection(http_server, 8080)
    #~ conn.request('GET', 'dummy.html')

    #~ #get response from server
    #~ rsp = conn.getresponse()
    
    #~ #print server response and data
    #~ print(rsp.status, rsp.reason)
    #~ data_received = rsp.read()
    #~ print(data_received)
