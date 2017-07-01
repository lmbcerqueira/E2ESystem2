from http.server 	import BaseHTTPRequestHandler,HTTPServer
from window 		import Window_Element, isBetween, Window
from request 		import get_sqNrList
from settings 		import *

import json
import time
import threading
import socket
import settings

DELAY = 7 #check first the time where the server is going to run
windows = [] #windows - each element is a DCU's window
seq_nr = 0 #0 ate infinito

class acksManagementThread(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):

		start = time.localtime(time.time()-DELAY)
		end = time.localtime(time.time()-DELAY)

		while True:

			time.sleep(5)

			start = end
			end = time.localtime(time.time()-DELAY)

			## get seqNrs that arrived to the cloud -> store them on settings.sqNr_list
			get_sqNrList(start, end)

			## build acks list to send to the OBU
			global windows
			for DCUwindow in windows:
				for i in range(WINDOW_SIZE):
					for sqNr in settings.sqNr_list[DCUwindow.DCU_id]:
						if int(sqNr) == DCUwindow.window_elements[i].get_id():
							DCUwindow.window_elements[i].set_ack(True)
							DCUwindow.acks_list.append(int(sqNr))
							break
			## also append lost acks
			for DCUwindow in windows:
				for sqNr in settings.sqNr_list[DCUwindow.DCU_id]:
					if not isBetween(DCUwindow.window_elements[0].get_id(), int(sqNr), DCUwindow.window_elements[WINDOW_SIZE-1].get_id()):
						DCUwindow.acks_list.append(int(sqNr))
				settings.sqNr_list[DCUwindow.DCU_id] = []

			for DCUwindow in windows:
				while DCUwindow.window_elements[0].get_ack() == True:

					#shift para a esquerda
					for i in range(WINDOW_SIZE-1):
						DCUwindow.window_elements[i].set_id(DCUwindow.window_elements[i+1].get_id())
						DCUwindow.window_elements[i].set_ack(DCUwindow.window_elements[i+1].get_ack())

					#acrescentar novo elem no fim
					DCUwindow.window_elements[WINDOW_SIZE -1].set_ack(False)
					DCUwindow.window_elements[WINDOW_SIZE -1].set_id(DCUwindow.seqNr % (MAX_SEQ_NUMBER+1))
					DCUwindow.seqNr += 1

			#DEBUG
			#for DCUWindow in windows:
				#for i in range(WINDOW_SIZE):
					#print("[DCU %d]: %d; ack: %s" % (DCUWindow.DCU_id, DCUWindow.window_elements[i].get_id(), DCUWindow.window_elements[i].get_ack()))
				#print()



class acksSender(BaseHTTPRequestHandler):

	#Handler for the GET requests
	def do_GET(self):

		global windows

		# Send the html message
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()

		dcu_id = self.headers.get("DCU_ID")

		for window in windows:
			if int(dcu_id) == window.DCU_id:
				if not window.acks_list:
					acks = "EMPTY"
					print("empty acks_list")
				else:
					acks = ''
					acks = ', '.join(str(x) for x in window.acks_list)
					print("acks: %s" % acks)
				self.wfile.write(acks.encode())
				window.acks_list = []
				break


if __name__ == '__main__':

	settings.init()

	for j in range(N_DCUS):
		seq_nr = 0
		window_elements = [] #elements of each DCU's window
		for i in range(WINDOW_SIZE):
			window_elements.append(Window_Element(seq_nr % (MAX_SEQ_NUMBER+1)))
			seq_nr += 1
		windows.append(Window(j , window_elements, seq_nr, []))

	## Start thread to manage acks
	acksMng = acksManagementThread()
	acksMng.start()

	## start thread to manage OBUs' requests ##
	try:
		server_address = (SERVER_IP, PORT_OBU)
		server = HTTPServer(server_address, acksSender)
		print ("Started httpserver on port %d" % PORT_OBU)

		server.serve_forever()

	except KeyboardInterrupt:
		print ("^C received, shutting down the web server")
		server.socket.close()
