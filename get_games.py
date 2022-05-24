import csv
from datetime import datetime

import pytz
import requests

request_url = "https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions?locale=en-US&country=US&allowCountries=US"
game_base_url = "https://store.epicgames.com/en-US/p/"


def get_all_games(url):
    res = requests.get(url)
    request_json = res.json()
    elements = request_json['data']['Catalog']['searchStore']['elements']
    free_now = []
    for element in elements:
        if len(element['promotions'].get('promotionalOffers', [])) > 0:
            free_now.append(element)
    return free_now


def get_game_info(game_element):
    promotional_offer = game_element['promotions']['promotionalOffers'][0]['promotionalOffers'][0]
    offer_end_date = datetime.strptime(promotional_offer['endDate'], '%Y-%m-%dT%H:%M:%S.%f%z')
    offer_end_date_utc = offer_end_date.replace(tzinfo=pytz.UTC)

    end_date = offer_end_date_utc.strftime('%d %B %Y')
    end_hour = offer_end_date_utc.strftime('%H:%M')

    end_datetime_str = f"{end_date} at {end_hour} - {offer_end_date_utc.tzinfo}"
    game_url = game_base_url + game_element['productSlug']
    return [game_element['title'], game_url, end_datetime_str]


def is_free(game_element):
    if not game_element['promotions']:
        return False
    if not game_element['promotions']['promotionalOffers']:
        return False

    promotional_offer = game_element['promotions']['promotionalOffers'][0]['promotionalOffers'][0]
    offer_end_date = datetime.strptime(promotional_offer['endDate'], '%Y-%m-%dT%H:%M:%S.%f%z')
    offer_end_date_utc = offer_end_date.replace(tzinfo=pytz.UTC)

    now = datetime.now().replace(tzinfo=pytz.UTC)
    game_price = game_element['price']['totalPrice']['fmtPrice']['intermediatePrice']
    if now < offer_end_date_utc and game_price == '0':
        return True

    return False


if __name__ == '__main__':
    all_games = get_all_games(request_url)
    game_list = []
    for game in all_games:
        game_info = get_game_info(game)
        if game_info:
            game_list.append(game_info)

    print(game_list)
    # write to csv file if there are new games
    if game_list:
        with open('new_games.csv', 'w') as f:
            csv_writer = csv.writer(f)
            for game in game_list:
                csv_writer.writerow(game)
