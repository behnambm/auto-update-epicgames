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

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.firefox.options import Options
# from selenium.common.exceptions import NoSuchElementException
# import csv
#
# url = 'https://www.epicgames.com/store/en-US/free-games'
#
# option = Options()
# option.headless = True
# driver = webdriver.Firefox(options=option)
# driver.get(url)
#
# try:
#     WebDriverWait(driver, 20).until(
#         EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[4]/main/div[3]/div/div/div/div/div[2]/span/div/div/section/div/div[1]'))
#     )
#
#     elements = driver.find_elements_by_xpath('/html/body/div[1]/div/div[4]/main/div[3]/div/div/div/div/div[2]/span/div/div/section/div/div')
#
#     game_list = []
#     for element in elements:
#         try:
#             status_tag = element.find_element_by_tag_name('a')
#             status_text = status_tag.find_element_by_css_selector('span.css-os6fbq')
#         except NoSuchElementException:
#             continue
#         if status_text and 'Free Now' in status_text.text:
#             game_name = element.find_element_by_css_selector('.css-2ucwu').text
#             free_until = status_text.text.split(' - ')[1]
#             game_link = status_tag.get_attribute('href')
#             game_list.append([game_name, game_link, free_until])
#
#
#     # write to csv file if there are new games
#     if game_list:
#         with open('new_games.csv', 'w') as f:
#             csv_writer = csv.writer(f)
#             for game in game_list:
#                 csv_writer.writerow(game)
#
# finally:
#     driver.quit()
