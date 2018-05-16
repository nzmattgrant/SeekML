import csv
import Config

def get_corpus_from_descriptions(text_to_compare = ""):
    fields = ['title', 'description', 'advertiser-name', 'date', 'work-type', "keywords", "important-keywords"]
    with open(Config.listings_file, 'r', encoding='utf-8') as csvinput:
        reader = csv.DictReader(csvinput, fieldnames=fields)

        corpus = []

        for row in reader:
            corpus.append({"description": str(row["description"]).lower(), "title": str(row["title"])})

        if text_to_compare is not "":
            corpus.append({"description": text_to_compare, "title": "self"})

        return corpus

def get_stackoverflow_tags():
    fields = ['tags']
    with open(Config.tag_file, 'r', encoding='utf-8') as csvinput:
        reader = csv.DictReader(csvinput, fieldnames=fields)

        tags = []

        for row in reader:
            tags.append(row["tags"])

        return tags
