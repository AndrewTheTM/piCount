# Train an image classifier for trucks!
# @author Andrew Rohne, OKI Regional Council, @okiAndrew, 8/25/2015
#
# DO NOT RUN THIS ON A RASPBERRY PI!  IT WILL VIOLENTLY EXPLODE!
# I'M KIDDING BUT IT WON'T RUN BECAUSE TOO MUCH MEMORY IS NEEDED!
# USE A BAD-ASS COMPUTER FOR THIS!

import os
from PIL import Image as image

nFiles = os.listdir("C:\\Modelrun\\TruckModel\\RPi\\PiCount\\truckTrain\\negative")

# Negative files should be just a list at a relative path

outFile = open("C:\\Modelrun\\TruckModel\\RPi\\PiCount\\truckTrain\\negative.dat","w")
for file in nFiles:
    outFile.write("negative\\" + file + "\n")
outFile.close()

# Positive files should be a list of file, 1, detect coords (4, space delim)
pFiles = os.listdir("C:\\Modelrun\\TruckModel\\RPi\\PiCount\\truckTrain\\positive")
outFile = open("C:\\Modelrun\\TruckModel\\RPi\\PiCount\\truckTrain\\positive.dat","w")
for file in pFiles:
    imgFile = image.open(os.path.join("C:\\Modelrun\\TruckModel\\RPi\\PiCount\\truckTrain\\positive\\",file))
    outFile.write("positive\\" + file + " 1 0 0 " + str(imgFile.size[0]) + " " + str(imgFile.size[1]) + "\n")
outFile.close()

#
#outFile = open("C:\\Modelrun\\TruckModel\\RPi\\PiCount\\truckTrain\\train.bat","w")
#for file in pFiles:
#    bg = nFiles[randrange(0,len(nFiles),)]
#    outFile.write("opencv_createsamples -img " + file + " -bg " + bg " -info ")

#outFile.close()


#opencv_createsamples -img /home/user/logo.png -bg /home/user/bg.txt -info /home/user/annotations.lst -pngoutput -maxxangle 0.1 -maxyangle 0.1 -maxzangle 0.1
