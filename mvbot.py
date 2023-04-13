from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from database import Database
from apiOperation import ApiOperation
from datetime import date as dt
from inlineKeyboardEvent import InlineKeyboardEvent

# region Constants

TOKEN = "5149320687:AAEuCMs7xshTAJYgGjBRLgW1yTRPULpsiG0"
API_TOKEN = "9tdyx0v-kj946kd-j7ea9bb-rm2yrfw"
BOT = Bot(token=TOKEN)
DATE_PARSE = dt(2022, 3, 29)
DB = Database('db.db')
ADMINISTRATORS = [514133808]

# endregion

# region Variables

storage = MemoryStorage()
dp = Dispatcher(BOT, storage=storage)
Actualization_InProcess = False
JamDays = []  # Кол-во фильмов у каждой даты
JamDate = []  # Лист с датами
Jam = []  # Json в памяти

# endregion

# region Commands


@dp.message_handler(commands=['help'])
async def process_start_command6(message: types.Message):
    if message.from_user.id in ADMINISTRATORS:
        await BOT.send_message(message.from_user.id,
                               "💻Команды, доступные в боте:" +
                               "\n\n/ressing [текст] - глобал рассылка сообщения" +
                               "\n/msgtousr [id] [текст] - Сообщение конкретному челу" +
                               "\n/listusers - список челов в боте")


@dp.message_handler(commands=['ressing'])
async def process_start_command(message: types.Message):
    if message.from_user.id in ADMINISTRATORS:
        dbConnection = Database.GetCurrentDBConnection()
        dbCursor = dbConnection.cursor()
        dbCursor.execute('SELECT ID FROM Users')
        outputData = dbCursor.fetchall()
        tempArrray = []

        for x in outputData:
            tempArrray += x
        for user_id in tempArrray:
            try:
                await BOT.send_message(user_id, (str(message.text))[8:-1])
            except:
                print(str(user_id) + "заблокировал бота(")
    else:
        return


@dp.message_handler(commands=['msgtousr'])
async def process_start_command(message: types.Message):
    if message.from_user.id in ADMINISTRATORS:
        arrayMsg = message.text.split(" ")
        try:
            await BOT.send_message(int(arrayMsg[1]), (str(message.text))[10 + len(arrayMsg[1]):])
            await BOT.send_message(message.from_user.id, "Отправлено!")
        except:
            await BOT.send_message(message.from_user.id, "Пользователь не найден!")
    else:
        return


@dp.message_handler(commands=['listusers'])
async def process_start_command3(message: types.Message):
    if message.from_user.id in ADMINISTRATORS:
        dbConnection = Database.GetCurrentDBConnection()
        dbCursor = dbConnection.cursor()
        dbCursor.execute('SELECT first_name FROM Users')
        first_name = dbCursor.fetchall()
        dbCursor.execute('SELECT Username FROM Users')
        username = dbCursor.fetchall()
        dbCursor.execute('SELECT ID FROM Users')
        id = dbCursor.fetchall()
        first_nameArray = []
        usernameArray = []
        idArray = []
        targetText = "💻Список пользователей бота:\n\n"
        iteration = 0

        for x in first_name:
            first_nameArray += x
        for x in username:
            usernameArray += x
        for x in id:
            idArray += x

        for x in usernameArray:
            if len(targetText) > 4095:
                tempo = targetText[-(len(targetText) - 4095):-1]
                targetText = targetText[:-(len(targetText) - 4095)]
                await BOT.send_message(message.from_user.id, targetText)
                targetText = tempo
                targetText += "\n#" + str(iteration) + " ID - " + str(idArray[iteration]) + ", " + str(
                    first_nameArray[iteration]) + ",  ссылка на профиль - @" + str(x) + "\n"
                iteration += 1
            else:
                targetText += "\n#" + str(iteration) + " ID - " + str(idArray[iteration]) + ", " + str(
                    first_nameArray[iteration]) + ",  ссылка на профиль - @" + str(x) + "\n"
                iteration += 1
        targetText += "\n👥Общее число пользователей - " + str(iteration)

        await BOT.send_message(message.from_user.id, targetText)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    DB.add_id_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name,
                   message.from_user.username, 0, "False", "False", 0, "False", "none", "False", "False", "False")

    if Actualization_InProcess:
        await BOT.answer_callback_query(
            message.chat.id,
            text='♻️В настоящий момент бот актуализирует данные по киношкам.\nПогоди немного🙂', show_alert=True)
        return

    button_hx = KeyboardButton('🍿Просмотр афиш')
    button_h1 = KeyboardButton('💻Просмотр кино онлайн')
    button_h2 = KeyboardButton('🎰Рандомный фильм🎰')
    button_h4 = KeyboardButton('📜Правила')
    button_h5 = KeyboardButton('💡О нас')
    greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(button_hx, button_h1, button_h2,
                                                                                      button_h4, button_h5)
    sti = open('AnimatedSticker.tgs', 'rb')
    await BOT.send_sticker(message.chat.id, sti)
    await message.reply(
        "Велком, {0.first_name}!\nСервис предоставляет вам список сеансов, которые идут в кинотеатрах города Киров, а так же то, что идет в инете:)🍿".format(
            message.from_user), parse_mode='html', reply_markup=greet_kb)


# endregion

# region Обработка текста

@dp.message_handler(content_types=['text'])
async def process_command_1(message: types.Message):
    if message.chat.type == 'private':
        test = str(DB.check_ACTIVE_TAB(message.from_user.id))[2:-3]
        try:
            #if Actualization_InProcess:
            #    await BOT.answer_callback_query(
            #        message.id,
            #        text='♻️В настоящий момент бот актуализирует данные по киношкам.\nПогоди немного🙂', show_alert=True)
            #    return

            if (str(DB.check_findByIdBool(message.from_user.id))[2:-3]) == 'True':
                await ApiOperation.FindFilmById(DB, BOT, message, API_TOKEN)
                return

            elif (str(DB.check_findByNameBool(message.from_user.id))[2:-3]) == 'True':
                await ApiOperation.FindFilmByName(DB, BOT, message, API_TOKEN)
                return

            elif (str(DB.check_findPersonByName(message.from_user.id))[2:-3]) == 'True':
                await ApiOperation.FindPersonByName(DB, BOT, message, API_TOKEN)
                return

            elif (str(DB.check_findReviewById(message.from_user.id))[2:-3]) == 'True':
                await ApiOperation.FindReviewById(DB, BOT, message, API_TOKEN)
                return

            if (str(DB.check_ACTIVE_TAB(message.from_user.id))[2:-3]) == 'True':
                await BOT.send_message(message.from_user.id,
                                       'У тебя уже есть активное окно, закончи с ним, чтобы открыть новое💡')
                return

            if message.text == '🍿Просмотр афиш':
                await InlineKeyboardEvent.ViewCinemaPosters(BOT, DB, message)
                DB.add_ACTIVE_TAB('True', message.from_user.id)
                return

            elif message.text == '💻Просмотр кино онлайн':
                await InlineKeyboardEvent.ViewOnlineCinema(BOT, message)
                DB.add_ACTIVE_TAB('True', message.from_user.id)
                return

            elif message.text == '🎰Рандомный фильм🎰':
                await InlineKeyboardEvent.SendRandomFilm(BOT, DB, message)
                return

            elif message.text == '📜Правила':
                await InlineKeyboardEvent.SendRules(BOT, message)
                DB.add_ACTIVE_TAB('False', message.from_user.id)
                return

            elif message.text == '💡О нас':
                await InlineKeyboardEvent.AboutUs(BOT, DB, message)
                return

            else:
                DB.add_ACTIVE_TAB('False', message.from_user.id)
                await BOT.send_message(message.from_user.id, 'Пользуйся кнопками, я же бот, а не собеседник😊')
                return
        except:
            pass
    else:
        pass


# endregion

# region Обработка кнопок

@dp.callback_query_handler(lambda c: c.data)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    global dt, DATE_PARSE, Jam, JamDate, JamDays, Actualization_InProcess
    try:
        #if (DATE_PARSE < dt.today()):
        #    DATE_PARSE = dt.today()
        #    #(jam, jamDate, jamDays) = Parser.Actualization_Data(Jam, JamDate, JamDays)
        #    return
        if (Actualization_InProcess):
            await BOT.answer_callback_query(
                callback_query.id,
                text='♻️В настоящий момент бот актуализирует данные по киношкам.\nПогоди немного🙂', show_alert=True)
            return

        code = callback_query.data
        if code == 'exit' and (str(DB.check_findByIdBool(callback_query.from_user.id))[2:-3]) == 'False' and (
                str(DB.check_findByNameBool(callback_query.from_user.id))[2:-3]) == 'False':
            DB.add_ACTIVE_TAB('False', callback_query.message.chat.id)
            try:
                await BOT.edit_message_text(chat_id=callback_query.message.chat.id,
                                            message_id=callback_query.message.message_id, text="Жду твоих указаний👾",
                                            reply_markup=None)
            except:
                await BOT.delete_message(chat_id=callback_query.message.chat.id,
                                         message_id=callback_query.message.message_id)
            return

        elif code == "exitOne" and (str(DB.check_findByIdBool(callback_query.from_user.id))[2:-3]) == 'False' and (
                str(DB.check_findByNameBool(callback_query.from_user.id))[2:-3]) == 'False':
            DB.add_Panel(0, callback_query.from_user.id)
            await BOT.delete_message(chat_id=callback_query.message.chat.id,
                                     message_id=callback_query.message.message_id)
            return

        elif code == "smenaPanelLeft" and (
                str(DB.check_findByIdBool(callback_query.from_user.id))[2:-3]) == 'False' and (
                str(DB.check_findByNameBool(callback_query.from_user.id))[2:-3]) == 'False':
            await InlineKeyboardEvent.ScrollFrirendPanel(BOT, DB, callback_query, "Left", Jam, "smenaPanelLeft", "smenaPanelRight", "smenaCinema")
            return

        elif code == "smenaPanelRight" and (
                str(DB.check_findByIdBool(callback_query.from_user.id))[2:-3]) == 'False' and (
                str(DB.check_findByNameBool(callback_query.from_user.id))[2:-3]) == 'False':
            await InlineKeyboardEvent.ScrollFrirendPanel(BOT, DB, callback_query, "Right", Jam, "smenaPanelLeft", "smenaPanelRight", "smenaCinema")
            return

        elif code == "goCinemaKirow" and (
                str(DB.check_findByIdBool(callback_query.from_user.id))[2:-3]) == 'False' and (
                str(DB.check_findByNameBool(callback_query.from_user.id))[2:-3]) == 'False':
            await InlineKeyboardEvent.GetCinemaKirow(BOT, DB, callback_query)
            return

        elif code == 'payCinema' and (str(DB.check_findByIdBool(callback_query.from_user.id))[2:-3]) == 'False' and (
                str(DB.check_findByNameBool(callback_query.from_user.id))[2:-3]) == 'False':
            await InlineKeyboardEvent.GetPayCinemaCallback(BOT, DB, callback_query)
            return

        elif code == 'findById' and (str(DB.check_findByIdBool(callback_query.from_user.id))[2:-3]) == 'False' and (
                str(DB.check_findByNameBool(callback_query.from_user.id))[2:-3]) == 'False':
            await BOT.delete_message(chat_id=callback_query.message.chat.id,
                                     message_id=callback_query.message.message_id)
            await BOT.send_message(callback_query.message.chat.id, "Введите идентификатор фильма!")
            DB.add_findByIdBool('True', callback_query.from_user.id)
            return

        elif code == 'findByName' and (str(DB.check_findByIdBool(callback_query.from_user.id))[2:-3]) == 'False' and (
                str(DB.check_findByNameBool(callback_query.from_user.id))[2:-3]) == 'False':
            await BOT.delete_message(chat_id=callback_query.message.chat.id,
                                     message_id=callback_query.message.message_id)
            await BOT.send_message(callback_query.message.chat.id, "Введите название фильма")
            DB.add_findByNameBool('True', callback_query.from_user.id)
            return

        elif code == 'findPersonByName' and (str(DB.check_findByIdBool(callback_query.from_user.id))[2:-3]) == 'False' and (
                str(DB.check_findByNameBool(callback_query.from_user.id))[2:-3]) == 'False':
            await BOT.delete_message(chat_id=callback_query.message.chat.id,
                                     message_id=callback_query.message.message_id)
            await BOT.send_message(callback_query.message.chat.id, "Введите название персоны")
            DB.add_findPersonByName('True', callback_query.from_user.id)
            return

        elif code == 'findReviewById' and (str(DB.check_findByIdBool(callback_query.from_user.id))[2:-3]) == 'False' and (
                str(DB.check_findByNameBool(callback_query.from_user.id))[2:-3]) == 'False':
            await BOT.delete_message(chat_id=callback_query.message.chat.id,
                                     message_id=callback_query.message.message_id)
            await BOT.send_message(callback_query.message.chat.id, "Введите идентификатор фильма, отзыв на который хотите прочитать! =)")
            DB.add_findReviewById('True', callback_query.from_user.id)
            return

        elif code == 'goBack' and (str(DB.check_findByIdBool(callback_query.from_user.id))[2:-3]) == 'False' and (
                str(DB.check_findByNameBool(callback_query.from_user.id))[2:-3]) == 'False':
            await InlineKeyboardEvent.GoBack(BOT, callback_query)
            return

        elif code == 'freeCinema' and (str(DB.check_findByIdBool(callback_query.from_user.id))[2:-3]) == 'False' and (
                str(DB.check_findByNameBool(callback_query.from_user.id))[2:-3]) == 'False':
            await InlineKeyboardEvent.GetFreeCinema(BOT, DB, callback_query)
            return

        elif code == 'smenaCinema' and (str(DB.check_findByIdBool(callback_query.from_user.id))[2:-3]) == 'False' and (
                str(DB.check_findByNameBool(callback_query.from_user.id))[2:-3]) == 'False':
            await InlineKeyboardEvent.GetSmenaCinema(BOT, DB, JamDate, callback_query)
            return
        if ((str(DB.check_ACTIVE_TAB(callback_query.from_user.id))[2:-3]) == 'True') and (
                str(DB.check_findByIdBool(callback_query.from_user.id))[2:-3]) == 'False' and (
                str(DB.check_findByNameBool(callback_query.from_user.id))[2:-3]) == 'False' and (
                str(DB.check_findPersonByName(callback_query.from_user.id))[2:-3] == 'False'):
            await InlineKeyboardEvent.GetjamFilmsPanel(
                BOT, DB, JamDate, Jam, callback_query, code)
    except Exception as e:
        print(str(e))

# endregion


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)