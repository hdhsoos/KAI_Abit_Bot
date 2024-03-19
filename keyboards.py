from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types

first_qu = ReplyKeyboardBuilder()  # Первая клавиатура - спрашиваем, кем является пользователь
for el in ["📚 Заканчиваю школу", "👩‍🎓 Хочу в магистратуру", "👨‍👩‍👧‍👦 Я родитель", "🙊 Не хочу отвечать"]:
    first_qu.add(types.KeyboardButton(text=el))
first_qu.adjust(1)

universal = ReplyKeyboardBuilder()  # Пока что универсальная клавиатура, предлагающая информацию
for el in ["👋 О нас", "📋 Направления", "🌟 Мероприятия", "❓ Задать вопрос"]:
    universal.add(types.KeyboardButton(text=el))
universal.adjust(1)

question = ReplyKeyboardBuilder()  # Клавиатура для того, чтобы задать вопрос
for el in ["👋 О нас", "📋 Направления", "🌟 Мероприятия", "❌ Вернуться в меню"]:
    universal.add(types.KeyboardButton(text=el))
universal.adjust(1)