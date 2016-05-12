__author__='Togo'

'''
设定一个状态记录，如果和之前一样，就不再判断。直接跳过。


共有0,1,2三种状态。
如果是2状态，就不再接受。
0.是不是与之前的重合了。
1.下的形状是规则中的一个。
2.下的形状之前没有下过。
3.没有覆盖当前的
4.邻顶不邻边


'''

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

DIM=14
btn=[[Button for x in range(DIM)]for y in range(DIM)]
ScoreDisplay=[Label]*3
btnCB=[[0 for x in range(DIM)]for y in range(DIM)]
colors=['WHITE','ORANGE','PURPLE']
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

'''

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

'''
def clear():
    for x in range(DIM):
        for y in range(DIM):
            btn[x][y].config(bg=colors[btnCB[x][y]])

rec_planstr=[]
rec_planstr.append("")
rec_planstr.append("")
rec_planstr.append("")
rec_chessid=[]
rec_chessid.append('0')
rec_chessid.append('0')
rec_chessid.append('0')
rec_flag=[]
rec_flag.append(0)
rec_flag.append(0)
rec_flag.append(0)
unMoveCount=[]
unMoveCount.append(-1)
unMoveCount.append(-1)
unMoveCount.append(-1)
status=[]
status.append(0)
status.append(0)
status.append(0)
used=[]
used.append([0]*22)
used.append([0]*22)
used.append([0]*22)
used[1][0]=1
used[2][0]=1

def printSQ(a,n):
    for x in range(n):
        for y in range(n):
            print(a[x][y],end=' ')
        print()
    print()

def getData(z=1):
    global step
    global btnCB
    while (1):
        try:
            sleep(0.1)
            if status[z]<0:
                print('Player'+str(z)+" dont't put the right format!"+' Current Step: '+str(step))
                print('Wrong Code:',status[z])
                break
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
            if flag==2:
                outf=open(GUIFile[3-z],'w')
                outf.write('-1 -1\n'+str(step)+'\n0')
                outf.close()
                continue

            if (planStr==rec_planstr[z])&(ChessID==rec_chessid[z])&(flag==rec_flag[z]):
                continue
            rec_planstr[z]=planStr
            rec_chessid[z]=ChessID
            rec_flag[z]=flag

            if flag==0:
                if int(ChessID)>unMoveCount[z]:
                    unMoveCount[z]=int(ChessID)

            if flag==1:
                ChessNum=Chess(Plan)
                cid=int(ChessID)
                if not(1<=cid<=21):
                    status[z]=-10
                    continue
                if ChessNum!=ChessDict[ChessID]:
                    status[z]=-9 #lost
                    continue
                if used[z][cid]:
                    status[z]=-8
                    continue
                used[z][cid]=1
                for x,y in Plan:
                    if (x<0)|(y<0)|(x>=DIM)|(y>=DIM):
                        status[z]=-7
                        break
                    if btnCB[x][y]>0:
                        status[z]=-6
                        break
                    if (x-1>=0):
                        if (btnCB[x-1][y]==z):
                            status[z]=-5
                            break
                    if (y-1>=0):
                        if (btnCB[x][y-1]==z):
                            status[z]=-4
                            break
                    if (x+1<DIM):
                        if (btnCB[x+1][y]==z):
                            status[z]=-3
                            break
                    if (y+1<DIM):
                        if (btnCB[x][y+1]==z):
                            status[z]=-2
                            break
                    if (x-1>=0)&(y-1>=0):
                        if (btnCB[x-1][y-1]==z):
                            status[z]=1
                    if (x-1>=0)&(y+1<DIM):
                        if (btnCB[x-1][y+1]==z):
                            status[z]=1
                    if (x+1<DIM)&(y-1>=0):
                        if (btnCB[x+1][y-1]==z):
                            status[z]=1
                    if (x+1<DIM)&(y+1<DIM):
                        if (btnCB[x+1][y+1]==z):
                            status[z]=1

                if status[z]<0:
                    continue
                if step<=2:
                    if z==1:
                        status[z]=([4,4]in Plan)
                    elif z==2:
                        status[z]=([9,9]in Plan)
                    status[z]-=1
                    if status[z]<0:
                        continue
                if step>2:
                    status[z]-=1
                    if status[z]==-1: #没有邻顶。注意判断第一步。
                        continue

            ####if ok then=
            step+=1
            if flag==1:
                for x,y in Plan:
                    btn[x][y].config(bg=colors[z])
                    btnCB[x][y]=z
                    score[z]+=1


            ScoreDisplay[z]['text']="Score"+str(z)+"="+str(score[z])

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
            outf.close()
            print('current step: ',step,'   ','from Player'+str(z))
        except:
            print("Something Unexpected Happened.")


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
        btnClear=Button(line,text="Clear",command=clear)
        btnClear.pack(side=LEFT,expand=YES,fill=BOTH)
        ScoreDisplay[1]=Label(line,text="Score1=0")
        ScoreDisplay[1].pack(side=LEFT,expand=YES,fill=BOTH)
        ScoreDisplay[2]=Label(line,text="Score2=0")
        ScoreDisplay[2].pack(side=LEFT,expand=YES,fill=BOTH)

        # ScoreDisplay[1]=Label(line,text="Score1=0")
        # ScoreDisplay[1].pack(side=LEFT,expand=YES,fill=BOTH)
        # ScoreDisplay[2]=Label(line,text="Score2=0")
        # ScoreDisplay[2].pack(side=LEFT,expand=YES,fill=BOTH)

######################################Main#########################
#
# _thread.start_new_thread(getData1,())
# _thread.start_new_thread(getData2,())
_thread.start_new_thread(getData,(1,))
_thread.start_new_thread(getData,(2,))
cb=ChessBoard(DIM)
cb.mainloop()
