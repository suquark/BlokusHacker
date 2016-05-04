__author__ = 'Togo-PC'

from tkinter import *
import string
import _thread
from time import sleep


DIM=14
btn=[[Button for x in range(DIM)]for y in range(DIM)]
btnCB=[]
for i in range(DIM):
    btnCB.append([])
    for j in range(DIM):
        btnCB[i].append(0)
#colors=['WHITE','RED','YELLOW','BLUE','PURPLE']
#colors=['WHITE','ORANGE','PURPLE','RED','BLUE']
colors=['WHITE','ORANGE','PURPLE']

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


def Chess(point,level=0,maxRotate=8):
    rotate_count=0
    matrix=[[0 for col in range(5)]for row in range(5)]
    minp0,minp1=DIM,DIM
    for p in point:
        minp0=p[0] if p[0]<minp0 else minp0
        minp1=p[1] if p[1]<minp1 else minp1

    for p in point:
        matrix[p[0]-minp0][p[1]-minp1]=1


    def rotate(rotate_count,matrix):
        rotate_count += 1
        if (rotate_count != 5):
            matrix = [[matrix[4 - row][col] for row in range(5)] for col in range(5)]
        else:
            matrix = [[matrix[4 - row][col] for col in range(5)] for row in range(5)]
        rotate_count = 0 if rotate_count == maxRotate else rotate_count
        return rotate_count,matrix
    def minxy():
        minx,miny=5,5
        for x in range(5):
            for y in range(5):
                if matrix[x][y]:
                    minx=x if x<minx else minx
                    miny=y if y<miny else miny
        return minx,miny
    def calc():
        minx,miny=minxy()
        ans=0
        for x in range(5):
            for y in range(5):
                if matrix[x][y]:
                    realx,realy=x-minx,y-miny
                    id=realx*5+realy
                    ans+=1<<id
        return ans


    minans=calc()

    #print("minans=",minans,sep='')
    rotate_count,matrix=rotate(rotate_count,matrix)
    while rotate_count:
        minans=calc() if minans>calc() else minans
        #print("minans=",minans,calc())
        rotate_count,matrix=rotate(rotate_count,matrix)
    return minans


ChessDict = {}
ChessDict['1'] = Chess([[2,2]], 0, 1)  # the level is given by subjectivity
ChessDict['2'] = Chess([[1, 2], [2, 2]], 0, 2)
ChessDict['3'] = Chess([[2, 1], [2, 2], [2, 3]], 0, 2)
ChessDict['4'] = Chess([[1, 2], [2, 2], [2, 3]], 0, 4)
ChessDict['5'] = Chess([[2, 0], [2, 1], [2, 2], [2, 3]], 0, 2)
ChessDict['6'] = Chess([[1, 1], [2, 1], [2, 2], [2, 3]], 1, 4)
ChessDict['7'] = Chess([[1, 2], [2, 1], [2, 2], [2, 3]], 0, 4)
ChessDict['8'] = Chess([[1, 1], [1, 2], [2, 1], [2, 2]], 0, 1)
ChessDict['9'] = Chess([[1, 1], [1, 2], [2, 2], [2, 3]])
ChessDict['10'] = Chess([[2, 0], [2, 1], [2, 2], [2, 3], [2, 4]], 0, 2)
ChessDict['11'] = Chess([[2, 0], [2, 1], [2, 2], [2, 3], [1, 3]], 1)
ChessDict['12'] = Chess([[1, 0], [1, 1], [2, 1], [2, 2], [2, 3]], 1)
ChessDict['13'] = Chess([[1, 2], [1, 3], [2, 1], [2, 2], [2, 3]])
ChessDict['14'] = Chess([[1, 1], [2, 1], [2, 2], [2, 3], [1, 3]], 0, 4)
ChessDict['15'] = Chess([[1, 1], [2, 0], [2, 1], [2, 2], [2, 3]], 1)
ChessDict['16'] = Chess([[1, 2], [2, 2], [3, 1], [3, 2], [3, 3]], 0, 4)
ChessDict['17'] = Chess([[1, 1], [2, 1], [3, 1], [3, 2], [3, 3]], 0, 4)
ChessDict['18'] = Chess([[1, 1], [1, 2], [2, 2], [2, 3], [3, 3]], 0, 4)
ChessDict['19'] = Chess([[1, 1], [2, 1], [2, 2], [2, 3], [3, 3]])
ChessDict['20'] = Chess([[1, 1], [2, 1], [2, 2], [2, 3], [3, 2]])
ChessDict['21'] = Chess([[1, 2], [2, 1], [2, 2], [2, 3], [3, 2]], 0, 1)




def confirm():
    global btnCB
    down=[]
    out=[]
    id=1

    #print(btnCB)
    for x in range(DIM):
        for y in range(DIM):
            if ((btn[x][y]['bg']==colors[id])&(btnCB[x][y]!=id)):
                #print(x,y)
                down.append([x,y])
                out.append(x)
                out.append(y)
                btnCB[x][y]=id
                #print(btnCB)
    #print(str(down))
    '''
    for x in range(len(down)):
        for y in range(len(down[x])):
            if (x==len(down) & y==len(down[x])):
                print(down[x][y])
            else:
                print(str(down[x][y]),end='')
    '''
    #print(down)
    #print(len(out))
    for x in range(len(out)):
        if (x==len(out)-1):
            print(out[x])
        else:
            print(out[x],',',sep='',end='')

    f=open("Player2Data.txt","w")
    for x in range(len(out)):
        if (x==len(out)-1):
            f.write(str(out[x])+'\n')
        else:
            f.write(str(out[x])+',')
    CID=Chess(down)
    for x in range(1,22):
        if ChessDict[str(x)]==CID:
            break
    print(x)
    print(1)

    f.write(str(x)+"\n")######################################################ChessID
    f.write("1\n")

    #f.write(str(down))
    #print(btnCB)
    #print()



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
        '''
        displayX=IntVar()
        entryX=Entry(line,relief=SUNKEN)
        entryX.pack(side=LEFT,expand=YES,fill=BOTH)
        displayY=IntVar()
        entryY=Entry(line,relief=SUNKEN)
        entryY.pack(side=LEFT,expand=YES,fill=BOTH)     
        btncc=Button(line,text="C C",command=lambda : btn[int(entryX.get())][int(entryY.get())].config(bg=nextColor(btn[int(entryX.get())][int(entryY.get())]['bg'])) )
        btncc.pack(side=LEFT,expand=YES,fill=BOTH)
        '''
        btnConfirm=Button(line,text="Confirm",command=confirm)
        btnConfirm.pack(side=LEFT,expand=YES,fill=BOTH)
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
            if (not (0<=z<len(colors))):
                continue
            if 1<=z<=2:
                z=3-z
            btn[x][y].config(bg=colors[z])
        f.close()

_thread.start_new_thread(ml,())
_thread.start_new_thread(rf,())
sleep(1000)