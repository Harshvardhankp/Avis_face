import numpy as np
import cv2
import datetime
from datetime import timedelta
from datetime import time
from datetime import date
import os


start=datetime.datetime.now().replace(microsecond=0)
delta=+ timedelta(days=5,hours=10) #- configuration part
end=start+delta

print(start)
print(end)
dele=end-start
print(dele)

yr=str(datetime.datetime.now().strftime("%Y"))
mn=str(datetime.datetime.now().strftime("%m"))
dy=str(datetime.datetime.now().strftime("%d"))

root="/media/harsh/D42CD6E22CD6BF24"

statvfs = os.statvfs(root)

print("File system size",(statvfs.f_frsize * statvfs.f_blocks)/(1024*1024*1024))     # Size of filesystem in bytes
print("Free Bytes",(statvfs.f_frsize * statvfs.f_bfree)/(1024*1024*1024) )     # Actual number of free bytes
print("Available to user",(statvfs.f_frsize * statvfs.f_bavail)/(1024*1024*1024) )


FYear=root + "/" + yr
monpath=FYear + "/" + mn
dypath=monpath +"/" + dy

if not os.path.exists(root):
    try:
        os.makedirs(root)
    except:
        print (root,"unable to create directory")


if not os.path.exists(FYear):
    try:
        os.makedirs(FYear)
    except:
        print (FYear,"unable to create directory")


if not os.path.exists(monpath):
    try:
        os.makedirs(monpath)
    except:
        print (monpath,"unable to create directory")


if not os.path.exists(dypath):
    try:
        os.makedirs(dypath)
    except:
        print (dypath,"unable to create directory")



print(FYear)
print(monpath)
print(dypath)
