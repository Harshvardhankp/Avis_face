import numpy as np
import cv2
import datetime
from datetime import timedelta
from datetime import time
from datetime import date
import os


def createdir(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except:
            print ("unable to create directory", path)


def main():

    root="./videos"
    date.today()
    print("printig time",time().replace(microsecond=0))
    yr=str(datetime.datetime.now().strftime("%Y"))
    mn=str(datetime.datetime.now().strftime("%m"))
    dy=str(datetime.datetime.now().strftime("%d"))

    FYear=root + "/" + yr
    monpath=FYear + "/" + mn
    dypath=monpath +"/" + dy
    createdir(FYear)
    createdir(monpath)
    createdir(dypath)

    start=datetime.datetime.now().replace(microsecond=0)
    delta=+ timedelta(minutes=1) #- configuration part
    end=start+delta
    filename = dypath + "/"+str(start.strftime("%Y%m%d%H%M%S")) +".mp4"

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc("H","2","6","4")
    out = cv2.VideoWriter(filename,fourcc, 18.0, (320,240))

    cap = cv2.VideoCapture(0)

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret==True:

            frame=cv2.resize(frame,(320,240))
            # write the flipped frame
            if datetime.datetime.now().replace(microsecond=0) >= end:

                #Reset the directory path
                yr=str(date.today().strftime("%Y"))
                mn=str(date.today().now().strftime("%m"))
                dy=str(date.today().now().strftime("%d"))
                FYear=root + "/" + yr
                monpath=FYear + "/" + mn
                dypath=monpath +"/" + dy
                createdir(FYear)
                createdir(monpath)
                createdir(dypath)
                start = datetime.datetime.now()
                end = start + delta
                filename = dypath + "/" + str(start.strftime("%Y%m%d%H%M%S")) + ".mp4"
                print ("creating file")
                print(filename)
                out.write(frame)
                out.release()
                out = cv2.VideoWriter(filename, fourcc, 18.0, (320, 240))


            else:
                out.write(frame)
                x = datetime.datetime.now().time()
                print(x)
            #print(start)

            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()


main()
