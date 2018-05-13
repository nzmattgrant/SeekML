from tempfile import NamedTemporaryFile
import shutil
import csv

# filename = "testfile.csv"
# tempfile = NamedTemporaryFile(mode='w', delete=False)

# fields = ['title', 'description', 'advertiser-name', 'date', 'work-type', "keywords"]
# newFields = fields
# newFields.append("important-keywords")
#
# with open(filename, 'r', encoding='utf-8') as csvfile, tempfile:
#     reader = csv.DictReader(csvfile, fieldnames=fields)
#     writer = csv.DictWriter(tempfile, fieldnames=newFields)
#     for row in reader:
#         row["important-keywords"] = "test"
#         writer.writerow(row)
#
# shutil.move(tempfile.name, filename)

import math
from textblob import TextBlob as tb

def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

fields = ['title', 'description', 'advertiser-name', 'date', 'work-type', "keywords", "important-keywords"]

with open('Large data set.csv','r', encoding='utf-8') as csvinput:
    with open('output.csv', 'w', encoding='utf-8') as csvoutput:
        writer = csv.DictWriter(csvoutput, fieldnames=fields)
        reader = csv.DictReader(csvinput, fieldnames=fields)

        allRows = []
        bloblist = []

        for row in reader:
            allRows.append(row)
            bloblist.append(tb(row["description"]))

        for row in allRows:
            keyword_dict = {}
            blob = tb(row["description"]).lower()
            for word in blob.words:
                #efficiency
                if keyword_dict.get(word, None) is None:
                    keyword_dict[word] = tfidf(word, blob, bloblist)

            important_keywords = ",".join(str(item[0]) for item in (sorted(keyword_dict.items(), key=lambda x: x[1], reverse=True)[0:50]))
            print(important_keywords)
            row["important-keywords"] = important_keywords

        writer.writerows(allRows)

