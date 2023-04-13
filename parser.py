import json
import requests
import json
import random
import csv
from random import randint
from stringValidation import StringValidation
from datetime import date, timedelta

HEADERS = {
    'Accept': '*/*',
    'Content-Type': 'application/JSON',
    'Host': 'kinokassa.kinoplan24.ru',
    'Origin': 'https://kirov.kinojam.club/',
    'user_agent': 'generate_user_agent()',
    'X-Application-Token': '08sSh6VKlsapX8N3MVedOsHRMuddKi1q',
    'X-Platform': 'widget'
}

class Parser:
    def GetDataFromCSV(file):
        reader = csv.DictReader(file, delimiter=';')
        tempArray = []
        filmArray = []

        for line in reader:
            tempArray.append(
                f"🎬Место в списке: {line['rating']}\n" +
                f"\n🔮Название: {line['movie']}\n" +
                f"\n🎭Описание: {StringValidation.ShortenText(line['overview'], 180)}\n" +
                f"\n⌛️Год выпуска: {line['year']}\n" +
                f"🎲Рейтинг: {line['rating_ball']}\n" +
                f"📜Страна: {line['country']}\n" +
                f"🎨Режиссер: {line['director']}\n" +
                f"🎥Сценарист: {line['screenwriter']}\n" +
                f"\n🎎Актеры: {line['actors']}")

            filmArray.append(line['url_logo'])
        randValue = randint(0, 249)
        url = filmArray[randValue]
        return tempArray[randValue], url[1:-1]

    def JsonInitParce(jsonName):
        with open(jsonName, "r", encoding='utf-8') as read_file:
            data = json.load(read_file)
        iter = 0
        tempArray = []
        tempDate = []
        tempDays = []
        for temp in data:
            jsonData = data.get(temp)
            tempDate.append(str(temp))
            tempDays.append(len(jsonData))
            tempArray.append([])
            for item in jsonData:
                tempArray[iter].append(
                    {
                        "name": item.get("name"),
                        "id": item.get("id"),
                        "genre": StringValidation.GenreStrValidation(item.get("genre")),
                        "description": StringValidation.ShortenText(item.get("description"), 145),
                        "countries": item.get("countries"),
                        "cast": item.get("cast"),
                        "directors": item.get("directors"),
                        "duration": item.get("duration"),
                        "year": item.get("year"),
                        "rating": item.get("rating"),
                        "image": item.get("image"),
                        "seances": item.get("seances")
                    })
            iter += 1
        return tempArray, tempDate, tempDays
    
    def Actualization_Data(jam, jamDate, jamDays):
        
        (jam, jamDate, jamDays) = Parser.JsonInitParce("C:\\Jam.json")
        return jam, jamDate, jamDays
        #(drusba, drusbaDate, drusbaDays) = JsonInitParce("Druzhba.json");
        #(jam, jamDate, jamDays) = MV_PARSER.get_json_Jam();
        #Actualization_InProcess = False
    
    
    
    #def get_json_Jam():
    #    day = 0
    #    information_dict = {}
    #    print(f'Дата запроса на парсер - {date.today()}')
    #    while True:
    #        URL = f'https://kinokassa.kinoplan24.ru/api/v2/release/playbill?city_id=83&date={date.today() + timedelta(days=day)}'
    #        r = requests.get(url=URL, headers=HEADERS)
    #        data = r.json()
             #if data['releases']:
             #    #print(f'Дата {date.today() + timedelta(days=day)}')
             #    data = data['releases']
             #    result = []
             #    for item in data:
             #        #print(f'[INFO] Обработка фильма: {data.index(item) + 1}/{len(data)}')
             #        film_url = f"https://kinokassa.kinoplan24.ru/api/v2/release/{item['id']}?city_id=83"
             #        r = requests.get(url=film_url, headers=HEADERS)
             #        film_data = r.json()
             #        result.append(
             #            {
             #                'name': item['title'],
             #                'id': item['id'],
             #                'genre': [item['title'] for item in item['genres']] if item['genres'] else 'Не указан',
             #                'description': film_data['release']['description'],
             #                'countries': [item['title'] for item in film_data['release']['countries']],
             #                'cast': [item['title'] for item in film_data['release']['cast']],
             #                'directors': [item['title'] for item in film_data['release']['directors']],
             #                'duration': f"{film_data['release']['duration']} мин.",
             #                'year': film_data['release']['year'],
             #                'rating': {
             #                    'Кинопоиск': film_data['release']['rating']['kinopoisk'] if 'kinopoisk' in
             #                                                                                film_data['release'][
             #                                                                                    'rating'].keys() else 'Нет',
             #                    'IMDB': film_data['release']['rating']['imdb'] if 'imdb' in film_data['release'][
             #                        'rating'].keys() else 'Нет'
             #                },
             #                'image': item['poster'],
             #                'seances': {
             #                    'seance_time':
             #                        [item['start_date_time'][11:16] for item in item['seances']] if item[
             #                            'seances'] else 'Нет на указанную дату',
             #                    'seance_price':
             #                        [item['price']['max'] / 100 for item in item['sean'
             #                                                                    'ces']] if item[
             #                            'seances'] else 'Нет на указанную дату',
             #                    'seance_hall': [item['hall']['title'] for item in item['seances']] if item[
             #                        'seances'] else 'Нет'
             #                }

             #            }
             #        )
             #    information_dict[f'{date.today() + timedelta(days=day)}'] = result
             #    day += 1
             #else:
             #    with open('Jam.json', 'w', encoding='utf-8') as file:
             #        json.dump(information_dict, file, indent=4, ensure_ascii=False)
             #    with open("Jam.json", "r", encoding='utf-8') as read_file:
             #        data = json.load(read_file)
             #    iter = 0
             #    tempArray = []
             #    tempDate = []
             #    tempDays = []
             #    for temp in data:
             #        jsonData = data.get(temp)
             #        tempDate.append(str(temp))
             #        tempDays.append(len(jsonData))
             #        tempArray.append([])
             #        for item in jsonData:
             #            tempArray[iter].append(
             #                {
             #                    "name": item.get("name"),
             #                    "id": item.get("id"),
             #                    "genre": getGenreStr(item.get("genre")),
             #                    "description": getValidStr(item.get("description")),
             #                    "countries": item.get("countries"),
             #                    "cast": item.get("cast"),
             #                    "directors": item.get("directors"),
             #                    "duration": item.get("duration"),
             #                    "year": item.get("year"),
             #                    "rating": item.get("rating"),
             #                    "image": item.get("image"),
             #                    "seances": item.get("seances")
             #                })
             #        iter += 1
             #    print("Парсер отработал")
             #    return tempArray, tempDate, tempDays;
