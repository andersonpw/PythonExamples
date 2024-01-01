# The MVP here is Scikit-Learn, which is a package for general-purpose
# data analysis. It has some fun tools for working with text that are described
# at https://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html
from sklearn.feature_extraction.text import CountVectorizer

# NumPy is a massive package that implements vectors, matrices, and all sorts
# of common operations on them. https://numpy.org/
import numpy

# "re" is Python's built-in package for regular expressions
import re

# Boring stuff
import urllib.request
from pathlib import Path
import os

# Download a copy of the Bible from Project Gutenberg. Don't re-download if
# the file already exists
if not os.path.exists("./bible.txt"):
    urllib.request.urlretrieve(
        "https://www.gutenberg.org/cache/epub/10/pg10.txt", "bible.txt")


# Read the text of the bible into a string called bible
bible = Path("bible.txt").read_text(encoding="utf-8")

# Use regular expressions to remove verse numbers from the text
bible_clean = re.sub("[0-9]", "", bible)

# Use a "count vectorizer" to analyze the text. Since it's set to look
# for five-grams (https://en.wikipedia.org/wiki/N-gram), it returns a
# vector where each component represents a different five-gram and the
# value of that component is the number of occurrences of that five-gram
# in the text. We find the largest components of the resulting vector
# and map them back to the five-grams they represent, which gives us a top 10
# list
count_vectorizer = CountVectorizer(ngram_range=(5, 5))
sparse_matrix = count_vectorizer.fit_transform([bible_clean])
x = sparse_matrix.toarray()
y = x.flatten()
indexes = y.argsort()[-10:][::-1]
features = count_vectorizer.get_feature_names_out()
grams = [(features[index], y[index]) for index in indexes]

for index, gram in enumerate(grams):
    print("#" + str(index + 1) + ":", gram[0], "(" + str(gram[1]) + " times)")
