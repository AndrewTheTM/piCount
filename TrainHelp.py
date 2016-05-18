#
# Training Zone Helper
#

import Tkinter, tkFileDialog, os
from PIL import Image, ImageTk

init = Tkinter.Tk()
dirname = tkFileDialog.askdirectory(parent=init, initialdir = "C:\\Modelrun\\TruckModel\\RPi\\PiCount\\rampTrain\\pos", title = "Please Select Image Folder")

imageFiles = os.listdir(dirname)
init.destroy()

outFile = "C:\\Modelrun\\TruckModel\\RPi\\PiCount\\rampTrain\\positive.dat"
if os.path.exists:
    if os.path.isfile(outFile):
        os.remove(outFile)
        of = open(outFile,"w")
        of.close()
else:
    os.removedir(outFile)

doneCnt = 0

for imageFile in imageFiles:
    progress = str(doneCnt) + " of " + str(len(imageFiles)) + " completed"
    root = Tkinter.Tk()
    canvas = Tkinter.Canvas(root, width = 640, height = 220)
    canvas.pack()
    photo = ImageTk.PhotoImage(master=canvas, image=Image.open(dirname + "/" + imageFile))
    canvas.create_image(0,0,anchor="nw", image=photo)

    global x1, y1
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    rect = canvas.create_rectangle(0,0,0,0,outline="green",width=2)

    def cbDown(event):
        x1 = event.x
        y1 = event.y
        canvas.coords(rect,x1,y1,x1,y1)
        #rect = canvas.create_rectangle(x1,y1,1,1,outline="green",width=2)

    def cbUp(event):
        x2 = event.x
        y2 = event.y
        #print canvas.coords(rect)[0]
        #print event.x, event.y

    def cbMotion(event):
        x1 = canvas.coords(rect)[0]
        y1 = canvas.coords(rect)[1]
        x2 = event.x
        y2 = event.y
        canvas.coords(rect,x1,y1,x2,y2)
        #FIXME: Can't drag from low to high

    def cbButton(imageFile,outFile):
        x1 = canvas.coords(rect)[0]
        y1 = canvas.coords(rect)[1]
        x2 = canvas.coords(rect)[2]
        y2 = canvas.coords(rect)[3]
        if x1 == 0 and y1 == 0 and x2 == 0 and y2 == 0:
            print "No rectangle"
        else:
            print "pos/" + imageFile + " 1 " + str(int(x1)) + " " + str(int(y1)) +" " + str(int(x2)) + " " + str(int(y2))
            of = open(outFile,"a")
            of.write("pos/" + imageFile + " 1 " + str(int(x1)) + " " + str(int(y1)) +" " + str(int(x2)) + " " + str(int(y2)) + "\n")
            of.close()
            root.destroy()

    def cbButtMove(dirname,imageFile):
        print dirname
        newdirname = dirname[:dirname.find("pos")] + "Trash"
        os.rename(dirname+"/"+imageFile,newdirname+"/"+imageFile)
        print newdirname

        root.destroy()

    button = Tkinter.Button(root, text="Write and Continue", anchor="se", justify="left", command=lambda: cbButton(imageFile,outFile))
    button.configure(width=15,height=1)
    button_window = canvas.create_window(520, 185, anchor="nw", window=button)

    butMove = Tkinter.Button(root,text="Remove",anchor="nw",justify="left", command=lambda: cbButtMove(dirname,imageFile))
    butMove_window = canvas.create_window(300,185,anchor="nw",window=butMove)

    progLabel = Tkinter.Label(root,text=progress)
    progLabel.configure(anchor="nw")
    label_window = canvas.create_window(10,185,anchor="nw", window=progLabel)

    doneCnt += 1

    canvas.bind("<Button-1>", cbDown)
    canvas.bind("<ButtonRelease-1>",cbUp)
    canvas.bind("<B1-Motion>",cbMotion)

    root.mainloop()

# 1. select folder
# 2. show image
# 3. select area of interest
# 4. output text file of fname # x1 y1 x2 y2
