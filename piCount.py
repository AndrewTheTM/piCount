# Raspberry Pi Counting System
# @author Andrew Rohne, OKI Regional Council, @okiAndrew, 8/25/2015

import numpy, cv2, matplotlib, sys, os, picamera, io
#cascPath = "C:\\Modelrun\\TruckModel\\RPi\\PiCount\\faceCascades\\haarcascade_frontalface_default.xml"

runPath = os.path.join(os.path.dirname(sys.argv[0]))

cascPath = runPath + "\\cascade.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

stream = io.BytesIO()
with picamera.PiCamera() as camera:
    camera.capture(stream, format='jpeg')

data = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)


#cv2.namedWindow("Preview")
#capture = cv2.VideoCapture(0)
capture = cv2.imdecode(data,1)
if capture.isOpened():
    rval, frame = capture.read()
else:
    rval = False

while rval:
    fr2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        fr2,
        scaleFactor = 1.3,
        minNeighbors = 5,
        minSize = (30,30),
        flags = cv2.CASCADE_SCALE_IMAGE
    )
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow("Preview",frame)
    rval, frame = capture.read()
    key = cv2.waitKey(20)
    if key == 27:
        break

capture.release()
cv2.destroyWindow("Preview")
