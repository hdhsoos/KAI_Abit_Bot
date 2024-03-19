from api import api_token  # Токен в отдельном файле
from ids import *  # На данный момент только id беседы модераторов в отдельном файле
from keyboards import *  # Клавиатура в отдельном файле
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
import asyncio
import logging
import json

bot = Bot(token=api_token)  # Классические пункты для работы с aiogram
dp = Dispatcher()
logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="a")
with open('users.json', 'r') as fh:
    USERS = json.load(fh)  # Здесь будем хранить id пользователей
with open('moderator_flags.json', 'r') as fh:
    MODFLAG = json.load(fh)  # Здесь будем хранить флаги для модераторов


@dp.message(Command("start"))  # Реакция на команду старт
async def send_welcome(message: types.Message):
    if str(message.from_user.id) not in USERS:  # Если это первый старт
        USERS[str(message.from_user.id)] = ['', False]  # Добавляем пользователя, [type, question]
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
        USERS[str(message.from_user.id)] = [el, False]  # Сохраняем информацию о том, кем себя назвал пользователь.
        with open('users.json', 'w') as fp:
            json.dump(USERS, fp)  # Сохраняем в json
        await message.answer("Приятно познакомиться! Выбери на кнопках интересующий тебя раздел.",
                             reply_markup=universal.as_markup())

for el in ["👋 О нас", "📋 Направления", "🌟 Мероприятия"]:
    @dp.message(F.text == el)
    async def about_us(message: types.Message):
        await message.answer("Бот ещё в разработке, скоро здесь будет информация. Извини.",
                             reply_markup=universal.as_markup())


@dp.message(F.text == "❓ Задать вопрос")
async def askme(message: types.Message):
    USERS[str(message.from_user.id)] = [USERS[str(message.from_user.id)][0], True]  # Поднимаем флаг
    with open('users.json', 'w') as fp:
        json.dump(USERS, fp)  # Сохраняем в json
    await message.answer('Напиши свой вопрос. Если передумал, нажми кнопку "❌ Вернуться в меню" ниже.',
                         reply_markup=question.as_markup())


@dp.message(F.text == "❌ Вернуться в меню")
async def cancel(message: types.Message):
    USERS[str(message.from_user.id)] = [USERS[str(message.from_user.id)][0], False]  # Опускаем флаг
    with open('users.json', 'w') as fp:
        json.dump(USERS, fp)  # Сохраняем в json
    await message.answer("Хорошо, вернёмся в меню.",
                         reply_markup=universal.as_markup())


@dp.message(Command("answer"))  # Реакция на команду старт
async def answer(message: types.Message):
    if str(message.from_user.id) in MODFLAG:
        await message.answer("Введите id пользователя. В беседе нужно отвечать на сообщение бота, чтобы он увидел.")
        MODFLAG[str(message.from_user.id)] = [True, False, ""]
        with open('moderator_flags.json', 'w') as fp:
            json.dump(MODFLAG, fp)  # Сохраняем в json


@dp.message(F.text)
async def new_text(message: types.Message):
    if USERS[str(message.from_user.id)][1] is True:
        quest = 'Пользователь @{} написал сообщение: {}'.format(message.from_user.username, message.text)
        how_to_answer = "Чтобы ответить пользователю, отправьте команду /answer и укажите его id {}.".format(
            message.from_user.id)
        await bot.send_message(chat_id=moder_chat_id, text=quest)
        await bot.send_message(chat_id=moder_chat_id, text=how_to_answer)  # Отправляем информацию в чат модераторов
        await message.answer('Спасибо за вопрос, мы ответим вам в ближайшее время.', reply_markup=universal.as_markup())
        USERS[str(message.from_user.id)] = [USERS[str(message.from_user.id)][0], False]  # Опускаем флаг
        with open('users.json', 'w') as fp:
            json.dump(USERS, fp)  # Сохраняем в json
    elif str(message.from_user.id) in MODFLAG:
        if MODFLAG[str(message.from_user.id)][0] is True:  # Если модератор присылает id
            MODFLAG[str(message.from_user.id)] = [False, True, message.text]
            with open('moderator_flags.json', 'w') as fp:
                json.dump(MODFLAG, fp)  # Сохраняем в json
            await message.answer('Теперь напишите ответ. В беседе нужно отвечать на сообщение бота, чтобы он увидел.')
        elif MODFLAG[str(message.from_user.id)][1] is True:
            try:
                answ = 'Вам пришёл ответ на ваш вопрос!\n{}'.format(message.text)
                await bot.send_message(chat_id=MODFLAG[str(message.from_user.id)][2], text=answ)
                MODFLAG[str(message.from_user.id)] = [False, False, '']
                with open('moderator_flags.json', 'w') as fp:
                    json.dump(MODFLAG, fp)  # Сохраняем в json
                await message.answer('Сообщение отправлено.')
            except:
                await message.answer('Произошла ошибка.')


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
