from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from telebot.async_telebot import AsyncTeleBot
from sqlalchemy import create_engine
import asyncio, telebot

base = declarative_base()

class User(base):
    __tablename__ = 'user'
    
    user_id = Column(Integer, primary_key=True)
    usage = Column(Integer, nullable=False, default=10)
    last_message = Column(String, nullable=False, default="This is our first chat.")

    def __init__(self, user_id: int, usage: int=None) -> None:
        self.user_id = user_id
        self.usage = usage

    def __repr__(self):
        return f'User({self.user_id}, {self.usage})'


engine = create_engine('sqlite:///app.db')
base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
aquire_lock = asyncio.Lock()


async def add_to_database(message: telebot.types.Message, bot: AsyncTeleBot, admin=5166934462) -> None:
    user = session.query(User).filter_by(user_id=message.chat.id).first()
    username = message.from_user.username
    chat_id = message.chat.id
    
    if user is None:
        user = User(message.chat.id)
        async with aquire_lock:
            session.add(user)
            session.commit()
            
        await bot.send_message(
                chat_id=admin, parse_mode='Markdown',
                text = f'*New User*\n\n{chat_id}\n@{username}'
        )
        return


async def check_usage(message: telebot.types.Message) -> bool:
    user = session.query(User).filter_by(user_id=message.chat.id).first()
    limit = 0
    if user.usage > limit:
        user.usage -= 1
        async with aquire_lock:
            session.add(user)
            session.commit()
        return True
        
    return False
    

async def previous_message(message: telebot.types.Message) -> str:
    previous = session.query(User).filter_by(user_id=message.chat.id).first()
    if previous:
        return previous.last_message


async def remember_message(message: telebot.types.Message) -> None:
    previous = session.query(User).filter_by(user_id=message.chat.id).first()
    if previous:
        previous.last_message = message.text
        async with aquire_lock:
            session.add(previous)
            session.commit()
        return