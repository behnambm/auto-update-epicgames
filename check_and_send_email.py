import csv 
import smtplib
import ssl 
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#====================================== get env variables
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
RECEIVER = os.environ['RECEIVER']

#====================================== read old & new games from csv files
old_games = []
with open('old_games.csv', 'r') as f:
    csv_reader = csv.reader(f)
    for game in csv_reader:
        old_games.append(game)
old_games_name = [game[0] for game in old_games] # 1st index is game_name & 2nd index is game_link
#--------------------
new_games = []
with open('new_games.csv', 'r') as f:
    csv_reader = csv.reader(f)
    for game in csv_reader:
        new_games.append(game)
new_games_name = [game[0] for game in new_games]

# ===================================== check for new games
send_email = False

for game in new_games_name:
    if game not in old_games_name:
        send_email = True

# ===================================== send email
if send_email:
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "🔥New Free Games🎮 🔥"
    msg['From'] = EMAIL_HOST_USER
    msg['To'] = RECEIVER

    text = f"New Games => {' --- '.join(new_games_name)}"
    html = f"""\
    <html>
    <head></head>
    <body>
        <p>
        <h1>Free Games 🎮</h1>
    """

    for game in new_games:
        html += f"""
            <a href={game[1]} style="font-size: 1.2rem;">{game[0]}</a>
            <br>
        """

    html += "</p></body></html>"

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            # use default CA certificates on system to prevent auth errors
            context = ssl.create_default_context() 
            server.starttls(context=context)

            server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

            server.sendmail(EMAIL_HOST_USER, RECEIVER, msg.as_string())
            server.close()

        # update `old_games.csv` 
        with open('old_games.csv', 'w') as f:
            csv_writer = csv.writer(f)
            for game in new_games:
                csv_writer.writerow(game)

    except Exception as e:
        print(e)
