# run this program on the Mac to display image streams from multiple RPis
import cv2
import imagezmq
import socket

from Config import LOCALE, IMAGE_REC_SOCKET_BUFFER_SIZE, WIFI_IP, IMAGEREC_PORT

from PIL import Image
from io import BytesIO
import numpy as np
import base64

s = socket.socket()

#port = 12345

s.connect((WIFI_IP, IMAGEREC_PORT))
# while True:
#       print(s.recv(1024).decode())
#       pass
#s.send('client says hi!'.encode())

print(s.recv(1024))
s.send('image rec client says hi!'.encode())

image_hub = imagezmq.ImageHub()
   # show streamed images until Ctrl-C
rpi_name, image = image_hub.recv_image()
cv2.imshow(rpi_name, image) # 1 window for each RPi
cv2.waitKey(1)
image_hub.send_reply(b'OK')

s.close()