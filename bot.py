import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.types import BotCommand
import os
from dotenv import load_dotenv

from handlers.register import include_all_routers

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

if not API_TOKEN:
    exit("Error: no token provided")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()

dp.include_router(router)
include_all_routers(dp)


# На будущее ->
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать работу"),
        BotCommand(command="/help", description="Получить помощь"),
    ]
    await bot.set_my_commands(commands)


async def main():
    print("Bot started")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())