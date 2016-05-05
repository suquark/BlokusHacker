__author__ = 'Togo-PC'

from tkinter import *
import string
import _thread
from time import sleep


DIM=14
btn=[[Button for x in range(DIM)]for y in range(DIM)]
#colors=['WHITE','RED','YELLOW','BLUE','PURPLE']
colors=['WHITE','ORANGE','PURPLE','RED','BLUE']

def frame(root,side):
    w=Frame(root)
    w.pack(side=side,expand=YES,fill=BOTH)  #可拉伸，横纵向填充
    return w

def nextColor(color):
    global colors
    num=len(colors)
    for i in range(num):
        if colors[i]==color:
            return colors[(i+1)%num]  #############################
    #return 'BLUE'


def button(root,side,text,command=None,bg='WHITE'):
    w=Button(root,text=text,command=lambda:w.config(bg=nextColor(w['bg'])   ),bg=bg)
    w.pack(side=side,expand=YES,fill=BOTH)
    return w

def allToWhite():
    for x in range(DIM):
        for y in range(DIM):
            btn[x][y].config(bg='WHITE')

def ReadFile(num=0):
    result=[]
    with open("data"+str(num)+".txt",'r') as f:
        for line in f:
            result.append(list(map(int,line.split(' '))))
    for xy in result:
        x,y=xy[0],xy[1]
        btn[x][y].config(bg=colors[num])
    f.close()
    #print(result)
'''
def BtnCmd():
    i=0
    while (1):
        i=i+1
        if (i==1000000):
            ReadFile(1)
            ReadFile(2)
            i=0
'''

def CCFO(x,y,num):
    btn[x][y].config(bg=colors[num])

class ChessBoard(Frame):
    def __init__(self,DIM):
        Frame.__init__(self)  #############################important
        self.pack(expand=YES,fill=BOTH)
        self.master.title("Blokus Board")
        self.master.geometry('600x600')

        global btn

        for x in range(DIM):
            line=frame(self,TOP)
            for y in range(DIM):
                btn[x][y]=button(line,LEFT,'')

        line=frame(self,TOP)
        displayX=IntVar()
        entryX=Entry(line,relief=SUNKEN)
        entryX.pack(side=LEFT,expand=YES,fill=BOTH)
        displayY=IntVar()
        entryY=Entry(line,relief=SUNKEN)
        entryY.pack(side=LEFT,expand=YES,fill=BOTH)     
        btncc=Button(line,text="C C",command=lambda : btn[int(entryX.get())][int(entryY.get())].config(bg=nextColor(btn[int(entryX.get())][int(entryY.get())]['bg'])) )
        btncc.pack(side=LEFT,expand=YES,fill=BOTH)
        btnClear=Button(line,text="Clear",command=allToWhite)
        btnClear.pack(side=LEFT,expand=YES,fill=BOTH)

        btnFile1=Button(line,text="Read",command=lambda x=1:ReadFile(x))
        #btnFile1=Button(line,text="Read",command=BtnCmd)
        btnFile1.pack(side=LEFT,expand=YES,fill=BOTH)
        btnFile2=Button(line,text="Read",command=lambda x=2:ReadFile(x))
        btnFile2.pack(side=LEFT,expand=YES,fill=BOTH)
'''
if __name__=='__main__':
    #print('Here we go')
    cb=ChessBoard(DIM)
    cb.mainloop()


cb=ChessBoard(DIM)
cb.mainloop()
'''

cb=ChessBoard(DIM)
def ml():
    global cb
    cb.mainloop()

def rf():
    while (1):
        sleep(1)
        result=[]
        with open("data0.txt",'r') as f:
            for line in f:
                result.append(list(map(int,line.split(' '))))
        for xyz in result:
            l=len(xyz)
            if (not (0<=l<DIM)):
                continue
            x,y,z=xyz[0],xyz[1],xyz[2]
            if (not (0<=z<=4)):
                continue
            btn[x][y].config(bg=colors[z])
        f.close()

_thread.start_new_thread(ml,())
_thread.start_new_thread(rf,())
sleep(1000)