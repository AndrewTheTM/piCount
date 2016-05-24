# Raspberry Pi Counting System
# @author Andrew Rohne, OKI Regional Council, @okiAndrew, 8/25/2015

# Large parts taken from https://github.com/berak/opencv_smallfry/blob/master/mjpg_serve.py
from __future__ import print_function
import sys, numpy as np, cv2, os, io, time, traceback
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from piVideoStream import PiVideoStream

min_area = 200

class CamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # params for ShiTomasi corner detection
        # feature_params = dict( maxCorners = 100,
        #     qualityLevel = 0.3,
        #     minDistance = 7,
        #     blockSize = 7 )

        # Parameters for lucas kanade optical flow
        # lk_params = dict( winSize  = (15,15),
        #     maxLevel = 2,
        #     criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

        if self.path.endswith('.mjpg'):
            self.send_response(200)
            self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()
            cap = 0
            while cap < 40:
                old_frame = piVidStream.read()
                cap = cap + 1

            #TODO: This needs to be a parameter!
            omask = np.zeros(old_frame.shape[:2],np.uint8)
            inputmask = cv2.imread('Mask.jpg', cv2.IMREAD_GRAYSCALE)
            inputmask = inputmask[0, 0, old_frame.size.width, old_frame.size.height]
            omask[inputmask == 0] = 0
            omask[inputmask == 255] = 1

            old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

            fgbg = cv2.createBackgroundSubtractorMOG2(history = 120, varThreshold = 16, detectShadows=False)

            while True:
                try:
                    # Get frame
                    img = piVidStream.read()
                    img = cv2.bitwise_and(img, img, mask = omask)
                    frame_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                    mask = fgbg.apply(frame_gray)
                    kernelsm = np.ones((2,2),np.float32)/4
                    kernellg = np.ones((6,4),np.float32)/24
                    mask = cv2.dilate(mask, kernelsm, iterations = 2)

                    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernellg)
                    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernellg)

                    # Setup SimpleBlobDetector parameters.
                    params = cv2.SimpleBlobDetector_Params()

                    # Change thresholds
                    params.minThreshold = 1; #50
                    params.maxThreshold = 220;

                    # Filter by Area.
                    params.filterByArea = True
                    params.minArea = 150
                    params.maxArea = 15000

                    # No circles
                    params.filterByCircularity = False
                    params.filterByInertia = False
                    params.filterByConvexity = False

                    detector = cv2.SimpleBlobDetector_create(params)
                    keypoints = detector.detect(cv2.bitwise_and(img, img, mask = mask))
                    #keypoints = detector.detect(cv2.bitwise_not(mask))

                    img2 = cv2.drawKeypoints(img, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)



                    #img2 = cv2.bitwise_and(img, img, mask = mask)
                    #img2 = img

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
    global piVidStream
    piVidStream = PiVideoStream().start()
    time.sleep(2.0)
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
