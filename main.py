from api import api_token  # Токен в отдельном файле
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
import asyncio
import logging
import json
from keyboards import *

bot = Bot(token=api_token)  # Классические пункты для работы с aiogram
dp = Dispatcher()
logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="a")
with open('users.json', 'r') as fh:
    USERS = json.load(fh)  # Здесь будем хранить id пользователей


@dp.message(Command("start"))  # Реакция на команду старт
async def send_welcome(message: types.Message):
    if str(message.from_user.id) not in USERS:  # Если это первый старт
        USERS[str(message.from_user.id)] = []  # Добавляем пользователя
        with open('users.json', 'w') as fp:
            json.dump(USERS, fp)  # Сохраняем в json
        await message.answer(
            'Привет, {}. Я бот КНИТУ-КАИ, и я помогу тебе узнать информацию о поступлении в 2024 году.'.format(
                message.from_user.first_name))
        await message.answer("Выбери кто ты на клавиатуре внизу.", reply_markup=first_qu.as_markup())
    else:
        # Если это не первый старт
        await message.answer('Мы уже здоровались! Выбери команду на кнопках ниже.', reply_markup=universal.as_markup())


for el in ["📚 Заканчиваю школу", "👩‍🎓 Хочу в магистратуру", "👨‍👩‍👧‍👦 Я родитель", "🙊 Не хочу отвечать"]:
    # Пока что упрощенная реакция на каждый выбор
    @dp.message(F.text == el)
    async def schoolkid(message: types.Message):
        await message.answer("Приятно познакомиться! Выбери на кнопках интересующий тебя раздел.", reply_markup=universal.as_markup())


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
