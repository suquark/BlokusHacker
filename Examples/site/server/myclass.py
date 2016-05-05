
#from simplejson import JSONDecoder
#from simplejson import JSONEncoder


# --------------------------------------------------------------------------------------
# This block define the input of the app
# the name of style is not difined
# json_example:
# '{"State": "Normal", "Style": "10", "Moves": [[1, 2], [1, 0], [0, 0], [1, 1], [1, 3]]}'
# 
# dict_example:
# {'State': 'Normal', 'Style': '10', 'Moves': [(1, 2), (1, 0), (0, 0), (1, 1), (1, 3)]}
# Moves could be a set or a list
# --------------------------------------------------------------------------------------
# rule one: using tuple to define a point
# rule two: the massage flow in the program is dict:last_move
# rule three: the procession in this file only work well if you make sure that  "move" is not empty
# --------------------------------------------------------------------------------------
class Information(object):
    """ This class define the information using in communication between server and users """

    def __init__(self, moves=None):  # moves contains the position in the chess board
        self.moves = moves
        self.movesD = {}
        self.movesJ = ''
        if isinstance(self.moves, str):
            self.movesJ = self.moves
            self.Decode()
            if not self.movesD.__contains__('State'):  # the name of 'State' may should Change
                self.movesD['State'] = 'Normal'
            elif not self.movesD.__contains__('Moves'):
                self.movesD['Moves'] = ''
            elif not self.movesD.__contains__('Style'):
                self.movesD['Style'] = ''
            self.Decode()
        elif isinstance(self.moves, dict):
            self.movesD = self.moves
            if not self.movesD.__contains__('State'):  # the name of 'State' may should Change
                self.movesD['State'] = 'normal'
            elif not self.movesD.__contains__('Moves'):
                self.movesD['Moves'] = ''
            elif not self.movesD.__contains__('Style'):
                self.movesD['Style'] = ''
            self.Encode()

    def Encode(self):
        self.movesJ = JSONEncoder().encode(self.movesD)

    def Decode(self):
        self.movesD = JSONDecoder().decode(self.movesJ)


class ChessBoard(object):
    """ChessBoard is the board of the game"""

    def __init__(self, size, moves=None, value=0):
        self.board = array.create2D(size, size, value)
        self.size = size
        self.essentialPoints = self.initEsentialPoints()
        self.forbiddenPoints = self.initForbiddenPoints()
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
            elif point in self.forbiddenPoints:
                print('Forbidden')
                break
        return flag  # moves is a list of pooints

    def initForbiddenPoints(self):
        return []

    def initEsentialPoints(self):
        return [(4, 4), (9, 9)]

    def setForbiddenPoint(self, points):
        for point in points:
            if point not in self.forbiddenPoints:
                self.board[point[0]][point[1]] = 2
                self.forbiddenPoints.append(point)

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
        for point in self.forbiddenPoints:
            if point in self.essentialPoints:
                self.board[point[0]][point[1]] = 2
                self.essentialPoints.remove(point)

    def update(self, last_move):
        # print 'db update'
        is_valid = self.checkMoves(last_move)
        if is_valid:
            move = last_move['Moves']
            for point in move:
                self.addEssentialPoint(point)
                self.addForbiddenPoint(point)
            self.rmEssentialPoint()
        return is_valid

    def judgeStyle(self, Moves):  # lastmoves is the information of the last move
        style = Style(Moves)
        return style.ID

    def Show(self):
        # for point in self.forbiddenPoints:
        #	self.board[point[0]][point[1]] = -1
        # for point in self.essentialPoints:
        # self.board[point[0]][point[1]] = 1
        array.write2D(self.board)


class Player(object):
    def __init__(self, id=None):
        self.id = id
        self.size = 14
        self.board = ChessBoard(self.size)
        self.chess_ID_list = [i for i in range(1, 22)]

    def checkmove_player(self, last_move):
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
        """
        这个方法用来判定某个玩家是否有子可下，使用的时枚举法
        过程：
        1.判断是否还有棋子（没有棋子不可下）
        2.对于：剩下的每个棋子，每个正反面，每个方向，每个棋子中的点，平移至每个essential point的情况做判定 （估算运算量21×2×4×5×20=16800）
        :return:
        """
        # 1.判断是否还有棋子（没有棋子不可下）
        if self.chess_ID_list is []:
            return True
        else:
            # 2.对于：剩下的每个棋子，每个正反面，每个方向，每个棋子中的点，平移至每个essential point的情况做判定
            for chess_ID in self.chess_ID_list:  # 每个棋子
                chess = Style(chess_ID)
                for i in range(2):
                    chess.Invert()  # 每个正反面
                    for j in range(4):
                        chess.Rotate()  # 每个方向
                        for point in chess.pointsSet:  # 每个棋子中的点
                            for essentialPoint in self.board.essentialPoints:
                                line_shift = essentialPoint[0] - point[0]  # 平移至每个essential point
                                row_shift = essentialPoint[1] - point[1]
                                possible_move = self.shift_chess(line_shift, row_shift, chess.pointsSet, chess_ID)
                                if possible_move is not None:
                                    flag = self.board.checkMoves(possible_move)
                                    if flag:
                                        return False
        return True

    def shift_chess(self, line_shift, row_shift, pointsSet, chess_ID):
        move = {'State': 'Normal', 'Style': chess_ID, 'Moves': []}
        for point in pointsSet:
            if point[0] + line_shift > self.size - 1 or point[1] + row_shift > self.size or point[0] + line_shift < 0 \
                    or point[1] + row_shift < 0:
                return None
            move['Moves'].append((point[0] + line_shift, point[1] + row_shift))
        return move

    def my_move(self, last_move):
        move_style = Style(last_move)
        is_valid = self.checkmove_player(last_move)
        if is_valid:
            self.popChess(move_style.ID)
            self.board.update(last_move)
        return is_valid

    def other_move(self, other_move):
        self.board.setForbiddenPoint(other_move['Moves'])

    def countScores(self):
        score = 0
        for ID in self.chess_ID_list:
            if ID == 1:
                score += 1
            elif ID == 2:
                score += 2
            elif ID <= 4:
                score += 3
            elif ID <= 9:
                score += 4
            else:
                score += 5
        return score


class Game(object):
    def __init__(self, p1, p2, last_moves=None):
        assert isinstance(p1, Player) and isinstance(p2, Player)
        self.p1 = p1
        self.p2 = p2
        self.last_moves = last_moves

    def update(self, player_id, last_moves):
        is_valid = True
        self.last_moves = last_moves
        assert last_moves.__contains__('State') and last_moves.__contains__('Moves')
        if last_moves['State'] is not 'Normal':
            if last_moves['State'] is 'Unmove':
                pass
        elif player_id is self.p1.id:
            is_valid = self.p1.my_move(last_moves['Moves'])
            self.p2.other_move(last_moves['Moves'])
            self.last_moves = last_moves
        else:
            is_valid = self.p2.my_move(last_moves['Moves'])
            self.p1.other_move(last_moves['Moves'])
            self.last_moves = last_moves
        return is_valid

    def check_end(self):
        is_end = False
        if self.p1.Judge_nomoves() and self.p2.Judge_nomoves():
            is_end = True
        return is_end

    def get_winner(self):
        p1_score = self.p1.countScores()
        p2_score = self.p2.countScores()
        if p1_score > p2_score:
            return self.p1.id
        else:
            return self.p2.id


from generator import *


def main():
    player = Player()
    while True:
        for i in range(1000):
            if player.Judge_nomoves():
                last_move_l = Generator().generate_chess()
                # Generator().showChess(last_move_l)
                last_move = {'Stste': 'Normal', 'Style': '', 'Moves': last_move_l}
                player.my_move(last_move)
        player.board.Show()
        A = input()
        if A == 'show':
            print(player.chess_ID_list)
            input()
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
            # lastmoves = {'Stste': 'Normal', 'Style': '10', 'Moves': [(1, 2), (1, 0), (0, 0), (1, 1), (1, 3)]}
            # cb = ChessBoard(14)
            # cb.essentialPoints = [(0, 0)]
            # cb.update(lastmoves)
            # cb.Show()


if __name__ == '__main__':
    main()
