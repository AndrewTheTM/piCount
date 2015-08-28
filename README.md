# Raspberry Pi Truck Counting System

This is a system to eventually count trucks using a Raspberry Pi and it's camera.
Ideally, this would be placed near a business (with a known number of employees).
Currently, there is a classifier included for cars based on the instructions at
http://abhishek4273.com/2014/03/16/traincascade-and-car-detection-using-opencv/.

# The Plan

I've collected some internet pictures of trucks that I am going to use to train
the classifier for trucks.  I will also set this up to save images and count the
frames to see what the count is and do some comparisons (eventually).

One of the biggest (if not _THE_ biggest) todo items is to make this run even
when someone isn't pulling up the webpage.  That sounds more difficult than it
likely will be.

# Included

The included classifier (cascade.xml) is for cars and trucks.  I generated it
using the instructions on the link above.  

piCount.py is the actual program.  It runs a python service that can be
viewed by going to http://ip_address:9090.  This runs extremely slow as it is,
so I would highly recommend not using it as a streaming server.

Don't use piTruckTrain.py yet.  I haven't been working on it.

# Current Status

Don't use this yet.  Please.  If you want to help, contact Andrew Rohne @okiAndrew or arohne@oki.org
