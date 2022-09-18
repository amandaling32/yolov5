import io
import cv2
import socket
import struct
from PIL import Image
import numpy
import os

from Config import LOCALE, IMAGE_REC_SOCKET_BUFFER_SIZE, WIFI_IP, IMAGEREC_PORT

s = socket.socket()

s.connect((WIFI_IP, IMAGEREC_PORT))

# print(s.recv(1024).decode())
# s.send('image rec client says hi!'.encode())

connection = s.makefile('rb')
try:
    i = 0
    while True:
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        image_stream.seek(0)
        image = Image.open(image_stream).convert('RGB')
        open_cv_image = numpy.array(image)
        open_cv_image = open_cv_image[:, :, ::-1].copy()
        # cv2.imshow('Network Image',open_cv_image)
        # cv2.waitKey(0)
        # print('Image is %dx%d' % image.size)
        # image.verify()
        # print('Image is verified')

        path = './images'
        cv2.imwrite(os.path.join(path, 'frame_{}.jpg'.format(i)), open_cv_image)
        i=i+1
finally:
    connection.close()
    s.close()

