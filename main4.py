import io
import shutil
import cv2
import socket
import struct
from PIL import Image
import numpy
import os
import imagezmq
import time

# from Config import LOCALE, IMAGE_REC_SOCKET_BUFFER_SIZE, WIFI_IP, IMAGEREC_PORT

import subprocess

class ImageRec:
    def __init__(self):
        self.save_dir = "./images"
        self.image_hub = imagezmq.ImageHub()
        self.i = 0

    # def connect(self):
    #     try: 
    #         self.s.connect((WIFI_IP, IMAGEREC_PORT))
    #     except Exception as error:
    #         print('Image Rec connection failed: ' + str(error))

    # def disconnect(self):
    #     try:
    #         self.s.close()
    #     except Exception as error:
    #         print('Image Rec disconnection failed: ' + str(error))

    #------------RECEIVE PICS FROM RPI------------#
    def recv_pic(self):
        try:
            # show streamed images until Ctrl-C
            self.message, image = self.image_hub.recv_image()
            self.start = time.time()
            print("message: ", self.message)
            cv2.imwrite(os.path.join(self.save_dir, 'frame_{}.jpg'.format(self.i)), image)
        except Exception as error:
            print('Image Rec take_pic failed: ' + str(error))

    #------------PREDICTION------------#
    def predict(self):
        try: 
            self.detect_output = subprocess.check_output("python detect2.py --weights best_leftright.pt --img 640 --conf 0.6 --source ./images/frame_{}.jpg --data ./mdpimages4-merge2-2/data.yaml".format(self.i), shell=True)
            self.detect_dir = self.detect_output.decode('utf-8')
        except Exception as error:
            print('Image Rec predict failed: ' + str(error))

    #------------SEND RESULTS TO RPI------------#
    def send_results(self):
        try:
            self.detect_labels = f"{self.detect_dir.strip()}\labels"
            results = []
            area = []
            for file in os.listdir(self.detect_labels):
                current_path = self.detect_labels + "\\" + file
                current_file = open(current_path, 'r')
                for line in current_file:
                    id = line.split()
                    results.append(id[0])
                    width = float(id[3])
                    height = float(id[4])
                    ar = width * height
                    area.append(ar)
                current_file.close()
            print(results)
            length = len(results)
            max = 0
            # for i in range(length):
            #     count[int(results[i])] = count[int(results[i])] + 1
            #     if max < count[int(results[i])]:
            #         max = count[int(results[i])]
            #         result = results[i]
            for i in range(length):
                if area[i] > max and results[i] != '2':
                    max = area[i]
                    result = results[i]
        
            if max == 0:
                result = ":(" # no symbol

            self.detect_images = f"{self.detect_dir.strip()}"
            for folder, sub_folder, img_files in os.walk(self.detect_images):
                
                for img_file in img_files:

                    if img_file.split('.')[1] == 'jpg':
                        img_pil = Image.open(f"{folder}/{img_file}")

                        if result != ":(":
                            img_pil.save(f"./image_result_success/result_frame_{self.i}.jpg")
                        else:
                            img_pil.save(f"./image_result_fail/result_frame_{self.i}.jpg")

            self.image_hub.send_reply(('I'+result).encode())
            self.i = self.i + 1
            return result
        except Exception as error:
            print('Image Rec send_results failed: ' + str(error))

    #------------DISPLAY PICS FROM RPI------------#
    def display_pics(self):
        try:
            # self.detect_images = f"{self.detect_dir.strip()}"
            for img in os.listdir("./image_result_success"):
                image_path = os.path.join("./image_result_success", img)
                image = Image.open(image_path)
                width = image.width
                height = image.height
            color = (255, 255, 255)
            view = Image.new('RGB', ((4 * width + 30), (2 * height + 10)), color)
            img_no = 0
            for img in os.listdir("./image_result_success"):
                image_path = os.path.join("./image_result_success", img)
                image = Image.open(image_path)
                if img_no == 0:
                    view.paste(image, (0, 0))
                elif img_no == 1:
                    view.paste(image, (image.width+10, 0))
                elif img_no == 2:
                    view.paste(image, (2 * image.width+20, 0))
                elif img_no == 3:
                    view.paste(image, (3 * image.width+30, 0))
                elif img_no == 4:
                    view.paste(image, (0, image.height+10))
                elif img_no == 5:
                    view.paste(image, (image.width+10, image.height+10))
                elif img_no == 6:
                    view.paste(image, (2 * image.width+20, image.height+10))
                elif img_no == 7:
                    view.paste(image, (3 * image.width+30, image.height+10))
                img_no = img_no + 1
            view.save(f"./image_view/image_view.jpg")
            view.show()
        except Exception as error:
                print('Image Rec display_pics failed: ' + str(error))


if __name__ == '__main__':
    A = ImageRec()
    
    while True:
        #start = time.time()
        A.recv_pic()
        print("recv_pic successful")
        A.predict()
        print("predict successful")
        result = A.send_results()
        print("send_results successful")
        end = time.time()
        print("time: ", end - A.start)

        if A.message == "last picture" and (result == "3" or result == "4"):
            break

    A.display_pics()
    print("display_pics successful")
