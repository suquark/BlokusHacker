"""
使用 Python 3 标准编写

此处使用了numpy. numpy方便, 速度快, 适合数值计算和线性代数

"""
import json
import numpy as np


class ChessBoard(object):
    """
    这个类描述了棋盘对象, 并且提供特征抽取的功能(以供机器学习或者搜索使用)

        '特征'是指能够提供信息的一种表述, 比如当前自己和对手占据的格子以及空白, 能下的棋等
         类中表述的特征一般遵循以下的规则: 没有特征标记为0, 自己的特征标记为1, 对手的特征标记为-1

    自己和对手下的棋本身也可以作为特征, 自己下的棋覆盖的地方为1, 对手为-1

    """

    def __init__(self, saved_board=None):
        """
        :param saved_board: 先前保存的棋盘, 可以直接从先前json序列化保存的结果json.load得到, 默认不查错


        """
        if saved_board is not None:
            self.matrix = np.array(saved_board.matrix)  # 将普通数组转化为Numpy数组
            self.my_chess = np.array(saved_board.my_chess)
            self.op_chess = np.array(saved_board.op_chess)
            self.state = saved_board.state
        else:
            self.matrix = np.zeros((14, 14))  # 棋盘为14 * 14的二维数组
            self.my_chess = np.ones(21)  # 每玩家21个棋子, 没有用表示为1, 摆在棋盘上为0
            self.op_chess = np.ones(21)
            self.state = 1  # 1代表Player1先棋, 2代表是Player2的回合

    def angle_feature(self):
        pass
