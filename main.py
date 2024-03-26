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
    if str(message.from_user.id) not in USERS or USERS[
        str(message.from_user.id)] == '':  # Если это первый старт или пользователь не представился
        await message.answer(
            'Привет, {}. Я бот КНИТУ-КАИ, и я помогу тебе узнать информацию о поступлении в 2024 году.'.format(
                message.from_user.first_name))
        await message.answer("Выбери на клавиатуре, куда ты будешь поступать.",
                             reply_markup=first_qu.as_markup(resize_keyboard=True))
    else:
        # Если это не первый старт
        if USERS[
            str(message.from_user.id)] == 'bachelor':  # приходится проверять, потому что для разных пользователей разные клавиатуры
            await message.answer('Мы уже здоровались! Выбери команду на кнопках ниже.',
                                 reply_markup=forbachelor.as_markup(resize_keyboard=True))
        else:
            await message.answer('Мы уже здоровались! Выбери команду на кнопках ниже.',
                                 reply_markup=universal.as_markup(resize_keyboard=True))


@dp.message(Command("clear"))  # Команда clear, которая позволяет перевыбрать направление
async def clear(message: types.Message):
    USERS[str(message.from_user.id)] = ''
    await message.answer('Теперь ты можешь заново выбрать, куда хочешь поступать, для этого отправь команду /start')


@dp.message(F.text == "📚 На бакалавриат")  # Если написавший пользователь - бакалавр
async def bachelor(message: types.Message):
    USERS[str(message.from_user.id)] = 'bachelor'  # Сохраняем информацию о том, кем себя назвал пользователь.
    with open('users.json', 'w') as fp:
        json.dump(USERS, fp)  # Сохраняем в json
    await message.answer(
        "Приятно познакомиться! Ты сделаешь правильный выбор, если поступишь к нам, ведь в КНИТУ-КАИ более 40 направлений подготовки бакалавриата и образовательных программ специалитета. Поступив к нам, ты не просто получишь престижный диплом об образовании – ты получишь реально востребованную на рынке труда профессию. Выбери на клавиатуре, о чем хочешь узнать подробнее.",
        reply_markup=forbachelor.as_markup(resize_keyboard=True))


for el in ["👩‍🎓 В магистратуру", "📔 На СПО", "🔭 В аспирантуру"]:
    # Пока что упрощенная реакция на каждый выбор
    @dp.message(F.text == el)
    async def schoolkid(message: types.Message):
        USERS[str(message.from_user.id)] = el  # Сохраняем информацию о том, кем себя назвал пользователь.
        with open('users.json', 'w') as fp:
            json.dump(USERS, fp)  # Сохраняем в json
        await message.answer("Приятно познакомиться! Выбери на кнопках интересующий тебя раздел.",
                             reply_markup=universal.as_markup(resize_keyboard=True))

for el in ["👋 О нас", "🌟 Мероприятия"]:
    # Пока что упрощенная реакция на каждый выбор
    @dp.message(F.text == el)
    async def about_us(message: types.Message):
        await message.answer("Бот ещё в разработке, скоро здесь будет информация. Извини.",
                             reply_markup=universal.as_markup(resize_keyboard=True))


@dp.message(F.text == "❓ Задать вопрос")  # Если нажата кнопка для вопроса
async def askme(message: types.Message):
    await message.answer('Чтобы задать вопрос напиши @abit_kai_help_bot, наши модераторы тебе помогут!')


@dp.message(F.text == "👋 Больше о нас")
async def askme(message: types.Message):
    if str(message.from_user.id) in USERS and USERS[str(message.from_user.id)] != '':
        if USERS[str(message.from_user.id)] == 'bachelor':
            await message.answer(
                'В КАИ обучение – это не только лекции и сессии. У нас жизнь кипит и играет: мы поем, танцуем и творим на «Студенческой весне» и театральном фестивале «Икариада», укрепляем тело и дух в классном спорткомплексе с бассейном и тренажеркой, выезжаем на природу в загородный лагерь. А еще у нас есть коворкинги, вайфай, удобные общежития и вкусняшки в столовых.',
                reply_markup=next_back.as_markup(resize_keyboard=True))
    else:
        await message.answer('Кажется, мы незнакомы. Отправь команду /start и представься, пожалуйста.')


@dp.message(F.text == "📋 Направления")
async def directions(message: types.Message):
    if str(message.from_user.id) in USERS and USERS[str(message.from_user.id)] != '':
        if USERS[str(message.from_user.id)] == 'bachelor':
            await message.answer("""Все направления подготовки и специальности разделены по институтам и факультетам, нажми на любое название и попадёшь на наш сайт, где сможешь подробно всё изучить.

<a href="https://abiturientu.kai.ru/iante/obrazovatel-nye-programmy-bakalavriata">✈️ Институт авиации, наземного транспорта и энергетики (ИАНТЭ)</a>
<a href="https://abiturientu.kai.ru/fmf-/-obrazovatel-nye-programmy-bakalavriata">⚛️ Физико-математический факультет (ФМФ)</a>
<a href="https://abiturientu.kai.ru/iaep-/-obrazovatel-nye-programmy-bakalavriata">🎚️ Институт автоматики и электронного приборостроения (ИАЭП)</a>
<a href="https://abiturientu.kai.ru/iktzi-/-obrazovatel-nye-programmy-bakalavriata">🖥 Институт компьютерных технологий и защиты информации (ИКТЗИ)</a>
<a href="https://abiturientu.kai.ru/iret-/-obrazovatel-nye-programmy-bakalavriata">📡 Институт радиоэлектроники, фотоники и цифровых технологий (ИРЭФ-ЦТ)</a>
<a href="https://abiturientu.kai.ru/ieust-/-obrazovatel-nye-programmy-bakalavriata">💰 Институт инженерной экономики и предпринимательства (ИИЭиП)</a>
<a href="https://abiturientu.kai.ru/vspit-/-obrazovatel-nye-programmy-bakalavriata">🚀 Высшая школа прикладных информационных технологий (ВШПИТ)</a>""",
                                 parse_mode="HTML")
    else:
        await message.answer('Кажется, мы незнакомы. Отправь команду /start и представься, пожалуйста.')


@dp.message(F.text == "🌟 Важно ознакомиться")
async def important(message: types.Message):
    if str(message.from_user.id) in USERS and USERS[str(message.from_user.id)] != '':
        if USERS[str(message.from_user.id)] == 'bachelor':
            await message.answer("""В первую очередь зарегистрируйся в личном кабинете абитуриента lk.kai.ru - там ты сможешь подать документы в электронной форме, отследить свой рейтинг и узнать о том, что поступил!
Также можешь ознакомиться с <a href="https://abiturientu.kai.ru/documents/1470594/10919962/Правила+приема+BO.pdf/2f8200d9-c9e8-4672-a0d1-be511bd781ad">правилами приёма</a> и <a href="https://abiturientu.kai.ru/normativnye-dokumenty">нормативными документами</a>.
А на <a href="https://abiturientu.kai.ru/bakalavriat">сайте КАИ</a> ты можешь узнать подробнее о порядке поступления на бакалавриат и специалитет.""", parse_mode="HTML")
    else:
        await message.answer('Кажется, мы незнакомы. Отправь команду /start и представься, пожалуйста.')

@dp.message(F.text == "🔍 Ещё")
async def askme(message: types.Message):
    if str(message.from_user.id) in USERS and USERS[str(message.from_user.id)] != '':
        if USERS[str(message.from_user.id)] == 'bachelor':
            await message.answer(
                '🏆 КНИТУ-КАИ входит в ТОП-50 лучших вузов страны: 👇\nhttps://raex-rr.com/education/russian_universities/top-100_universities/2023/',
                reply_markup=back_menu.as_markup(resize_keyboard=True))
    else:
        await message.answer('Кажется, мы незнакомы. Отправь команду /start и представься, пожалуйста.')


@dp.message(F.text == "❌ Вернуться в меню")  # Если нажата кнопка возврата в меню
async def cancel(message: types.Message):
    if USERS[str(message.from_user.id)] == 'bachelor':
        await message.answer("Хорошо, вернёмся в меню.", reply_markup=forbachelor.as_markup(resize_keyboard=True))
    else:
        await message.answer("Хорошо, вернёмся в меню.",
                             reply_markup=universal.as_markup(resize_keyboard=True))


@dp.message(F.text)  # Обработка любых текстовых сообщений
async def new_text(message: types.Message):
    if str(message.from_user.id) in USERS and USERS[str(message.from_user.id)] != '':
        if USERS[str(message.from_user.id)] == 'bachelor':
            await message.answer('Я не понял, что ты хочешь. Воспользуйся кнопками ниже.',
                                 reply_markup=forbachelor.as_markup(resize_keyboard=True))
    else:
        await message.answer('Я не понял, что ты хочешь. Воспользуйся кнопками ниже.',
                             reply_markup=universal.as_markup(resize_keyboard=True))


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
