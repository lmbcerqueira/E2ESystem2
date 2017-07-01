from http.server import BaseHTTPRequestHandler, HTTPServer
import ssl

#~ class myHandler(BaseHTTPRequestHandler):
	
	#~ #Handler for the GET requests
	#~ def do_GET(self):
		#~ self.send_response(200)
		#~ self.send_header('Content-type','application/json')
		#~ self.end_headers()
		#~ # Send acks
		#~ #acks_list_test = {"acks":"1, 2, 3"}
		#~ #outMsg = json.loads(acks_list_test)
		#~ #self.wfile.write(outMsg)
		
		#~ # Send the html message
		#~ print("HERE")
		#~ self.send_response(200)
		#~ self.send_header('Content-type','text/html')
		#~ self.end_headers()		
		#~ self.wfile.write("Hello World !")
		#~ return
				
#~ if __name__ == '__main__':
	
	
	#~ try:
		#~ server = HTTPServer(('', PORT_OBU), myHandler)
		#~ print ("Started httpserver on port %d" % PORT_OBU)
		
		#~ server.serve_forever()

	#~ except KeyboardInterrupt:
		#~ print ("^C received, shutting down the web server")
		#~ server.socket.close()

class HTTPRequestHandler(BaseHTTPRequestHandler):
  
	#handle GET command
	def do_GET(self):

		#send code 200 response
		self.send_response(200)

		#send header first
		self.send_header('Content-type','text-html')
		self.end_headers()

		#send file content to client
		self.wfile.write('helloworld')
		return
      


  
if __name__ == '__main__':
	print('http server is starting...')

	#ip and port of servr
	#by default http server port is 80
	server_address = ('127.0.0.1', 4000)
	httpd = HTTPServer(server_address, HTTPRequestHandler)
	print('http server is running...')
	httpd.serve_forever()
