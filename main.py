from api import api_token  # Токен в отдельном файле
from keyboards import *  # Клавиатура в отдельном файле
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
import asyncio
import logging
import json

bot = Bot(token=api_token)  # Классические пункты для работы с aiogram
dp = Dispatcher()
logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="a")  # logging
with open('users.json', 'r') as fh:
    USERS = json.load(fh)  # Здесь будем хранить id пользователей
    # {id: [type]}

@dp.message(Command("start"))  # Реакция на команду старт
async def send_welcome(message: types.Message):
    if str(message.from_user.id) not in USERS:  # Если это первый старт
        USERS[str(message.from_user.id)] = ['']  # Добавляем пользователя, [type]
        with open('users.json', 'w') as fp:
            json.dump(USERS, fp)  # Сохраняем в json
        await message.answer(
            'Привет, {}. Я бот КНИТУ-КАИ, и я помогу тебе узнать информацию о поступлении в 2024 году.'.format(
                message.from_user.first_name))
        await message.answer("Выбери кто ты на клавиатуре внизу.",
                             reply_markup=first_qu.as_markup(resize_keyboard=True))
    else:
        # Если это не первый старт
        await message.answer('Мы уже здоровались! Выбери команду на кнопках ниже.',
                             reply_markup=universal.as_markup(resize_keyboard=True))


for el in ["📚 Заканчиваю школу", "👩‍🎓 Хочу в магистратуру", "👨‍👩‍👧‍👦 Я родитель", "🙊 Не хочу отвечать"]:
    # Пока что упрощенная реакция на каждый выбор
    @dp.message(F.text == el)
    async def schoolkid(message: types.Message):
        USERS[str(message.from_user.id)] = [el]  # Сохраняем информацию о том, кем себя назвал пользователь.
        with open('users.json', 'w') as fp:
            json.dump(USERS, fp)  # Сохраняем в json
        await message.answer("Приятно познакомиться! Выбери на кнопках интересующий тебя раздел.",
                             reply_markup=universal.as_markup(resize_keyboard=True))

for el in ["👋 О нас", "📋 Направления", "🌟 Мероприятия"]:
    # Пока что упрощенная реакция на каждый выбор
    @dp.message(F.text == el)
    async def about_us(message: types.Message):
        await message.answer("Бот ещё в разработке, скоро здесь будет информация. Извини.",
                             reply_markup=universal.as_markup(resize_keyboard=True))


@dp.message(F.text == "❓ Задать вопрос")  # Если нажата кнопка для вопроса
async def askme(message: types.Message):
    await message.answer('Чтобы задать вопрос напиши @abit_kai_help_bot, наши модераторы тебе помогут!')


"""@dp.message(F.text == "❌ Вернуться в меню")  # Если нажата кнопка возврата в меню
async def cancel(message: types.Message):
    USERS[str(message.from_user.id)] = [USERS[str(message.from_user.id)][0],
                                        False]  # Опускаем флаг о том, что задан вопрос
    with open('users.json', 'w') as fp:
        json.dump(USERS, fp)  # Сохраняем в json
    await message.answer("Хорошо, вернёмся в меню.",
                         reply_markup=universal.as_markup(resize_keyboard=True))"""


@dp.message(F.text)  # Обработка любых текстовых сообщений
async def new_text(message: types.Message):
    await message.answer('Я не понял, что ты хочешь. Воспользуйся кнопками ниже.',
                         reply_markup=universal.as_markup(resize_keyboard=True))


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
