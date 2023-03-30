from main import bot
import asyncio


if __name__ == '__main__':
	print('Listening...')
	asyncio.run(bot.polling())