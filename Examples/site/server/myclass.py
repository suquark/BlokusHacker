from simple_json import JSONEncoder
from simple_json import JSONDecoder
import requests


# --------------------------------------------------------------------------------------
# This block define the input of the app
# the name of style is not difined
# json_example:
# '{"Stste": "Normal", "Style": "10", "Moves": [[1, 2], [1, 0], [0, 0], [1, 1], [1, 3]]}'
# 
# dict_example:
# {'Stste': 'Normal', 'Style': '10', 'Moves': [(1, 2), (1, 0), (0, 0), (1, 1), (1, 3)]}
##Moves could be a set or a list
# --------------------------------------------------------------------------------------
# rule one: using tuple to define a point
# rule two: the massage flow in the program is dict:last_move
# rule three: the procession in this file only work well if you make sure that  "move" is not empty
# --------------------------------------------------------------------------------------
class Information(object):
    """ This class define the information uning in communication between server and users """

    def __init__(self, moves):  # moves cotains the position in the chess board
        self._moves = moves
        self._movesD = {}
        self._movesJ = ''
        if isinstance(self._moves, str):
            self._movesJ = self._moves
            self.Decode()
            if not self._movesD.__contains__('State'):  # the name of 'State' may should Change
                d['State'] = 'normal'
            elif not self._movesD.__contains__('Moves'):
                d['Moves'] = ''
            elif not self._movesD.__contains__('Style'):
                d['Style'] = ''
            self.Encode()
        elif isinstance(self._moves, dict):
            self._movesD = self._moves
            if not self._movesD.__contains__('State'):  # the name of 'State' may should Change
                d['State'] = 'normal'
            elif not self._movesD.__contains__('Moves'):
                d['Moves'] = ''
            elif not self._movesD.__contains__('Style'):
                d['Style'] = ''
            self.Encode()

    def Encode(self):
        self._movesJ = JSONEncoder().encode(self._movesD)

    def Decode(self):
        self._movesD = JSONDecoder().decode(self._movesJ)


from styles import Style
import stdlib.stdarray as array


class ChessBoard(object):
    """ChessBoard is the board of the game"""

    def __init__(self, size, moves={}, value=0):
        self.board = array.create2D(size, size, value)
        self.size = size
        self.essentialPoints = self.initEsentialPoints()
        self.fordidenPoints = self.initForbiddenPoints()
        self.styles = Style(moves)

    def showboard(self):
        array.write2D(self.board)

    def checkMoves(self, last_move):
        flag = False
        moves = last_move["Moves"]
        for point in moves:
            # print self.essentialPoints
            if point in self.essentialPoints:
                flag = True
            elif point in self.fordidenPoints:
                print 'Forbidden'
                break
        return flag  # moves is a list of pooints

    def initForbiddenPoints(self):
        return []

    def initEsentialPoints(self):
        return [(4, 4), (9, 9)]

    def setForbiddenPoint(self, points):
        for point in points:
            if point not in self.fordidenPoints:
                self.board[point[0]][point[1]] = 2
                self.fordidenPoints.append(point)

    def setEssentialPoint(self, points):
        for point in points:
            if point not in self.essentialPoints:
                self.board[point[0]][point[1]] = 1
                self.essentialPoints.append(point)

    def addEssentialPoint(self, point):
        points = []
        if point[0] < self.size - 1 and point[1] < self.size - 1:
            points.append((point[0] + 1, point[1] + 1))
        if point[0] < self.size - 1 and point[1] > 0:
            points.append((point[0] + 1, point[1] - 1))
        if point[0] > 0 and point[1] < self.size - 1:
            points.append((point[0] - 1, point[1] + 1))
        if point[0] > 0 and point[1] > 0:
            points.append((point[0] - 1, point[1] - 1))
        self.setEssentialPoint(points)

    def addForbiddenPoint(self, point):
        points = [point]
        if point[0] < self.size - 1:
            points.append((point[0] + 1, point[1]))
        if point[0] > 0:
            points.append((point[0] - 1, point[1]))
        if point[1] < self.size - 1:
            points.append((point[0], point[1] + 1))
        if point[1] > 0:
            points.append((point[0], point[1] - 1))
        self.setForbiddenPoint(points)

    def rmEssentialPoint(self):
        for point in self.fordidenPoints:
            if point in self.essentialPoints:
                self.board[point[0]][point[1]] = 2
                self.essentialPoints.remove(point)

    def update(self, last_move):
        print 'db update'
        print self.checkMoves(last_move)
        if (self.checkMoves(last_move)):
            move = last_move['Moves']
            for point in move:
                self.addEssentialPoint(point)
                self.addForbiddenPoint(point)
            self.rmEssentialPoint()

    def judgeStyle(self, Moves):  # last_moves is the information of the last move
        style = Style(Moves)
        return style.ID

    def Show(self):
        # for point in self.fordidenPoints:
        #	self.board[point[0]][point[1]] = -1
        # for point in self.essentialPoints:
        # self.board[point[0]][point[1]] = 1
        array.write2D(self.board)


from styles import Style


class Player(object):
    def __init__(self, name=''):
        self.name = name
        self.size = 14
        self.board = ChessBoard(self.size)
        self.chess_ID_list = self.initChesslist()

    def initChesslist(self):
        chess_list = []
        for i in range(1, 22):
            chess_list.append(i)
        return chess_list

    def checkmovePlayer(self, last_move):
        flag = True
        move_style_ID = Style(last_move).ID
        if move_style_ID not in self.chess_ID_list:
            flag = False
        # print 'not in chess list'
        if not self.board.checkMoves(last_move):
            flag = False
        # print 'not valiate'
        return flag

    def popChess(self, move_style_ID):
        self.chess_ID_list.remove(move_style_ID)

    def Judge_nomoves(self):
        if self.chess_ID_list is []:
            return False
        else:
            for chess_ID in self.chess_ID_list:
                chess = Style(chess_ID)
                for i in range(2):
                    chess.Invert()
                    for j in range(4):
                        chess.Rotate()
                        for point in chess.pointsSet:
                            for essentialPoint in self.board.essentialPoints:
                                line_shift = essentialPoint[0] - point[0]
                                row_shift = essentialPoint[1] - point[1]
                                possible_move = self.shiftChess(line_shift, row_shift, chess.pointsSet, chess_ID)
                                if possible_move is {}:
                                    pass
                                else:
                                    flag = self.board.checkMoves(possible_move)
                                    if flag:
                                        print possible_move
                                        return True
        return False

    def shiftChess(self, line_shift, row_shift, pointsSet, chess_ID):
        move = {'State': 'Normal', 'Style': chess_ID, 'Moves': []}
        for point in pointsSet:
            if point[0] + line_shift > self.size - 1 or point[1] + row_shift > self.size or point[0] + line_shift < 0 or \
                                    point[1] + row_shift < 0:
                return {}
            move['Moves'].append((point[0] + line_shift, point[1] + row_shift))
        return move

    def myMove(self, last_move):
        move_style = Style(last_move)
        if self.checkmovePlayer(last_move):
            self.popChess(move_style.ID)
            self.board.update(last_move)

    def otherMove(self, other_move):
        self.board.setForbiddenPoint(other_move['Moves'])

    def countScores(self):
        Score = 0
        for ID in self.chess_ID_list:
            if ID == 1:
                score = score + 1
            elif ID == 2:
                score = score + 2
            elif ID <= 4:
                score = score + 3
            elif ID <= 9:
                score = score + 4
            else:
                score = score + 5
        return score


from generator import *


def main():
    player = Player()
    while True:
        for i in range(1000):
            if player.Judge_nomoves():
                last_move_l = Generator().generate_chess()
                # Generator().showChess(last_move_l)
                last_move = {'Stste': 'Normal', 'Style': '', 'Moves': last_move_l}
                player.move(last_move)
        player.board.Show()
        A = raw_input()
        if A == 'show':
            print player.chess_ID_list
            raw_input()
        # if A is not '\n':
        # 	ID = int(raw_input('ID: '))
        # 	line_shift = int(raw_input('line_shift: '))
        # 	row_shift = int(raw_input('row_shift: '))
        # 	sty = Style(ID)
        # 	point_list = []
        # 	for point in sty.pointsSet:
        # 		point_list.append((point[0]+line_shift, point[1]+row_shift))
        # 	input_move = {'Stste': 'Normal', 'Style' : '', 'Moves' : point_list}
        # 	player.move(input_move)
        # 	player.board.Show()
        # 	raw_input()


        # player1 = Player()
        # player2 = Player()
        # last_moves = {'Stste': 'Normal', 'Style': '10', 'Moves': [(1, 2), (1, 0), (0, 0), (1, 1), (1, 3)]}
        # cb = ChessBoard(14)
        # cb.essentialPoints = [(0, 0)]
        # cb.update(last_moves)
        # cb.Show()


if __name__ == '__main__':
    main()
