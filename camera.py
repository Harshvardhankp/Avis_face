#from time import time
import time
import os
from ginilib.db import dbops


fileDir = os.path.dirname(os.path.realpath(__file__))

counter = 0

class camera(object):
    def __init__(self,name):
        self.name=name.upper()
        dbs = dbops()
        # create a directory for camera
        settingdetails = dbs.get_settingsdetails()
        self.rootpathprimary = settingdetails[0][2]
        self.rootpathsecondary = settingdetails[0][3]
        self.rootpathtertiary = settingdetails[0][4]

    def get_frame(self):
        self.roots=self.rootpathprimary+"/videos/"+self.name+"/live/live"
        try:
            self.frames = [open(self.roots + f + '.jpg', 'rb').read() for f in [ '0','1', '2', '3']]
            time.sleep(0.3)
            print(time.time())
        except:
            print("Unable to open files")
            #self.roots=fileDir+ "/static/live0.png"
            #self.frame=open(self.roots , 'rb').read()
        return self.frames[int(time.time()) % 3]
