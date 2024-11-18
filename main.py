import bs4
import pymongo
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

page_number = -1
frontier = ["https://www.cpp.edu/sci/computer-science/"]

def crawlerthread(frontier):
    while page_number < frontier.length:
        url = frontier[page_number+1]
        html = getHTML(url)
        storePage(url, html)

def getHTML(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(e)
    except URLError as e:
        print(url, "could not be found", e)
    else:
        return html.read()
    return ""

def storePage(url, html):
    # store page
    return

def main():
    html = urlopen('https://www.cpp.edu/sci/computer-science/')


if __name__  == "__main__":
    main()
