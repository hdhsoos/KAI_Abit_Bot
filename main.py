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
        elif USERS[str(message.from_user.id)] == 'magistracy':
            await message.answer('Мы уже здоровались! Выбери команду на кнопках ниже.',
                                 reply_markup=formagistracy.as_markup(resize_keyboard=True))
        elif USERS[str(message.from_user.id)] == 'spo':
            await message.answer('Мы уже здоровались! Выбери команду на кнопках ниже.',
                                 reply_markup=forspo.as_markup(resize_keyboard=True))
        elif USERS[str(message.from_user.id)] == 'grad':
            await message.answer('Мы уже здоровались! Выбери команду на кнопках ниже.',
                                 reply_markup=forgrad.as_markup(resize_keyboard=True))


@dp.message(Command("clear"))  # Команда clear, которая позволяет перевыбрать направление
async def clear(message: types.Message):
    USERS[str(message.from_user.id)] = ''
    with open('users.json', 'w') as fp:
        json.dump(USERS, fp)  # Сохраняем в json
    await message.answer('Теперь ты можешь заново выбрать, куда хочешь поступать, для этого отправь команду /start',
                         reply_markup=types.ReplyKeyboardRemove())


@dp.message(F.text == "📚 На бакалавриат")  # Если написавший пользователь - бакалавр
async def bachelor(message: types.Message):
    USERS[str(message.from_user.id)] = 'bachelor'  # Сохраняем информацию о том, кем себя назвал пользователь.
    with open('users.json', 'w') as fp:
        json.dump(USERS, fp)  # Сохраняем в json
    await message.answer(
        "Приятно познакомиться! Ты сделаешь правильный выбор, если поступишь к нам, ведь в КНИТУ-КАИ более 40 направлений подготовки бакалавриата и образовательных программ специалитета. Поступив к нам, ты не просто получишь престижный диплом об образовании – ты получишь реально востребованную на рынке труда профессию. Выбери на клавиатуре, о чем хочешь узнать подробнее.",
        reply_markup=forbachelor.as_markup(resize_keyboard=True))


@dp.message(F.text == "👩‍🎓 В магистратуру")  # Если написавший пользователь - магистрант
async def magistracy(message: types.Message):
    USERS[str(message.from_user.id)] = 'magistracy'  # Сохраняем информацию о том, кем себя назвал пользователь.
    with open('users.json', 'w') as fp:
        json.dump(USERS, fp)  # Сохраняем в json
    await message.answer(
        "Приятно познакомиться! Выбери на клавиатуре, о чем хочешь узнать подробнее.",
        reply_markup=formagistracy.as_markup(resize_keyboard=True))


@dp.message(F.text == "📔 На СПО")  # Если написавший пользователь поступает на спо
async def spo(message: types.Message):
    USERS[str(message.from_user.id)] = 'spo'  # Сохраняем информацию о том, кем себя назвал пользователь.
    with open('users.json', 'w') as fp:
        json.dump(USERS, fp)  # Сохраняем в json
    await message.answer(
        "Приятно познакомиться! Выбери на клавиатуре, о чем хочешь узнать подробнее.",
        reply_markup=forspo.as_markup(resize_keyboard=True))


@dp.message(F.text == "🔭 В аспирантуру")
async def grad(message: types.Message):
    USERS[str(message.from_user.id)] = 'grad'  # Сохраняем информацию о том, кем себя назвал пользователь.
    with open('users.json', 'w') as fp:
        json.dump(USERS, fp)  # Сохраняем в json
    await message.answer("Приятно познакомиться! Выбери на кнопках интересующий тебя раздел.",
                         reply_markup=forgrad.as_markup(resize_keyboard=True))


@dp.message(F.text == "❓ Задать вопрос")  # Если нажата кнопка для вопроса
async def askme(message: types.Message):
    await message.answer('Чтобы задать вопрос напиши @abit_kai_help_bot, наши модераторы тебе помогут!')


@dp.message(F.text == "👋 О нас")
async def askme(message: types.Message):
    if str(message.from_user.id) in USERS and USERS[str(message.from_user.id)] != '':
        if USERS[str(message.from_user.id)] == 'bachelor':
            await message.answer(
                'В КАИ обучение – это не только лекции и сессии. У нас жизнь кипит и играет: мы поем, танцуем и творим на «Студенческой весне» и театральном фестивале «Икариада», укрепляем тело и дух в классном спорткомплексе с бассейном и тренажеркой, выезжаем на природу в загородный лагерь. А еще у нас есть коворкинги, вайфай, удобные общежития и вкусняшки в столовых.',
                reply_markup=next_back.as_markup(resize_keyboard=True))
        elif USERS[str(message.from_user.id)] == 'spo':
            await message.answer("""В КНИТУ-КАИ два отделения среднего профессионального образования. 
Колледж информационных технологий и технический колледж. Выбери на клавиатуре, о каком колледже хочешь узнать подробнее.""",
                                 reply_markup=spo_about.as_markup(resize_keyboard=True))
    else:
        await message.answer('Кажется, мы незнакомы. Отправь команду /start и представься, пожалуйста.')


@dp.message(F.text == "📃 Необходимые документы")
async def docs(message: types.Message):
    if str(message.from_user.id) in USERS and USERS[str(message.from_user.id)] != '':
        if USERS[str(message.from_user.id)] == 'bachelor':
            await message.answer("""При подаче заявления о приеме поступающий предоставляет/прикрепляет:

🔹Документ, удостоверяющий личность, гражданство (для иностранных граждан нотариально заверенный перевод);
🔹Документ государственного образца об образовании (для иностранных граждан нотариально заверенный перевод);
🔹Документы, подтверждающие особые права абитуриента при поступлении в высшие учебные  заведения, установленные законодательством Российской Федерации (при наличии);
🔹Документы, подтверждающие индивидуальные достижения абитуриентов в соответствии с <a href="https://abiturientu.kai.ru/documents/1470594/10922774/Порядок+учета+результатов+ИД+поступающих.pdf/607793cf-f308-4169-9b70-ef9c2f32f3b8">положением</a> (при наличии);
🔹Страховое свидетельство обязательного пенсионного страхования (при наличии);
🔹<a href="https://abiturientu.kai.ru/documents/10181/9641606/doverennost.docx/df8f7652-9c55-4f79-96fe-fdec143f000c">Доверенность</a> (в случае подаче документов доверенным лицом).""",
                                 parse_mode="HTML", disable_web_page_preview=True)
        elif USERS[str(message.from_user.id)] == 'magistracy':
            await message.answer("""При подаче заявления о приеме поступающий предоставляет/прикрепляет:

🔹Копию или скан-копию документа, удостоверяющего его личность, гражданство.
🔹Оригинал, копию или скан-копию документа государственного образца об образовании.
🔹Копию или скан-копию страхового свидетельства обязательного пенсионного страхования (при наличии).

Также требуется подать заявления в электронном виде. Это нужно сделать в личном кабинете абитуриента - lk.kai.ru""")
        elif USERS[str(message.from_user.id)] == 'spo':
            await message.answer("""При подаче заявления о приеме поступающий предоставляет/прикрепляет:

🔹Копию или скан-копию документа, удостоверяющего его личность, гражданство.
🔹Оригинал, копию или скан-копию документа государственного образца об образовании.
🔹Копию или скан-копию страхового свидетельства обязательного пенсионного страхования (при наличии).

Также требуется подать заявления в электронном виде. Это нужно сделать в личном кабинете абитуриента - lk.kai.ru""")
    else:
        await message.answer('Кажется, мы незнакомы. Отправь команду /start и представься, пожалуйста.')


@dp.message(F.text == "📋 Направления")
async def directions(message: types.Message):
    if str(message.from_user.id) in USERS and USERS[str(message.from_user.id)] != '':
        if USERS[str(message.from_user.id)] == 'bachelor':
            await message.answer("""Все направления подготовки и специальности разделены по институтам и факультетам, нажми на любое название и попадёшь на наш сайт, где сможешь подробно всё изучить.

<a href="https://abiturientu.kai.ru/iante/obrazovatel-nye-programmy-bakalavriata">✈️ Институт авиации, наземного транспорта и энергетики (ИАНТЭ)</a>
<a href="https://abiturientu.kai.ru/fmf-/-obrazovatel-nye-programmy-bakalavriata">⚛️ Физико-математический факультет (ФМФ)</a>
<a href="https://abiturientu.kai.ru/iaep-/-obrazovatel-nye-programmy-bakalavriata">🎛️️ Институт автоматики и электронного приборостроения (ИАЭП)</a>
<a href="https://abiturientu.kai.ru/iktzi-/-obrazovatel-nye-programmy-bakalavriata">🖥 Институт компьютерных технологий и защиты информации (ИКТЗИ)</a>
<a href="https://abiturientu.kai.ru/iret-/-obrazovatel-nye-programmy-bakalavriata">📡 Институт радиоэлектроники, фотоники и цифровых технологий (ИРЭФ-ЦТ)</a>
<a href="https://abiturientu.kai.ru/ieust-/-obrazovatel-nye-programmy-bakalavriata">💰 Институт инженерной экономики и предпринимательства (ИИЭиП)</a>
<a href="https://abiturientu.kai.ru/vspit-/-obrazovatel-nye-programmy-bakalavriata">🚀 Высшая школа прикладных информационных технологий (ВШПИТ)</a>

Также ты можешь выбрать направление подготовки <a href="https://abiturientu.kai.ru/obrazovatel-nye-programmy?ed=1">по этой ссылке</a> с помощью фильтров.

Проходные баллы за 2023 год можно найти <a href="https://abiturientu.kai.ru/documents/1470594/10927743/Результаты+конкурсного+приема+2023.pdf/1015e6e2-f98e-4f84-88eb-57b99c258d07">здесь</a>.""",
                                 parse_mode="HTML", disable_web_page_preview=True)
        elif USERS[str(message.from_user.id)] == 'magistracy':
            await message.answer("""<a href="https://abiturientu.kai.ru/obrazovatel-nye-programmy?ed=2">По этой ссылке</a> ты можешь выбрать образовательную программу, используя фильтры. Также предлагаю ознакомиться с планом приёма (количество мест):
🔸<a href="https://abiturientu.kai.ru/documents/1470594/12192680/ПЛАН+ПРИЁМА+маг+бюджет+2024.pdf/e99089c6-51e2-421b-a2f7-b1f1ce37edd6">На бюджетное обучение</a>
🔸<a href="https://abiturientu.kai.ru/documents/1470594/12192680/ПЛАН+ПРИЁМА+маг+договор+2024.pdf/63161d0b-5466-4c28-a1ba-4718ba791dcb">С оплатой стоимости</a>
🔸<a href="https://abiturientu.kai.ru/documents/1470594/12192680/ПЛАН+ПРИЁМА+цно+маг+договор+2024.pdf/2e4a2f9f-36e1-4a48-8d7d-fa521e340375">С оплатой стоимости, заочное обучение</a>

Проходные баллы за 2023 год можно найти <a href="https://abiturientu.kai.ru/documents/1470594/10927743/Результаты+конкурсного+приема+2023.pdf/1015e6e2-f98e-4f84-88eb-57b99c258d07">здесь</a>.""",
                                 parse_mode="HTML", disable_web_page_preview=True)
        elif USERS[str(message.from_user.id)] == 'spo':
            await message.answer("""<a href="https://abiturientu.kai.ru/obrazovatel-nye-programmy?ed=3">По этой ссылке</a> ты можешь выбрать образовательную программу, используя фильтры.
            
Также можешь ознакомиться с правилами приёма (количеством мест):
▪️ <a href="https://abiturientu.kai.ru/documents/1470594/12196147/ПЛАН+ПРИЕМА+СПО+бюджет.pdf/d7545213-5190-4cb1-b667-344f4772af4a">На бюджетное обучение</a>
▪️ <a href="https://abiturientu.kai.ru/documents/1470594/12196147/ПЛАН+ПРИЕМА+СПО+договор.pdf/7ea9acca-8072-4150-b19c-664f52a050b2">С оплатой стоимости</a>

Проходные баллы за 2023 год можно найти <a href="https://abiturientu.kai.ru/documents/1470594/10927743/Результаты+конкурсного+приема+2023.pdf/1015e6e2-f98e-4f84-88eb-57b99c258d07">здесь</a>.""",
                                 parse_mode="HTML", disable_web_page_preview=True)
        elif USERS[str(message.from_user.id)] == 'grad':
            await message.answer("""""", parse_mode="HTML", disable_web_page_preview=True)
    else:
        await message.answer('Кажется, мы незнакомы. Отправь команду /start и представься, пожалуйста.')


@dp.message(F.text == "🌟 Важно ознакомиться")
async def important(message: types.Message):
    if str(message.from_user.id) in USERS and USERS[str(message.from_user.id)] != '':
        if USERS[str(message.from_user.id)] == 'bachelor':
            await message.answer("""В первую очередь зарегистрируйся в личном кабинете абитуриента lk.kai.ru - там ты сможешь подать документы в электронной форме, отследить свой рейтинг и узнать о том, что поступил!
Также можешь ознакомиться с <a href="https://abiturientu.kai.ru/documents/1470594/10919962/Правила+приема+BO.pdf/2f8200d9-c9e8-4672-a0d1-be511bd781ad">правилами приёма</a> и <a href="https://abiturientu.kai.ru/normativnye-dokumenty">нормативными документами</a>.
А на <a href="https://abiturientu.kai.ru/bakalavriat">сайте КАИ</a> ты можешь узнать подробнее о порядке поступления на бакалавриат и специалитет.""",
                                 parse_mode="HTML", disable_web_page_preview=True)
    else:
        await message.answer('Кажется, мы незнакомы. Отправь команду /start и представься, пожалуйста.')


@dp.message(F.text == "Колледж Информационных Технологий")
async def kit(message: types.Message):
    await message.answer("""Благодаря обучению на СПО ИКТЗИ КИТ ты получишь возможность получения перспективной специальности и диплома государственного образца через 3-4 года, сможешь сразу опробовать себя в конкретной специальности, опережая сверстников.
Также ты получишь отсрочку от армии на весь срок обучения. После обучения ты можешь поступить в университет на ускоренные программы по схожей специальности. 
Организация учебного процесса базируется на инновационных образовательных технологиях, электронных учебниках, все аудитории оснащены электронной доской и подключены к внутренней компьютерной сети.

<a href="https://kai.ru/web/kolledz-informacionnyh-tehnologij/">По ссылке ты можешь ознакомиться с сайтом колледжа</a>""", reply_markup=forspo.as_markup(resize_keyboard=True), parse_mode="HTML",
                         disable_web_page_preview=True)


@dp.message(F.text == "Технический колледж")
async def tk(message: types.Message):
    await message.answer("""Наше отделение - современное, динамично развивающееся образовательное подразделение КНИТУ-КАИ.
Технический колледж готовит высококвалифицированных, ответственных, инициативных специалистов и руководителей среднего звена, способных обеспечить безопасное, надежное и эффективное функционирование процессов, руководителями или исполнителями которых они станут по окончанию колледжа.

<a href="https://kai.ru/web/tehniceskij-kolledz">По ссылке ты можешь ознакомиться с сайтом колледжа</a>""",
                         reply_markup=forspo.as_markup(resize_keyboard=True), parse_mode="HTML",
                         disable_web_page_preview=True)


@dp.message(F.text == "✍️ Вступительные испытания")
async def exams(message: types.Message):
    if str(message.from_user.id) in USERS and USERS[str(message.from_user.id)] != '':
        if USERS[str(message.from_user.id)] == 'magistracy':
            await message.answer("""С программами вступительных испытаний по каждому направлению можно ознакомиться <a href="https://abiturientu.kai.ru/programmy-vstupitel-nyh-ispytanij1">здесь</a>.

Расписание вступительных испытаний на 2024 год появится позже.""", parse_mode="HTML", disable_web_page_preview=True)
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
    elif USERS[str(message.from_user.id)] == 'magistracy':
        await message.answer("Хорошо, вернёмся в меню.", reply_markup=formagistracy.as_markup(resize_keyboard=True))
    elif USERS[str(message.from_user.id)] == 'spo':
        await message.answer("Хорошо, вернёмся в меню.", reply_markup=forspo.as_markup(resize_keyboard=True))
    elif USERS[str(message.from_user.id)] == 'grad':
        await message.answer("Хорошо, вернёмся в меню.", reply_markup=forgrad.as_markup(resize_keyboard=True))
    else:
        await message.answer('Кажется, мы незнакомы. Отправь команду /start и представься, пожалуйста.')


@dp.message(F.text)  # Обработка любых текстовых сообщений
async def new_text(message: types.Message):
    if str(message.from_user.id) in USERS and USERS[str(message.from_user.id)] != '':
        if USERS[str(message.from_user.id)] == 'bachelor':
            await message.answer('Я не понял, что ты хочешь. Воспользуйся кнопками ниже.',
                                 reply_markup=forbachelor.as_markup(resize_keyboard=True))
        elif USERS[str(message.from_user.id)] == 'magistracy':
            await message.answer('Я не понял, что ты хочешь. Воспользуйся кнопками ниже.',
                                 reply_markup=formagistracy.as_markup(resize_keyboard=True))
        elif USERS[str(message.from_user.id)] == 'spo':
            await message.answer('Я не понял, что ты хочешь. Воспользуйся кнопками ниже.',
                                 reply_markup=forspo.as_markup(resize_keyboard=True))
        elif USERS[str(message.from_user.id)] == 'grad':
            await message.answer('Я не понял, что ты хочешь. Воспользуйся кнопками ниже.',
                                 reply_markup=forgrad.as_markup(resize_keyboard=True))
    else:
        await message.answer('Кажется, мы незнакомы. Отправь команду /start и представься, пожалуйста.')


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
