# Train an image classifier for trucks!
# @author Andrew Rohne, OKI Regional Council, @okiAndrew, 8/25/2015

import os

nFiles = os.listdir("C:\\Modelrun\\TruckModel\\RPi\\PiCount\\truckTrain\\negative")

outFile = open("C:\\Modelrun\\TruckModel\\RPi\\PiCount\\truckTrain\\negative.dat","w")
for file in nFiles:
    outFile.write("negative\\" + file + "\n")
outFile.close()

pFiles = os.listdir("C:\\Modelrun\\TruckModel\\RPi\\PiCount\\truckTrain\\positive")
outFile = open("C:\\Modelrun\\TruckModel\\RPi\\PiCount\\truckTrain\\positive.dat","w")
for file in pFiles:
    outFile.write("positive\\" + file + "\n")
outFile.close()

#
#outFile = open("C:\\Modelrun\\TruckModel\\RPi\\PiCount\\truckTrain\\train.bat","w")
#for file in pFiles:
#    bg = nFiles[randrange(0,len(nFiles),)]
#    outFile.write("opencv_createsamples -img " + file + " -bg " + bg " -info ")

#outFile.close()


#opencv_createsamples -img /home/user/logo.png -bg /home/user/bg.txt -info /home/user/annotations.lst -pngoutput -maxxangle 0.1 -maxyangle 0.1 -maxzangle 0.1
