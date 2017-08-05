import socket
import threading
import signal
import sys
import fnmatch
from imp import reload
from logging.handlers import RotatingFileHandler
from urllib.parse import urlparse

import config
import logging


def is_ip_allowed(host):
    for ip in config.ip_allowed:
        if fnmatch.fnmatch(host, ip):
            return True
    return False


# logging
my_handler = RotatingFileHandler(
    config.log_file,
    maxBytes=config.max_bytes,
    backupCount=config.backup_count
)
my_handler.setFormatter(logging.Formatter(config.log_formatter, datefmt=config.date_fmt))
my_handler.setLevel(logging.INFO)

app_log = logging.getLogger('root')
app_log.setLevel(logging.INFO)
app_log.addHandler(my_handler)


def log(method, message):
    reload(config)
    if config.log_on:
        # call_function = "app_log.%s" % method + "(" + message + ")"
        call_function = getattr(app_log, method)
        call_function(message)


class Server:
    def __init__(self):
        reload(config)
        # socket
        signal.signal(signal.SIGINT, self.shutdown)
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSocket.bind((config.host, config.port))

    def listen(self):
        while True:
            self.serverSocket.listen(10)
            client_socket, client_address = self.serverSocket.accept()  # Establish the connection
            threading.Thread(target=self.proxy_thread, args=(client_socket, client_address)).start()

    @staticmethod
    def proxy_thread(conn, client_address):
        reload(config)
        data = conn.recv(config.max_request_length)
        http = data.decode().split('\n')[0]
        try:
            url = http.split(' ')[1]
            host = urlparse(url)
        except:
            log('error', http)
            raise

        if host.hostname is None:
            log('error', '404 Not found: ' + http)
            conn.send(str.encode('HTTP/1.1 404 Not Found\r\n'))
            conn.close()
            return

        if not is_ip_allowed(client_address[0]):
            log('error', '403 Forbidden: ' + http)
            conn.send(str.encode('HTTP/1.1 403 Forbidden\r\n'))
            conn.close()
            return

        port = 80 if host.port is None else host.port

        log('info', 'Request: ' + http)

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(config.connection_timeout)
            s.connect((host.hostname, port))
            s.sendall(data)
        except socket.error as e:
            # Something else happened, handle error, exit, etc.
            log('error', e)
            if s:
                s.close()
            if conn:
                conn.close()

        while True:
            try:
                data = s.recv(config.max_request_length)
                if len(data) > 0:
                    conn.send(data)
                else:
                    s.close()
                    conn.close()
                    break
            except socket.timeout as e:
                err = e.args[0]
                if err == 'timed out':
                    log('info', 'function recv timed out, retry later')
                    continue
                else:
                    log('error', e)
                    s.close()
                    conn.close()
                    break
            except socket.error as e:
                # Something else happened, handle error, exit, etc.
                log('error', e)
                s.close()
                conn.close()
                break

    def shutdown(self):
        log('warning', 'Shutting down')
        main_thread = threading.currentThread()  # Wait all client to exit
        for t in threading.enumerate():
            if t is main_thread:
                continue
            log('info', 'joining ' + t.getName())
            t.join()
        self.serverSocket.close()
        sys.exit(0)


if __name__ == "__main__":
    server = Server()
    server.listen()
