import cv2
import time
import socket
import threading
import numpy as np
from TCP_common import tcp_common

class tcp_server(tcp_common):
    def __init__(self, ip, port):
        super().__init__(ip, port)
        self.client_init = super().create_sock_client()

    def recieve_camera_image(self, connection):
        try:
            # get recieve length for get each buffer size of an image
            length = super().receiveall(connection, 16)
            
            # If length is 0, server transmit means complete
            if length is None:
                print('Recieve None')
                return False
            elif int(length) == 0:
                print('Recieve End')
                return False
            else:
                start_time = time.time()
                # Base on recv size to get each img 
                stringData = super().receiveall(self.client_init, int(length))
                # creat matrix for data
                data = np.fromstring(stringData, dtype='uint8')
                # decode the image
                decimg=cv2.imdecode(data,1)
                end_time = time.time()
                seconds = end_time - start_time
                fps  = 1 / seconds
                print( "Estimated frames per second : {0}".format(fps))
                cv2.imshow('CLIENT2',decimg)

                if cv2.waitKey(1) &0xFF ==ord('q'):
                    return False

                return True
        except Exception as e:
            print('Recieve camera image fail. Error {}'.format(e))
            cv2.destroyAllWindows()
            return False
        else:
            cv2.destroyAllWindows()
            return False

    def handle_connection(self):
        try:
            # set var to handle client receive status
            complete_transmit = True

            # Connect to server
            while complete_transmit is True:
                complete_transmit = self.recieve_camera_image(self.client_init)

        except Exception as e:
            print('Handdle connection client fail. Error {}'.format(e))
        else:
            self.client_init.shutdown(socket.SHUT_RDWR)
            self.client_init.close()
            print('Client close')


if __name__ == '__main__':
    a = tcp_server(ip, port)
    a.handle_connection()
    # main()

