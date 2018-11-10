import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import wordpunct_tokenize
import Utils
from nltk import ngrams
import itertools
import csv
from collections import defaultdict
from multiprocessing import Pool

def plot_experience_count():
    corpus = Utils.get_corpus_from_descriptions()
    corpus_size = len(corpus)
    experience_count = 0
    for item in corpus:
        if "experience" in item["description"].lower():
            experience_count += 1

    plt.pie([experience_count, corpus_size - experience_count],
            labels=["has experience", "doesn't have experience"],
            shadow=True,
            startangle=90,
            explode=(0, 0.1))
    plt.axis('equal')
    plt.title("Experience vs no experience")
    plt.show()

def plot_key_word_frequency():
    corpus = Utils.get_corpus_from_descriptions()
    counts = {
        "junior": 0,
        "intermediate": 0,
        "senior": 0,
        "5 years": 0,
        "3 years": 0,
        "1 year": 0
    }
    for item in corpus:
        description = item["description"].lower()
        for word in counts:
            if word in description:
                counts[word] += 1

    x = counts.keys()
    y = counts.values()
    ax = plt.gca()
    ax.bar(x, y, align='center')
    plt.show()


def is_tag_in_n_grams(tag, n_grams_collections):
    # this is needed because if we put everything into one list it will get too big and crash the app
    for n_gram_collection in n_grams_collections:
        if tag in n_gram_collection or tag.replace("-", " ") in n_gram_collection:
            return True
    return False

def get_ngrams(split_text):
    n_grams_collection = [split_text]
    for n in range(2, 5):
        n_gram_tuples = ngrams(split_text, n)
        n_grams_collection.append(list(' '.join(grams) for grams in n_gram_tuples))
    return n_grams_collection

def plot_tag_distribution():
    corpus = Utils.get_corpus_from_descriptions()
    tags = Utils.get_stackoverflow_tags()
    tag_counts = {}
    document_counts = {}
    for item in corpus:
        description = item["description"].lower()
        title = item["title"].lower()
        title = ''.join(c for c in title if c.isalnum() or c.isspace())
        tokenized_description_ngrams = get_ngrams(wordpunct_tokenize(description))
        for tag in tags:
            if is_tag_in_n_grams(tag, tokenized_description_ngrams):
                if tag_counts.get(tag, None) is None:
                    tag_counts[tag] = 1
                else:
                    tag_counts[tag] += 1
                if document_counts.get(title, None) is None:
                    document_counts[title] = 1
                else:
                    document_counts[title] += 1

    sorted_tag_counts = sorted([(i,tag_counts[i]) for i in tag_counts], key=lambda x:x[1], reverse=True)
    sorted_document_counts = sorted([(i,document_counts[i]) for i in document_counts], key=lambda x:x[1], reverse=True)

    print(sorted_tag_counts)
    print(sorted_document_counts[0:10])

    document_tallys = [(k, len(list(v))) for k, v in itertools.groupby(sorted(dict(sorted_document_counts).values()))]
    print(document_tallys)
    tallys_dict = dict(document_tallys)
    x = []
    y = range(0, document_tallys[len(document_tallys) - 1][0] + 1)
    for i in y:
        if tallys_dict.get(i, None) is None:
            x.append(0)
        else:
            x.append(tallys_dict[i])

    print(x)
    print(y)

    plt.plot(x)

    plt.show()


def get_freq_dict(corpus_item):
    return dict(nltk.FreqDist(tag for (word, tag) in nltk.pos_tag(corpus_item["description"])))

# types of graphs
# find word types and graph them

def graph_part_of_speech_tags_from_excel():
    x = []
    y = []
    dict_of_vals = {}
    with open('word_types.csv', 'r', encoding='utf-8') as csvinput:
        reader = csv.DictReader(csvinput, fieldnames=["type", "count"])
        for row in reader:
            dict_of_vals[row["type"]] = int(row["count"])

    for key in dict(sorted(dict_of_vals.items(), key=lambda kv: kv[1])):
        x.append(key)
        y.append(dict_of_vals[key])

    descriptions = []
    description_mappings = Utils.get_pos_description_mappings()
    for pos in x:
        description = [m["description"] for (index, m) in enumerate(description_mappings) if m["tag"] == pos]
        if len(description) > 0:
            descriptions.append(description[0])
        else:
            descriptions.append(pos)

    x = descriptions
    plt.plot(y)
    plt.xticks(range(1, len(x)), x, rotation='vertical')
    plt.show()

def graph_part_of_speech_tags(pool):
    corpus = Utils.get_corpus_from_descriptions()
    tag_fd = defaultdict(int)
    results = pool.map(get_freq_dict, corpus)
    for dict_of_freq in results:
        for freq_item in dict_of_freq:
            tag_fd[freq_item] += dict_of_freq[freq_item]

    x = [x for x in tag_fd]
    y = [tag_fd[x] for x in tag_fd]
    with open('word_types.csv', 'w', encoding='utf-8') as csvoutput:
        writer = csv.DictWriter(csvoutput, fieldnames=["type", "count"])
        for freq_item in sorted(tag_fd.items(), key=lambda kv: kv[1]):
            writer.writerow({"type": freq_item, "count": tag_fd[freq_item]})

    plt.plot(x, y)
    plt.show()
    #print(tag_fd.most_common())


# graph the documents with the word experience
def graph_experience_match():
    #find the number of documents with experience
    #find number with 5 years, 10 years
    #plot total number and all the other numbers
    experience_count = 0
    five_years_count = 0
    ten_years_count = 0
    corpus = Utils.get_corpus_from_descriptions()
    total_count = len(corpus)
    for item in corpus:
        description = item["description"].lower() if item["description"] is not None else ""
        experience_count += description.count("experience")
        five_years_count += description.count("five years") + \
                            description.count("5 years") + \
                            description.count("5+ years")
        ten_years_count += description.count("ten years") + \
                        description.count("10 years") + \
                        description.count("10+ years")
    x = [1, 2, 3, 4, 5, 6]
    plt.bar(x, [experience_count,five_years_count, ten_years_count, total_count], align='center')
    plt.xticks(x, ["experience count", "five year count", "10 year count", "total count"])
    plt.show()

# plot_experience_count()
# plot_key_word_frequency()
#plot_tag_distribution()

#try find the words surrounding experience
#try lda

def Main():
    graph_experience_match()
    #graph_part_of_speech_tags(Pool())
    #graph_part_of_speech_tags_from_excel()

if __name__ == "__main__":
    Main()

