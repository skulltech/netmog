import argparse
import socket
import subprocess
import sys
import threading


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

    def receive(self):
        response = b''
        while True:
            chunk = self.client.recv(4096)
            response = response + chunk
            if len(chunk) < 4096:
                break
        return response

    def send(self, data):
        self.client.send(data)

    def run_once(self, data):
        self.client.send(data.encode('UTF-8'))
        received = self.receive()
        print(received.decode('UTF-8'))

    def run(self):
        while True:
            data = input('[ netmog ] $ ')
            self.run_once(data)


class Server:
    def __init__(self, host, port, banner=None):
        self.host = host
        self.port = port
        self.banner = banner

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)

    def run(self):
        while True:
            conn, addr = self.server.accept()
            print(f'[*] Accepted connection from: {addr[0]}:{addr[1]}')

            handler_thread = threading.Thread(target=self.connection_handler, args=(conn, addr))
            handler_thread.start()

    def connection_handler(self, conn, addr):
        if self.banner:
            conn.send(self.banner.encode('UTF-8'))

        while True:
            command = self.receive(conn)
            command = command.splitlines()[0]
            command = command.decode('UTF-8')

            if command == '!quit':
                print(f'[*] Closing connection from {addr[0]}:{addr[1]}')
                conn.send(b'remote says :: connection closed')
                conn.close()
                return

            print(f'[*] Executing command: {command}')
            process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            conn.send(process.stdout)

    def receive(self, conn):
        response = b''
        while True:
            chunk = conn.recv(4096)
            response = response + chunk
            if len(chunk) < 4096:
                break
        return response


def main():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(title='mode', description='')
    client_parser = subparser.add_parser('client', help='client mode: for sending commands to a remote server')
    client_parser.add_argument('-t', '--host', required=True, help='target host')
    client_parser.add_argument('-p', '--port', required=True, type=int,
                               help='the port on which the target host is listening on')
    client_parser.set_defaults(mode='client')
    server_parser = subparser.add_parser('server', help='server mode: for executing commands from remote client')
    server_parser.add_argument('-t', '--host', default='0.0.0.0', help='hostname to bind to')
    server_parser.add_argument('-p', '--port', required=True, type=int, help='the port to listen on')
    server_parser.set_defaults(mode='server')
    args = parser.parse_args()

    try:
        mode = args.mode
    except AttributeError:
        parser.print_usage()
        return

    if mode == 'client':
        client = Client(args.host, args.port)
        data = ''.join(sys.stdin.readlines())
        if data:
            client.run_once(data)
        else:
            print(f'[*] Connected to {args.host}:{args.port}')
            client.run()
    else:
        server = Server(args.host, args.port)
        print(f'[*] Listening on {args.host}:{args.port}')
        server.run()


if __name__ == '__main__':
    main()
