import os
import sys
import logging
import unidecode
import ast

import numpy as np
import pandas as pd

from gensim.models import Word2Vec
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict

from ingredientParse import ingredient_parser

def getAndSortCorpus(data):
    corpusSorted = []
    for doc in data.ingredientsParsed.values:
        # doc.sort()
        if isinstance(doc, str) == True:
            corpusSorted.append(doc)
    return corpusSorted

# calculate average length of each document 
def get_window(corpus):
    lengths = []
    for doc in corpus:
        if isinstance(doc, str) == True:
            lengths.append(len(doc))
    avg_len = float(sum(lengths)) / len(lengths)
    return round(avg_len)

class MeanEmbeddingVectorizer(object):
    def __init__(self, word_model):
        self.word_model = word_model
        self.vector_size = word_model.wv.vector_size

    def fit(self):  # comply with scikit-learn transformer requirement
        return self

    def transform(self, docs):  # comply with scikit-learn transformer requirement
        doc_word_vector = self.word_average_list(docs)
        return doc_word_vector

    def word_average(self, sent):
        """
		Compute average word vector for a single doc/sentence.
		:param sent: list of sentence tokens
		:return:
			mean: float of averaging word vectors
		"""
        mean = []
        for word in sent:
            if word in self.word_model.wv.index_to_key:
                mean.append(self.word_model.wv.get_vector(word))

        if not mean:  # empty words
            # If a text is empty, return a vector of zeros.
            # logging.warning(
            #     "cannot compute average owing to no vector for {}".format(sent)
            # )
            return np.zeros(self.vector_size)
        else:
            mean = np.array(mean).mean(axis=0)
            return 

if __name__ == "__main__":
    data = pd.read_csv('foodNetworkFullParsed.csv')
    # parse the ingredients for each recipe
    # data['parsed'] = data.ingredients.apply(ingredient_parser)
    # get corpus
    corpus = getAndSortCorpus(data)
    print(f"Length of corpus: {len(corpus)}")
    # train and save CBOW Word2Vec model
    model_cbow = Word2Vec(
      corpus, sg=0, workers=8, window=get_window(corpus), min_count=1, vector_size=100
    )
    model_cbow.save('models/model_cbow.bin')
    print("Word2Vec model successfully trained")

