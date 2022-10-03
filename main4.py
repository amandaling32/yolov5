import io
import cv2
import socket
import struct
from PIL import Image
import numpy
import os
import imagezmq

from Config import LOCALE, IMAGE_REC_SOCKET_BUFFER_SIZE, WIFI_IP, IMAGEREC_PORT

import subprocess

class ImageRec:
    def __init__(self, host =WIFI_IP, port=IMAGEREC_PORT):
        self.save_dir = "./images"
        self.image_hub = imagezmq.ImageHub()

    def connect(self):
        try: 
            self.s.connect((WIFI_IP, IMAGEREC_PORT))
        except Exception as error:
            print('Image Rec connection failed: ' + str(error))

    def disconnect(self):
        try:
            self.s.close()
        except Exception as error:
            print('Image Rec disconnection failed: ' + str(error))

    #------------RECEIVE PICS FROM RPI------------#
    def recv_pic(self):
        try:
            # show streamed images until Ctrl-C
            print("enter while loop")
            rpi_name, image = self.image_hub.recv_image()
            cv2.imshow(rpi_name, image) # 1 window for each RPi
            # cv2.waitKey()
            cv2.imwrite(os.path.join(self.save_dir, 'frame_0.jpg'), image)
            # self.image_hub.send_reply(b'OK')
        except Exception as error:
            print('Image Rec take_pic failed: ' + str(error))
        # finally:
        #     self.connection.close()

    #------------PREDICTION------------#
    def predict(self):
        try: 
            self.detect_output = subprocess.check_output("python detect.py --weights best_merged2.pt --img 640 --conf 0.6 --source ./images --data ./mdpimages-1/data.yaml", shell=True)
            self.detect_dir = self.detect_output.decode('utf-8')
        except Exception as error:
            print('Image Rec predict failed: ' + str(error))

    #------------SEND RESULTS TO RPI------------#
    def send_results(self):
        try:
            # self.detect_label = ".\\" + os.path.dirname(self.detect_dir)+'\labels'
            self.detect_label = ".\\runs\\detect\\exp25\\labels"
            print(type(self.detect_dir))
            print("FK"+self.detect_dir.strip())
            # fuck = "\\" + self.detect_dir
            path = f"{self.detect_dir.strip()}\labels"
            # print("path: "+path)
            # print("FK PATH:"+ fuck + '\\labels')
            results = []
            for file in os.listdir(path):
                print("FUCK"+file)
                current_path = path + "\\" + file
                print(current_path)
                current_file = open(current_path, 'r')
                print(current_file)
                for line in current_file:
                    id = line.split()
                    results.append(id[0])
                    print(line)
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
                result = str(0) # no symbol
            if result == '29':
                result = '25'   # up arrow
            if result == '26':
                result = '26'  # down arrow
            if result == '28':
                result = '27'  # right arrow
            if result == '27':
                result = '28'  # left arrow
            if result == '30':
                result = '29'  # yellow circle
            if result == '25':
                result = '30'  # bullseye
            print('I' + result)
            # self.s.send(('I'+result).encode())
            self.image_hub.send_reply(('I'+result).encode())
        except Exception as error:
            print('Image Rec send_results failed: ' + str(error))

    #------------DISPLAY PICS FROM RPI------------#
    def display_pics(self):
        try:
            src_images = "./images"
            for img in os.listdir(src_images):
                width = image_path = os.path.join(src_images, img)
                image = Image.open(image_path)
                width = image.width
                height = image.height
            color = (255, 255, 255)
            view = Image.new('RGB', ((3 * width + 20), (2 * height + 10)), color)
            i = 0
            for img in os.listdir(src_images):
                image_path = os.path.join(src_images, img)
                image = Image.open(image_path)
                if i == 0:
                    view.paste(image, (0, 0))
                elif i == 1:
                    view.paste(image, (image.width+10, 0))
                elif i == 2:
                    view.paste(image, (2 * image.width+20, 0))
                elif i == 3:
                    view.paste(image, (0, image.height+10))
                elif i == 4:
                    view.paste(image, (image.width+10, image.height+10))
                elif i == 5:
                    view.paste(image, (2 * image.width+20, image.height+10))
                i = i+1
            view.save(f"./image_view/{img}")
            view.show()
        except Exception as error:
                print('Image Rec send_results failed: ' + str(error))


if __name__ == '__main__':
    A = ImageRec()
    for i in range(5):
        A.recv_pic()
        print("recv_pic successful")
        A.predict()
        print("predict successful")
        A.send_results()
        print("send_results successful")
        # A.display_pics()
        # print("display_pics successful")
