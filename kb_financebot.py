from telebot import types
import financeBot_baza as baza

# Кнопки для старта
def start_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    knopka1 = types.KeyboardButton('💸Доходы')
    knopka2 = types.KeyboardButton('💸Расходы')


    # Добавляем кнопки
    kb.add(knopka1,knopka2)

    # Вывод кнопок
    return kb

# Кнопки для выбора типа доходов
def type_inc():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    knopka1 = types.KeyboardButton('Карта')
    knopka2 = types.KeyboardButton('Наличка')

    # Добавляем кнопки
    kb.add(knopka1,knopka2)

    # Вывод кнопок
    return kb

# Кнопки для выбора категорий
def categories():
    kb = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    for category in baza.get_all_categories():
        kb.add(category[0])

    return kb

# Кнопки для выбора действий
def actions():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    knopka1 = types.KeyboardButton('💰Доходы/Расходы')
    knopka2 = types.KeyboardButton('🗂Excel')

    kb.add(knopka1, knopka2)
    return kb

# Кнопки для выбора метода внесения расходов
def exp_types():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    knopka1 = types.KeyboardButton('QRcode')
    knopka2 = types.KeyboardButton('Вручную')
    knopka3 = types.KeyboardButton('🔙Назад')
    kb.add(knopka1, knopka2, knopka3)
    return kb

# Кнопки для выбора файла выгрузки
def excel_files():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    knopka1 = types.KeyboardButton('📈Доходы')
    knopka2 = types.KeyboardButton('📉Расходы')

    kb.add(knopka1, knopka2)
    return kb

# Кнопки для выбора внесения данных
def inc_exp():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    knopka1 = types.KeyboardButton('💸Доходы')
    knopka2 = types.KeyboardButton('💸Расходы')
    knopka3 = types.KeyboardButton('🔙Назад')

    # Добавляем кнопки
    kb.add(knopka1,knopka2, knopka3)

    # Вывод кнопок
    return kb