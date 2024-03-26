from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types

first_qu = ReplyKeyboardBuilder()  # Первая клавиатура - спрашиваем, кем является пользователь
for el in ["📚 На бакалавриат", "👩‍🎓 В магистратуру", "📔 На СПО", "🔭 В аспирантуру"]:
    first_qu.add(types.KeyboardButton(text=el))
first_qu.adjust(1)

universal = ReplyKeyboardBuilder()  # Пока что универсальная клавиатура, предлагающая информацию
for el in ["👋 О нас", "📋 Направления", "🌟 Мероприятия", "❓ Задать вопрос"]:
    universal.add(types.KeyboardButton(text=el))
universal.adjust(1)

forbachelor = ReplyKeyboardBuilder()  # Клавиатура для бакалавров
for el in ["📋 Направления", "🌟 Важно ознакомиться", "📃 Необходимые документы", "❓ Задать вопрос"]:
    forbachelor.add(types.KeyboardButton(text=el))
forbachelor.adjust(1)

formagistracy = ReplyKeyboardBuilder()  # Клавиатура для магистрантов
for el in ["👋 Больше о нас", "📋 Направления", "✍️ Вступительные испытания", "📃 Необходимые документы", "❓ Задать вопрос"]:
    formagistracy.add(types.KeyboardButton(text=el))
formagistracy.adjust(1)

back_menu = ReplyKeyboardBuilder()  # Клавиатура для того, чтобы вернуться в меню
for el in ["❌ Вернуться в меню"]:
    back_menu.add(types.KeyboardButton(text=el))
back_menu.adjust(1)

next_back = ReplyKeyboardBuilder()  # Клавиатура для того, чтобы пойти дальше или вернуться в меню
for el in ["🔍 Ещё", "❌ Вернуться в меню"]:
    next_back.add(types.KeyboardButton(text=el))
next_back.adjust(1)
