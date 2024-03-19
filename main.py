from api import api_token
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
import asyncio
import logging
import json

bot = Bot(token=api_token)  # Классические пункты для работы с aiogram
dp = Dispatcher()
logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="a")
with open('users.json', 'r') as fh:
    USERS = json.load(fh) # Здесь будем хранить id пользователей

@dp.message(Command("start")) # Реакция на команду старт
async def send_welcome(message: types.Message):
    if str(message.from_user.id) not in USERS:  # Если это первый старт
        USERS[str(message.from_user.id)] = []  # Добавляем пользователя
        with open('users.json', 'w') as fp:
            json.dump(USERS, fp)  # Сохраняем в json
        kb = [[types.KeyboardButton(text="📚 Заканчиваю школу")],
              [types.KeyboardButton(text="👩‍🎓 Хочу в магистратуру")],
              [types.KeyboardButton(text="👨‍👩‍👧‍👦 Я родитель")],
              [types.KeyboardButton(text="🙊 Не хочу отвечать")]]  # Создаем кнопки
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
        await message.answer('Привет, {}. Я бот КНИТУ-КАИ, и я помогу тебе узнать информацию о поступлении в 2024 году.'.format(message.from_user.first_name))
        await message.answer("Выбери кто ты на клавиатуре внизу.", reply_markup=keyboard)
    else:
        # Если это не первый старт
        await message.answer('Мы уже здоровались! Выбери команду на кнопках ниже.')

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
