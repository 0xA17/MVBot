from inlineKeyboardEvent import InlineKeyboardEvent
from stringValidation import StringValidation
import requests
import json


class ApiOperation:
    async def FindFilmByName(DB, BOT, message, API_TOKEN):
        response = requests.get(
            f"https://api.kinopoisk.dev/movie?search={message.text}&field=name&token={API_TOKEN}")
        film = ApiOperation.APIReader(json.loads(response.text))
        # Если по рандомному вводу нет результатов
        if len(film[0]) == 0:
            await BOT.send_message(message.chat.id, "По Вашему запросу ничего не нашлось! 👀")
            DB.add_findByNameBool('False', message.from_user.id)
            await InlineKeyboardEvent.GetPayCinemaMessage(BOT, DB, message)
            return
        # Если найден один фильм
        elif len(film[0]) == 1:
            for item in film:
                text = f"🔮Название: {item[0]['name']}\n\n🎬Оригинальное имя: {item[0]['alternativeName']}\n\n🎲Рейтинг Кинопоиска: {item[0]['ratingKP']}\n\n🏆Рейтинг IMDB: {item[0]['ratingIM']}\n\n🎪Тип фильма: {item[0]['type']}\n\n🎭Описание: {item[0]['description']}\n\n⌛️Год выпуска: {item[0]['year']}"
                await BOT.send_photo(message.chat.id, item[0]["url"], text)
            DB.add_findByNameBool('False', message.from_user.id)
            await InlineKeyboardEvent.GetPayCinemaMessage(BOT, DB, message)
            return
        else:
            # Спамит всеми найденными фильмами
            countFilm = len(film[0])
            count = 0
            for item in film[0]:
                if count < countFilm:
                    text = f"🔮Название: {item['name']}\n\n🎬Оригинальное имя: {item['alternativeName']}\n\n🎲Рейтинг Кинопоиска: {item['ratingKP']}\n\n🏆Рейтинг IMDB: {item['ratingIM']}\n\n🎪Тип фильма: {item['type']}\n\n🎭Описание: {item['description']}\n\n⌛️Год выпуска: {item['year']}"
                    try:
                        await BOT.send_photo(message.chat.id, item["url"], text)
                    except:
                        pass
                    count += 1

            DB.add_findByNameBool('False', message.from_user.id)
            await InlineKeyboardEvent.GetPayCinemaMessage(BOT, DB, message)
            return

    async def FindPersonByName(DB, BOT, message, API_TOKEN):
        response = requests.get(
            # https://api.kinopoisk.dev/person?search=Лео&field=name&token=9tdyx0v-kj946kd-j7ea9bb-rm2yrfw
            f"https://api.kinopoisk.dev/person?search={message.text}&field=name&token={API_TOKEN}")
        film = ApiOperation.PersonReader(json.loads(response.text))
        if len(film[0]) == 0:
            await BOT.send_message(message.chat.id, "По Вашему запросу ничего не нашлось! 👀")
            DB.add_findPersonByName('False', message.from_user.id)
            await InlineKeyboardEvent.GetPayCinemaMessage(BOT, DB, message)
            return
        if response.status_code == 404:
            await BOT.send_message(message.chat.id, "Актёр отсутствует! 🥺")
            DB.add_findPersonByName('False', message.from_user.id)
            await InlineKeyboardEvent.GetPayCinemaMessage(BOT, DB, message)
            return
        elif len(film[0]) == 1:
            for item in film:
                text = f"🔮 Имя: {item[0]['name']}\n\n🎬Оригинальное имя: {item[0]['enName']}\n\n🎭Возраст: {item[0]['age']}\n\n⌛️Год выпуска: {item[0]['year']}"
                await BOT.send_photo(message.chat.id, item[0]["photo"], text)
            DB.add_findPersonByName('False', message.from_user.id)
            await InlineKeyboardEvent.GetPayCinemaMessage(BOT, DB, message)
            return
        else:
            # Спамит всеми найденными фильмами
            countFilm = len(film[0])
            count = 0
            for item in film[0]:
                if count < 2:
                    text = f"🔮 Имя: {item['name']}\n\n🎬Оригинальное имя: {item['enName']}\n\n🎭Возраст: {item['age']}\n\n"
                    try:
                        await BOT.send_photo(message.chat.id, item["photo"], text)
                    except:
                        pass
                    count += 1

            DB.add_findPersonByName('False', message.from_user.id)
            await InlineKeyboardEvent.GetPayCinemaMessage(BOT, DB, message)
            return

    async def FindFilmById(DB, BOT, message, API_TOKEN):
        DB.add_findByIdText(message.text, message.from_user.id)
        # Проверяем введенное число.
        if (str(DB.check_findByIdText(message.from_user.id))[1:-2]).isdigit():
            link = f"https://api.kinopoisk.dev/movie?search={StringValidation.SearchValidation(DB, message.from_user.id)}&field=id&token={API_TOKEN}"
            response = requests.get(link)
            await BOT.send_chat_action(message.chat.id, 'typing')

            # Если фильм отсутствует.
            if response.status_code == 404:
                await BOT.send_message(message.chat.id, "Фильм отсутствует! 🥺")
                DB.add_findByIdBool('False', message.from_user.id)
                await InlineKeyboardEvent.GetPayCinemaMessage(BOT, DB, message)
                return

            (film, url, persons, facts) = ApiOperation.API_ID_Reader(
                json.loads(response.text))

            # Если фактов нету, выводим без них.
            if len(facts) == 0:
                for line in film:
                    text = line + \
                           f"🎎Актеры: {persons[0]}, {persons[1]}, {persons[3]}.\n\n"
                await BOT.send_photo(message.chat.id, url, text)
                DB.add_findByIdBool('False', message.from_user.id)
                await InlineKeyboardEvent.GetPayCinemaMessage(BOT, DB, message)
                return
            # Если есть факты, выводим с ними.
            elif len(facts) != 0:
                for line in film:
                    text = line + \
                           f"🎎Актеры: {persons[0]}, {persons[1]}, {persons[3]}.\n\n" + \
                           f"🎁Факт: {facts[0]}\n"
                await BOT.send_photo(message.chat.id, url, text)
                DB.add_findByIdBool('False', message.from_user.id)
                await InlineKeyboardEvent.GetPayCinemaMessage(BOT, DB, message)
                return
        else:
            await BOT.send_message(message.chat.id, "Идентификатор не является корректным!")
            DB.add_findByIdBool('False', message.from_user.id)
            await InlineKeyboardEvent.GetPayCinemaMessage(BOT, DB, message)
            return

    async def FindReviewById(DB, BOT, message, API_TOKEN):
        DB.add_findReviewById('False', message.from_user.id)
        if (str(message.text)).isdigit():
            # if (str(DB.check_findReviewById(message.from_user.id))[1:-2]).isdigit():
            link = f"https://api.kinopoisk.dev/review?search={message.text}&field=movieId&token={API_TOKEN}"
            response = requests.get(link)
            reviews = ApiOperation.ReviewReader(json.loads(response.text))
            await BOT.send_chat_action(message.chat.id, 'typing')

            if len(reviews[0]) == 0:
                await BOT.send_message(message.chat.id, "По Вашему запросу ничего не нашлось! 👀")
                DB.add_findReviewById('False', message.from_user.id)
                await InlineKeyboardEvent.GetPayCinemaMessage(BOT, DB, message)
                return

            if response.status_code == 404:
                await BOT.send_message(message.chat.id, "Фильм отсутствует! 🥺")
                DB.add_findReviewById('False', message.from_user.id)
                await InlineKeyboardEvent.GetPayCinemaMessage(BOT, DB, message)
                return

            count = 0
            dlina = len(reviews[0])
            if len(reviews) != 0:
                for review in reviews[0]:
                    if count < dlina:
                        text = f"Автор: {review['author']}\n\nРейтинг автора: {review['userRating']}\n\nИдентификатор фильма: {review['movieId']}\n\nТип отзыва: {review['type']}\n\n" \
                               f"Заголовок: {review['type']}\n\nОтзыв: {StringValidation.ShortenText(review['review'], 4000)}\n\nКол-во дизлайков: {review['reviewDislikes']}\n\nКол-во лайков: {review['reviewLikes']}\n\n"
                        try:
                            await BOT.send_message(message.chat.id, text)
                        except:
                            pass
                        count += 1

                DB.add_findReviewById('False', message.from_user.id)
                await InlineKeyboardEvent.GetPayCinemaMessage(BOT, DB, message)
                return
        else:
            await BOT.send_message(message.chat.id, "Идентификатор не является корректным!")
            DB.add_findReviewById('False', message.from_user.id)
            await InlineKeyboardEvent.GetPayCinemaMessage(BOT, DB, message)
            return

    def ReviewReader(data):
        tempArray = []
        iter = 0
        for temp in data:
            jsonData = data['docs']
            tempArray.append([])
            for item in jsonData:
                tempArray[iter].append(
                    {
                        "userRating": item['userRating'],
                        "movieId": item['movieId'],
                        "title": item['title'],
                        "type": item['type'],
                        "review": item['review'],
                        "author": item['author'],
                        "reviewDislikes": item['reviewDislikes'],
                        "reviewLikes": item['reviewLikes'],
                    }
                )
            return tempArray

    def PersonReader(data):
        tempArray = []
        iter = 0
        for temp in data:
            jsonData = data['docs']
            tempArray.append([])
            for item in jsonData:
                tempArray[iter].append(
                    {
                        "name": item['name'],
                        "enName": item['enName'],
                        "age": item['age'],
                        "photo": item['photo']
                    }
                )
        return tempArray

    def APIReader(data):
        tempArray = []
        iter = 0
        for temp in data:
            jsonData = data['docs']
            tempArray.append([])
            for item in jsonData:
                if item['description'] is None:
                    if 'shortDescription' in jsonData:
                        tempArray[iter].append(
                            {
                                "name": item['name'],
                                "alternativeName": item['alternativeName'],
                                "ratingIM": item['rating']['imdb'],
                                "ratingKP": item['rating']['kp'],
                                "type": item['type'],
                                "description": item['shortDescription'],
                                "year": item['year'],
                                "url": item['poster']['url']
                            })
                    elif item['poster'] is not None:
                        tempArray[iter].append(
                            {
                                "name": item['name'],
                                "alternativeName": item['alternativeName'],
                                "ratingIM": item['rating']['imdb'],
                                "ratingKP": item['rating']['kp'],
                                "type": item['type'],
                                "description": 'Отсутствует!',
                                "year": item['year'],
                                "url": item['poster']['url']
                            })
                else:
                    if item['poster'] != None:
                        tempArray[iter].append(
                            {
                                "name": item['name'],
                                "alternativeName": item['alternativeName'],
                                "ratingIM": item['rating']['imdb'],
                                "ratingKP": item['rating']['kp'],
                                "type": item['type'],
                                "description": StringValidation.ShortenText(item['description'], 180),
                                "year": item['year'],
                                "url": item['poster']['url']
                            })
                    else:
                        tempArray[iter].append(
                            {
                                "name": item['name'],
                                "alternativeName": item['alternativeName'],
                                "ratingIM": item['rating']['imdb'],
                                "ratingKP": item['rating']['kp'],
                                "type": item['type'],
                                "description": StringValidation.ShortenText(item['description'], 180),
                                "year": item['year'],
                                "url": 'https://avatars.mds.yandex.net/get-kinopoisk-post-img/1374145/09792ccb925715f9b5d85fc22ed445d8/960'
                            })
            break
        return tempArray

    def API_ID_Reader(data):
        array = []
        facts = []
        persons = []
        count = 0
        url = data['poster']['url']
        # Ищем факты без HTML-разметки.
        try:
            for fact in data['facts']:
                if (fact['value'].find("href") == -1) and (fact['value'].find("&") == -1):
                    facts.append(fact['value'])
                    break
        except:
            pass
        # При наличии бюджета в фильме.
        if 'budget''value' in data:
            array.append(
                f"🔮Название: {data['name']}\n\n" +
                f"🎥Слоган: {data['slogan']}\n\n" +
                f"⌛️Год выпуска: {data['year']}\n" +
                f"🎲Рейтинг Кинопоиск: {data['rating']['kp']}\n" +
                f"🏆Рейтинг IMDB: {data['rating']['imdb']}\n" +
                f"💎Жанр: {data['genres'][0]['name']}\n" +
                f"📌Страна: {data['countries'][0]['name']}\n" +
                f"🎬Дистрибьютор: {data['distributors']['distributor']}\n" +
                f"💵Бюджет: {data['budget']['value']}-{data['budget']['currency']}\n")

        # При отсутствии бюджета в фильме.
        else:
            array.append(
                f"🔮Название: {data['name']}\n\n" +
                f"🎥Слоган: {data['slogan']}\n\n" +
                f"⌛️Год выпуска: {data['year']}\n" +
                f"🎲Рейтинг Кинопоиск: {data['rating']['kp']}\n" +
                f"🏆Рейтинг IMDB: {data['rating']['imdb']}\n" +
                f"💎Жанр: {data['genres'][0]['name']}\n" +
                f"📌Страна: {data['countries'][0]['name']}\n" +
                f"🎬Дистрибьютор: {data['distributors']['distributor']}\n")

        # Первые 5 актеров.
        for person in data['persons']:
            if count <= 3:
                persons.append(person['name'])
                count += 1

        return array, url, persons, facts
