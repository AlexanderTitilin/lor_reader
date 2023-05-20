import requests
import markdownify
import re
import datetime
from itertools import chain
from article import Article
from bs4 import BeautifulSoup

URL = "https://www.linux.org.ru"


def get_news(url=URL):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return [Article(*(article.find("h1").find("a").text,
               URL+article.find("h1").find("a").get("href"),
               makeDate(article.find("time").get("datetime")))) for article in soup.findAll("article", class_="msg")]


def get_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.find("div", itemprop="articleBody")


def get_news_by_tag(tag):
    url = f"https://www.linux.org.ru/search.jsp?q={tag}&range=TOPICS&interval=ALL&user=&_usertopic=on&sort=RELEVANCE&section=news&group=&offset="
    try:
        return sorted( list(chain.from_iterable([get_news(url+str(i)) for i in range(0,count_news(tag) // 25,25)])),key=lambda x: x.date,reverse=True)
    except:
        return []


def save_article(url, name):
    with open(f"{name}.md", "w") as f:
        articleText = get_text(url).text
        f.write(markdownify.markdownify(articleText))


def makeDate(s):
    d = datetime.date(
        *map(int, re.findall(r"\d{4}-\d{2}-\d{2}", s)[0].split("-")))
    return d


def count_news(tag):
    url = f"https://www.linux.org.ru/search.jsp?q={tag}&range=TOPICS&interval=ALL&user=&_usertopic=on&sort=RELEVANCE&section=news&group=&offset=0"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return int(re.findall(r"\d* результатов", soup.text)[0].split()[0]
               )


if __name__ == "__main__":
    print(sorted(get_news_by_tag("python"),key =lambda x: x.date,reverse=True))
