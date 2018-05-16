import requests
import csv
from selenium import webdriver
from bs4 import BeautifulSoup,NavigableString,Comment
from html.parser import HTMLParser
from rake_nltk import Rake
import string
import Config

#todo split out the common functionality

def get_listings_from_seek():
    printable = set(string.printable)

    site_root = "https://www.seek.co.nz"
    r = Rake()

    current_page = ""
    next_page = site_root + "/jobs-in-information-communication-technology"
    job_links = []
    current_page_number = 0
    while current_page != next_page: #and len(job_links) <= 10
        current_page = next_page
        current_page_number = current_page_number + 1
        current_request = requests.get(current_page)
        soup = BeautifulSoup(current_request.text, "html.parser")
        for link in soup.find_all('a', attrs={"data-automation": "jobTitle"}):
            job_links.append(link.get('href'))
        next_page_link_element = soup.find('a', attrs={'data-automation': 'page-next'})
        if next_page_link_element is not None:
            next_page = site_root + next_page_link_element.get('href')
        print("current page number: " + str(current_page_number))
        print("number of links: " + str(len(job_links)))

        print("current page: " + current_page)
        print("next page: " + next_page)
    print(job_links)
    with open("first10WithKeyWords.csv", "w+", encoding='utf-8') as csvfile:
        fieldnames = ['title', 'description', 'advertiser-name', 'date', 'work-type', "keywords"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for link in job_links:
            driver = webdriver.Chrome("chromedriver.exe")
            driver.get(site_root + link)
            page_soup = BeautifulSoup(driver.page_source, "html.parser")
            row_object = {}
            title = page_soup.find(attrs={"data-automation": "job-detail-title"})
            if title is not None:
                row_object.update({"title": title.text})
            description = page_soup.find("div", attrs={"data-automation": "jobDescription"}).find("div", attrs={"class": "templatetext"})

            if description is not None:
                description_text = ""
                for child in [c for c in BeautifulSoup(HTMLParser().unescape(description.text), "html.parser").recursiveChildGenerator() if type(c) == NavigableString]:
                    if isinstance(child, Comment) or child.isspace() or child == "":
                        continue
                    print("child = " + child)
                    description_text = description_text + " " + child.strip()
                filter(lambda x: x in printable, description_text)
                row_object.update({"description": description_text})
                r.extract_keywords_from_text(description_text)
                keywords = r.get_ranked_phrases()
                filtered_keywords = []
                for keyword in [item for item in keywords if len(item.split()) < 4]:
                    filtered_keywords.append(keyword)
                keyword_text = ', '.join(filtered_keywords)
                filter(lambda x: x in printable, keyword_text)
                row_object.update({"keywords": keyword_text})

            advertiser_name = page_soup.find(attrs={"data-automation": "job-details-header-advertiser-name"})
            if advertiser_name is not None:
                row_object.update({"advertiser-name": advertiser_name.text})
            date = page_soup.find(attrs={"data-automation": "job-detail-date"})
            if date is not None:
                row_object.update({"date": date.text})
            work_type = page_soup.find(attrs={"data-automation": "job-detail-work-type"})
            if work_type is not None:
                row_object.update({"work-type": work_type.text})
            writer.writerow(row_object)

def get_tags_from_stackoverflow():

    site_root = "https://stackoverflow.com"

    current_page = ""
    next_page = site_root + "/tags"
    tags = []
    current_page_number = 0
    # get the top 100 pages of popular tags
    # todo should we collect more tags than this?
    while current_page != next_page and current_page_number < 101:
        current_page = next_page
        current_page_number = current_page_number + 1
        current_request = requests.get(current_page)
        soup = BeautifulSoup(current_request.text, "html.parser")
        for link in soup.find_all('a', attrs={"class": "post-tag"}):
            tags.append(link.getText())
        next_page_link_element = soup.find('a', attrs={'rel': 'next'})
        if next_page_link_element is not None:
            next_page = site_root + next_page_link_element.get('href')
        print("current page number: " + str(current_page_number))
        print("number of tags: " + str(len(tags)))
        print("current page: " + current_page)
        print("next page: " + next_page)
    print(tags)
    with open(Config.tag_file, "w+", encoding='utf-8') as csvfile:
        fieldnames = ['tags']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for tag in tags:
            writer.writerow({"tags": tag})

get_tags_from_stackoverflow()

#todo maybe get linkedin tags?