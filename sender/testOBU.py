from queue 				import Queue , Empty
from settings 			import *
from windowbuffer		import WindowBuffer_Element
from sender 			import send_bundle
from threading 			import Lock
from time 				import sleep
from windowManagement	import *
from log 				import *

import threading
import socket
import sys
import json
import settings
import time

seq_nr = 0
n_buffered = 0 ## from 0 to WINDOW_SIZE-1
window_elements = []
q = Queue()

class WindowManagThread(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):

		k=0
		global seq_nr

		while True:

			k += 1

			if k%7 == 0:
				sleep(3)
				print("sleep")

			if not q.empty():

					if q.empty():
						#print("empty queue")
						break
					try:
						bundle = q.get(False)
					except Empty:
						pass
					else: #add bundle to window
						print(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime(time.time())))
						bundle = json.loads(bundle)
						seq_bundle = seq_nr % (MAX_SEQ_NUMBER+1)
						bundle.update({'seqNr':seq_bundle}) #append seqNr to the message
						print(bundle)
						send_bundle(bundle)
						seq_nr += 1

class HandleConnThread(threading.Thread):

	def __init__(self, clientSocket, clientAddress):

		threading.Thread.__init__(self)
		self.clientSocket = clientSocket
		self.clientAddress = clientAddress

	def run(self):

		try:
			while True:

				inData = self.clientSocket.recv(1024)
				inData = inData.decode('utf-8')

				if inData:
					global q
					q.put(inData)
					#print("message added to queue: %s" % inData)
				else:
					print("no more data from OBU")
					break
		finally:
			clientSocket.close()


if __name__ == '__main__':

	settings.init()

	print("window size %d" % WINDOW_SIZE)

	windowMngThread = WindowManagThread()
	windowMngThread.start()

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = ('localhost', PORT)
	sock.bind(server_address)

	sock.listen(1)

	while True:

		(clientSocket, clientAddress) = sock.accept()
		connThread = HandleConnThread(clientSocket, clientAddress)
		connThread.start()
