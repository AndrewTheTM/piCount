# Raspberry Pi Counting System
# @author Andrew Rohne, OKI Regional Council, @okiAndrew, 8/25/2015

# Large parts taken from https://github.com/berak/opencv_smallfry/blob/master/mjpg_serve.py
from __future__ import print_function
import sys, numpy, cv2, os, io, time
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

# from imutils.video.pivideostream import PiVideoStream
# from imutils.video import FPS

global RPI
RPI = True

min_area = 200

if RPI:
    from piVideoStream import PiVideoStream


class CamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if RPI:
            piVidStream = PiVideoStream().start()
            time.sleep(2.0)

        # params for ShiTomasi corner detection
        feature_params = dict( maxCorners = 100,
            qualityLevel = 0.3,
            minDistance = 7,
            blockSize = 7 )

        # Parameters for lucas kanade optical flow
        lk_params = dict( winSize  = (15,15),
            maxLevel = 2,
            criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

        if self.path.endswith('.mjpg'):

            self.send_response(200)
            self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()
            cap = 0
            while cap < 40:
                if RPI:
                    old_frame = piVidStream.read()
                    cap = cap + 1
                else:
                    ret, old_frame = camera.read()
                    cap = cap + 1
                    if not ret:
                        cap = 0

            old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

            while True:
                try:
                    # Get frame
                    if RPI:
                        img = piVidStream.read()
                    else:
                        cap, img = camera.read()
                    frame_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    # get absolute diff between current and first frame
                    frameDelta = cv2.absdiff(old_gray, frame_gray)
                    thres = cv2.threshold(frameDelta, 50, 255, cv2.THRESH_BINARY)[1]

                    #Dilate the thresholded image to fill in holes and then find contours on thresholded image
                    # H/T: http://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/
                    thres = cv2.dilate(thres, None, iterations = 2)
                    (_, cnts, _) = cv2.findContours(thres.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    for c in cnts:
                        # if the contour is too small, ignore it
                        if cv2.contourArea(c) < min_area:
                            continue

                        # compute the bounding box for the contour, draw it on the frame,
                        # and update the text
                        (x, y, w, h) = cv2.boundingRect(c)
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        text = "Occupied"

                    #img2 = cv2.bitwise_and(img, mask)
                    #img2 = cv2.add(img, mask)
                    img2 = img
                    r, buf = cv2.imencode(".jpg",img2)
                    self.wfile.write("--jpgboundary\r\n")
                    self.send_header('Content-type','image/jpeg')
                    self.send_header('Content-length',str(len(buf)))
                    self.end_headers()
                    self.wfile.write(bytearray(buf))
                    self.wfile.write('\r\n')

                    #FIXME: broken pipe when closing page
                except KeyboardInterrupt:
                    break
            return
        if self.path.endswith('.html') or self.path=="/":
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write('<html><head></head><body>')
            self.wfile.write('<img src="/cam.mjpg"/>')
            self.wfile.write('</body></html>')
            return

def main():
    global camera
    if RPI:
        # camera = picamera.PiCamera()
        # camera.resolution = (640,480)
        # camera.hflip = True
        # camera.vflip = True
        print("RPI Mode")
    else:
        camera = cv2.VideoCapture(0)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640);
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480);
    try:
        server = HTTPServer(('',9090),CamHandler)
        print("server started")
        server.serve_forever()
    except KeyboardInterrupt:
		#capture.release()
        #camera.release()
        server.socket.close()

if __name__ == '__main__':
	main()
