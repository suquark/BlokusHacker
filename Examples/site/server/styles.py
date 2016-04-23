# import stdlib.stdarray as array
class array(object):
    @staticmethod
    def create2D(rowCount, colCount, value=None):
        """
        Create and return a 2D array having rowCount rows and colCount
        columns, with each element initialized to value.
        """
        a = [None] * rowCount
        for row in range(rowCount):
            a[row] = [value] * colCount
        return a

    @staticmethod
    def write2D(arr):
        print(str(arr).replace("],", "]\n"))


class Style(object):
    """Style contains the 21 style of the blokus"""

    def __init__(self, arg):
        self._squaresize = 5
        self.points = [[0] * 5] * 5
        self.pointsSet = set([])
        self.ID = 0
        if isinstance(arg, int) and arg in range(1, 22):
            self.ID = arg
            self.ID2Points()
            self.Points2PointSet()
        elif isinstance(arg, list) and len(arg) > 0:
            self.points = arg
            self.Points2ID()
            self.Points2PointSet()
        elif isinstance(arg, set) and arg is not set([]):
            self.pointsSet = arg
            self.Pointset2Points()
            self.Points2ID()
            self.Points2PointSet()
        elif isinstance(arg, dict):
            if 'Moves' in arg:
                self.pointsSet = self.initPointset(arg['Moves'])
                self.Pointset2Points()
                self.Points2ID()
                self.Points2PointSet()
        elif arg == None:
            pass
        else:
            raise ("Unkonwn")

    def initPointset(self, move):
        point_list = []
        point_list_r = []
        point_list_l = []
        for point in move:
            point_list_l.append(point[0])
            point_list_r.append(point[1])
        min_l = min(point_list_l)
        min_r = min(point_list_r)
        for point in move:
            point_list.append((point[0] - min_l, point[1] - min_r))
        return set(point_list)

    def _normolize(self):
        square = array.create2D(self._squaresize, self._squaresize, 0)
        temp_list_r = []
        temp_list_l = []
        for i in range(self._squaresize):
            for j in range(self._squaresize):
                if self.points[i][j] is 1:
                    temp_list_l.append(i)
                    temp_list_r.append(j)
        if bool(temp_list_l):
            min_l = min(temp_list_l)
        else:
            min_l = 0
        if bool(temp_list_r):
            min_r = min(temp_list_r)
        else:
            min_r = 0
        for i in range(self._squaresize - min_l):
            for j in range(self._squaresize - min_r):
                square[i][j] = self.points[i + min_l][j + min_r]
        self.points = square

    def Rotate(self):
        square = array.create2D(self._squaresize, self._squaresize, 0)
        mid = 2
        for i in range(self._squaresize):
            for j in range(self._squaresize):
                square[i][j] = self.points[j][2 * mid - i]
        self.points = square
        self._normolize()

    def Invert(self):
        square = array.create2D(self._squaresize, self._squaresize, 0)
        for i in range(self._squaresize):
            for j in range(self._squaresize):
                square[i][j] = self.points[j][i]
        self.points = square
        self._normolize()

    def Points2PointSet(self):
        temp_list = []
        for i in range(self._squaresize):
            for j in range(self._squaresize):
                if self.points[i][j] is 1:
                    temp_list.append(tuple([i, j]))
        self.pointsSet = set(temp_list)

    def ID2PointSet(self):
        self.ID2Points()
        self.Points2PointSet()

    def Pointset2Points(self):
        square = array.create2D(5, 5, 0)
        row_index_min = min([point[0] for point in self.pointsSet])
        line_index_min = min([point[1] for point in self.pointsSet])
        for point in self.pointsSet:
            square[point[0]-row_index_min][point[1]-line_index_min] = 1
        self.points = square

    def Points2ID(self):
        for i in range(2):
            if i is 1:
                self.Invert()
            for j in range(4):
                if j is not 0:
                    self.Rotate()
                self.Points2PointSet()
                return_val = self.Pointset2ID()
                if return_val > 0:
                    self.ID = return_val
                    return return_val
        return return_val

    def showStyle(self):
        array.write2D(self.points)
        print(self.ID)
        print(self.pointsSet)

    def CompareID(self, other_ID):
        if self.ID == other_ID:
            return True

    def ComparePoints(self, other_points):
        if self.points == other_points:
            return True

    def ComparePointSet(self, other_pointSet):
        if self.pointsSet == other_pointSet:
            return True

    def ID2Points(self):
        Style_size = self._squaresize
        square = array.create2D(Style_size, Style_size, 0)
        if self.ID == 0:
            pass
        elif self.ID == 1:
            square[0][0] = 1
        elif self.ID == 2:
            square[0][0] = 1
            square[0][1] = 1
        elif self.ID == 3:
            square[0][0] = 1
            square[0][1] = 1
            square[0][2] = 1
        elif self.ID == 4:
            square[0][0] = 1
            square[0][1] = 1
            square[1][1] = 1
        elif self.ID == 5:
            square[0] = [1, 1, 0, 0, 0]
            square[1] = [1, 1, 0, 0, 0]
        elif self.ID == 6:
            square[0] = [1, 1, 1, 0, 0]
            square[1] = [0, 1, 0, 0, 0]
        elif self.ID == 7:
            square[0] = [1, 1, 1, 1, 0]
        elif self.ID == 8:
            square[0] = [1, 1, 1, 0, 0]
            square[1][0] = 1
        elif self.ID == 9:
            square[0] = [0, 1, 1, 0, 0]
            square[1] = [1, 1, 0, 0, 0]
        elif self.ID == 10:
            square[0][0] = 1
            square[1] = [1, 1, 1, 1, 0]
        elif self.ID == 11:
            square[0][1] = 1
            square[1][1] = 1
            square[2] = [1, 1, 1, 0, 0]
        elif self.ID == 12:
            square[0][0] = 1
            square[1][0] = 1
            square[2] = [1, 1, 1, 0, 0]
        elif self.ID == 13:
            square[0] = [0, 1, 1, 1, 0]
            square[1] = [1, 1, 0, 0, 0]
        elif self.ID == 14:
            square[0][2] = 1
            square[1] = [1, 1, 1, 0, 0]
            square[2][0] = 1
        elif self.ID == 15:
            square[0] = [1, 1, 1, 1, 1]
        elif self.ID == 16:
            square[0] = [1, 1, 1, 0, 0]
            square[1] = [1, 1, 0, 0, 0]
        elif self.ID == 17:
            square[0] = [0, 1, 1, 0, 0]
            square[1] = [1, 1, 0, 0, 0]
            square[2] = [1, 0, 0, 0, 0]
        elif self.ID == 18:
            square[0] = [1, 1, 0, 0, 0]
            square[1] = [1, 0, 0, 0, 0]
            square[2] = [1, 1, 0, 0, 0]
        elif self.ID == 19:
            square[0] = [0, 1, 1, 0, 0]
            square[1] = [1, 1, 0, 0, 0]
            square[2] = [0, 1, 0, 0, 0]
        elif self.ID == 20:
            square[0][1] = 1
            square[1] = [1, 1, 1, 0, 0]
            square[2][1] = 1
        elif self.ID == 21:
            square[0][1] = 1
            square[1] = [1, 1, 1, 1, 0]
        else:
            pass
        self.points = square

    def Pointset2ID(self):
        if self.pointsSet == set([(0, 0)]):
            self.ID = 1
            return 1
        elif self.pointsSet == set([(0, 1), (0, 0)]):
            self.ID = 2
            return 2
        elif self.pointsSet == set([(0, 1), (0, 0), (0, 2)]):
            self.ID = 3
            return 3
        elif self.pointsSet == {(0, 1), (0, 0), (1, 1)}:
            self.ID = 4
            return 4
        elif self.pointsSet == set([(0, 1), (1, 0), (0, 0), (1, 1)]):
            self.ID = 5
            return 5
        elif self.pointsSet == set([(0, 1), (0, 0), (0, 2), (1, 1)]):
            self.ID = 6
            return 6
        elif self.pointsSet == set([(0, 1), (0, 3), (0, 0), (0, 2)]):
            self.ID = 7
            return 7
        elif self.pointsSet == set([(0, 1), (1, 0), (0, 0), (0, 2)]):
            self.ID = 8
            return 8
        elif self.pointsSet == set([(0, 1), (1, 0), (0, 2), (1, 1)]):
            self.ID = 9
            return 9
        elif self.pointsSet == set([(1, 2), (1, 0), (0, 0), (1, 1), (1, 3)]):
            self.ID = 10
            return 10
        elif self.pointsSet == set([(0, 1), (2, 0), (1, 1), (2, 1), (2, 2)]):
            self.ID = 11
            return 11
        elif self.pointsSet == set([(2, 0), (1, 0), (0, 0), (2, 1), (2, 2)]):
            self.ID = 12
            return 12
        elif self.pointsSet == set([(0, 1), (1, 1), (0, 3), (0, 2), (1, 0)]):
            self.ID = 13
            return 13
        elif self.pointsSet == set([(1, 2), (2, 0), (1, 0), (0, 2), (1, 1)]):
            self.ID = 14
            return 14
        elif self.pointsSet == set([(0, 1), (0, 3), (0, 0), (0, 2), (0, 4)]):
            self.ID = 15
            return 15
        elif self.pointsSet == set([(0, 1), (1, 0), (0, 0), (0, 2), (1, 1)]):
            self.ID = 16
            return 16
        elif self.pointsSet == set([(0, 1), (2, 0), (1, 0), (0, 2), (1, 1)]):
            self.ID = 17
            return 17
        elif self.pointsSet == set([(0, 1), (2, 0), (1, 0), (0, 0), (2, 1)]):
            self.ID = 18
            return 18
        elif self.pointsSet == set([(0, 1), (1, 0), (0, 2), (2, 1), (1, 1)]):
            self.ID = 19
            return 19
        elif self.pointsSet == set([(0, 1), (1, 2), (1, 0), (1, 1), (2, 1)]):
            self.ID = 20
            return 20
        elif self.pointsSet == set([(0, 1), (1, 2), (1, 0), (1, 3), (1, 1)]):
            self.ID = 21
            return 21
        else:
            return -1


import string


def main():
    f = open('text.py', 'w')
    # f.writelines('def Pointset2ID(self):\n')
    for i in range(1, 22):
        sty = Style(i)
        f.write(str(sty.ID) + '\n')
        f.write(str(sty.pointsSet) + '\n')
        f.close()
        # 	if i == 1:
        # 		tempstr = ''
        # 	else:
        # 		tempstr = 'el'
        # 	f.writelines('\t%sif self.pointsSet == %s:\n' %(tempstr,str(sty.pointsSet)))
        # 	f.writelines('\t\tself.ID = %s\n' %str(sty.ID))
        # 	f.writelines('\t\treturn %d\n' %sty.ID)

        # while True:
        # 	num = raw_input()
        # 	if num == 'q':
        # 		break;
        # 	else:
        # 		num = int(num)
        # 		sty = Style(num)
        # 		sty.showStyle()
        # 		print 'sty2:\n'
        # 		sty2 = Style(sty.points)
        # 		sty2.showStyle()
        # 		print 'sty3:\n'
        # 		sty3 = Style(sty.pointsSet)
        # 		sty3.showStyle()
        # 		print 'sty:\n'
        # 		# while True:
        # 		# 	op = raw_input()
        # 		# 	if op is 'q':
        # 		# 		break;
        # 		# 	for i in range(int(op)):
        # 		# 		sty.Rotate()
        # 		# 	sty.showStyle()
        # 		# while True:
        # 		# 	op = raw_input()
        # 		# 	if op is 'q':
        # 		# 		break;
        # 		# 	for i in range(int(op)):
        # 		# 		sty.Invert()
        # 		# 	sty.showStyle()


if __name__ == '__main__':
    main()
