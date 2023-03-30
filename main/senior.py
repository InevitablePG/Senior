from telebot.async_telebot import AsyncTeleBot
from dotenv import load_dotenv
from typing import Union
import telebot, asyncio
import openai, os

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
openai.api_key = os.getenv('api_key')


class Senior(object):
	def __init__(self, message: str) -> None:
		self.message = message

	async def create_completion(self, message: telebot.types.Message,
							bot: AsyncTeleBot) -> Union[str, None]:
		try:
			_, complete = await asyncio.gather(
				bot.send_chat_action(message.chat.id, 'typing'),
				openai.ChatCompletion.acreate(
							messages=[{
								"role": "user",
								"content": f"{self.message}"
							}],
							model="gpt-3.5-turbo"
				)
			)
			return complete.choices[0].message.content
			
		except Exception as e:
			print(e)
			return None