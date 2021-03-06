import numpy as np
import matplotlib.pyplot as plt
import csv

#total keyword count
def print_keyword_counts():
    keyword_dict = {}
    with open("Large data set.csv", "r", encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            keywords = row['keywords'].split(',')
            for keyword in keywords:
                keyword_lowered = keyword.lower().strip("'")
                if keyword_lowered in keyword_dict.keys():
                    keyword_dict[keyword_lowered] += keyword_dict[keyword_lowered] + 1
                else:
                    keyword_dict[keyword_lowered] = 1

    for key, value in sorted(keyword_dict.items(), key=lambda x:x[1]):
        print("%s: %s" % (key.strip("'"), value))

#print_keyword_counts()
def print_keywords_in_listings_count():
    keyword_in_listing_dict = {}
    with open("Large data set.csv", "r", encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        index = 0
        for row in reader:
            keywords = row['keywords'].split(',')
            for keyword in keywords:
                keyword_lowered = keyword.lower().strip("'")
                if keyword_lowered not in keyword_in_listing_dict.keys():
                    keyword_in_listing_dict[keyword_lowered] = {}
                if keyword_in_listing_dict[keyword_lowered].get(index, False) is False:
                    keyword_in_listing_dict[keyword_lowered][index] = True
            index += 1

    for key, value in keyword_in_listing_dict.items():
        keys_length = len(value.keys())
        if keys_length > 300:
            print("%s: %s" % (key, keys_length))

def print_important_keywords():
    keyword_in_listing_dict = {}
    with open("Large data set.csv", "r", encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        index = 0
        for row in reader:
            keywords = row['keywords'].split(',')
            description = row["description"].lower()
            for keyword in keywords:
                keyword_lowered = keyword.lower().strip("'")
                if keyword_lowered not in keyword_in_listing_dict.keys():
                    keyword_in_listing_dict[keyword_lowered] = {}
                if keyword_in_listing_dict[keyword_lowered].get(index, 0) is 0:
                    description_count = description.count(keyword_lowered)
                    keyword_in_listing_dict[keyword_lowered][index] = description_count
            index += 1

    for key, value in keyword_in_listing_dict.items():
        filtered_dict = {k: v for k, v in value.items() if v > 1}
        keys_length = len(filtered_dict.keys())
        if keys_length > 0 and keys_length < 100:
            print("%s: %s" % (key, keys_length))



#print_keyword_counts()
#print_keywords_in_listings_count()
print_important_keywords()

