import cv2
import socket
import threading
import numpy as np
from image_model import imgmain
from TCP_common import tcp_common

class tcp_server(tcp_common):
    """
    Use to create TCP server in vehicle side use it to pass data

    Fuctions

    handle_connection() : Use it to create a listening TCP server
    send_camera_image(socket_connection) : Use it to send image, this fuction will be auto include when you call handle_connection() 
    """
    def __init__(self, ip, port):
        super().__init__(ip, port)
        self.server_init = super().create_sock_server()

    def send_camera_image(self, connection):
        """
        Need to give it a socket connection, this function default to capture 3 cameras images from left, center to right.
        """
        try:
            # Get for camera image
            cap_left = cv2.VideoCapture('solidWhiteRight.mp4')
            cap_center = cv2.VideoCapture('solidWhiteRight.mp4')
            cap_right = cv2.VideoCapture('solidWhiteRight.mp4')

            # Check if camera opened successfully  
            if (cap_left.isOpened() == False and cap_center.isOpened() == False and cap_right.isOpened() == False):
                print("Error opening video stream or file")
            else:
                print('Success open 3 camera')

            # Read until video is completed  
            while(cap_left.isOpened() and cap_center.isOpened() and cap_right.isOpened()):
                # Capture frame-by-frame
                ret_left, frame_left = cap_left.read()
                ret_center, frame_center = cap_center.read()
                ret_right, frame_right = cap_right.read()
                
                if (ret_left == True and ret_center == True and ret_right == True):
                    # Set img encoding parameter 
                    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
                    # Combine 3 img into 1
                    frame_combine = imgmain(frame_left, frame_center, frame_right)
                    # Img encode for socket transmit
                    result, imgencode = cv2.imencode('.jpg', frame_combine, encode_param)
                    data = np.array(imgencode)
                    
                    str_data = data.tostring()
                    # send size information and encode image to client
                    connection.send(str(len(str_data)).ljust(16).encode())
                    connection.send(str_data)
                else:
                    connection.send(str(0).ljust(16).encode())

        except Exception as e:
            print('Send camera image fail. Error {}'.format(e))
        else:
            # When everything done, release the video capture object
            cap_left.release()
            cap_center.release()
            cap_right.release()
            connection.close()

    def handle_connection(self):
        """
        Use to create a TCP server which can handle the client connection
        """
        try:
            # Server listen
            self.server_init.listen(5)

            # Waiting connection
            while True:
                # socket server on
                conn, addr = self.server_init.accept()

                if conn:
                    threading.Thread(target=self.send_camera_image, args=(conn,)).start()

        except Exception as e:
            print('Handdle connection fail server. Error {}'.format(e))


if __name__ == '__main__':
    a = tcp_server(ip, port)
    a.handle_connection()
    
    # main()

