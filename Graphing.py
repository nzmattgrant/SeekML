import matplotlib.pyplot as plt
from nltk.tokenize import wordpunct_tokenize
import Utils
from nltk import ngrams

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
    for item in corpus:
        description = item["description"].lower()
        tokenized_description_ngrams = get_ngrams(wordpunct_tokenize(description))
        for tag in tags:
            if is_tag_in_n_grams(tag, tokenized_description_ngrams):
                if tag_counts.get(tag, None) is None:
                    tag_counts[tag] = 1
                else:
                    tag_counts[tag] += 1

    sorted_tag_counts = sorted([(i,tag_counts[i]) for i in tag_counts], key=lambda x:x[1], reverse=True)
    print(sorted_tag_counts)

    pass
# types of graphs
# find word types and graph them

# find the word type count over all documents some kind of frequency graph

# find the word type distribution over all the files e.g. nouns per document

# graph the documents with the word experience

# see how many contain that

# see the the ones that contain intermediate vs senior etc
# plot_experience_count()
# plot_key_word_frequency()
plot_tag_distribution()