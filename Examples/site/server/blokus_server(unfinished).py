import random
import time
import tornado.gen
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

from myclass import Game
from myclass import Information
from myclass import Player

define("port", default=8000, help="run on the given port", type=int)

used_index = []
wait_player_list = []
player_dict = {}
game_dict = {}

"""
There are mainly a problems in the programs 1. asy operation is falid it is not asy at all
"""
def generate_index():
    index = 0
    while index in used_index:
        index = random.randint(1, 100000)
    return index


def check_match(player, callback=None):
    had_match = False
    while not had_match:
        wait_player_num = len(wait_player_list)
        for game in game_dict.itervalues():                 # check if I had been matched
            if game.p1 == player or game.p2 == player:
                had_match = True
        if not had_match and wait_player_num > 1:           # if I had not been match and there is someone else waiting
            wait_player_list.remove(player)
            other_player = wait_player_list.pop(0)
            game_id = generate_index()
            new_game = Game(player, other_player)
            game_dict[game_id] = new_game
            had_match = True
        else:
            time.sleep(1)


def check_other_moved(game_id, moves, callback=None):
    had_moved = False
    while not had_moved:
        if game_id.last_moves is not moves:
            had_moved = True
        else:
            time.sleep(1)
    return moves

class TestHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write('TestHandler: ')
        self.write(str(wait_player_list))


class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        # first this function generate a player and then it check whether there is someone is waiting
        # if there is, it will start a game, if not it will append the player into the waiting line
        player_id = generate_index()
        self.player = Player(player_id)
        wait_player_list.append(self.player)
        yield tornado.gen.Task(check_match, self.player)  # asynchronous part
        player_dict[player_id] = self.player
        game_id = self.get_game_id()
        if player_id == game_dict[game_id].p1.id:
            self.write(player_id)
        else:
            yield tornado.gen.Task(check_other_moved, [game_id, None])
        self.finish()

    def get_game_id(self):
        game_id = -1
        for (index, game) in game_dict.iteritems():
            if self.player == game.p1 or self.player == game.p2:
                game_id = index
                break
        return game_id

    @tornado.gen.engine
    def post(self):
        # Form is define as the format: {'id' : value1, 'Moves' : value2} while value1 is an int num, and value a list
        # of tuples which shows the point to be covered
        winner_id = None
        player_id = self.get_argument('id')
        last_move = self.get_argument('Moves')
        # get player id and moves
        self.player = player_dict[player_id]
        # get game id
        game_id = self.get_game_id()
        game_dict[game_id].update(player_id, last_move)
        # check whether the id is valid and the game come to the end
        information = Information()
        if game_id not in game_dict.iterkeys():
            information.movesD['State'] = 'invalid id'
        else:
            # return the winner and del the game and players
            if isinstance(game_dict[game_id], int):  # the winner has already decided and game is replaced with id
                winner_id = game_dict[game_id]  # del all
                del used_index[player_id]
                del player_dict[player_id]
                del game_dict[game_id]
            elif isinstance(game_dict[game_id], Player):
                if game_dict[game_id].check_end():  # haven't come to the end of the game then check
                    winner_id = game_dict[game_id].get_winner()
                    del used_index[player_id]
                    del player_dict[player_id]
                    del game_dict[game_id]
                    game_dict[game_id] = winner_id  # winner_id is used to sent information to an other player
        # handle the end of the game
        if winner_id is not None:
            if winner_id == player_id:
                information.movesD['State'] = 'Win'
            else:
                information.movesD['State'] = 'Lost'
        else:
            # wait until the op move and get the return information
            yield tornado.gen.Task(check_other_moved, [game_id, last_move])
            information = Information(game_dict[game_id].last_moves)
        return_information = information.Encode()
        self.write(return_information)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler), (r"/test", TestHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
