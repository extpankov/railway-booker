from aiogram import Router, types, F
from aiogram.filters import StateFilter, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.handlers import CallbackQueryHandler
from aiogram.fsm.context import FSMContext

from keyboards.sample import get_sample_keyboard

router = Router()

class TravelInfoStates(StatesGroup):
    waiting_for_date_time = State()
    waiting_for_direction = State()
    waiting_for_train_number = State()
    waiting_for_carriage = State()
    waiting_for_location = State()


@router.message(Command("start"))
async def start_command(message: types.Message, state: FSMContext):
    await message.answer("Пожалуйста, введите дату отправления поезда (например 23.12.2023):")
    await state.set_state(TravelInfoStates.waiting_for_date_time)

@router.message(TravelInfoStates.waiting_for_date_time)
async def process_date_time(message: types.Message, state: FSMContext):
    await state.update_data(date_time=message.text)
    await message.answer("Введите направление поезда, например Москва - Нижний Новгород:")
    await state.set_state(TravelInfoStates.waiting_for_direction)

@router.message(TravelInfoStates.waiting_for_direction)
async def process_direction(message: types.Message, state: FSMContext):
    await state.update_data(direction=message.text)
    await message.answer("Введите номер поезда:")
    await state.set_state(TravelInfoStates.waiting_for_train_number)

@router.message(TravelInfoStates.waiting_for_train_number)
async def process_train_number(message: types.Message, state: FSMContext):
    await state.update_data(train_number=message.text)
    await message.answer("Введите номер вагона:")
    await state.set_state(TravelInfoStates.waiting_for_carriage)

@router.message(TravelInfoStates.waiting_for_carriage)
async def process_carriage(message: types.Message, state: FSMContext):
    await state.update_data(carriage=message.text)
    await message.answer("Введите номера мест (через пробел, если много):")
    await state.set_state(TravelInfoStates.waiting_for_location)

@router.message(TravelInfoStates.waiting_for_location)
async def process_location(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(f"Data received:\n"
                         f"Date and Time: {user_data['date_time']}\n"
                         f"Direction: {user_data['direction']}\n"
                         f"Train Number: {user_data['train_number']}\n"
                         f"Carriage: {user_data['carriage']}\n"
                         f"Location: {user_data['location']}")
    await state.clear()

