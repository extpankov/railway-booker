# Сюда подключаются новые хендлеры

from aiogram import Dispatcher

from .hello import router as hello_router

def include_all_routers(dp: Dispatcher):
    dp.include_router(hello_router)
