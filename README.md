# netmog
A `netcat` alternative with remote code execution.

# Usage

```console
sumit@HAL9000:~/Coding/netmog$ python3 netmog.py -h
usage: netmog.py [-h] {client,server} ...

optional arguments:
  -h, --help       show this help message and exit

mode:

  {client,server}
    client         client mode: for sending commands to a remote server
    server         server mode: for executing commands from remote client

```

As you can see above, `netmog` has two modes — _client_ and _server_. 

## Client mode

```console
sumit@HAL9000:~/Coding/netmog$ python3 netmog.py client -h
usage: netmog.py client [-h] -t HOST -p PORT [-s]

optional arguments:
  -h, --help            show this help message and exit
  -t HOST, --host HOST  target host
  -p PORT, --port PORT  the port on which the target host is listening on
  -s, --shell           shell mode, to use with a remote netmog server
```

If you're using `netmog` to send commands to a remote `netmog` server, use the `--shell` flag to use it in shell mode. For example, the following connects to the remote `netmog` server at `localhost:5050` ::

### Shell mode
```console
sumit@HAL9000:~/Coding/netmog$ python3 netmog.py client -t localhost -p 5050 --shell
[*] Connected to localhost:5050
[ netmog ] $ ls
LICENSE
netmog.py
README.md

[ netmog ] $ 
```
Of course, for this to work, you'll have to run a `netmog` server at `localhost:5050`. Get the instructions for that [here](#server-mode).

### Netcat mode

You can also use `netmog` as a standard `netcat`-like utility, which is the actually default mode for the `netmog` client. Only thing you have to keep in mind is 

__Note__ — In this mode, pressing `Enter`// newline doesn't send the request; `Ctrl+D`// `EOF` does. This is done so that the request body can contain newlines.

In the following example, `netmog` is used to send an HTTP `GET` request to `google.com`.
```console
sumit@HAL9000:~/Coding/netmog$ python3 netmog.py client -t google.com -p 80
GET / HTTP/1.1
Host: google.com

HTTP/1.1 301 Moved Permanently
Location: http://www.google.com/
Content-Type: text/html; charset=UTF-8
Date: Tue, 14 Apr 2020 17:47:57 GMT
Expires: Thu, 14 May 2020 17:47:57 GMT
Cache-Control: public, max-age=2592000
Server: gws
Content-Length: 219
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN

<HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">
<TITLE>301 Moved</TITLE></HEAD><BODY>
<H1>301 Moved</H1>
The document has moved
<A HREF="http://www.google.com/">here</A>.
</BODY></HTML>
```

## Server mode
```console
sumit@HAL9000:~/Coding/netmog$ python3 netmog.py server -h
usage: netmog.py server [-h] [-t HOST] -p PORT

optional arguments:
  -h, --help            show this help message and exit
  -t HOST, --host HOST  hostname to bind to
  -p PORT, --port PORT  the port to listen on
```

The `netmog` server binds to a mentioned `host:port` and keeps listening for incoming connections. Once it receives a message, it executes that as a `shell` command and returns the resulting output, i.e. `stdout` and `stderr` combined.

One thing to note is that here the `--host` argument is optional, by default it takes the value of `0.0.0.0`. See the following example to see it in action ::

```console
sumit@HAL9000:~/Coding/netmog$ python3 netmog.py server -p 5050
[*] Listening on 0.0.0.0:5050
[*] Accepted connection from: 127.0.0.1:41784
[*] Executing command: ls
```
