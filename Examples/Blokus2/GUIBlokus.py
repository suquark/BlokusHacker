__author__='Togo'

from tkinter import *
import string
import _thread
from time import sleep

PlayerFile=[]
PlayerFile.append('Player1Data.txt')
PlayerFile.append('Player1Data.txt')
PlayerFile.append('Player2Data.txt')
GUIFile=[]
GUIFile.append('GUI1Data.txt')
GUIFile.append('GUI1Data.txt')
GUIFile.append('GUI2Data.txt')
outFile='UnName.txt'

unMoveCount=-1
DIM=14
btn=[[Button for x in range(DIM)]for y in range(DIM)]
ScoreDisplay=[Label]*3
btnCB=[[0 for x in range(DIM)]for y in range(DIM)]
colors=['WHITE','ORANGE','PURPLE']
used=[0]*22
used[0]=1
cantMove=[0]*3
step=0
score=[0]*3
###############################for GUI start################################
def frame(root,side):
    w=Frame(root)
    w.pack(side=side,expand=YES,fill=BOTH)
    return w
def nextColor(color):
    global colors
    num=len(colors)
    for i in range(num):
        if colors[i]==color:
            return colors[(i+1)%num]
    return 'WHITE'  #IF NOT FIND

def button(root,side,text,command=None,bg='WHITE'):
    w=Button(root,text=text,command=lambda:w.config(bg=nextColor(w['bg'])),bg=bg)
    w.pack(side=side,expand=YES,fill=BOTH)
    return w
###############################for GUI end  ################################

#################################for ChessDict start################################
def Chess(point,level=0,maxRotate=8):
    rotate_count=0
    matrix=[[0 for col in range(5)]for row in range(5)]
    minp0,minp1=DIM,DIM
    for [p0,p1] in point:
        minp0=p0 if p0<minp0 else minp0
        minp1=p1 if p1<minp1 else minp1

    for [p0,p1] in point:
        matrix[p0-minp0][p1-minp1]=1

    def rotate(rotate_count,matrix):
        rotate_count+=1
        if (rotate_count != 4):
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
                    minx=x if x <minx else minx
                    miny=y if y <miny else miny
        return minx,miny
    def calc():
        minx,miny=minxy()
        ans=0
        for x in range(5):
            for y in range(5):
                if matrix[x][y]:
                    rx,ry=x-minx,y-miny
                    id=rx*5+ry
                    ans+=1<<id
        return ans

    minans=calc() #rotate_count=0
    rotate_count,matrix=rotate(rotate_count,matrix)
    while rotate_count:
        minans=calc() if calc()<minans else minans #rotate_count=1,2,3,4,5,6,7
        rotate_count,matrix=rotate(rotate_count,matrix)
    return minans

ChessDict = {}
ChessDict['1'] = Chess([[2,2]])  # the level is given by subjectivity
ChessDict['2'] = Chess([[1, 2], [2, 2]])
ChessDict['3'] = Chess([[2, 1], [2, 2], [2, 3]])
ChessDict['4'] = Chess([[1, 2], [2, 2], [2, 3]])
ChessDict['5'] = Chess([[2, 0], [2, 1], [2, 2], [2, 3]])
ChessDict['6'] = Chess([[1, 1], [2, 1], [2, 2], [2, 3]])
ChessDict['7'] = Chess([[1, 2], [2, 1], [2, 2], [2, 3]])
ChessDict['8'] = Chess([[1, 1], [1, 2], [2, 1], [2, 2]])
ChessDict['9'] = Chess([[1, 1], [1, 2], [2, 2], [2, 3]])
ChessDict['10'] = Chess([[2, 0], [2, 1], [2, 2], [2, 3], [2, 4]])
ChessDict['11'] = Chess([[2, 0], [2, 1], [2, 2], [2, 3], [1, 3]])
ChessDict['12'] = Chess([[1, 0], [1, 1], [2, 1], [2, 2], [2, 3]])
ChessDict['13'] = Chess([[1, 2], [1, 3], [2, 1], [2, 2], [2, 3]])
ChessDict['14'] = Chess([[1, 1], [2, 1], [2, 2], [2, 3], [1, 3]])
ChessDict['15'] = Chess([[1, 1], [2, 0], [2, 1], [2, 2], [2, 3]])
ChessDict['16'] = Chess([[1, 2], [2, 2], [3, 1], [3, 2], [3, 3]])
ChessDict['17'] = Chess([[1, 1], [2, 1], [3, 1], [3, 2], [3, 3]])
ChessDict['18'] = Chess([[1, 1], [1, 2], [2, 2], [2, 3], [3, 3]])
ChessDict['19'] = Chess([[1, 1], [2, 1], [2, 2], [2, 3], [3, 3]])
ChessDict['20'] = Chess([[1, 1], [2, 1], [2, 2], [2, 3], [3, 2]])
ChessDict['21'] = Chess([[1, 2], [2, 1], [2, 2], [2, 3], [3, 2]])

#Check if ok
for x in range(1,22):
    print("ChessDict["+str(x)+"]=",ChessDict[str(x)])


#################################for ChessDict end  ################################



def confirm():
    global btnCB
    global used
    down=[]
    out=[]
    id=1

    for x in range(DIM):
        for y in range(DIM):
            if ((btn[x][y]['bg']==colors[id])&(btnCB[x][y]!=id)):
                down.append([x,y])
                btnCB[x][y]=id
    cft=Chess(down)
    for CID in range(1,22):
        if ChessDict[str(CID)]==cft:
            break
    if (ChessDict[str(CID)]!=cft):
        CID=0
    if used[CID]:
        for [x,y] in down:
            btnCB[x][y]=0
        clear()
        return
    else:
        used[CID]=1

    f=open(outFile,'w')
    for x in range(len(down)):
        if (x==len(down)-1):
            f.write(str(down[x][0])+' '+str(down[x][1])+'\n')
        else:
            f.write(str(down[x][0])+' '+str(down[x][1])+' ')
    f.write(str(CID)+'\n')
    f.write('1')
    f.close()

def unMove():
    global unMoveCount
    f=open(outFile,'w')
    f.write('-1 -1\n')
    unMoveCount+=1
    f.write(str(unMoveCount)+'\n')
    f.write('0')
    f.close()


def clear():
    for x in range(DIM):
        for y in range(DIM):
            btn[x][y].config(bg=colors[btnCB[x][y]])

def getData2(z=2):
    global step
    while (1):
        try:
            sleep(1)
            f=open(PlayerFile[z],'r')
            planStr=f.readline()
            planStr=planStr.rstrip()
            num_iter = iter(planStr.split(' '))
            Plan = [[int(x), int(next(num_iter))] for x in num_iter]
            ChessID=f.readline()
            ChessID=str(int(ChessID))
            flag=int(f.readline())
            f.close()

            ####check if ok
            ####if ok then=
            step+=1
            if flag==1:
                for x,y in Plan:
                    btn[x][y].config(bg=colors[z])
                    btnCB[x][y]=z
                    score[z]+=1
            #ScoreDisplay[1][Text]="Score"+str(z)+"="+str(score[z])

            outf=open(GUIFile[3-z],'w')
            # if flag==0:
            #     outf.write(planStr+'\n')
            #     outf.write(str(step)+'\n')
            #     outf.write(str(flag))
            # elif flag==1:
            #     outf.write(planStr+'\n')
            #     outf.write(ChessID+'\n')
            #     outf.write(str(flag))
            # elif flag==2:
            #     outf.write('-1 -1\n'+str(step)+'\n0')
            if flag<=1:
                outf.write(planStr+'\n')
                outf.write(ChessID+'\n')
                outf.write(str(flag))
            else:
                outf.write('-1 -1\n'+str(step)+'\n0')
            outf.close()
        except:
            pass

def getData1(z=1):
    global step
    while (1):
        try:
            sleep(1)
            f=open(PlayerFile[z],'r')
            planStr=f.readline()
            planStr=planStr.rstrip()
            num_iter = iter(planStr.split(' '))
            Plan = [[int(x), int(next(num_iter))] for x in num_iter]
            ChessID=f.readline()
            ChessID=str(int(ChessID))
            flag=int(f.readline())
            f.close()

            ####check if ok
            ####if ok then=
            step+=1
            if flag==1:
                for x,y in Plan:
                    btn[x][y].config(bg=colors[z])
                    btnCB[x][y]=z
                    score[z]+=1
            # w=Button(root,text=text,command=lambda:w.config(bg=nextColor(w['bg']))
            # ScoreDisplay[1]['Text']="Score"+str(z)+"="+str(score[z])
            #ScoreDisplay[1].config(Text="Score"+str(z)+"="+str(score[z]))


            outf=open(GUIFile[3-z],'w')
            # if flag==0:
            #     outf.write(planStr+'\n')
            #     outf.write(str(step)+'\n')
            #     outf.write(str(flag))
            # elif flag==1:
            #     outf.write(planStr+'\n')
            #     outf.write(ChessID+'\n')
            #     outf.write(str(flag))
            # elif flag==2:
            #     outf.write('-1 -1\n'+str(step)+'\n0')
            if flag<=1:
                outf.write(planStr+'\n')
                outf.write(ChessID+'\n')
                outf.write(str(flag))
            else:
                outf.write('-1 -1\n'+str(step)+'\n0')
            outf.close()
        except:
            pass


class ChessBoard(Frame):
    def __init__(self,DIM):
        Frame.__init__(self)
        self.pack(expand=YES,fill=BOTH)
        self.master.title("Blokus Board Z.Q.")
        self.master.geometry('600x600')

        global btn
        global ScoreDisplay
        global ScoreDisPlay1
        global ScoreDisPlay2
        for x in range(DIM):
            line=frame(self,TOP)
            for y in range(DIM):
                btn[x][y]=button(line,LEFT,'')
        line=frame(self,TOP)  #last line for Command
        btnConfirm=Button(line,text="Confirm",command=confirm)
        btnConfirm.pack(side=LEFT,expand=YES,fill=BOTH)
        btnClear=Button(line,text="Clear",command=clear)
        btnClear.pack(side=LEFT,expand=YES,fill=BOTH)
        btnUnMove=Button(line,text="UnMove",command=unMove)
        btnUnMove.pack(side=LEFT,expand=YES,fill=BOTH)
        ScoreDisplay1=Label(line,text="Score1=0")
        ScoreDisplay1.pack(side=LEFT,expand=YES,fill=BOTH)
        ScoreDisplay2=Label(line,text="Score2=0")
        ScoreDisplay2.pack(side=LEFT,expand=YES,fill=BOTH)

        # ScoreDisplay[1]=Label(line,text="Score1=0")
        # ScoreDisplay[1].pack(side=LEFT,expand=YES,fill=BOTH)
        # ScoreDisplay[2]=Label(line,text="Score2=0")
        # ScoreDisplay[2].pack(side=LEFT,expand=YES,fill=BOTH)

######################################Main#########################

_thread.start_new_thread(getData1,())
_thread.start_new_thread(getData2,())
cb=ChessBoard(DIM)
cb.mainloop()
