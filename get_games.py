import csv
from datetime import datetime

import pytz
import requests

request_url = "https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions?locale=en-US&country=US&allowCountries=US"
game_base_url = "https://store.epicgames.com/en-US/p/"


def get_all_games(url):
    res = requests.get(url)
    request_json = res.json()
    return request_json['data']['Catalog']['searchStore']['elements']


def find_free_now(game):
    if game['promotions'] is None or len(game['promotions']['promotionalOffers']) < 1:
        return False
    else:
        game_date_info = game['promotions']['promotionalOffers'][0]['promotionalOffers'][0]
        full_start_date = datetime.strptime(game_date_info['startDate'], '%Y-%m-%dT%H:%M:%S.%f%z')

        full_end_date = datetime.strptime(game_date_info['endDate'], '%Y-%m-%dT%H:%M:%S.%f%z')
        end_date = full_end_date
        end_hour = full_end_date.time()

        if (datetime.utcnow().replace(tzinfo=pytz.utc) < end_date and
                game['price']['totalPrice']['fmtPrice']['intermediatePrice'] == '0'
        ):
            end_datetime = f"{end_date.strftime('%d %B %Y')} at {end_hour.strftime('%H:%M')} - {end_date.tzinfo}"
            game_url = game_base_url + game['catalogNs']['mappings'][0]['pageSlug']
            return [game['title'], game_url, end_datetime]
        else:
            return False


if __name__ == '__main__':
    all_game = get_all_games(request_url)
    game_list = []
    for item in all_game:
        result = find_free_now(item)
        if result:
            game_list.append(result)
    print(game_list)
    # write to csv file if there are new games
    if game_list:
        with open('new_games.csv', 'w') as f:
            csv_writer = csv.writer(f)
            for game in game_list:
                csv_writer.writerow(game)
