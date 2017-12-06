import socket
import threading

host = '127.0.0.1'
port = 4000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
client.send(b'Hello! Is there anybody in there?!')
response = client.recv(4096)

print(response)


class TCPServer:
	def __init__(self, host='0.0.0.0', port=8000):
		self.host = host
		self.port = port
		self.connections = []

		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.bind((self.host, self.port))
		self.server.listen(5)
		print('[*] Listening on {}:{}'.format(bind_ip, bind_port))
		self.mthread = threading.Thread(target=self.mainthread, args=(,))

	def mainthread(self):
		while True:
			conn, addr = self.server.accept()
			print('[*] Accepted connection from: {}:{}'.format(addr[0], addr[1]))

			handler = threading.Thread(target=connhandler, args=(client,))
			handler.start()
			self.connections.append(handler)

	@staticmethod
	def connhandler(conn):
		request = conn.recv(1024)
		print('[*] Received: {}'.format(request))
		conn.send(b'ACK!')
		conn.close()
