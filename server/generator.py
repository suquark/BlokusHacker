import random
import styles
from stdlib import stdarray as array
from styles import Style


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
            print item

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
        return chess_pos_list

    def showChess(self, chess_pos_list):
        board = array.create2D(14, 14, 0)
        for point in chess_pos_list:
            board[point[0]][point[1]] = 1
        array.write2D(board)


def main():
    chess_pos_list = Generator().generate_chess()


# Generator().showChess(chess_pos_list)



if __name__ == '__main__':
    main()
