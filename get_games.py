from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import csv 

url = 'https://www.epicgames.com/store/en-US/free-games'

option = Options()
option.headless = True
driver = webdriver.Firefox(options=option)
driver.get(url)

try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.css-7z9jo1-OfferCard__content'))
    )

    elements = driver.find_elements_by_css_selector('.css-53yrcz-CardGridDesktopLandscape__cardWrapperDesktop')
    
    game_list = []    
    for element in elements:
        status_tag = element.find_element_by_tag_name('a')
        status_text = status_tag.get_attribute('aria-label')
        if 'Free Now' in status_text: 
            game_name = element.find_element_by_css_selector('.css-2ucwu').text
            game_link = status_tag.get_attribute('href')
            game_list.append([game_name, game_link])             


    # write to csv file if there are new games
    if game_list:
        with open('new_games.csv', 'w') as f:
            csv_writer = csv.writer(f)
            for game in game_list:
                csv_writer.writerow(game)

finally:
    driver.quit()
