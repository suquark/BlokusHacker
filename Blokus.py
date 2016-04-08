import math
import os
import sys
import random

change_around = [[-1, 0], [0, 1], [1, 0], [0, -1]]
change_diag = [[-1, 1], [1, 1], [1, -1], [-1, -1]]
change_7square = [[-3 + i, -3 + j] for i in range(7) for j in range(7)]
change_11square = [[-5 + i, -5 + j] for i in range(11) for j in range(11)]


class ChessBoard:
    def __init__(self, obj, size=14, ChessBoard=[], ChessDict={}, oppChessBoard=None):
        self.obj = obj
        self.oppChessBoard = oppChessBoard
        if not ChessBoard:
            self.matrix = [[0 for col in range(size)] for row in range(size)]
            self.ChessDict = ChessDict.copy()
            self.size = size
        else:
            self.matrix = [ChessBoard.matrix[i][:] for i in range(ChessBoard.size)]
            self.ChessDict = ChessBoard.ChessDict.copy()
            self.size = ChessBoard.size

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
        objChess = self.selfChess if obj == self.obj else self.oppChess
        for change in change_around:
            if self.inBoard(*Add([x, y], change)):
                if objChess(*Add([x, y], change)):
                    return True
        return False

    def diagHaveChess(self, obj, x, y):
        objChess = self.selfChess if obj == self.obj else self.oppChess
        for change in change_diag:
            if self.inBoard(*Add([x, y], change)):
                if objChess(*Add([x, y], change)):
                    return True
        return False

    def diagHaveDiag(self, obj, x, y):
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
        for point in pointList:
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

    def getScores(self):
        return random.random()

    def getGoodPlan(self):
        max = -10010
        diagPointList = self.getDiagList()
        for diag in diagPointList:
            for key, chess in self.ChessDict.items():
                for i in range(chess.maxRotate):
                    chess.rotate()
                    pointList = chess.getPointList()
                    for center in pointList:
                        newPointList = [Add(Minus(point, center), diag) for point in pointList]
                        if self.canPut(newPointList):
                            scores = self.getScores()
                            if max < scores:
                                goodPlan = newPointList
                                max = scores
                                goodPlanChessKey = key
        return goodPlan, goodPlanChessKey


class Chess(object):
    def __init__(self, point, level=0, maxRotate=8):
        self.level = level
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
    print out


def Minus(a, b):
    return [x - y for x, y in zip(a, b)]


def Add(a, b):
    return [x + y for x, y in zip(a, b)]


def L2Minus(a, b):
    return math.sqrt(sum([(x - y) ** 2 for x, y in zip(a, b)]))


ChessDict = {}
ChessDict['1'] = Chess([[2, 2]], 0, 1)
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

"""
#1
	O
#2
	OO
#3
	OOO
#4
	O
	OO
#5
	OOOO
#6
	O
	OOO
#7
	 O
	OOO
#8
	OO
	OO
#9
	OO
	 OO
#10
	OOOOO
#11
	   O
	OOOO
#12
	OO
	 OOO
#13
	 OO
	OOO
#14
	O O
	OOO
#15
	 O
	OOOO
#16
	 O
	 O
	OOO
#17
	O
	O
	OOO
#18
	OO
	 OO
	  O
#19
	O
	OOO
	  O
#20
	O
	OOO
	 O
#21
	 O
	OOO
	 O
"""

BlokusBoard1 = ChessBoard(obj=0, size=14, ChessDict=ChessDict)
BlokusBoard2 = ChessBoard(obj=1, size=14, ChessDict=ChessDict)
BlokusBoard1.setOppChessBoard(BlokusBoard2)
BlokusBoard2.setOppChessBoard(BlokusBoard1)
state1 = 1
player1Plan = []
player2Plan = []
player2Fail = 1
count1 = 0

UnMove = 0
OK = 1
OverTime = 2


def getData():
    error = 1
    while error == 1:
        try:
            player2Plan_str = raw_input("Your Plan:")
            num_iter = iter(player2Plan_str.split(','))
            player2Plan = [[int(x), int(next(num_iter))] for x in num_iter if x != '-1']
            player2ChessID = raw_input("Your Chess's ID:")
            flag = raw_input("Flag(UnMove = 0OK = 1OverTime = 2):")
            error = 0
        except:
            print 'Please enter in right format!'
            # raise Exception("Wrong move")
    return player2Plan, player2ChessID, flag


def postData(pointList):
    pass


while state1:
    try:
        player2Plan, player2ChessID, flag = getData()
        if flag == OK:
            BlokusBoard2.updateBoard(player2Plan, obj=BlokusBoard2.obj)
            showArray(BlokusBoard2.matrix)
            del BlokusBoard2.ChessDict[player2ChessID]
        BlokusBoard1.updateBoard(player2Plan, obj=BlokusBoard2.obj)
        if count1 == 0:
            player1Plan = [[9, 9], [8, 9], [8, 8], [7, 8], [7, 7]]
            del BlokusBoard1.ChessDict['18']
            BlokusBoard1.updateBoard(player1Plan, obj=BlokusBoard1.obj)
            BlokusBoard2.updateBoard(player1Plan, obj=BlokusBoard1.obj)
        else:
            player1Plan, player1ChessID = BlokusBoard1.getGoodPlan()
            BlokusBoard1.updateBoard(player1Plan, obj=BlokusBoard1.obj)
            BlokusBoard2.updateBoard(player1Plan, obj=BlokusBoard1.obj)
        if not player1Plan:
            player1Plan = []
            state1 = 0
        else:
            count1 += 1
            showArray(BlokusBoard1.matrix)
    except:
        state1 = 0
        print "Player1 can't put any chess!"
    for i in range(5 - len(player1Plan)):
        player1Plan.append([-1, -1])
    postData(player1Plan)
