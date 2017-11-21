import requests
import csv
from selenium import webdriver
from bs4 import BeautifulSoup,NavigableString,Comment
from html.parser import HTMLParser
from rake_nltk import Rake

site_root = "https://www.seek.co.nz"
r = Rake()

current_page = ""
next_page = site_root + "/jobs-in-information-communication-technology"
job_links = []
current_page_number = 0
while current_page != next_page and len(job_links) <= 10:
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
    for link in job_links[0:5]:
        driver = webdriver.Chrome("chromedriver.exe")
        driver.get(site_root + link)
        page_soup = BeautifulSoup(driver.page_source, "html.parser")
        row_object = {}
        title = page_soup.find(attrs={"data-automation": "job-detail-title"})
        if title is not None:
            row_object.update({"title": title.text})
        description = page_soup.find("div", attrs={"data-automation": "jobDescription"})

        if description is not None:
            description_text = ""
            for child in [c for c in BeautifulSoup(HTMLParser().unescape(description.text), "html.parser").recursiveChildGenerator() if type(c) == NavigableString]:
                if isinstance(child, Comment) or child.isspace() or child == "":
                    continue
                print("child = " + child)
                description_text = description_text + " " + child.strip()
            row_object.update({"description": description_text})
            r.extract_keywords_from_text(description_text)
            keywords = r.get_ranked_phrases()
            row_object.update({"keywords": keywords})

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
