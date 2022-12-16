import telebot
import kb_financebot as kb
import financeBot_baza as baza
import web_scraping


bot = telebot.TeleBot('API_TOKEN')

# Обработка комманды старт
@bot.message_handler(commands=['start'])
def start(message):
    check_user = baza.check_user(message.from_user.id)
    if not check_user:
        bot.send_message(message.from_user.id,
                         "Добро пожаловать, {0.first_name}!\nЭтот бот поможет вам с учетом доходов и расходов."
                         "\nВыберите, что вы хотите внести.".format(message.from_user, bot.get_me()),
                         reply_markup=kb.start_kb())
        bot.register_next_step_handler(message, inc_exp)
    else:
        bot.send_message(message.from_user.id,
                         "Выберите действие", reply_markup=kb.actions())
        bot.register_next_step_handler(message, finance)

# Обработчик сообщений с текстом, файлом и фото
@bot.message_handler(content_types=['text', 'photo', 'document'])
def finance(message):
    if message.text == '💰Доходы/Расходы':
        bot.send_message(message.from_user.id, 'Выберите, что вы хотите внести', reply_markup=kb.inc_exp())
        bot.register_next_step_handler(message, inc_exp)
    elif message.text == '🗂Excel':
        bot.send_message(message.from_user.id, 'Выберите отчет, который хотите видеть', reply_markup=kb.excel_files())
        bot.register_next_step_handler(message, get_files)

# Выбор команды внесения Доходов/Расходов
def inc_exp(message):
    if message.text == '🔙Назад':
        bot.send_message(message.from_user.id, 'Отправьте любой текст, чтобы вернуться назад')
        bot.register_next_step_handler(message, start)
    elif message.text == '💸Доходы':
        bot.send_message(message.from_user.id, 'Выберите тип вашего дохода', reply_markup=kb.type_inc())
        bot.register_next_step_handler(message, get_inc)
    elif message.text == '💸Расходы':
        bot.send_message(message.from_user.id, 'Выберите, как вы хотите занести ваши расходы', reply_markup=kb.exp_types())
        bot.register_next_step_handler(message, get_exp)

# Тип дохода
def get_inc(message):
    type_inc = message.text
    bot.send_message(message.from_user.id, 'Отправьте сумму дохода')
    bot.register_next_step_handler(message, checker_inc, type_inc)

# Внесение суммы дохода, проверка на численное значение
def checker_inc(message, type_inc):
    try:
        sum_inc = float(message.text)
        if sum_inc>=0:
            baza.add_income(message.from_user.id, type_inc, sum_inc)

            bot.send_message(message.from_user.id,
                             'Ваши доходы успешно добавлены, отправьте любой текст, чтобы выбрать действие',
                             reply_markup=kb.start_kb())
            bot.register_next_step_handler(message, start)
        else:
            bot.send_message(message.from_user.id, 'Отправьте положительное значение дохода')
            bot.register_next_step_handler(message, checker_inc, type_inc)

    except ValueError:
        bot.send_message(message.from_user.id, 'Отправьте сумму вашего дохода в числах')
        bot.register_next_step_handler(message, checker_inc, type_inc)

# Выбор внесения расхода
def get_exp(message):
    if message.text == '🔙Назад':
        bot.send_message(message.from_user.id, 'Отправьте любой текст, чтобы вернуться назад')
        bot.register_next_step_handler(message, start)
    elif message.text == 'Вручную':
        bot.send_message(message.from_user.id, 'Выберите категорию расхода', reply_markup=kb.categories())
        bot.register_next_step_handler(message, get_cat)
    elif message.text == 'QRcode':
        bot.send_message(message.from_user.id, 'Отправьте QRcode, используя 📎', reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_qr_exp)

# Внесение расхода через qr код
def get_qr_exp(message):
    from pathlib import Path
    Path(f'files/{message.chat.id}/').mkdir(parents=True, exist_ok=True)
    if message.content_type == 'photo':
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = f'files/{message.chat.id}/' + file_info.file_path.replace('photos/', '')
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        page = web_scraping.decode(src)
        try:
            list_name = web_scraping.pr_name(page)
            cat_list = web_scraping.category(page)
            list_number = web_scraping.pr_number(page)
            list_sum = web_scraping.pr_sum(page)
            year = web_scraping.get_year(page)
            month = web_scraping.get_month(page)
            date = web_scraping.get_date(page)

            for i in range(len(list_name)):
                name = list_name[i]
                category = cat_list[i]
                number = list_number[i]
                pr_sum = list_sum[i]
                baza.add_qr_expenses(message.from_user.id, category, name, number, pr_sum, year, month, date)

            bot.send_message(message.from_user.id, 'Ваши расходы успешно добавлены, отправьте любой текст, '
                                                   'чтобы выбрать действие', reply_markup=kb.actions())
            bot.register_next_step_handler(message, start)
        except ValueError:
            bot.send_message(message.from_user.id, 'Отправьте более четкую картинку')
            bot.register_next_step_handler(message, get_qr_exp)

# Внесение категории расхода вручную
def get_cat(message):
    category = message.text
    bot.send_message(message.from_user.id, 'Напишите название продукта/услуги')
    bot.register_next_step_handler(message, get_item, category)

# Внесение название расхода вручную
def get_item(message, category):
    item = message.text
    bot.send_message(message.from_user.id, 'Напишите количество продукта/услуги')
    bot.register_next_step_handler(message, get_num, category, item)

# Внесение количества расхода вручную
def get_num(message, category, item):
    try:
        num = float(message.text)
        bot.send_message(message.from_user.id, 'Напишите сумму расхода')
        bot.register_next_step_handler(message, get_sum, category, item, num)
    except ValueError:
        bot.send_message(message.from_user.id, 'Отправьте количество в числах')
        bot.register_next_step_handler(message, get_item, category)

# Внесение суммы расхода вручную
def get_sum(message, category,item,num):
    try:
        sum = float(message.text)
        baza.add_expenses(message.from_user.id, category,item,num,sum)

        bot.send_message(message.from_user.id, 'Ваши расходы успешно добавлены, отправьте любой текст, чтобы выбрать действие', reply_markup=kb.actions())
        bot.register_next_step_handler(message, start)
    except ValueError:
        bot.send_message(message.from_user.id, 'Отправьте сумму в числах')
        bot.register_next_step_handler(message, get_num, category, item)

# Выбор файла выгрузки Доходы/Расходы
def get_files(message):
    if message.text == '📈Доходы':
        baza.get_income_file(message.from_user.id)
        file = open('Доходы.xlsx', 'rb')
        bot.send_document(message.from_user.id, file, reply_markup=kb.actions())
        bot.send_message(message.from_user.id, 'Отправьте любой текст, чтобы вернуться назад')
        bot.register_next_step_handler(message, start)
    elif message.text == '📉Расходы':
        baza.get_expenses_file(message.from_user.id)
        file = open('Расходы.xlsx', 'rb')
        bot.send_document(message.from_user.id, file, reply_markup=kb.actions())
        bot.send_message(message.from_user.id, 'Отправьте любой текст, чтобы вернуться назад')
        bot.register_next_step_handler(message, start)


bot.polling()


