from csv import writer
import nltk
import json
from newspaper import Article
from datetime import datetime
import re
from time import sleep
from bs4 import BeautifulSoup
import requests

search_subject = input('What would you like to search for? ')

template = 'https://news.search.yahoo.com/search?p={}'

url = template.format(search_subject)

headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'referer': 'https://www.google.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44'
}

responce = requests.get(url, headers = headers)
soup = BeautifulSoup(responce.text, 'html.parser')
cards = soup.find_all('div', 'NewsArticle')

links = []
for card in cards:
    link = card.find('a').get('href')
    clean_link = requests.utils.unquote(link)
    pattern = re.compile(r'RU=(.+)\/RK')
    source_link = re.search(pattern, clean_link).group(1)
    links.append(source_link)


def get_article(url):
    article = Article(url)
    # do some nlp
    article.download()
    article.parse()
    # nltk.download('punkt')
    article.nlp()

    authers = article.authors    
    publish_date = str(article.publish_date)
    str_published_date = (str(publish_date))
    image = article.top_image
    article_full_text = article.text
    article_summery = article.summary
    article_headline = article.title


    data = {
        'Auther(s)': authers,
        'Publish Date': str_published_date,
        'Title': article_headline,
        'Summery': article_summery,
        'Article Link': url,
        'Image Link': image,
        'Article': article_full_text
    }

    with open('articles/'+search_subject+'-'+str(datetime.now())+'.txt', 'w') as outfile:
        json.dump(data, outfile, indent=4)


for link in links:
    try:
        get_article(link)
    except:
        pass



