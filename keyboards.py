from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types

first_qu = ReplyKeyboardBuilder()  # Первая клавиатура - спрашиваем, кем является пользователь
for el in ["📚 На бакалавриат", "👩‍🎓 В магистратуру", "📔 На СПО"]: #, "🔭 В аспирантуру"
    first_qu.add(types.KeyboardButton(text=el))
first_qu.adjust(1)

forbachelor = ReplyKeyboardBuilder()  # Клавиатура для бакалавров
for el in ["👋 О нас", "📋 Направления", "🌟 Важно ознакомиться", "📃 Необходимые документы",  "👤 Личный кабинет", "🔍 Рекомендации", "❓ Задать вопрос", "✖️ Изменить выбор"]:
    forbachelor.add(types.KeyboardButton(text=el))
forbachelor.adjust(2)

formagistracy = ReplyKeyboardBuilder()  # Клавиатура для магистрантов
for el in ["📋 Направления", "✍️ Вступительные испытания", "📃 Необходимые документы", "❓ Задать вопрос", "✖️ Изменить выбор"]:
    formagistracy.add(types.KeyboardButton(text=el))
formagistracy.adjust(2)

forspo = ReplyKeyboardBuilder()  # Клавиатура для спо
for el in ["👋 О нас", "📋 Направления", "📃 Необходимые документы", "❓ Задать вопрос", "✖️ Изменить выбор"]:
    forspo.add(types.KeyboardButton(text=el))
forspo.adjust(2)

forgrad = ReplyKeyboardBuilder()  # Клавиатура для аспирантов
for el in ["📋 Направления", "🌟 Важно ознакомиться", "📃 Необходимые документы", "❓ Задать вопрос", "✖️ Изменить выбор"]:
    forgrad.add(types.KeyboardButton(text=el))
forgrad.adjust(2)

back_menu = ReplyKeyboardBuilder()  # Клавиатура для того, чтобы вернуться в меню
for el in ["❌ Вернуться в меню"]:
    back_menu.add(types.KeyboardButton(text=el))
back_menu.adjust(1)

spo_about = ReplyKeyboardBuilder()  # Клавиатура для того, чтобы узнать про один из двух колледжей
for el in ["Колледж Информационных Технологий", "Технический колледж", "❌ Вернуться в меню"]:
    spo_about.add(types.KeyboardButton(text=el))
spo_about.adjust(1)

next_back = ReplyKeyboardBuilder()  # Клавиатура для того, чтобы пойти дальше или вернуться в меню
for el in ["🔍 Ещё", "❌ Вернуться в меню"]:
    next_back.add(types.KeyboardButton(text=el))
next_back.adjust(1)

buttons = [[types.InlineKeyboardButton(text="Посмотреть проходные баллы", callback_data="see_points")]]
see_point_keyb = types.InlineKeyboardMarkup(inline_keyboard=buttons)

buttons = [[types.InlineKeyboardButton(text="✈️ ИАНТЭ", callback_data="IANTE"), types.InlineKeyboardButton(text="⚛️ ФМФ", callback_data="FMF")],
           [types.InlineKeyboardButton(text="🎛️ ИАЭП", callback_data="IAEP"), types.InlineKeyboardButton(text="🖥 ИКТЗИ", callback_data="IKTZI")],
           [types.InlineKeyboardButton(text="📡 ИРЭФ-ЦТ", callback_data="IREF"), types.InlineKeyboardButton(text="💰 ИИЭиП", callback_data="IIEP")],
           [types.InlineKeyboardButton(text="🚀 ВШПИТ", callback_data="VSHPIT"),  types.InlineKeyboardButton(text="Посмотреть все", url="https://abiturientu.kai.ru/documents/1470594/10927743/Результаты+конкурсного+приема+2023.pdf/1015e6e2-f98e-4f84-88eb-57b99c258d07")]]
facult_keyb = types.InlineKeyboardMarkup(inline_keyboard=buttons)

# Математика, Русский, Информатика, Физика, Химия, Обществознание, Иностранный, Доп
buttons = [[types.InlineKeyboardButton(text="Ввести номер заявления", callback_data="number_doc")],
            [types.InlineKeyboardButton(text="Математика", callback_data="Subj_0"), types.InlineKeyboardButton(text="Русский", callback_data="Subj_1")],
           [types.InlineKeyboardButton(text="Информатика", callback_data="Subj_2"), types.InlineKeyboardButton(text="Физика", callback_data="Subj_3")],
           [types.InlineKeyboardButton(text="Химия", callback_data="Subj_4"), types.InlineKeyboardButton(text="Обществознание", callback_data="Subj_5")],
           [types.InlineKeyboardButton(text="Иностранный", callback_data="Subj_6"),  types.InlineKeyboardButton(text="Дополнительные баллы", callback_data="Subj_7")]]
subj_keyb = types.InlineKeyboardMarkup(inline_keyboard=buttons)