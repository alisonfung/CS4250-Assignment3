#-------------------------------------------------------------------------
# AUTHOR: Alison Fung
# FILENAME: parser.py
# SPECIFICATION: Parses the CPP CS faculty page for faculty information.
# FOR: CS 4250- Assignment #3
# TIME SPENT: 2 hours
#-----------------------------------------------------------*/

import re
from bs4 import BeautifulSoup
from pymongo import MongoClient

def connect_database():
    client = MongoClient(host="localhost", port=27017)
    db = client.assignment3
    return db

def main():
    db = connect_database()
    professors = db["professors"]
    pages = db["pages"]
    # retrieve html document
    html = pages.find_one({"target": True}).get("html")
    #name, title, office, phone, email, and
    bs = BeautifulSoup(html, "html.parser")
    data = bs.find_all("div", {"class": "clearfix"})
    for div in data:
        prof_names = div.find_all("h2")
        for name in prof_names:
            prof_info = {}
            info = name.next_sibling
            prof_info["name"] = name.get_text().replace("\xa0", "")
            prof_info["title"] = (info.next_sibling.find('strong', string=re.compile("Title"))
                                  .next_sibling.get_text().replace("\xa0", " ")
                                  .translate(str.maketrans('', '', ":"))
                                  .strip())
            prof_info["office"] = (info.next_sibling.find('strong', string=re.compile("Office"))
                                  .next_sibling.get_text().replace("\xa0", " ")
                                  .translate(str.maketrans('', '', ":"))
                                  .strip())
            prof_info["phone"] = (info.next_sibling.find('strong', string=re.compile("Phone"))
                                  .next_sibling.get_text().replace("\xa0", " ")
                                  .translate(str.maketrans('', '', ":"))
                                  .strip())
            prof_info["email"] = (info.next_sibling.find('strong', string=re.compile("Email"))
                                 .next_sibling.next_sibling.get_text().replace("\xa0", " ")
                                 .translate(str.maketrans('', '', ":"))
                                 .strip())
            try:
                prof_info["website"] = (info.next_sibling.find('strong', string=re.compile("Web"))
                                   .next_sibling.next_sibling.get_text().replace("\xa0", " ")
                                   .translate(str.maketrans('', '', ":"))
                                   .strip())
            except:
                prof_info["website"] = "No website"
            print(prof_info)
            professors.insert_one(prof_info)




if __name__  == "__main__":
    main()

