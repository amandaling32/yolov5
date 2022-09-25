import io
import cv2
import socket
import struct
from PIL import Image
import numpy
import os

from Config import LOCALE, IMAGE_REC_SOCKET_BUFFER_SIZE, WIFI_IP, IMAGEREC_PORT

import subprocess

class ImageRec:
    def __init__(self, host =WIFI_IP, port=IMAGEREC_PORT):

        # print("initialise")

        self.s = socket.socket()

        self.s.connect((WIFI_IP, IMAGEREC_PORT))

        self.connection = self.s.makefile('rb')

        print("Connection successful - PC")

    def connect(self):
        try: 
            self.s.connect((WIFI_IP, IMAGEREC_PORT))
        except:
            print('Image Rec connection failed: ' + str(error))

    def disconnect(self):
        try:
            self.s.close()
        except:
            print('Image Rec disconnection failed: ' + str(error))

    #------------RECEIVE PICS FROM RPI------------#
    def take_pic(self):
        try:
            
            i = 0
            while True:
                # Read the length of the image as a 32-bit unsigned int. If the
                # length is zero, quit the loop
                image_len = struct.unpack('<L', self.connection.read(struct.calcsize('<L')))[0]
                if not image_len:
                    break
                # Construct a stream to hold the image data and read the image
                # data from the connection
                image_stream = io.BytesIO()
                image_stream.write(self.connection.read(image_len))
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

        except Exception as error:
            print('Image Rec take_pic failed: ' + str(error))
        
        # finally:
        #     self.connection.close()
           

    #------------PREDICTION------------#
    
    # os.system("python detect.py --weights ./best_100epoch.pt --img 640 --conf 0.25 --source ./images --data ./mdpimages-1/data.yaml")

    # def predict(self):
    #     try: 
    #         print(detect.main())
    #     except Exception as error:
    #         print('Image Rec predict failed: ' + str(error))

    def predict(self):
        try: 
            detect_output = subprocess.check_output("python detect.py --weights best_171epoch.pt --img 640 --conf 0.25 --source ./images --data ./mdpimages-1/data.yaml", shell=True)
            self.detect_labels = detect_output.decode('utf-8')
        except Exception as error:
            print('Image Rec predict failed: ' + str(error))

    #------------SEND RESULTS TO RPI------------#

    def send_results(self):
        try:

            self.detect_dir = os.path.dirname(self.detect_labels)+'\labels'
            print(self.detect_dir)

            results = []
            # This starts the 'walk' through the directory
            for folder, sub_folder, files in os.walk(str(self.detect_dir)):
                
                for f in files:
                    
                    # create the current path using the folder variable plus the file variable
                    current_path = folder + "\\" + f

                    # Open the file to read the contents
                    current_file = open(current_path, 'r')
                    
                    # read each line one at a time and then write them to your file
                    for line in current_file:
                        
                        results.append(line[:2])

                    # close the file
                    current_file.close()
            
            print(results)

            count = [0] * 31

            length = len(results)
            max = 0

            for i in range(length):
                count[int(results[i])] = count[int(results[i])] + 1
                if max < count[int(results[i])]:
                    max = count[int(results[i])]
                    result = results[i]

            if max == 0:
                result = str(-1)

            if count[25] > 0:
                result = str(25)

            print('I' + result)

            self.s.send(('I'+result).encode())

        except Exception as error:
            print('Image Rec send_results failed: ' + str(error))

        

if __name__ == '__main__':
    A = ImageRec()
    # A.connect()
    # print("connection successful")
    # A.take_pic()
    # print("take_pic successful")
    # # A.disconnect()
    # # print("disconnection successful")
    # A.predict()
    # print("predict successful")
    # # A.connect()
    # # print("connection successful")
    # A.send_results()
    # print("send_results successful")
    # A.disconnect()
    # print("disconnection successful")

    
    A.take_pic()
    print("take_pic successful")
    A.predict()
    print("predict successful")
    A.send_results()
    print("send_results successful")
