import requests
import os
from dotenv import load_dotenv


def get_address_from_coords(coords):
    # заполняем параметры, которые описывались выже. Впиши в поле apikey свой токен!
    load_dotenv()
    PARAMS = {
        "apikey": str(os.getenv("ya_api")),
        "format": "json",
        "lang": "ru_RU",
        "kind": "house",
        "geocode": coords
    }

    # отправляем запрос по адресу геокодера.
    try:
        r = requests.get(url="https://geocode-maps.yandex.ru/1.x/", params=PARAMS)
        # получаем данные
        json_data = r.json()
        # вытаскиваем из всего пришедшего json именно строку с полным адресом.
        address_str = json_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["AddressDetails"]["Country"]["AddressLine"]
        # возвращаем полученный адрес
        return address_str
    except Exception as e:
        # если не смогли, то возвращаем ошибку
        return e
