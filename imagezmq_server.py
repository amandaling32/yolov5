# run this program on the Mac to display image streams from multiple RPis
import cv2
import imagezmq
import os

save_dir = "./images"
image_hub = imagezmq.ImageHub()

for i in range(15):  # show streamed images until Ctrl-C
    print("enter while loop")
    rpi_name, image = image_hub.recv_image()
    cv2.imshow(rpi_name, image) # 1 window for each RPi
    # cv2.waitKey()
    cv2.imwrite(os.path.join(save_dir, 'frame_{}.jpg'.format(i+245)), image)
    image_hub.send_reply(b'OK')