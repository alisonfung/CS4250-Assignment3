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

# connect to database
def connect_database():
    client = MongoClient(host="localhost", port=27017)
    db = client.assignment3
    return db

def main():
    db = connect_database()
    # set up database
    professors = db["professors"]
    pages = db["pages"]
    # retrieve html document
    html = pages.find_one({"target": True}).get("html")
    bs = BeautifulSoup(html, "html.parser")
    # get all divs in clearfix class for professor information
    data = bs.find_all("div", {"class": "clearfix"})
    for div in data:
        # get all professor names in h2 tags
        prof_names = div.find_all("h2")
        for name in prof_names:
            prof_info = {}
            # access the p tag
            info = name.next_sibling
            # get name, fix spacing
            prof_info["name"] = name.get_text().replace("\xa0", "").strip()
            # get title after "Title" strong tag, fix spacing
            prof_info["title"] = (info.next_sibling.find('strong', string=re.compile("Title"))
                                  .next_sibling.get_text().replace("\xa0", " ")
                                  .translate(str.maketrans('', '', ":"))
                                  .strip())
            # get office after "Office" strong tag, fix spacing
            prof_info["office"] = (info.next_sibling.find('strong', string=re.compile("Office"))
                                  .next_sibling.get_text().replace("\xa0", " ")
                                  .translate(str.maketrans('', '', ":"))
                                  .strip())
            # get phone after "Phone" strong tag, fix spacing
            prof_info["phone"] = (info.next_sibling.find('strong', string=re.compile("Phone"))
                                  .next_sibling.get_text().replace("\xa0", " ")
                                  .translate(str.maketrans('', '', ":"))
                                  .strip())
            # get email from anchor tag, after "Website" strong tag, fix spacing
            prof_info["email"] = (info.next_sibling.find('strong', string=re.compile("Email"))
                                 .next_sibling.next_sibling.get_text().replace("\xa0", " ")
                                 .translate(str.maketrans('', '', ":"))
                                 .strip())
            # get website from anchor tag, after "Web" strong tag, fix spacing
            try:
                prof_info["website"] = (info.next_sibling.find('strong', string=re.compile("Web"))
                                   .next_sibling.next_sibling.get_text().replace("\xa0", " ")
                                   .translate(str.maketrans('', '', ":"))
                                   .strip())
            # catch exception for no websites
            except:
                prof_info["website"] = "No website"
            print(prof_info)
            # insert professor into the collection
            professors.insert_one(prof_info)

if __name__  == "__main__":
    main()

