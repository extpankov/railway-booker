from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_sample_keyboard():
    builder = InlineKeyboardBuilder()

    # Добавление кнопок
    builder.button(text="Кнопка 1", callback_data="button1")
    builder.button(text="Кнопка 2", callback_data="button2")
    builder.button(text="Кнопка 3", callback_data="button3")

    # Регулировка расположения кнопок
    builder.adjust(2, 1)  # Первые две кнопки в первой строке, третья во второй

    # Получение готовой клавиатуры
    return builder.as_markup()