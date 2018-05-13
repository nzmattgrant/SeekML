import matplotlib.pyplot as plt
import Utils

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

# types of graphs
# find word types and graph them

# find the word type count over all documents some kind of frequency graph

# find the word type distribution over all the files e.g. nouns per document

# graph the documents with the word experience

# see how many contain that

# see the the ones that contain intermediate vs senior etc
# plot_experience_count()
plot_key_word_frequency()