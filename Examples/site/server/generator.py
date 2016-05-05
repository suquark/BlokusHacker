import random

from requests import post

from myclass import Information, ChessBoard
from styles import Style, array


class Generator(object):
    # def generate_int(self, num, range_top, range_button = 0):
    # 	int_list = []
    # 	for i in range(num):
    # 		int_list.append(random.randint((range_button, range_top))
    # 	for item in int_list:
    # 		print item
    def generate_order_int(self, num, range_top, range_button=0):
        int_list = []
        for i in range(range_button, range_top):
            int_list.append(i)
        for item in int_list:
            print(item)

    def generate_chess(self):
        chess_pos_list = []
        chess = Style(random.randint(1, 21))
        # chess.showStyle()
        shift_l = random.randint(0, 14)
        shift_r = random.randint(0, 14)
        # print shift_r
        # print shift_l
        for pos in chess.pointsSet:
            chess_pos_list.append((min(13, pos[0] + shift_l), min(pos[1] + shift_r, 13)))
        return set(chess_pos_list)

    def showChess(self, chess_pos_list):
        board = array.create2D(14, 14, 0)
        for point in chess_pos_list:
            board[point[0]][point[1]] = 1
        array.write2D(board)

    def generate_post_data(self):
        points = self.generate_chess()
        print(points)
        chess = Style(points)
        info = Information({'Moves': list(chess.pointsSet)})
        return info.movesJ

    def generate_first_data(self):
        is_valid = False
        point_set = None
        board = ChessBoard(14)
        print(board.essentialPoints)
        while not is_valid:
            point_set = self.generate_chess()
            is_valid = board.checkMoves({'Moves': list(point_set)})
        # info = Information({'Moves': list(point_set)})
        return list(point_set)


class Tester(object):
    """
    tester = Tester()
    tester.post_last_move()
    """

    def __init__(self):
        self.generator = Generator()
        self.desk_url = 'http://localhost:8000/game'

    def post_last_moves(self, id):
        moves_json = self.generator.generate_post_data()
        print(moves_json)
        post(self.desk_url, json=moves_json)

    def post_first_moves(self, player_id):
        moves_json = self.generator.generate_first_data()
        print(moves_json)
        post(self.desk_url, data={'id': player_id, 'last_move': moves_json})


def main():
    player_id = int(input('id:'))
    tester = Tester()
    tester.post_first_moves(player_id)


    # print(Generator().generate_first_data())


if __name__ == '__main__':
    main()
