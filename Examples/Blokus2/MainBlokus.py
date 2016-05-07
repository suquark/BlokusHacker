#data0.txt   Player2Data.txt

import _thread
from time import sleep

#
# def importCore():
#     import CoreBlokus
# def importGUI():
#     import GUIBlokus
def invitePlayer1():
    try:
        import Player1.py
    except:
        print("Player1 can't put any Chess ---Message from GUI.")
def invitePlayer2():
    try:
        import Player2.py
    except:
        print("Player2 can't put any Chess ---Message from GUI.")
def inviteGUI():
    import GUIBlokus.py



f=open("Player2Data.txt",'w')
f.write('-1 -1\n0\n0')
f.close()
f=open("Player1Data.txt",'w')
f.close()
f=open("GUI1Data.txt",'w')
f.close()
f=open("GUI2Data.txt",'w')
f.close()


_thread.start_new_thread(invitePlayer1,())
_thread.start_new_thread(invitePlayer2,())
_thread.start_new_thread(inviteGUI,())
sleep(1000)
