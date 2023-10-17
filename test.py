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

df = pd.read_csv('foodNetworkFullParsed1.csv')
df.sort_values('ingredientsParsed')
df.to_csv(r"/Users/sahiti/Desktop/recipeRecommender/testingredorder.csv", index=False)