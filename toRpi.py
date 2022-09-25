import os
import socket

from Config import LOCALE, IMAGE_REC_SOCKET_BUFFER_SIZE, WIFI_IP, IMAGEREC_PORT

# s = socket.socket()

# s.connect((WIFI_IP, IMAGEREC_PORT))

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

print('l'+result)

# s.send('l'+result.encode())
# s.close()