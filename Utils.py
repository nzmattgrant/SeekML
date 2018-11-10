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

def get_pos_description_mappings():
    return [{"tag":"CC","description":"Coordinating conjunction"},{"tag":"CD","description":"Cardinal number"},{"tag":"DT","description":"Determiner"},{"tag":"EX","description":"Existential <i>there<i> </i></i>"},{"tag":"FW","description":"Foreign word"},{"tag":"IN","description":"Preposition or subordinating conjunction"},{"tag":"JJ","description":"Adjective"},{"tag":"JJR","description":"Adjective, comparative"},{"tag":"JJS","description":"Adjective, superlative"},{"tag":"LS","description":"List item marker"},{"tag":"MD","description":"Modal"},{"tag":"NN","description":"Noun, singular or mass"},{"tag":"NNS","description":"Noun, plural"},{"tag":"NNP","description":"Proper noun, singular"},{"tag":"NNPS","description":"Proper noun, plural"},{"tag":"PDT","description":"Predeterminer"},{"tag":"POS","description":"Possessive ending"},{"tag":"PRP","description":"Personal pronoun"},{"tag":"PRP$","description":"Possessive pronoun"},{"tag":"RB","description":"Adverb"},{"tag":"RBR","description":"Adverb, comparative"},{"tag":"RBS","description":"Adverb, superlative"},{"tag":"RP","description":"Particle"},{"tag":"SYM","description":"Symbol"},{"tag":"TO","description":"<i>to</i>"},{"tag":"UH","description":"Interjection"},{"tag":"VB","description":"Verb, base form"},{"tag":"VBD","description":"Verb, past tense"},{"tag":"VBG","description":"Verb, gerund or present participle"},{"tag":"VBN","description":"Verb, past participle"},{"tag":"VBP","description":"Verb, non-3rd person singular present"},{"tag":"VBZ","description":"Verb, 3rd person singular present"},{"tag":"WDT","description":"Wh-determiner"},{"tag":"WP","description":"Wh-pronoun"},{"tag":"WP$","description":"Possessive wh-pronoun"},{"tag":"WRB","description":"Wh-adverb"}]