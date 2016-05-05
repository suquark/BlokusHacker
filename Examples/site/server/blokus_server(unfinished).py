# -*- coding:utf-8 -*-
import random
import time
import json
import tornado.gen
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.web
from tornado.concurrent import run_on_executor
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import RequestHandler, Application

from myclass import Game
from myclass import Information
from myclass import Player

# python 3+ with the futures itself,however you should install it while using python2+
from concurrent.futures import ThreadPoolExecutor

define("port", default=8000, help="run on the given port", type=int)

used_index = [0]
wait_player_list = []
player_dict = {}
game_dict = {}


def generate_index():
    index = 0
    while index in used_index:
        index = random.randint(1, 100000)
    used_index.append(index)
    return index


def check_match(player):
    had_match = False
    while not had_match:
        wait_player_num = len(wait_player_list)
        for game in game_dict.values():  # check if I had been matched
            if game.p1 == player or game.p2 == player:
                had_match = True
        if not had_match and wait_player_num > 1:  # if I had not been match and there is someone else waiting
            wait_player_list.remove(player)
            other_player = wait_player_list.pop(0)
            game_id = generate_index()
            new_game = Game(player, other_player)
            game_dict[game_id] = new_game
            had_match = True
        else:
            time.sleep(1)


def check_other_moved(game_id, last_moves):
    had_moved = False
    while not had_moved:
        if game_dict[game_id].last_moves is not last_moves:
            had_moved = True
        else:
            time.sleep(1)
    return game_dict[game_id].last_moves


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<html><body><form action="/" method="post">'
                   '<input type="text" name="message">'
                   '<input type="submit" value="Submit">'
                   '</form></body></html>')

    def post(self):
        self.set_header("Content-Type", "text/plain")
        self.write("You wrote " + self.get_argument("message"))


class TestHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.write('TestHandler: ')
        self.write(str(wait_player_list) + '\n')
        self.write(str(player_dict) + '\n')
        self.write(str(isinstance(player_dict, dict)) + '\n')
        self.write(str(game_dict) + '\n')
        self.write(str(isinstance(player_dict, dict)) + '\n')
        for key, game in game_dict.items():
            self.write(str(key) + ' ' + str(game) + ' ' + str(game.last_moves) + '\n')

    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        self.write(data)
        f = open('test.txt', 'w')
        f.write(data)
        f.close()


class IndexHandler(RequestHandler):
    executor = ThreadPoolExecutor(20)

    @run_on_executor
    def get(self):
        """
        first this function generate a player and then it check whether there is someone is waiting
        if there is, it will start a game, if not it will append the player into the waiting line
        """
        player_id = generate_index()
        self.player = Player(player_id)
        wait_player_list.append(self.player)
        check_match(self.player)  # asynchronous part
        player_dict[player_id] = self.player
        game_id = self.get_game_id()
        if player_id == game_dict[game_id].p1.id:
            self.write(str(player_id) + '\n')
        else:
            check_other_moved(game_id, None)
            self.write(str(player_id) + '\n')
            info = Information(game_dict[game_id].last_moves)
            self.write(info.movesJ + '\n')

    def get_game_id(self):
        game_id = -1
        for (index, game) in game_dict.items():
            if self.player == game.p1 or self.player == game.p2:
                game_id = index
                break
        return game_id


class GameHandler(RequestHandler):
    executor = ThreadPoolExecutor(20)

    @run_on_executor
    def post(self):
        """
        This function is used to get the moves of the player and then update the board
        Form is define as the format: {'id' : value1, 'Moves' : value2} while value1 is an int num, and value a list
         of tuples which shows the point to be covered
        :return:
        基本操作：
        1.获取数据（用户传来的player_id和形式为json的data，然后获取game_id）
        2.先检查棋局是否已经处于‘已结束’的状态（如果结束则返回是否胜利）
        3.更新棋盘（先更新用户自己的棋盘，然后是对方的棋盘）
        4.检查棋局是否结束（如果棋局结束获得胜利者的id，并将棋局标记为‘已结束’的状态）
        5.异步获取对方的下一步
        6.返回下一步
        """
        # 1.获取数据（用户传来的player_id和形式为json的data，然后获取game_id)
        end = False
        data = self.get_argument('last_move')
        player_id = int(self.get_argument('id'))
        print(data)
        # f = open('test.txt', 'w')
        # f.write(data)
        # f.close()
        data = {"Moves": data}
        last_move = Information(data).movesD
        self.player = player_dict[player_id]
        game_id = self.get_game_id()
        return_information = Information()

        # 1.1检查棋局是否存在
        if game_id not in game_dict.keys():
            return_information.movesD['State'] = 'invalid id'
        else:
            # 2.先检查棋局是否已经处于‘已结束’的状态（如果结束彻底删除棋局，返回是否胜利)
            if isinstance(game_dict[game_id], int):
                end = True
                winner_id = game_dict[game_id]
                del used_index[player_id]
                del player_dict[player_id]
                del game_dict[game_id]
                if winner_id == player_id:
                    return_information.movesD['State'] = 'Win'
                else:
                    return_information.movesD['State'] = 'Lost'
        # 3.更新棋盘（先检查棋子是否可下，如可下更新用户自己的棋盘，然后是对方的棋盘）
        is_valid = True
        if not end:
            is_valid = game_dict[game_id].update(player_id, last_move)
            return_information.movesD['State'] = 'Invalid'
        # 4.检查棋局是否结束（如果棋局结束获得胜利者的id，并将棋局标记为‘已结束’的状态）
        assert isinstance(game_dict[game_id], Game)
        if is_valid and game_dict[game_id].check_end():
            end = True
            winner_id = game_dict[game_id].get_winner()
            del used_index[player_id]
            del player_dict[player_id]
            del game_dict[game_id]
            game_dict[game_id] = winner_id  # 标记棋局已结束，同时传递胜者id
            if winner_id == player_id:
                return_information.movesD['State'] = 'Win'
            else:
                return_information.movesD['State'] = 'Lost'
        if not end:
            # 5.异步获取对方的下一步
            other_moves = check_other_moved(game_id, last_move)
            return_information = Information(other_moves)
        # 6.返回下一步
        return_information.Encode()
        assert isinstance(return_information, Information)
        self.write(return_information.movesJ + '\n')

    def get_game_id(self):
        game_id = -1
        for (index, game) in game_dict.items():
            if self.player == game.p1 or self.player == game.p2:
                game_id = index
                break
        return game_id


# if __name__ == '__main__':
#     tornado.options.parse_command_line()
#     app = tornado.web.Application(handlers=[(r"/", IndexHandler), (r"/test", TestHandler)])
#     http_server = tornado.httpserver.HTTPServer(app)
#     http_server.listen(options.port)
#     tornado.ioloop.IOLoop.instance().start()

settings = {
    # cookie_secret : base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
    "cookie_secret": "udhdchguygG^&*Y%76798UH&*GfD%^&TG%^$D^%&TXg*(YG7xf677",
    # "login_url": "/login",
    # "xsrf_cookies": True,
    # "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "xheaders": True  # make "self.request.remote_ip" a real IP instead of agent's (self.request.headers['X-Real-Ip'])
}

# 路由表
application = Application([
    (r"/", IndexHandler),
    (r"/test", TestHandler),
    (r"/test2", MainHandler),
    (r'/game', GameHandler),
], **settings)

# 如果是主模块, 开始新的服务例程
if __name__ == "__main__":
    application.listen(options.port)
    IOLoop.instance().start()
