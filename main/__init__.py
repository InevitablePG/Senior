from .database import add_to_database, check_usage, previous_message, remember_message
from telebot.async_telebot import AsyncTeleBot
from .antiflood import RequestAntiflood
from dotenv import load_dotenv
import asyncio, telebot, os
from .senior import Senior


load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
TOKEN = os.getenv('TOKEN')
bot = AsyncTeleBot(TOKEN)


@bot.message_handler(commands=['start'])
async def welcome(message: telebot.types.Message) -> None:
    await add_to_database(message, bot)
    await bot.send_chat_action(message.chat.id, 'typing', timeout=10)
    await bot.send_message(message.chat.id, "💬 Hello, how can I assist you?")


@bot.message_handler(func = lambda message: True, content_types=['text'])
async def openai(message: telebot.types.Message) -> None:
    await add_to_database(message, bot)
    usage = True # await check_usage(message) if message.chat.id != 5166934462 else True
    
    if usage:
        prev = await previous_message(message)
        question = f'I know that as an AI language model, you don\'t have memories of our previous interactions unless I give you a context or reference, so here is the refference, it\'s optional though, \n\n"""{prev}"""\n\n' + message.text
        complete = await Senior(question).create_completion(message, bot)
        
        if complete is not None:
            await bot.send_chat_action(message.chat.id, 'typing')
            answer_user = await bot.send_message(message.chat.id, complete.replace('OpenAI', 'https://github.com/InevitablePG'),
                                    parse_mode='Markdown', disable_web_page_preview=True
            )
            await remember_message(answer_user)
            return
        
        await bot.send_chat_action(message.chat.id, 'typing')
        await bot.send_message(message.chat.id, '💬 Senior is at capacity right now, try again later.', parse_mode='Markdown')
        return
    
    await bot.send_message(message.chat.id, '💬 Senior is just an implementation of ChatGPT API developed by @InevitablePG for demonstration purposes only. If your are interested in implementing the ChatGPT API on your projects or willing to use this bot without any limit you can contact the developer. Thank you for passing by. 👋', parse_mode='Markdown')


bot.setup_middleware(RequestAntiflood(20, bot))