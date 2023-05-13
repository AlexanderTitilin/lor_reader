import requests
import markdownify
from article import Article
from bs4 import BeautifulSoup

URL = "https://www.linux.org.ru/news/"


def get_news(url=URL):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return [Article(URL[:-6] + n.find("a").get("href"), n.text.strip()) for n in soup.findAll("h1")[1::]]


def get_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.find("div", itemprop="articleBody")


def get_news_by_tag(tag):
    url = f"https://www.linux.org.ru/tag/{tag}"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        return get_news(url) + [Article(URL[:-6] + n.get("href"), n.text.strip()) for n in soup.find("div", id="tag-page-news").findAll("a")]
    except:
        return []


def save_article(url, name):
    with open(f"{name}.md","w") as f:
        articleText = get_text(url).text
        f.write(markdownify.markdownify(articleText))



if __name__ == "__main__":
    save_article("https://www.linux.org.ru/news/russia/17224117","djkdk")
