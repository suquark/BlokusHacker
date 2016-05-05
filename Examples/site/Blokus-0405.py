# -*- coding:utf-8 -*-

#
# Author : 庄涛
# Date : 2016/04
#

# Other deteals are at http://home.ustc.edu.cn/~ustczt/code/Blokus_sample_guide.html

import math
import random

from post_get import post_data, get_player_id



change_around = [[-1, 0], [0, 1], [1, 0], [0, -1]]
change_diag = [[-1, 1], [1, 1], [1, -1], [-1, -1]]
change_7square = [[-3 + i, -3 + j] for i in range(7) for j in range(7)]
change_11square = [[-5 + i, -5 + j] for i in range(11) for j in range(11)]


# used for coordinate transformation

class ChessBoard:
    def __init__(self, obj, size=14, ChessBoard=[], ChessDict={}, oppChessBoard=None):
        self.obj = obj  # 0 is player1 and 1 is player2
        self.oppChessBoard = oppChessBoard  # opponent's ChessBoard, it haven't been used in this sample
        if not ChessBoard:
            self.matrix = [[0 for col in range(size)] for row in range(size)]
            self.ChessDict = ChessDict.copy()
            self.size = size
        else:
            self.matrix = [ChessBoard.matrix[i][:] for i in range(ChessBoard.size)]
            self.ChessDict = ChessBoard.ChessDict.copy()
            self.size = ChessBoard.size

    def getScores(self, new_pointlist):
        """
        这是参赛者唯一需要完成的内容。
        这个程序的基本做法是对于每一种局面，它会遍历下一步可行的全部下法，对所有的可行下法调用getScores方法得到一个数
        据（这个数据只要是Python中可比较的就可以，不过一般推荐使用浮点数），然后选出分数最高的下法。
        可能用到的知识：
        1. 棋盘的信息可以由self获得，其中棋盘整体的信息以14*14的二维数组的形式保存在self.matrix中.
        2. 判断某一个点是自己的棋子，对方的棋子，自己可以下的对角，或是对方可以下的对角可以通过调用self.selfChess,
        self.selfDiag,self.oppChess, self.oppDiag四个方法得到True/False的布尔值。
        3. 视觉化整个棋盘可以用showArray(self.Matrix)实现。
        :param new_pointlist: 遍历过程中得到的某一中可下的棋子的坐标集（数据结构为list的list--数组的数组）。
        :return:返回值为任意可比较的数。
        """
        return random.random()

    def setOppChessBoard(self, chessBoard):
        self.oppChessBoard = chessBoard

    def inBoard(self, x, y):
        return x >= 0 and x < self.size and y >= 0 and y < self.size

    def oppChess(self, x, y):
        return (self.matrix[x][y] >> (1 if self.obj == 0 else 0)) % 2 == 1

    def oppDiag(self, x, y):
        return (self.matrix[x][y] >> (3 if self.obj == 0 else 2)) % 2 == 1

    def selfChess(self, x, y):
        return (self.matrix[x][y] >> (0 if self.obj == 0 else 1)) % 2 == 1

    def selfDiag(self, x, y):
        return (self.matrix[x][y] >> (2 if self.obj == 0 else 3)) % 2 == 1

    def empty(self, x, y):
        return self.matrix[x][y] % 4 == 0

    def aroundHaveChess(self, obj, x, y):
        # check around for obj's Chess at [x,y]
        objChess = self.selfChess if obj == self.obj else self.oppChess
        for change in change_around:
            if self.inBoard(*Add([x, y], change)):
                if objChess(*Add([x, y], change)):
                    return True
        return False

    def diagHaveChess(self, obj, x, y):
        # check diagonal place for obj's Chess at [x,y]
        objChess = self.selfChess if obj == self.obj else self.oppChess
        for change in change_diag:
            if self.inBoard(*Add([x, y], change)):
                if objChess(*Add([x, y], change)):
                    return True
        return False

    def diagHaveDiag(self, obj, x, y):
        # check diagonal place for obj's diagonal place at [x,y]
        objChess = self.selfChess if obj == self.obj else self.oppChess
        for change in change_around[i]:
            if self.inBoard(*Add([x, y], change)):
                if objChess(*Add([x, y], change)):
                    return True
        return False

    def updateBoard(self, pointList, obj):
        objDiag = self.selfDiag if obj == self.obj else self.oppDiag
        for point in pointList:
            self.matrix[point[0]][point[1]] = (1 << obj)
        # put Chess
        for point in pointList:
            # reset diagonal place
            for i in range(4):
                diag = Add(point, change_diag[i])
                aroundPoint = Add(point, change_around[i])
                if self.inBoard(*diag):
                    if self.empty(*diag) and not self.aroundHaveChess(obj, *diag):
                        self.matrix[diag[0]][diag[1]] |= (1 << (obj + 2))
                if self.inBoard(*aroundPoint):
                    self.matrix[aroundPoint[0]][aroundPoint[1]] &= 0xf - (1 << (obj + 2))

    def showPlan(self, plan):
        tempChessBoard = ChessBoard(obj=self.obj)
        tempChessBoard.updateBoard(plan, obj=self.obj)
        showArray(tempChessBoard.matrix)

    def getDiagList(self):
        # get self.obj's diagonal place List
        diagPointList = []
        for i in range(self.size):
            for j in range(self.size):
                if self.empty(i, j) and self.diagHaveChess(self.obj, i, j) and not self.aroundHaveChess(self.obj, i, j):
                    diagPointList.append([i, j])
        return diagPointList

    def canPut(self, pointList):
        for point in pointList:
            if not self.inBoard(*point) or not self.empty(*point) or self.aroundHaveChess(self.obj, *point):
                return False
        return True

    def getGoodPlan(self):
        # Plan is the final choise of the way to put a chess
        # eg:
        #	[[4,4], [4,5]]
        max = -10010
        diagPointList = self.getDiagList()
        # Iterate all feasible Plan for every self's diagonal place, chess, rotate and center
        for diag in diagPointList:
            for key, chess in self.ChessDict.items():
                for i in range(chess.maxRotate):
                    chess.rotate()
                    pointList = chess.getPointList()
                    for center in pointList:
                        # center is one of chess's points at diagplace
                        newPointList = [Add(Minus(point, center), diag) for point in pointList]
                        # coordinate transformation
                        if self.canPut(newPointList):
                            scores = self.getScores(newPointList)
                            if max < scores:
                                goodPlan = newPointList
                                max = scores
                                goodPlanChessKey = key
        return goodPlan, goodPlanChessKey


class Chess(object):
    def __init__(self, point, level=0, maxRotate=8):
        self.level = level  # a feature, but it haven't been used in this sample
        self.maxRotate = maxRotate
        self.rotate_count = 0
        self.matrix = [[0 for col in range(5)] for row in range(5)]
        for p in point:
            self.matrix[p[0]][p[1]] = 1

    def rotate(self):
        self.rotate_count += 1
        if (self.rotate_count != 5):
            self.matrix = [[self.matrix[4 - row][col] for row in range(5)] for col in range(5)]
        else:
            self.matrix = [[self.matrix[4 - row][col] for col in range(5)] for row in range(5)]
        self.rotate_count = 0 if self.rotate_count == self.maxRotate else self.rotate_count

    def getPointList(self):
        return [[i, j] for i in range(5) for j in range(5) if self.matrix[i][j]]


def showArray(array):
    out = ''
    for i in range(len(array)):
        for j in range(len(array[0])):
            # out += '%s '%('O' if array[i][j] % 2 == 1  else ( 'X' if array[i][j] % 4 == 2 else ( array[i][j] if array[i][j] != 0 else '-' ) ) )
            out += '%s ' % ('O' if array[i][j] % 2 == 1  else ('X' if array[i][j] % 4 == 2 else '-'))
        out += '\n'
    print(out)


def Minus(a, b):
    return [x - y for x, y in zip(a, b)]


def Add(a, b):
    return [x + y for x, y in zip(a, b)]


def L2Minus(a, b):
    return math.sqrt(sum([(x - y) ** 2 for x, y in zip(a, b)]))


ChessDict = {}
ChessDict['1'] = Chess([[2, 2]], 0, 1)  # the level is given by subjectivity
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

BlokusBoard1 = ChessBoard(obj=0, size=14, ChessDict=ChessDict)
BlokusBoard2 = ChessBoard(obj=1, size=14, ChessDict=ChessDict)
BlokusBoard1.setOppChessBoard(BlokusBoard2)
BlokusBoard2.setOppChessBoard(BlokusBoard1)

player1Plan = []
player2Plan = []

firstChess = 1
status = 1

UnMove = 0
OK = 1
OverTime = 2


def getData():
    error = 1
    while error == 1:
        try:
            player2Plan_str = input("Your Plan:")
            num_iter = iter(player2Plan_str.split(','))
            player2Plan = [[int(x), int(next(num_iter))] for x in num_iter if x != '-1']
            # clear [-1,-1]
            player2ChessID = input("Your Chess's ID:")
            flag = int(input("Flag(UnMove = 0OK = 1OverTime = 2):"))
            error = 0
        except:
            print('Please enter in right format!')
    return player2Plan, player2ChessID, flag


def test_get():
    player = get_player_id()
    print(player)


def run_ai():
    status = True
    firstChess = True
    player_id = get_player_id()
    while status:
        try:
            player2Plan, player2ChessID, flag = getData()
            # eg:
            #	player2Plan : [[4,4], [4,5]]
            #	player2ChessID : 2
            #	flag : 1
            if flag == OK:
                BlokusBoard2.updateBoard(player2Plan, obj=BlokusBoard2.obj)
                showArray(BlokusBoard2.matrix)
                del BlokusBoard2.ChessDict[player2ChessID]
                BlokusBoard1.updateBoard(player2Plan, obj=BlokusBoard2.obj)
                print('----------------------------------\n')
            if firstChess:
                player1Plan = [[9, 9], [8, 9], [8, 8], [7, 8], [7, 7]]
                player1ChessID = '18'
                firstChess = 0
            else:
                player1Plan, player1ChessID = BlokusBoard1.getGoodPlan()
            if not player1Plan:
                status = 0
                print("Player1 can't put any chess!")
            else:
                del BlokusBoard1.ChessDict[player1ChessID]
                BlokusBoard1.updateBoard(player1Plan, obj=BlokusBoard1.obj)
                BlokusBoard2.updateBoard(player1Plan, obj=BlokusBoard1.obj)
                showArray(BlokusBoard1.matrix)
                print('----------------------------------\n')
        except:
            # if something wrong happens, maybe it just has no plan.
            status = 0
            print("Player1 can't put any chess!")
        for i in range(5 - len(player1Plan)):
            player1Plan.append([-1, -1])
            # just for formatting
        post_data(player1Plan, player_id, None)

if __name__ == '__main__':
    run_ai()

