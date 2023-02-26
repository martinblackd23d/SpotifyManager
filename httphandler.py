import socket

class tcpserver():
	def __init__(self, port, mode, host = '', encoding = 'ascii', buffer = 65536):
		self.port = port
		self.host = host
		self.encoding = encoding
		self.buffer = buffer
		self.mode = mode
		return


	def estconn(self, host, port):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((host, port))
		s.listen()
		#print('listening')
		conn, address = s.accept()
		#print('accepted')
		return conn, address, s



class httpserver(tcpserver):
	def httpserver(self):
		conn, address, s = self.estconn(self.host, self.port)
		data = conn.recv(65536).decode('ascii')
		#print('Raw package:\n' + data)
		response, location = self.genresponse(data)
		#print(response)
		conn.send(bytes(response, 'ascii'))
		conn.close
		#print('connection closed')
		return location

	def genresponse(self, data):
		trequest = data.split('\r\n\r\n')
		if len(trequest) == 2:
			body = trequest[1]
		else:
			body = ''
		theaders = trequest[0].split('\r\n')
		request = theaders[0].split()
		method = request[0]
		location = request[1]
		version = request[2]	

		headers = {}
		for line in range(1, len(theaders)):
			header = theaders[line].split(': ')
			headers[header[0]] = header[1]

		if method == 'GET':
#			file = open('C:\\Users\\Martin\\Desktop\\Projects\\UniversalSuite\\webserver\\default.html')
#			content = file.read()
			content = '<!DOCTYPE html>/r/n<html>/r/n<h1>Universal Suite Webserver</h1>/r/n</html>'
			response ='HTTP/1.1 200 OK\r\n\r\n' + content
#			file.close()
		else:
			response = 'HTTP/1.1 405 Method Not Allowed\r\n\r\n'

		#print('processed message:')
		#print('method: ' + method)
		#print('location: ' + location)
		#print('version: ' + version)
		#print(headers)
		#print('body: ' + body)

		return response, location

def listen():
	server = httpserver(8888, 'httpserver', '127.0.0.1')
	location = server.httpserver()
	return location