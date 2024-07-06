# -*- coding: utf-8 -*-

from api import api_token  # Токен в отдельном файле
from keyboards import *  # Клавиатуры в отдельном файле
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
import aioschedule
import asyncio
import json
from datetime import date
from functions import *
from recs import *

bot = Bot(token=api_token)  # Классические пункты для работы с aiogram
dp = Dispatcher()
with open('users.json', 'r') as fh:
    USERS = json.load(fh)  # Здесь будем хранить id пользователей
    # {id: [type, [directions]]]}
with open('score.json', 'r') as fh:  # Здесь будем хранить баллы
    SCORES = json.load(fh)
    # {id: [0, 0, 0, 0, 0, 0, 0, 0]}
    # Математика, Русский, Информатика, Физика, Химия, Обществознание, Иностранный, Доп
with open('FLAG.json', 'r') as fh:  # Здесь будем хранить флаги
    FLAG = json.load(fh)
    # {id: [True]) задан ли вопрос
admins = ['397472187', '537266469']

basic_answer_unknown = 'Кажется, мы незнакомы. Отправь команду /start и представься, пожалуйста.'

@dp.message(Command("adm_change"))  # Реакция на команду старт
async def adm_change(message: types.Message):
    global forbachelor
    if str(message.from_user.id) in admins:
        file = open('flag.txt', 'r')
        x = file.read()
        file.close()
        file = open('flag.txt', 'w')
        if x == 'false':
            file.write('true')
            file.close()
        else:
            file.write('false')
            file.close()
        forbachelor = ReplyKeyboardBuilder()  # Клавиатура для бакалавров
        if x == 'false':
            A = ["👋 О нас", "📋 Направления", "🌟 Важно ознакомиться", "📃 Подача заявления", "👤 Личный кабинет",
                 "🔍 Рекомендации", "❓ Задать вопрос", "✖️ Изменить выбор"]
        else:
            A = ["👋 О нас", "📋 Направления", "🌟 Важно ознакомиться", "📃 Подача заявления", "👤 Личный кабинет",
                 "❓ Задать вопрос", "✖️ Изменить выбор"]
        for el in A:
            forbachelor.add(types.KeyboardButton(text=el))
        forbachelor.adjust(2)
        await message.answer('Изменения применены.',
                             reply_markup=forbachelor.as_markup(resize_keyboard=True))
    else:
        await message.answer('Эта функция для вас недоступна.',
                             reply_markup=forbachelor.as_markup(resize_keyboard=True))


@dp.message(Command("start"))  # Реакция на команду старт
async def send_welcome(message: types.Message):
    global USERS, COUNTER
    logging_date(str(message.from_user.id))
    if str(message.from_user.id) not in USERS:
        save_log('Новый пользователь {}'.format(str(message.from_user.id)))
    if str(message.from_user.id) not in USERS or USERS[
        str(message.from_user.id)][0] == '':  # Если это первый старт или пользователь не представился
        USERS[str(message.from_user.id)][0] = ['', '']
        with open('users.json', 'w') as fp:
            json.dump(USERS, fp)
        FLAG[str(message.from_user.id)] = [False]
        with open('FLAG.json', 'w') as fp:
            json.dump(FLAG, fp)
        await message.answer(
            'Привет, {}. Я бот КНИТУ-КАИ, и я помогу тебе узнать информацию о поступлении в 2024 году.'.format(
                message.from_user.first_name))
        await message.answer("Выбери на клавиатуре, куда ты будешь поступать.",
                             reply_markup=first_qu.as_markup(resize_keyboard=True))
    else:
        # Если это не первый старт
        if USERS[
            str(message.from_user.id)][
            0] == 'bachelor':  # приходится проверять, потому что для разных пользователей разные клавиатуры
            await message.answer('Мы уже здоровались! Выбери команду на кнопках ниже.',
                                 reply_markup=forbachelor.as_markup(resize_keyboard=True))
        elif USERS[str(message.from_user.id)][0] == 'magistracy':
            await message.answer('Мы уже здоровались! Выбери команду на кнопках ниже.',
                                 reply_markup=formagistracy.as_markup(resize_keyboard=True))
        elif USERS[str(message.from_user.id)][0] == 'spo':
            await message.answer('Мы уже здоровались! Выбери команду на кнопках ниже.',
                                 reply_markup=forspo.as_markup(resize_keyboard=True))
        elif USERS[str(message.from_user.id)][0] == 'grad':
            await message.answer('Мы уже здоровались! Выбери команду на кнопках ниже.',
                                 reply_markup=forgrad.as_markup(resize_keyboard=True))


@dp.message(Command("stats"))  # Реакция на команду stats
async def stats(message: types.Message):
    if str(message.from_user.id) in admins:
        count_b, count_m, count_s, count_today = 0, 0, 0, 0
        a = str(date.today())
        for el in USERS:
            if USERS[el][0] == 'bachelor':
                count_b += 1
            elif USERS[el][0] == 'magistracy':
                count_m += 1
            elif USERS[el][0] == 'spo':
                count_s += 1
        with open('stats.json', 'r') as fh:
            STATS = json.load(fh)
        for el in STATS:
            if STATS[el] == a:
                count_today += 1
        await message.answer("""Всего пользователей: {}
    Бакалавриат: {}
    Магистратура: {}
    СПО: {}""".format(len(USERS), count_b, count_m, count_s))
        await message.answer("""Пользователей заходило сегодня: {}""".format(count_today))
    else:
        await message.answer('Эта функция для вас недоступна.',
                             reply_markup=forbachelor.as_markup(resize_keyboard=True))

@dp.message(F.text == "✖️ Изменить выбор")  # Команда clear, которая позволяет перевыбрать направление
async def clear(message: types.Message):
    logging_date(str(message.from_user.id))
    USERS[str(message.from_user.id)][0] = ''
    with open('users.json', 'w') as fp:
        json.dump(USERS, fp)  # Сохраняем в json
    await message.answer('Теперь ты можешь заново выбрать уровень образования.',
                         reply_markup=first_qu.as_markup(resize_keyboard=True))


@dp.message(F.text == "🔍 Рекомендации")
async def recs_main(message: types.Message):
    file = open('flag.txt', 'r')
    x = file.read()
    file.close()
    if x == 'true':
        logging_date(str(message.from_user.id))
        max_score = get_scores(str(message.from_user.id), SCORES)
        doc = USERS[str(message.from_user.id)][1]
        if doc == [] or max_score == 'notin' or max_score == 'nosum':
            await message.answer(
                'Чтобы получить рекомендации по направлениям, введи баллы и направления в личном кабинете.',
                reply_markup=forbachelor.as_markup(resize_keyboard=True))
        else:
            spec = USERS[str(message.from_user.id)][1]
            counter_recs = 0
            res = 'Предлагаем вам данные направления в качестве альтернативы тех, на которые ваши шансы поступить невысоки. Проходные баллы указаны ориентировочно.\n\n'
            PR_BL = read_pr_bl()  # временно. потом надо перенести чтобы раз в неск часов
            for el in spec:
                y = PR_BL[el]
                res += el + ' ({}) \n'.format(y)
                if y > max_score:
                    j = 0
                    for pr in RECS[el]:
                        if j <= 4:
                            x = PR_BL[pr]
                            if x <= max_score:
                                res += '- {} ({})\n'.format(pr, x)
                                j += 1
                        else:
                            break
                    if j == 0:
                        res += 'Ничего не могу подсказать.\n'  # надо подсказывать куда берут
                    res += '\n'
                else:
                    counter_recs += 1
                    res += 'Ваших баллов достаточно.\n\n'
            if counter_recs == len(spec):
                res = 'Вы проходите на все желаемые направления!'
            await message.answer(res, reply_markup=forbachelor.as_markup(resize_keyboard=True))
    else:
        await message.answer('Эта функция на данный момент недоступна.',
                             reply_markup=forbachelor.as_markup(resize_keyboard=True))


@dp.message(F.text == "📚 На бакалавриат")  # Если написавший пользователь - бакалавр
async def bachelor(message: types.Message):
    USERS[str(message.from_user.id)][0] = 'bachelor'  # Сохраняем информацию о том, кем себя назвал пользователь.
    if str(message.from_user.id) not in SCORES:  # Чтобы при смене выбора баллы ЕГЭ не удалялись
        SCORES[str(message.from_user.id)] = [0, 0, 0, 0, 0, 0, 0, 0]  # Здесь будем хранить данные о пользователе позже
    with open('users.json', 'w') as fp:
        json.dump(USERS, fp)  # Сохраняем в json
    with open('score.json', 'w') as fp:
        json.dump(SCORES, fp)  # Сохраняем в json
    await message.answer(
        "Приятно познакомиться! Ты сделаешь правильный выбор, если поступишь к нам, ведь в КНИТУ-КАИ более 40 направлений подготовки бакалавриата и образовательных программ специалитета. Поступив к нам, ты не просто получишь престижный диплом об образовании – ты получишь реально востребованную на рынке труда профессию. Выбери на клавиатуре, о чем хочешь узнать подробнее.",
        reply_markup=forbachelor.as_markup(resize_keyboard=True))


@dp.message(F.text == "👩‍🎓 В магистратуру")  # Если написавший пользователь - магистрант
async def magistracy(message: types.Message):
    USERS[str(message.from_user.id)][0] = 'magistracy'  # Сохраняем информацию о том, кем себя назвал пользователь.
    with open('users.json', 'w') as fp:
        json.dump(USERS, fp)  # Сохраняем в json
    await message.answer(
        "Приятно познакомиться! Выбери на клавиатуре, о чем хочешь узнать подробнее.",
        reply_markup=formagistracy.as_markup(resize_keyboard=True))


@dp.message(F.text == "📔 На СПО")  # Если написавший пользователь поступает на спо
async def spo(message: types.Message):
    USERS[str(message.from_user.id)][0] = 'spo'  # Сохраняем информацию о том, кем себя назвал пользователь.
    with open('users.json', 'w') as fp:
        json.dump(USERS, fp)  # Сохраняем в json
    await message.answer(
        "Приятно познакомиться! Выбери на клавиатуре, о чем хочешь узнать подробнее.",
        reply_markup=forspo.as_markup(resize_keyboard=True))


@dp.message(F.text == "🔭 В аспирантуру")
async def grad(message: types.Message):
    logging_date(str(message.from_user.id))
    USERS[str(message.from_user.id)][0] = 'grad'  # Сохраняем информацию о том, кем себя назвал пользователь.
    with open('users.json', 'w') as fp:
        json.dump(USERS, fp)  # Сохраняем в json
    await message.answer("Приятно познакомиться! Выбери на кнопках интересующий тебя раздел.",
                         reply_markup=forgrad.as_markup(resize_keyboard=True))


@dp.message(F.text == "❓ Задать вопрос")  # Если нажата кнопка для вопроса
async def askme(message: types.Message):
    logging_date(str(message.from_user.id))
    await message.answer('💫 <a href="t.me/pk_kai24">Чтобы задать вопрос, напиши в наш чат!</a> 💫', parse_mode="HTML",
                         disable_web_page_preview=True)


@dp.message(F.text == "👤 Личный кабинет")
async def profile(message: types.Message):
    global SCORES
    logging_date(str(message.from_user.id))
    if str(message.from_user.id) not in SCORES or sum(SCORES[str(message.from_user.id)]) == 0:
        SCORES[str(message.from_user.id)] = [0, 0, 0, 0, 0, 0, 0, 0]
        with open('score.json', 'w') as fp:
            json.dump(SCORES, fp)  # Сохраняем в json
        await message.answer("""
Ты ещё не вводил(а) свои баллы ЕГЭ. Выбери предмет на кнопках выше и введи баллы, я запомню их.\nТакже можешь ввести свои направления по ОБЩЕМУ КОНКУРСУ, чтобы потом я сам отслеживал поступаешь ли ты туда, куда хочешь.""",
                             reply_markup=subj_keyb)
    else:
        A = ['Математика', 'Русский язык', 'Информатика', 'Физика', 'Химия', 'Обществознание', 'Иностранный язык',
             'Дополнительные баллы']
        res = ''
        end = ''
        s = SCORES[str(message.from_user.id)][-1]  # Сумма математика + русский + достижения
        usl = True  # Останется тру если русский и математика есть
        usl2 = False
        if s > 0:
            usl2 = True
        for i in range(8):
            x = SCORES[str(message.from_user.id)][i]
            if x != 0:
                res += '{}: {}\n'.format(A[i], x)
                if i < 2:
                    s += x
                elif 2 <= i < 7 and usl:
                    if usl2:
                        end += 'Математика + Русский + {} + Достижения = {}\n'.format(A[i], s + x)
                    else:
                        end += 'Математика + Русский + {} = {}\n'.format(A[i], s + x)
            else:
                if i < 2:
                    usl = False
        if end == '':
            end = 'Общая сумма: {}'.format(sum(SCORES[str(message.from_user.id)]))
        if USERS[str(message.from_user.id)][1] != []:
            end += '\nТвои направления: <code>{}</code>\n'.format(' '.join(USERS[str(message.from_user.id)][1]))
        await message.answer(
            """{}
{}
Нажми на кнопки ниже, если хочешь добавить или изменить баллы, ввести новые направления. Чтобы удалить баллы по какому-то предмету, выбери его и отправь 0.""".format(
                res, end), reply_markup=subj_keyb, parse_mode='HTML')


@dp.message(F.text == "👋 О нас")
async def askme(message: types.Message):
    logging_date(str(message.from_user.id))
    if str(message.from_user.id) in USERS and USERS[str(message.from_user.id)][0] != '':
        if USERS[str(message.from_user.id)][0] == 'bachelor':
            await message.answer(
                'В КАИ обучение – это не только лекции и сессии. У нас жизнь кипит и играет: мы поем, танцуем и творим на «Студенческой весне» и театральном фестивале «Икариада», укрепляем тело и дух в классном спорткомплексе с бассейном и тренажеркой, выезжаем на природу в загородный лагерь. А еще у нас есть коворкинги, вайфай, удобные общежития и вкусняшки в столовых.',
                reply_markup=next_back.as_markup(resize_keyboard=True))
        elif USERS[str(message.from_user.id)][0] == 'spo':
            await message.answer("""В КНИТУ-КАИ два отделения среднего профессионального образования. 
Колледж информационных технологий и технический колледж. Выбери на клавиатуре, о каком колледже хочешь узнать подробнее.""",
                                 reply_markup=spo_about.as_markup(resize_keyboard=True))
    else:
        await message.answer(basic_answer_unknown)


@dp.message(F.text == "📃 Подача заявления")
async def docs(message: types.Message):
    logging_date(str(message.from_user.id))
    if str(message.from_user.id) in USERS and USERS[str(message.from_user.id)][0] != '':
        if USERS[str(message.from_user.id)][0] == 'bachelor':
            await message.answer("""Подать заявление можно на госуслугах, <a href="lk.kai.ru">в личном кабинете на сайте каи</a>, а также лично в университете.
При подаче заявления о приеме поступающий предоставляет/прикрепляет:

🔹Документ, удостоверяющий личность, гражданство (для иностранных граждан нотариально заверенный перевод);
🔹Документ государственного образца об образовании (для иностранных граждан нотариально заверенный перевод);
🔹Документы, подтверждающие особые права абитуриента при поступлении в высшие учебные  заведения, установленные законодательством Российской Федерации (при наличии);
🔹Документы, подтверждающие индивидуальные достижения абитуриентов в соответствии с <a href="https://abiturientu.kai.ru/documents/1470594/10922774/Порядок+учета+результатов+ИД+поступающих.pdf/607793cf-f308-4169-9b70-ef9c2f32f3b8">положением</a> (при наличии);
🔹Страховое свидетельство обязательного пенсионного страхования (при наличии);
🔹<a href="https://abiturientu.kai.ru/documents/10181/9641606/doverennost.docx/df8f7652-9c55-4f79-96fe-fdec143f000c">Доверенность</a> (в случае подаче документов доверенным лицом).

Календарь приёма можно <a href="https://abiturientu.kai.ru/kalendar-priema">посмотреть тут</a>.""",
                                 parse_mode="HTML", disable_web_page_preview=True)
        elif USERS[str(message.from_user.id)][0] == 'magistracy':
            await message.answer("""При подаче заявления о приеме поступающий предоставляет/прикрепляет:

🔹Копию или скан-копию документа, удостоверяющего его личность, гражданство.
🔹Оригинал, копию или скан-копию документа государственного образца об образовании.
🔹Копию или скан-копию страхового свидетельства обязательного пенсионного страхования (при наличии).

Также требуется подать заявления в электронном виде. Это нужно сделать в личном кабинете абитуриента - lk.kai.ru\

Календарь приёма можно <a href="https://abiturientu.kai.ru/kalendar-priema">посмотреть тут</a>.""",
                                 parse_mode="HTML", disable_web_page_preview=True)
        elif USERS[str(message.from_user.id)][0] == 'spo':
            await message.answer("""При подаче заявления о приеме поступающий предоставляет/прикрепляет:

🔹Копию или скан-копию документа, удостоверяющего его личность, гражданство.
🔹Оригинал, копию или скан-копию документа государственного образца об образовании.
🔹Копию или скан-копию страхового свидетельства обязательного пенсионного страхования (при наличии).

Также требуется подать заявления в электронном виде. Это нужно сделать в личном кабинете абитуриента - lk.kai.ru

Календарь приёма можно <a href="https://abiturientu.kai.ru/kalendar-priema">посмотреть тут</a>.""",
                                 parse_mode="HTML", disable_web_page_preview=True)
    else:
        await message.answer(basic_answer_unknown)


@dp.message(F.text == "📋 Направления")
async def directions(message: types.Message):
    logging_date(str(message.from_user.id))
    if str(message.from_user.id) in USERS and USERS[str(message.from_user.id)][0] != '':
        if USERS[str(message.from_user.id)][0] == 'bachelor':
            await message.answer("""Все направления подготовки и специальности разделены по институтам и факультетам, нажми на любое название и попадёшь на наш сайт, где сможешь подробно всё изучить.

<a href="https://abiturientu.kai.ru/iante/obrazovatel-nye-programmy-bakalavriata">✈️ Институт авиации, наземного транспорта и энергетики (ИАНТЭ)</a>
<a href="https://abiturientu.kai.ru/fmf-/-obrazovatel-nye-programmy-bakalavriata">⚛️ Физико-математический факультет (ФМФ)</a>
<a href="https://abiturientu.kai.ru/iaep-/-obrazovatel-nye-programmy-bakalavriata">🎛️️ Институт автоматики и электронного приборостроения (ИАЭП)</a>
<a href="https://abiturientu.kai.ru/iktzi-/-obrazovatel-nye-programmy-bakalavriata">🖥 Институт компьютерных технологий и защиты информации (ИКТЗИ)</a>
<a href="https://abiturientu.kai.ru/iret-/-obrazovatel-nye-programmy-bakalavriata">📡 Институт радиоэлектроники, фотоники и цифровых технологий (ИРЭФ-ЦТ)</a>
<a href="https://abiturientu.kai.ru/ieust-/-obrazovatel-nye-programmy-bakalavriata">💰 Институт инженерной экономики и предпринимательства (ИИЭиП)</a>
<a href="https://abiturientu.kai.ru/vspit-/-obrazovatel-nye-programmy-bakalavriata">🚀 Высшая школа прикладных информационных технологий (ВШПИТ)</a>

Также ты можешь выбрать направление подготовки <a href="https://abiturientu.kai.ru/obrazovatel-nye-programmy?ed=1">по этой ссылке</a> с помощью фильтров.""",
                                 parse_mode="HTML", disable_web_page_preview=True, reply_markup=see_point_keyb)
        elif USERS[str(message.from_user.id)][0] == 'magistracy':
            await message.answer("""<a href="https://abiturientu.kai.ru/obrazovatel-nye-programmy?ed=2">По этой ссылке</a> ты можешь выбрать образовательную программу, используя фильтры. Также предлагаю ознакомиться с планом приёма (количество мест):
🔸<a href="https://abiturientu.kai.ru/documents/1470594/12192680/ПЛАН+ПРИЁМА+маг+бюджет+2024.pdf/e99089c6-51e2-421b-a2f7-b1f1ce37edd6">На бюджетное обучение</a>
🔸<a href="https://abiturientu.kai.ru/documents/1470594/12192680/ПЛАН+ПРИЁМА+маг+договор+2024.pdf/63161d0b-5466-4c28-a1ba-4718ba791dcb">С оплатой стоимости</a>
🔸<a href="https://abiturientu.kai.ru/documents/1470594/12192680/ПЛАН+ПРИЁМА+цно+маг+договор+2024.pdf/2e4a2f9f-36e1-4a48-8d7d-fa521e340375">С оплатой стоимости, заочное обучение</a>

Проходные баллы за 2023 год можно найти <a href="https://abiturientu.kai.ru/documents/1470594/10927743/Результаты+конкурсного+приема+2023.pdf/1015e6e2-f98e-4f84-88eb-57b99c258d07">здесь</a>.""",
                                 parse_mode="HTML", disable_web_page_preview=True)
        elif USERS[str(message.from_user.id)][0] == 'spo':
            await message.answer("""<a href="https://abiturientu.kai.ru/obrazovatel-nye-programmy?ed=3">По этой ссылке</a> ты можешь выбрать образовательную программу, используя фильтры.
            
Также можешь ознакомиться с правилами приёма (количеством мест):
▪️ <a href="https://abiturientu.kai.ru/documents/1470594/12196147/ПЛАН+ПРИЕМА+СПО+бюджет.pdf/d7545213-5190-4cb1-b667-344f4772af4a">На бюджетное обучение</a>
▪️ <a href="https://abiturientu.kai.ru/documents/1470594/12196147/ПЛАН+ПРИЕМА+СПО+договор.pdf/7ea9acca-8072-4150-b19c-664f52a050b2">С оплатой стоимости</a>

Проходные баллы за 2023 год можно найти <a href="https://abiturientu.kai.ru/documents/1470594/10927743/Результаты+конкурсного+приема+2023.pdf/1015e6e2-f98e-4f84-88eb-57b99c258d07">здесь</a>.""",
                                 parse_mode="HTML", disable_web_page_preview=True)
        elif USERS[str(message.from_user.id)][0] == 'grad':
            await message.answer("""""", parse_mode="HTML", disable_web_page_preview=True)
    else:
        await message.answer(basic_answer_unknown)


@dp.callback_query()
async def callbacks_num(callback: types.CallbackQuery):
    global FLAG
    action = callback.data
    if action.split('_')[0] == 'Subj':
        await callback.message.answer('Введи балл. Если передумал(а) отправь любой символ.')
        FLAG[str(callback.from_user.id)] = [action.split('_')[1]]
        with open('FLAG.json', 'w') as fp:
            json.dump(FLAG, fp)
    elif action == 'number_doc':
        await callback.message.answer(
            'Введи до пяти направлений через пробел. Например: "<code>09.03.04 10.03.01 01.03.02</code>". Если передумал(а) отправь "<code>стоп</code>".\n\nВажно! Существуют направления, которые ДУБЛИРУЮТСЯ.\nЕсли ты поступаешь на "Информатику и вычислительную технику" на ИКТЗИ, вводи <code>09.03.01</code>, а если на ВШПИТ, то <code>09.03.01(ВШПИТ)</code>. <code>12.03.04</code> для ИРЭФ-ЦТ и <code>12.03.04(ИАЭП)</code> для ИАЭП.', parse_mode="HTML")
        FLAG[str(callback.from_user.id)] = ['doc']
        with open('FLAG.json', 'w') as fp:
            json.dump(FLAG, fp)
    elif action == "see_points":
        await callback.message.answer("Выбери интересующий тебя институт или факультет.", reply_markup=facult_keyb)
    elif action == "IANTE":
        await callback.message.answer("""<b>13.03.01 Теплоэнергетика и теплотехника</b>
Бюджет: 165    Сверхплановое: 78

<b>13.03.03 Энергетическое машиностроение</b>
Бюджет: 169    Сверхплановое: 156

<b>15.03.01 Машиностроение</b>
Бюджет: 198    Сверхплановое: 138

<b>15.03.05 Конструкторско-технологическое обеспечение машиностроительных производств </b>
Бюджет: 191    Сверхплановое: 140

<b>22.03.01 Материаловедение и технологии материалов</b>
Бюджет: 173    Сверхплановое: 79

<b>23.03.03 Эксплуатация транспортно-технологических машин и комплексов</b>
Бюджет: 182    Сверхплановое: 139

<b>24.03.04 Авиастроение</b>
Бюджет: 231    Сверхплановое: 139

<b>24.03.05 Двигатели летательных аппаратов</b>
Бюджет: 205    Сверхплановое: 148

<b>25.03.01 Техническая эксплуатация летательных аппаратов и двигателей</b>
Бюджет: 220    Сверхплановое: 138

<b>26.03.02 Кораблестроение, океанотехника и системотехника объектов морской инфраструктуры</b>
Бюджет: 187    Сверхплановое: 143

<b>24.05.02 Проектирование авиационных и ракетных двигателей</b>
Бюджет: 196    Сверхплановое: 158

<b>24.05.07 Самолето- и вертолетостроение</b>
Бюджет: 218    Сверхплановое: 148""", parse_mode="HTML")
    elif action == "FMF":
        await callback.message.answer("""<b>12.03.05 Лазерная техника и лазерные технологии</b>
Бюджет: 208    Сверхплановое: 48

<b>16.03.01 Техническая физика</b>
Бюджет: 169    Сверхплановое: -

<b>28.03.02 Наноинженерия</b>
Бюджет: 182    Сверхплановое: -""", parse_mode="HTML")
    elif action == "IAEP":
        await callback.message.answer("""<b>12.03.01 Приборостроение</b>
Бюджет: 188    Сверхплановое: 73

<b>12.03.02 Оптотехника</b>
Бюджет: 160    Сверхплановое: 60

<b>12.03.04 Биотехнические системы и технологии</b>
Бюджет: 163    Сверхплановое: 141

<b>3.03.02 Электроэнергетика и электротехника</b>
Бюджет: 159    Сверхплановое: 138

<b>20.03.01 Техносферная безопасность</b>
Бюджет: 160    Сверхплановое: 144

<b>27.03.01 Стандартизация и метрология</b>
Бюджет: 167    Сверхплановое: 140

<b>27.03.02 Управление качеством</b>
Бюджет: 216    Сверхплановое: 138

<b>27.03.04 Управление в технических системах</b>
Бюджет: 214    Сверхплановое: 165""", parse_mode="HTML")
    elif action == "IKTZI":
        await callback.message.answer(
            """<b>01.03.02 Прикладная математика и информатика</b>
Бюджет: 252    Сверхплановое: 173

<b>09.03.01 Информатика и вычислительная техника</b>
Бюджет: 248    Сверхплановое: 159

<b>09.03.02 Информационные системы и технологии</b>
Бюджет: 259    Сверхплановое: 161

<b>09.03.03 Прикладная информатика</b>
Бюджет: 248    Сверхплановое: 166

<b>09.03.04 Программная инженерия</b>
Бюджет: 269    Сверхплановое: 139

<b>10.03.01 Информационная безопасность</b>
Бюджет: 253    Сверхплановое: 183

<b>10.05.02 Информационная безопасность телекоммуникационных систем</b>
Бюджет: 242    Сверхплановое: 199""", parse_mode="HTML")
    elif action == "IREF":
        await callback.message.answer("""<b>11.03.01 Радиотехника</b>
Бюджет: 175    Сверхплановое: 174

<b>11.03.02 Инфокоммуникационные технологии и системы связи</b>
Бюджет: 212    Сверхплановое: 137

<b>11.03.03 Конструирование и технология электронных средств</b>
Бюджет: 187    Сверхплановое: 172

<b>11.03.04 Электроника и наноэлектроника</b>
Бюджет: 177    Сверхплановое: -

<b>12.03.04 Биотехнические системы и технологии</b>
Бюджет: 163    Сверхплановое: -

<b>11.05.01 Радиоэлектронные системы и комплексы</b>
Бюджет: 177    Сверхплановое: 175

<b>25.05.03 Техническая эксплуатация транспортного радиооборудования </b>
Бюджет: 172    Сверхплановое: 154""", parse_mode="HTML")
    elif action == "IIEP":
        await callback.message.answer("""<b>27.03.05 Инноватика</b>
Бюджет: 237    Сверхплановое: 148

<b>38.03.01 Экономика</b>
Бюджет: 261    Сверхплановое: 145

<b>38.03.02 Менеджмент</b>
Бюджет: 278    Сверхплановое: 143

<b>38.03.03 Управление персоналом</b>
Бюджет: -    Сверхплановое: 141""", parse_mode="HTML")
    elif action == "VSHPIT":
        await callback.message.answer("""<b>09.03.01 Информатика и вычислительная техника</b>
Бюджет: 250    Сверхплановое: 190""", parse_mode="HTML")
    await callback.answer()


@dp.message(F.text == "🌟 Важно ознакомиться")
async def important(message: types.Message):
    logging_date(str(message.from_user.id))
    if str(message.from_user.id) in USERS and USERS[str(message.from_user.id)][0] != '':
        if USERS[str(message.from_user.id)][0] == 'bachelor':
            await message.answer("""В первую очередь зарегистрируйся в личном кабинете абитуриента lk.kai.ru - там ты сможешь подать документы в электронной форме, отследить свой рейтинг и узнать о том, что поступил(а)!
Также можешь ознакомиться с <a href="https://abiturientu.kai.ru/documents/1470594/10919962/Правила+приема+BO.pdf/2f8200d9-c9e8-4672-a0d1-be511bd781ad">правилами приёма</a> и <a href="https://abiturientu.kai.ru/normativnye-dokumenty">нормативными документами</a>.
А на <a href="https://abiturientu.kai.ru/bakalavriat">сайте КАИ</a> ты можешь узнать подробнее о порядке поступления на бакалавриат и специалитет.

Также предлагаем подписаться на наш <a href="https://www.youtube.com/c/knitukai">YouTube-канал</a>, чтобы узнавать новости. К тому же вступай в наш <a href="https://t.me/pk_kai24">чат в Telegram</a>, где можно пообщаться или задать вопросы.""",
                                 parse_mode="HTML", disable_web_page_preview=True)
    else:
        await message.answer(basic_answer_unknown)


@dp.message(F.text == "Колледж Информационных Технологий")
async def kit(message: types.Message):
    logging_date(str(message.from_user.id))
    await message.answer("""Благодаря обучению на СПО ИКТЗИ КИТ ты получишь возможность получения перспективной специальности и диплома государственного образца через 3-4 года, сможешь сразу опробовать себя в конкретной специальности, опережая сверстников.
Также ты получишь отсрочку от армии на весь срок обучения. После обучения ты можешь поступить в университет на ускоренные программы по схожей специальности. 
Организация учебного процесса базируется на инновационных образовательных технологиях, электронных учебниках, все аудитории оснащены электронной доской и подключены к внутренней компьютерной сети.

<a href="https://kai.ru/web/kolledz-informacionnyh-tehnologij/">По ссылке ты можешь ознакомиться с сайтом колледжа</a>""",
                         reply_markup=forspo.as_markup(resize_keyboard=True), parse_mode="HTML",
                         disable_web_page_preview=True)


@dp.message(F.text == "Технический колледж")
async def tk(message: types.Message):
    logging_date(str(message.from_user.id))
    await message.answer("""Наше отделение - современное, динамично развивающееся образовательное подразделение КНИТУ-КАИ.
Технический колледж готовит высококвалифицированных, ответственных, инициативных специалистов и руководителей среднего звена, способных обеспечить безопасное, надежное и эффективное функционирование процессов, руководителями или исполнителями которых они станут по окончанию колледжа.

<a href="https://kai.ru/web/tehniceskij-kolledz">По ссылке ты можешь ознакомиться с сайтом колледжа</a>""",
                         reply_markup=forspo.as_markup(resize_keyboard=True), parse_mode="HTML",
                         disable_web_page_preview=True)


@dp.message(F.text == "✍️ Вступительные испытания")
async def exams(message: types.Message):
    if str(message.from_user.id) in USERS and USERS[str(message.from_user.id)][0] != '':
        if USERS[str(message.from_user.id)][0] == 'magistracy':
            await message.answer("""С программами вступительных испытаний по каждому направлению можно ознакомиться <a href="https://abiturientu.kai.ru/programmy-vstupitel-nyh-ispytanij1">здесь</a>.

Расписание вступительных испытаний на 2024 год появится позже.""", parse_mode="HTML", disable_web_page_preview=True)
    else:
        await message.answer(basic_answer_unknown)


@dp.message(F.text == "🔍 Ещё")
async def askme(message: types.Message):
    if str(message.from_user.id) in USERS and USERS[str(message.from_user.id)][0] != '':
        if USERS[str(message.from_user.id)][0] == 'bachelor':
            await message.answer(
                '🏆 КНИТУ-КАИ входит в ТОП-50 лучших вузов страны: 👇\nhttps://raex-rr.com/education/russian_universities/top-100_universities/2023/',
                reply_markup=back_menu.as_markup(resize_keyboard=True))
    else:
        await message.answer(basic_answer_unknown)


@dp.message(F.text == "❌ Вернуться в меню")  # Если нажата кнопка возврата в меню
async def cancel(message: types.Message):
    logging_date(str(message.from_user.id))
    if USERS[str(message.from_user.id)][0] == 'bachelor':
        await message.answer("Хорошо, вернёмся в меню.", reply_markup=forbachelor.as_markup(resize_keyboard=True))
    elif USERS[str(message.from_user.id)][0] == 'magistracy':
        await message.answer("Хорошо, вернёмся в меню.", reply_markup=formagistracy.as_markup(resize_keyboard=True))
    elif USERS[str(message.from_user.id)][0] == 'spo':
        await message.answer("Хорошо, вернёмся в меню.", reply_markup=forspo.as_markup(resize_keyboard=True))
    elif USERS[str(message.from_user.id)][0] == 'grad':
        await message.answer("Хорошо, вернёмся в меню.", reply_markup=forgrad.as_markup(resize_keyboard=True))
    else:
        await message.answer(basic_answer_unknown)


@dp.message(F.text)  # Обработка любых текстовых сообщений
async def new_text(message: types.Message):
    # Математика, Русский, Информатика, Физика, Химия, Обществознание, Иностранный, Доп
    logging_date(str(message.from_user.id))
    if str(message.from_user.id) in FLAG:
        if FLAG[str(message.from_user.id)][0] != False:
            a = message.text
            if FLAG[str(message.from_user.id)][0] == 'doc':
                try:
                    a = a.split()
                    if a[0].lower() == 'стоп':
                        FLAG[str(message.from_user.id)] = [False]
                        with open('FLAG.json', 'w') as fp:
                            json.dump(FLAG, fp)
                        await message.answer('Хорошо, вернёмся в меню.',
                                             reply_markup=forbachelor.as_markup(resize_keyboard=True))
                    elif a[0] == '0':
                        USERS[str(message.from_user.id)][1] = []
                        with open('users.json', 'w') as fp:
                            json.dump(USERS, fp)
                        FLAG[str(message.from_user.id)] = [False]
                        with open('FLAG.json', 'w') as fp:
                            json.dump(FLAG, fp)
                        await message.answer('Принято. Можешь снова вызвать личный кабинет из меню.',
                                             reply_markup=forbachelor.as_markup(resize_keyboard=True))
                    else:
                        if len(a) > 5:
                            await message.answer('Ты можешь ввести не больше пяти направлений. Попробуй ещё раз.')
                        else:
                            usl = True  # все направления существуют
                            res = []
                            for i in range(len(a)):
                                el = a[i]
                                if el not in a[i + 1:]:
                                    if el not in RECS:
                                        usl = False
                                        await message.answer(
                                            'Направления {} не существует. Попробуй ещё раз.'.format(el))
                                    else:
                                        res.append(el)
                            if usl:
                                USERS[str(message.from_user.id)][1] = res
                                with open('users.json', 'w') as fp:
                                    json.dump(USERS, fp)
                                FLAG[str(message.from_user.id)] = [False]
                                with open('FLAG.json', 'w') as fp:
                                    json.dump(FLAG, fp)
                                await message.answer('Принято. Можешь снова вызвать личный кабинет из меню.',
                                                     reply_markup=forbachelor.as_markup(resize_keyboard=True))
                except:
                    FLAG[str(message.from_user.id)] = [False]
                    with open('FLAG.json', 'w') as fp:
                        json.dump(FLAG, fp)
                    await message.answer('Произошла ошибка, так что вернёмся в меню.',
                                         reply_markup=forbachelor.as_markup(resize_keyboard=True))
            else:
                try:
                    a = int(a)
                    if int(FLAG[str(message.from_user.id)][0]) == 7:
                        if 0 <= a <= 10:
                            SCORES[str(message.from_user.id)][int(FLAG[str(message.from_user.id)][0])] = a
                            with open('score.json', 'w') as fp:
                                json.dump(SCORES, fp)  # Сохраняем в json
                            FLAG[str(message.from_user.id)] = [False]
                            with open('FLAG.json', 'w') as fp:
                                json.dump(FLAG, fp)
                            await message.answer('Принято. Можешь снова вызвать личный кабинет из меню.',
                                                 reply_markup=forbachelor.as_markup(resize_keyboard=True))
                        else:
                            await message.answer('Введено неверное число. Попробуй снова.')
                    else:
                        if 0 <= a <= 100:
                            SCORES[str(message.from_user.id)][int(FLAG[str(message.from_user.id)][0])] = a
                            with open('score.json', 'w') as fp:
                                json.dump(SCORES, fp)  # Сохраняем в json
                            FLAG[str(message.from_user.id)] = [False]
                            with open('FLAG.json', 'w') as fp:
                                json.dump(FLAG, fp)
                            await message.answer('Принято. Можешь снова вызвать личный кабинет из меню.',
                                                 reply_markup=forbachelor.as_markup(resize_keyboard=True))
                        else:
                            await message.answer('Введено неверное число. Попробуй снова.')
                except:
                    FLAG[str(message.from_user.id)] = [False]
                    with open('FLAG.json', 'w') as fp:
                        json.dump(FLAG, fp)
                    await message.answer('Было введено не просто число, так что вернёмся в меню.',
                                         reply_markup=forbachelor.as_markup(resize_keyboard=True))
        elif str(message.from_user.id) in USERS and USERS[str(message.from_user.id)][0] != '':
            if USERS[str(message.from_user.id)][0] == 'bachelor':
                await message.answer('Я не понял, что ты хочешь. Воспользуйся кнопками ниже.',
                                     reply_markup=forbachelor.as_markup(resize_keyboard=True))
            elif USERS[str(message.from_user.id)][0] == 'magistracy':
                await message.answer('Я не понял, что ты хочешь. Воспользуйся кнопками ниже.',
                                     reply_markup=formagistracy.as_markup(resize_keyboard=True))
            elif USERS[str(message.from_user.id)][0] == 'spo':
                await message.answer('Я не понял, что ты хочешь. Воспользуйся кнопками ниже.',
                                     reply_markup=forspo.as_markup(resize_keyboard=True))
            elif USERS[str(message.from_user.id)][0] == 'grad':
                await message.answer('Я не понял, что ты хочешь. Воспользуйся кнопками ниже.',
                                     reply_markup=forgrad.as_markup(resize_keyboard=True))
            else:
                await message.answer(basic_answer_unknown)
    else:
        await message.answer(basic_answer_unknown)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    save_log('Работа бота начата.')
    asyncio.run(main())
