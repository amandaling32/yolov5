import io
import cv2
import socket
import struct
from PIL import Image
import numpy
import os

from Config import LOCALE, IMAGE_REC_SOCKET_BUFFER_SIZE, WIFI_IP, IMAGEREC_PORT

import detect

s = socket.socket()

s.connect((WIFI_IP, IMAGEREC_PORT))

connection = s.makefile('rb')

try:

    #------------RECEIVE PICS FROM RPI------------#

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

    #------------PREDICTION------------#
    
    # os.system("python detect.py --weights ./best_100epoch.pt --img 640 --conf 0.25 --source ./images --data ./mdpimages-1/data.yaml")

    

    #------------SEND RESULTS TO RPI------------#

    # Folder to copy from
    directory = './runs/detect/exp37/labels'

    # This starts the 'walk' through the directory
    for folder , sub_folders , files in os.walk(directory):

        results = []

        # For each file...
        for f in files:
            # create the current path using the folder variable plus the file variable
            current_path = folder+"\\"+f

            # Open the file to read the contents
            current_file = open(current_path, 'r')

            # read each line one at a time and then write them to your file
            for line in current_file:
                results.append(line[:2])

            # close the file
            current_file.close()

            count = [0] * 32

            len = len(results)
            max = 0

            for i in range(len):
                count[int(results[i])] = count[int(results[i])] + 1
                if max < count[int(results[i])]:
                    max = count[int(results[i])]
                    result = results[i]
            
            if max == 0:
                result = -1

            #print('l'+result)

            s.send(('l'+result).encode())


# finally:
#     connection.close()
#     s.close()

except Exception as error:
            print('Image Rec process failed: ' + str(error))

