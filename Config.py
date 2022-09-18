LOCALE = 'UTF-8'

#Android BT connection settings

RFCOMM_CHANNEL = 1
RPI_MAC_ADDR = 'b8:27:eb:4a:00:d7'
UUID = 'b101bb80-3338-4b94-a775-b3844f8f2aa8'
ANDROID_SOCKET_BUFFER_SIZE = 512

# Algorithm Wifi connection settings
# raspberryHotPotato: 192.168.3.1
WIFI_IP = '192.168.19.1'
ALGO_PORT = 8080
ALGORITHM_SOCKET_BUFFER_SIZE = 512

# Arduino USB connection settings
# SERIAL_PORT = '/dev/ttyACM0'
# Symbolic link to always point to the correct port that arudino is connected to
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 115200

# Image Recognition Seeintgs
IMAGEREC_PORT = 8081
IMAGE_REC_SOCKET_BUFFER_SIZE = 512
STOPPING_IMAGE = ''

IMAGE_WIDTH = 1920
IMAGE_HEIGHT = 1080
IMAGE_FORMAT = 'bgr'

BASE_IP = 'tcp://192.168.19.1'
PORT = ':5555'