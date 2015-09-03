#
# Training Zone Helper
#

import Tkinter, tkFileDialog, os
from PIL import Image, ImageTk

root = Tkinter.Tk()
canvas = Tkinter.Canvas(root)
canvas.grid(row = 1, column = 1)
dirname = tkFileDialog.askdirectory(parent=root, initialdir = "C:\\Modelrun\\TruckModel\\RPi\\PiCount\\rampTrain\\pos", title = "Please Select Image Folder")

print dirname

imageFiles = os.listdir(dirname)

#for imageFile in imageFiles:
imageFile = imageFiles[0]
photo = ImageTk.PhotoImage(Image.open(dirname + "/" + imageFile))
panel = Tkinter.Label(image = photo)
panel.pack(side="bottom",fill="both", expand="yes")
#TODO: Add X & Y coords, eventually bounding box
root.mainloop()
#canvas.create_image(0,0,image=photo)


# 1. select folder
# 2. show image
# 3. select area of interest
# 4. output text file of fname # x1 y1 x2 y2
