# Para testar juntamente com o OBUcomm.py - simula o helix client #

import threading
import socket
import sys
import time
import json

from settings import PORT
SLEEP = 2

def cycle(msg):

		try:
			# Send data

			outMsg = json.dumps(msg)

			outMsg_bytes = outMsg.encode('utf-8') #needed in python3
			sock.sendall(outMsg_bytes)

		finally:
			print ('msg sent: %s' %outMsg)


if __name__ == '__main__':


	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Connect the socket to the port where the server is listening
	server_address = ('localhost', PORT)
	print ('connecting to %s port %s' % server_address)
	sock.connect(server_address)

	while True:

		time.sleep(SLEEP)
		message = {"name":"John", "age":31, "city":"New York" }
		cycle(message)

		time.sleep(SLEEP)
		message = {"name":"Phil", "age":5, "city":"New" }
		cycle(message)

		time.sleep(SLEEP)
		message = {"name":"GG", "age":90, "city":"York" }
		cycle(message)

		time.sleep(SLEEP)
		message = {"name":"NNN", "age":12, "city":"Baltimore" }
		cycle(message)

		time.sleep(SLEEP)
		message = {"name":"NNN", "age":12, "city":"Baltimore" }
		cycle(message)

		time.sleep(SLEEP)
		message = {"name":"NNN", "age":12, "city":"Baltimore" }
		cycle(message)

		time.sleep(SLEEP)
		message = {"name":"NNN", "age":12, "city":"Baltimore" }
		cycle(message)

		time.sleep(SLEEP)
		message = {"name":"NNN", "age":12, "city":"Baltimore" }
		cycle(message)

		time.sleep(SLEEP)
		message = {"name":"GG", "age":90, "city":"York"}
		cycle(message)

	sock.close()
