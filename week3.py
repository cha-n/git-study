import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20201021',headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

songinfos = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

for songinfo in songinfos:
    rank = songinfo.select_one('td.number').text[0:2].strip()
    title = songinfo.select_one('td.info > a.title.ellipsis').text.strip()
    artist = songinfo.select_one('td.info > a.artist.ellipsis').text
    print(rank, title, artist)

    doc = {
        'rank': rank,
        'title': title,
        'artist': artist
    }

    db.genie_chart.insert_one(doc)