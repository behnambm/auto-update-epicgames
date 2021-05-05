# -*- coding: utf-8 -*-
from telegram.ext import Updater
import os
import csv 

#====================================== get env variables
TOKEN = os.environ['BOT_TOKEN'] 

#====================================== read old & new games from csv files
old_games = []
with open('old_games.csv', 'r') as f:
    csv_reader = csv.reader(f)
    for game in csv_reader:
        old_games.append(game)
old_games_name = [game[0] for game in old_games] # 1st index is game_name 
#--------------------
new_games = []
with open('new_games.csv', 'r') as f:
    csv_reader = csv.reader(f)
    for game in csv_reader:
        new_games.append(game)
new_games_name = [game[0] for game in new_games]

# ===================================== check for new games
update_channel = False

for game in new_games_name:
    if game not in old_games_name:
        update_channel = True

# ===================================== update channel
if update_channel:
    updater = Updater(token=TOKEN)

    for game in new_games:
        msg = f"🤖Automatic update🤖\n\n🔥 {game[0]} 🔥\n\n⏳Free until: {game[2]} \n\n\n{game[1]}"
        updater.bot.send_message(chat_id='@epicgames_free', text=msg)

    # update `old_games.csv` 
    with open('old_games.csv', 'w') as f:
        csv_writer = csv.writer(f)
        for game in new_games:
            csv_writer.writerow(game)
