import socket
import sys

class tcp_common():
    def __init__(self, rm_ip, rm_port):
        self.ip = rm_ip
        self.port = rm_port

    # count buffer due to socket recv size, break 16 to count size
    def receiveall(self, sock, count):
        # set buffer
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    def create_sock_server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind((self.ip, self.port))
        except Exception as e:
            print('Bind failed. Error {}'.format(e))
            sys.exit()
        else:
            print('Socket create')
            return s
        finally:
            pass

    def create_sock_client(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((self.ip, self.port))
        except Exception as e:
            print('Connect Server failed. Error {}'.format(e))
            sys.exit()
        else:
            print('Connect to server')
            return s
        finally:
            pass



if __name__ == '__main__':
    pass
    # a = tcp_common(socket.gethostname(), 12346)
    # s = a.create_sock_server()
    # s.listen(5)
