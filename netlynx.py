import socket
import threading
import subprocess
import argparse
import random


PORT = 5002


class TCPClient:
    def __init__(self):
        host = '127.0.0.1'
        port = PORT

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

    @staticmethod
    def receive(conn):
        response = ''
        while True:
            chunk = conn.recv(4096)
            response = response + chunk.decode('UTF-8')
            if len(chunk) < 4096:
                break
        return response

    def execute(self):
        while True:
            self.client.send(input().encode('UTF-8'))
            print(self.receive(self.client))


class TCPServer:
    def __init__(self, host='0.0.0.0', port=PORT):
        self.host = host
        self.port = port
        self.connections = []

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        print('[*] Listening on {}:{}'.format(self.host, self.port))
        self.mainthread()

    def mainthread(self):
        while True:
            conn, addr = self.server.accept()
            print('[*] Accepted connection from: {}:{}'.format(addr[0], addr[1]))

            handler = threading.Thread(target=self.connhandler, args=(conn,))
            handler.start()
            self.connections.append(handler)

    def connhandler(self, conn):
        conn.send('''
            Greeting from NetLynx at {}
            Now it is time to Fuck Shit Up, or as we like to call it, FSU!
            '''.format(self.host).encode('UTF-8'))
        
        while self.execute(conn):
            pass
        conn.close()

    def execute(self, conn):
        conn.send('FSU@NetLynx.. '.encode('UTF-8'))

        command = ''
        while True:
            chunk = conn.recv(1024)
            command = command + chunk.decode('UTF-8')
            if len(chunk) < 4096:
                break
        command = command.splitlines()[0]

        if command == 'qnl!':
            return False

        print('[!] Executing command: {}'.format(command))
        process = subprocess.Popen(command, stdout=subprocess.PIPE)
        output, err = process.communicate()
        conn.send(output)
        return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', help='Whether to send or receive', type=str, choices=['send', 'receive'])
    args = parser.parse_args()
    
    if args.mode=='send':
        client = TCPClient()
        client.execute()

    else:
        server = TCPServer()


if __name__ == '__main__':
    main()
