import os
import tweepy
import settings
import requests
import datetime 
import os
from pytz import timezone
from bs4 import BeautifulSoup
from threading import Timer
from flask import Flask

app = Flask(__name__)

# keys de validação
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_KEY = os.environ.get('ACCESS_KEY')
ACCESS_SECRET = os.environ.get('ACCESS_SECRET')

# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

@app.route("/")
# tweet stats
def tweet1():
    #getting date
    now = datetime.datetime.now()
    fuso_horario = timezone('America/Sao_Paulo')
    nowtime = now.astimezone(fuso_horario)

    # getting data from brazil
    url = "https://www.worldometers.info/coronavirus/country/brazil/"
    r = requests.get(url)
    s = BeautifulSoup(r.text,"html.parser")
    data = s.find_all("div",class_ = "maincounter-number")

    # getting data from world
    url2 = "https://www.worldometers.info/coronavirus/"
    r2 = requests.get(url2)
    s2 = BeautifulSoup(r2.text,"html.parser")
    data2 = s2.find_all("div",class_ = "maincounter-number")

    api.update_status("--" + nowtime.strftime("%Y-%m-%d %H:%M:%S") + "--" + "\n\nTotal Casos: 🇧🇷 "+ data[0].text.strip() + " // 🌎 " + data2[0].text.strip() + "\nTotal Mortes: 🇧🇷 " + data[1].text.strip() + " // 🌎 " + data2[1].text.strip() + "\nTotal Recuperados: 🇧🇷 " + data[2].text.strip()+ " // 🌎 " + data2[2].text.strip())

    print("tweetado1" + nowtime.strftime("%Y-%m-%d %H:%M"))

    Timer(300.0, tweet2).start()

def tweet2():
    #getting date
    now = datetime.datetime.now()
    fuso_horario = timezone('America/Sao_Paulo')
    nowtime = now.astimezone(fuso_horario)

    #getting data
    url = "https://www.worldometers.info/coronavirus/country/brazil/"
    r = requests.get(url)
    s = BeautifulSoup(r.text,"html.parser")
    data_name = s.find_all("div",class_ = "number-table-main")
    data_name2 = s.find_all("span",class_ = "number-table")

    api.update_status("--" + nowtime.strftime("%Y-%m-%d %H:%M:%S") + "--" + "\n\nCasos ativos 🇧🇷\nAtualmente infectados: " + data_name[0].text.strip() + "\nEm condições suaves: " + data_name2[0].text.strip() + " (" + data_name2[0].next_sibling.next_sibling.text.strip() + "%)\nSério ou Crítico: " + data_name2[1].text.strip() + " (" + data_name2[1].next_sibling.next_sibling.text.strip() + "%)\n\nCasos fechados 🇧🇷\nCasos que tiveram um resultado: " + data_name[1].text.strip() + "\nRecuperados: " + data_name2[2].text.strip() + " (" + data_name2[2].next_sibling.next_sibling.text.strip() + "%)\nMortos: " + data_name2[3].text.strip() + " (" + data_name2[3].next_sibling.next_sibling.text.strip() + "%)")

    print("tweetado2" + nowtime.strftime("%Y-%m-%d %H:%M"))

    Timer(10800.0, tweet1).start()

def tweet():
    tweet1()

Timer(10800.0, tweet).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    app.run(host='0.0.0.0', port=port)