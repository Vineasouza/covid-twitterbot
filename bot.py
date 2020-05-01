import tweepy
import settings
import requests
import datetime 
import os
from bs4 import BeautifulSoup
from threading import Timer
from flask import Flask

app = Flask(__name__)

# keys de validação
CONSUMER_KEY = settings.ENV['CONSUMER_KEY']
CONSUMER_SECRET = settings.ENV['CONSUMER_SECRET']
ACCESS_KEY = settings.ENV['ACCESS_KEY']
ACCESS_SECRET = settings.ENV['ACCESS_SECRET']

# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# getting data
url = "https://www.worldometers.info/coronavirus/country/brazil/"
r = requests.get(url)
s = BeautifulSoup(r.text,"html.parser")
data = s.find_all("div",class_ = "maincounter-number")

# console log
#print(now.strftime("%Y-%m-%d %H:%M:%S") + "\nTotal Casos: "+ data[0].text.strip() + "\nTotal Mortes: " + data[1].text.strip () + "\nTotal Recuperados: " + data[2].text.strip())

@app.route("/")
# tweet stats
def tweet():
    #getting date
    now = datetime.datetime.now()

    api.update_status("--⏱" + now.strftime("%Y-%m-%d %H:%M:%S") + "🇧🇷--" + "\nTotal Casos: "+ data[0].text.strip() + "\nTotal Mortes: " + data[1].text.strip () + "\nTotal Recuperados: " + data[2].text.strip())

    print("tweetado " + now.strftime("%Y-%m-%d %H:%M:%S"))

    Timer(7200.0, tweet).start()

Timer(7200.0, tweet).start()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    app.run(host='0.0.0.0', port=port)