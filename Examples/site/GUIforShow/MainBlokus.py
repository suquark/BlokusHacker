#data0.txt   Player2Data.txt

import _thread
from time import sleep

def importCore():
    import CoreBlokus
def importGUI():
    import GUIBlokus


f=open("Player2Data.txt",'w')
f.close()
f=open("data0.txt",'w')
f.close()


_thread.start_new_thread(importCore,())
_thread.start_new_thread(importGUI,())
sleep(1000)
