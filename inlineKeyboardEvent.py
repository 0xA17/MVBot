import os
import random
import aiogram
from random import randint
from parser import Parser
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class InlineKeyboardEvent:

    async def GoBack(bot, callback_query):

        if (bot is None):
            print("Parameter 'bot' has not been assigned a value")
            return

        if (callback_query is None):
            print("Parameter 'callback_query' has not been assigned a value")
            return

        inlineKeyboardButton = InlineKeyboardButton(
            'Платные кинотеатры💳', callback_data='payCinema')
        inline_kb_full = InlineKeyboardMarkup(
            row_width=1).add(inlineKeyboardButton)
        inline_kb_full.add(InlineKeyboardButton(
            'Бесплатные кинотеатры🏴‍☠️', callback_data='freeCinema'))
        inline_kb_full.add(InlineKeyboardButton(
            'Отмена', callback_data='exit'))
        try:
            await bot.delete_message(chat_id=callback_query.message.chat.id,
                                     message_id=callback_query.message.message_id)
        except:
            print("{0.first_name} дудосит кнопку -_-")
        await bot.send_message(
            callback_query.from_user.id,
            "➖➖➖➖➖➖➖➖➖➖➖➖\n✅Список онлайн кинотеатров📄\n➖➖➖➖➖➖➖➖➖➖➖➖",
            reply_markup=inline_kb_full)

    async def ViewCinemaPosters(bot, db, message):

        if (bot is None):
            print("Parameter 'bot' has not been assigned a value")
            return

        if (db is None):
            print("Parameter 'db' has not been assigned a value")
            return

        db.add_jamSelect('False', message.chat.id)
        smenaCinemaButton = InlineKeyboardButton(
            'КИНОjam🗿', callback_data='smenaCinema')

        cancelButton = InlineKeyboardButton('Отмена', callback_data='exit')
        menuCinemaButton = InlineKeyboardMarkup(row_width=1)
        menuCinemaButton.add(smenaCinemaButton, cancelButton)

        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await bot.send_photo(message.from_user.id,
                             "https://telegra.ph/file/f298b205ec7551b2fb740.jpg",
                             "🎬Выберете желаемый кинотеатр:",
                             reply_markup=menuCinemaButton)

    async def ViewOnlineCinema(bot, message):

        if (bot is None):
            print("Parameter 'bot' has not been assigned a value")
            return

        if (message is None):
            print("Parameter 'message' has not been assigned a value")
            return

        inlineKeyboardButton = InlineKeyboardButton(
            'Платные кинотеатры💳', callback_data='payCinema')
        inline_kb_full = InlineKeyboardMarkup(
            row_width=1).add(inlineKeyboardButton)
        inline_kb_full.add(InlineKeyboardButton(
            'Бесплатные кинотеатры🏴‍☠️', callback_data='freeCinema'))
        inline_kb_full.add(InlineKeyboardButton(
            'Отмена', callback_data='exit'))
        await bot.send_message(
            message.from_user.id,
            "➖➖➖➖➖➖➖➖➖➖➖➖\n✅Список онлайн кинотеатров📄\n➖➖➖➖➖➖➖➖➖➖➖➖",
            reply_markup=inline_kb_full)

    async def SendRandomFilm(bot, db, message):

        if (bot is None):
            print("Parameter 'bot' has not been assigned a value")
            return

        if (db is None):
            print("Parameter 'db' has not been assigned a value")
            return

        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

        with open("kinopoisk-top250.csv") as f_obj:
            (film, imageUrl) = Parser.GetDataFromCSV(f_obj)

        db.add_ACTIVE_TAB('False', message.from_user.id)
        await bot.send_photo(message.from_user.id, imageUrl, film)

    async def AboutUs(bot, db, message):

        if (bot is None):
            print("Parameter 'bot' has not been assigned a value")
            return

        if (db is None):
            print("Parameter 'db' has not been assigned a value")
            return

        db.add_ACTIVE_TAB('False', message.from_user.id)
        files = os.listdir("mem-img")
        image = open(
            "mem-img\\" + str(files[random.randint(0, (len(files) - 1))]), 'rb')

        await bot.send_photo(message.from_user.id, image)

    async def SendRules(bot, message):

        if (bot is None):
            print("Parameter 'bot' has not been assigned a value")
            return

        if (message is None):
            print("Parameter 'message' has not been assigned a value")
            return

        await bot.send_message(message.from_user.id,
                               "⚠️ Правила: "'[Ознакомиться](https://telegra.ph/MVbot-Pravila-03-03)',
                               parse_mode='Markdown')

    async def GetSmenaCinema(bot, db, jamDate, callback_query):

        if (bot is None):
            print("Parameter 'bot' has not been assigned a value")
            return

        if (db is None):
            print("Parameter 'db' has not been assigned a value")
            return

        if (jamDate is None):
            print("Parameter 'jamDate' has not been assigned a value")
            return

        if (callback_query is None):
            print("Parameter 'callback_query' has not been assigned a value")
            return

        db.add_jamSelect('True', callback_query.message.chat.id)
        dateMenu = InlineKeyboardMarkup(row_width=1)

        for tempBtn in jamDate:
            dateMenu.add(InlineKeyboardButton(
                str(tempBtn), callback_data=tempBtn))

        dateMenu.add(InlineKeyboardButton(
            'Назад', callback_data='goCinemaKirow'))

        await bot.delete_message(chat_id=callback_query.message.chat.id,
                                 message_id=callback_query.message.message_id)
        await bot.send_photo(callback_query.from_user.id, "https://telegra.ph/file/6566b9cd8a32675144e32.png",
                             "🍿Кинотеатр - КИНО Jam \n\n📍Адрес - ул. Горького, 5А.\n\nВыберете дату:",
                             reply_markup=dateMenu)

    async def GetFreeCinema(bot, db, callback_query):

        if (bot is None):
            print("Parameter 'bot' has not been assigned a value")
            return

        if (db is None):
            print("Parameter 'db' has not been assigned a value")
            return

        if (callback_query is None):
            print("Parameter 'callback_query' has not been assigned a value")
            return

        db.add_jamSelect('False', callback_query.message.chat.id)
        kinoepta = InlineKeyboardButton(
            'kino-epta.cc', url='https://kino-epta.cc/')
        lordFilm = InlineKeyboardButton(
            'LordFilm', url='https://r.10film.top/')
        fullsee = InlineKeyboardButton(
            'Fullsee', url='https://w1.fullsee.site/')
        hdfilmlenta = InlineKeyboardButton(
            'HDFilmLenta', url='https://www.hdfilmlenta.com/')
        tabfil = InlineKeyboardButton(
            'TABFILM', url='http://zq.tabfil.me/')

        cancelButton = InlineKeyboardButton('Назад', callback_data='goBack')
        menuCinema = InlineKeyboardMarkup(row_width=1)
        menuCinema.add(kinoepta, lordFilm, fullsee,
                       hdfilmlenta, tabfil, cancelButton)

        await bot.delete_message(chat_id=callback_query.message.chat.id,
                                 message_id=callback_query.message.message_id)
        await bot.send_photo(callback_query.from_user.id, "https://telegra.ph/file/7041abb4d4b71666a1659.png",
                             "🏴‍☠️Выберете любой сайт:", reply_markup=menuCinema)

    async def GetjamFilmsPanel(bot, db, jamDate, jam, callback_query, code):

        if (bot is None):
            print("Parameter 'bot' has not been assigned a value")
            return

        if (db is None):
            print("Parameter 'db' has not been assigned a value")
            return

        if (jamDate is None):
            print("Parameter 'jamDate' has not been assigned a value")
            return

        if (jam is None):
            print("Parameter 'jam' has not been assigned a value")
            return

        if (callback_query is None):
            print("Parameter 'callback_query' has not been assigned a value")
            return

        if (code is None):
            print("Parameter 'code' has not been assigned a value")
            return

        db.add_jamDay(0, callback_query.from_user.id)

        for date in jamDate:
            if date == code:
                db.add_Panel(0, callback_query.from_user.id)
                temp = jam[int(
                    str(db.check_jamDay(callback_query.from_user.id))[1:-2])]
                tempData = temp[int(
                    str(db.check_Panel(callback_query.from_user.id))[1:-2])]
                text = '🎬' + tempData["name"] + " (" + str(tempData["year"]) + ")🍿" + "\n\n🎭Категории: " + str(
                    tempData["genre"]) + "\n\n⌛️Продолжительность: " + tempData["duration"] + "\n\n📜Описание: " + \
                    tempData["description"]
                answer1 = InlineKeyboardButton(
                    '->', callback_data='smenaPanelRight')
                answer2 = InlineKeyboardButton(
                    'Назад', callback_data='smenaCinema')
                menu_p_1 = InlineKeyboardMarkup(row_width=2)
                menu_p_1.add(answer1, answer2)

                try:
                    await bot.delete_message(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id)
                except:
                    pass

                await bot.send_photo(callback_query.from_user.id, tempData["image"], text, reply_markup=menu_p_1)
                return
            else:
                db.add_jamDay(int(str(db.check_jamDay(callback_query.from_user.id))[1:-2]) + 1,
                              callback_query.from_user.id)

    async def GetPayCinemaCallback(bot, db, callback_query):

        if (bot is None):
            print("Parameter 'bot' has not been assigned a value")
            return

        if (db is None):
            print("Parameter 'db' has not been assigned a value")
            return

        if (callback_query is None):
            print("Parameter 'callback_query' has not been assigned a value")
            return

        db.add_jamSelect('False', callback_query.message.chat.id)
        findById = InlineKeyboardButton('Поиск фильма по ID 🔍', callback_data='findById')
        findbyName = InlineKeyboardButton('Поиск фильма по названию 🧩', callback_data='findByName')
        findPersonByName = InlineKeyboardButton('Поиск персоны по имени 🎎', callback_data='findPersonByName')
        findReviewById = InlineKeyboardButton('Поиск по отзывам', callback_data='findReviewById')
        cancel = InlineKeyboardButton('Назад', callback_data='goBack')
        menuCinema = InlineKeyboardMarkup(row_width=1)
        menuCinema.add(findById, findbyName, findPersonByName, findReviewById, cancel)

        await bot.delete_message(chat_id=callback_query.message.chat.id,
                                 message_id=callback_query.message.message_id)
        await bot.send_photo(callback_query.from_user.id, "https://telegra.ph/file/1f4ac49d339ef17e3b9bc.png",
                             "🎬Выберете действие:", reply_markup=menuCinema)

    async def GetPayCinemaMessage(bot, db, message):

        if (bot is None):
            print("Parameter 'bot' has not been assigned a value")
            return

        if (db is None):
            print("Parameter 'db' has not been assigned a value")
            return

        if (message is None):
            print("Parameter 'message' has not been assigned a value")
            return

        db.add_jamSelect('False', message.from_user.id)
        findbyId = InlineKeyboardButton('Поиск фильма по ID 🔍', callback_data='findById')
        findbyName = InlineKeyboardButton('Поиск фильма по названию 🧩', callback_data='findByName')
        findPersonByName = InlineKeyboardButton('Поиск персоны по имени 🎎', callback_data='findPersonByName')
        findReviewById = InlineKeyboardButton('Поиск по отзывам', callback_data='findReviewById')
        otmena = InlineKeyboardButton('Назад', callback_data='goBack')
        menuCinema = InlineKeyboardMarkup(row_width=1)
        menuCinema.add(findbyId, findbyName, findPersonByName, findReviewById, otmena)

        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await bot.send_photo(message.from_user.id, "https://telegra.ph/file/1f4ac49d339ef17e3b9bc.png", "🎬Выберете действие:", reply_markup=menuCinema)

    async def GetCinemaKirow(bot, db, callback_query):

        if (bot is None):
            print("Parameter 'bot' has not been assigned a value")
            return

        if (db is None):
            print("Parameter 'db' has not been assigned a value")
            return

        if (callback_query is None):
            print("Parameter 'callback_query' has not been assigned a value")
            return

        db.add_jamSelect('False', callback_query.message.chat.id)
        smenaCinema = InlineKeyboardButton(
            'КИНОjam🗿', callback_data='smenaCinema')
        cancel = InlineKeyboardButton('Отмена', callback_data='exit')
        menuCinema = InlineKeyboardMarkup(row_width=1)
        menuCinema.add(smenaCinema, cancel)

        await bot.delete_message(chat_id=callback_query.message.chat.id,
                                 message_id=callback_query.message.message_id)
        await bot.send_photo(callback_query.from_user.id, "https://telegra.ph/file/f298b205ec7551b2fb740.jpg",
                             "🎬Выберете желаемый кинотеатр:", reply_markup=menuCinema)

    async def ScrollFrirendPanel(bot, db, callback_query, direction, inpArray, panelLeft, panelRight, backCinema):

        if (bot is None):
            print("Parameter 'bot' has not been assigned a value")
            return

        if (db is None):
            print("Parameter 'db' has not been assigned a value")
            return

        if (callback_query is None):
            print("Parameter 'callback_query' has not been assigned a value")
            return

        if (direction is None):
            print("Parameter 'direction' has not been assigned a value")
            return

        if (inpArray is None):
            print("Parameter 'inpArray' has not been assigned a value")
            return

        if (panelLeft is None):
            print("Parameter 'panelLeft' has not been assigned a value")
            return

        if (panelRight is None):
            print("Parameter 'panelRight' has not been assigned a value")
            return

        if (backCinema is None):
            print("Parameter 'backCinema' has not been assigned a value")
            return

        buttonLeft = InlineKeyboardButton('<-', callback_data=panelLeft)
        buttonRight = InlineKeyboardButton('->', callback_data=panelRight)
        backButton = InlineKeyboardButton('Назад', callback_data=backCinema)
        mainMenu = InlineKeyboardMarkup(row_width=2)

        if direction == "Left":
            if (int(str(db.check_Panel(callback_query.from_user.id))[1:-2]) - 1 <= 0):
                db.add_Panel(int(str(db.check_Panel(callback_query.from_user.id))[
                    1:-2]) - 1, callback_query.from_user.id)
                mainMenu.add(buttonRight, backButton)
            else:
                db.add_Panel(int(str(db.check_Panel(callback_query.from_user.id))[
                    1:-2]) - 1, callback_query.from_user.id)
                mainMenu.add(buttonLeft, buttonRight, backButton)
        else:
            if (int(str(db.check_Panel(callback_query.from_user.id))[1:-2]) + 2 == len(
                    inpArray[int(str(db.check_jamDay(callback_query.from_user.id))[1:-2])])):
                db.add_Panel(int(str(db.check_Panel(callback_query.from_user.id))[
                    1:-2]) + 1, callback_query.from_user.id)
                mainMenu.add(buttonLeft, backButton)
            else:
                if (int(str(db.check_Panel(callback_query.from_user.id))[1:-2]) + 1 >= len(
                        inpArray[int(str(db.check_jamDay(callback_query.from_user.id))[1:-2])])):
                    db.add_Panel(int(str(db.check_Panel(callback_query.from_user.id))[1:-2]) + 1,
                                 callback_query.from_user.id)
                    mainMenu.add(buttonLeft, backButton)
                else:
                    db.add_Panel(int(str(db.check_Panel(callback_query.from_user.id))[1:-2]) + 1,
                                 callback_query.from_user.id)
                    mainMenu.add(buttonLeft, buttonRight, backButton)
        try:
            temp = inpArray[int(
                str(db.check_jamDay(callback_query.from_user.id))[1:-2])]
            tempData = temp[int(
                str(db.check_Panel(callback_query.from_user.id))[1:-2])]
        except:
            await bot.answer_callback_query(
                callback_query.id,
                text='Больше фильмов нету😊', show_alert=True)
            return
        textFromMessage = '🎬' + tempData["name"] + " (" + str(tempData["year"]) + ")🍿" + "\n\n🎭Категории: " + str(
            tempData["genre"]) + "\n\n⌛️Продолжительность: " + tempData["duration"] + "\n\n📜Описание: " + tempData[
            "description"]
        try:
            await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
        except:
            pass
        try:
            await bot.send_photo(callback_query.from_user.id, tempData["image"], textFromMessage, reply_markup=mainMenu)
        except:
            await bot.send_photo(callback_query.from_user.id, "https://telegra.ph/file/a07d88d27b07a185d0d9f.png", textFromMessage,
                                 reply_markup=mainMenu)