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

# web crawler
def crawler_thread(frontier, pages, visited):
    # while there are still pages to visit
    while len(frontier) != 0:
        # get the first page in the queue
        url = frontier.pop(0)
        # mark it as visited
        visited.add(url)
        print("visiting", url)
        # get the html of the page
        html = get_html(url)
        # if the html was retrieved:
        if html:
            # store the page data in the database
            store_page(pages, url, html, False)
            # if the page is the target:
            if check_target(html):
                # update the database record
                store_page(pages, url, html, True)
                # clear frontier to stop the web crawler
                frontier = []
            # if the page wasn't the target:
            else:
                # get all links on the page
                links = get_links(html)
                # add unvisited links to the frontier
                for link in links:
                    if link not in visited:
                        frontier.append(link)

# get the html from a url
def get_html(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(e)
    except URLError as e:
        print(url, "could not be found", e)
    else:
        # if html successfully retrieved, return it
        return html.read().decode('utf-8')
    # if any errors happened, return nothing
    return ""

# check if page is the target page
def check_target(html):
    bs = BeautifulSoup(html, "html.parser")
    return bs.find("h1", {"class": "cpp-h1"}, string="Permanent Faculty")

# get all links from a page
def get_links(html):
    bs = BeautifulSoup(html, "html.parser")
    # find all anchor tags and grab their links
    links = [tag["href"] for tag in bs.find_all("a")]
    for i in range (len(links)-1):
        # if this is a relative link, add the base link
        if links[i][0] == "/":
            links[i] = "https://www.cpp.edu" + links[i]
    # remove all links that are not from cpp
    links = [link for link in links if "https://www.cpp.edu/" in link]
    return links

# store a page in the database
def store_page(col, url, html, target):
    document = { "url": url,
                 "html": html,
                 "target": target
    }
    # use upsert to handle both new entries and updates
    col.update_one({"_id": url}, {"$set": {"url": url, "html": html, "target": target}}, True)

# connect to the database
def connect_database():
    client = MongoClient(host="localhost", port=27017)
    db = client.assignment3
    return db

def main():
    # connect to database and set up frontier url plus visited set
    db = connect_database()
    pages = db["pages"]
    visited = set()
    frontier = ["https://www.cpp.edu/sci/computer-science/"]
    # call crawler
    crawler_thread(frontier, pages, visited)

if __name__  == "__main__":
    main()
