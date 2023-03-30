from telebot.asyncio_handler_backends import BaseMiddleware, CancelUpdate

class RequestAntiflood(BaseMiddleware):
	
	def __init__(self, limit, bot) -> None:
		self.last_time = {}
		self.limit = limit
		self.bot = bot
		self.update_types = ['message']
		# Always specify update types, otherwise middlewares won't work

	async def pre_process(self, message, data):
		if not message.text.startswith("/"):
			if not message.from_user.id in self.last_time:
				# User is not in a dict, so lets add and cancel this function
				self.last_time[message.from_user.id] = message.date
				return
			if message.date - self.last_time[message.from_user.id] < self.limit:
				# User is flooding
				delta = self.limit - (message.date - self.last_time[message.from_user.id])
				await self.bot.reply_to(message, f'☺️ Please wait for other messages to be processed. Time left {delta}s')
				return CancelUpdate()	# CancelUpdate if user is flooding
				
			self.last_time[message.from_user.id] = message.date

	async def post_process(self, message, data, exception):
	        pass