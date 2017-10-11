import requests
from bs4 import BeautifulSoup

site_root = "https://www.seek.co.nz"

current_page = ""
next_page = site_root + "/jobs-in-information-communication-technology"
job_links = []
current_page_number = 0
while current_page != next_page:
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