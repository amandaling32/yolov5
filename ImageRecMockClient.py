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

# print(s.recv(1024).decode())
# print(s.recv(1024).decode())

image_data = s.recv(1024)
print(type(image_data))
# img_arr = np.fromstring(image_data, dtype="int", sep=",")
# print(img_arr)
# img = Image.fromarray(img_arr)

# image_data = s.recv(1048576)
# image = Image.frombytes('RGB', (640,480), image_data)
# image.show()
# image.save(f"./images/image.jpg")

# stream = BytesIO(s.recv(1024))

# image = Image.open(stream).convert("RGBA")
# stream.close()
# image.show()

# image = BytesIO(image_data)
# image = Image.frombytes('L', (416,416), image)
# image.show()

# sep = '|'.encode('utf-8')
# i_0 = image_data.find(sep)
# i_1 = image_data.find(sep, i_0 + 1)
# arr_dtype = image_data[:i_0].decode('utf-8')
# arr_shape = tuple([int(a) for a in image_data[i_0 + 1:i_1].decode('utf-8').split(',')])
# arr_str = image_data[i_1 + 1:]
# arr = np.frombuffer(arr_str, dtype = arr_dtype).reshape(arr_shape)
# print(type(arr))

# array = np.frombuffer(base64.binascii.a2b_base64(image_data.encode("ascii"))) 
# array = array.reshape(640,480)

# if np.array_equal(random_array, array) and random_array.shape == array.shape and random_array.dtype == array.dtype:
#     print("true")
# else:
#    print("false")

s.close()