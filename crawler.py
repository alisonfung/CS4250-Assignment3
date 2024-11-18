#-------------------------------------------------------------------------
# AUTHOR: Alison Fung
# FILENAME: crawler.py
# SPECIFICATION: Crawls the CPP CS website until finding the faculty page.
# FOR: CS 4250- Assignment #3
# TIME SPENT: 2 hours
#-----------------------------------------------------------*/

from bs4 import BeautifulSoup
from pymongo import MongoClient
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

def crawler_thread(frontier, pages, visited):
    while len(frontier) != 0:
        url = frontier.pop(0)
        visited.add(url)
        print("visiting", url)
        html = get_html(url)
        if html:
            store_page(pages, url, html, False)
            if check_target(html):
                store_page(pages, url, html, True)
                frontier = []
            else:
                links = get_links(html)
                for link in links:
                    if link not in visited:
                        frontier.append(link)
                #print("need to visit", frontier)


def get_html(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(e)
    except URLError as e:
        print(url, "could not be found", e)
    else:
        return html.read().decode('utf-8')
    return ""

def check_target(html):
    bs = BeautifulSoup(html, "html.parser")
    return bs.find("h1", {"class": "cpp-h1"}, string="Permanent Faculty")

def get_links(html):
    bs = BeautifulSoup(html, "html.parser")
    links = [tag["href"] for tag in bs.find_all("a")]
    for i in range (len(links)-1):
        if links[i][0] == "/":
            links[i] = "https://www.cpp.edu" + links[i]
    for link in links:
        links = [link for link in links if "https://www.cpp.edu/" in link]
    return links

def store_page(col, url, html, target):
    # store page
    document = { "url": url,
                 "html": html,
                 "target": target
    }
    col.update_one({"_id": url}, {"$set": {"_id": url, "html": html, "target": target}}, True)

def connect_database():
    client = MongoClient(host="localhost", port=27017)
    db = client.assignment3
    return db

def main():
    db = connect_database()
    pages = db["pages"]
    visited = set()
    frontier = ["https://www.cpp.edu/sci/computer-science/"]
    crawler_thread(frontier, pages, visited)

if __name__  == "__main__":
    main()
