import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.gen
import tornado.client

import hashlib
from tornado.options import define, options

from myclass import Player
import time
define("port", default = 8000, help="run on the given port", type = int)
md5_encoder = hashlib.md5()


class IndexHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	@tornado.gen.engine
	def get(self):
		game_ID = yield tornado.gen.Task(self.checkMatch)
		self.write(game_ID)

	def checkMatch(self):
		raise
				


		
		
if __name__ == '__main__':
	tornado.options.parse_command_line()
	app = tornado.web.Application(handlers = [(r"/", IndexHandler)])
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()