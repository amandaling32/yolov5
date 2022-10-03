import os

# Folder to copy from
directory = './runs/detect/exp15/labels'

# Open a new file to write to
output_file = open('output.txt','w+')

# This starts the 'walk' through the directory
for folder , sub_folders , files in os.walk(directory):

    # For each file...
    for f in files:
        # create the current path using the folder variable plus the file variable
        current_path = folder+"\\"+f

        # Open the file to read the contents
        current_file = open(current_path, 'r')

        # read each line one at a time and then write them to your file
        for line in current_file:
            output_file.write(line[:2])
            output_file.write("\n")

        # close the file
        current_file.close()

#close your output file
output_file.close()