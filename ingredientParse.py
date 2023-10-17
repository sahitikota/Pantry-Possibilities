import pandas as pd 
import nltk
from string import *
import ast
import re
import unidecode
# nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from collections import Counter

# need to remove \xa0 from some ingredients
def ingredient_parser(ingreds):
    measures = ['teaspoon', 't', 'tsp.', 'tablespoon', 'T', 'tbl.', 'tb', 'tbsp.', 'fluid ounce', 'fl oz', 'gill', 'cup', 'c', 'pint', 'p', 'pt', 'fl pt', 'quart', 'q', 'qt', 'fl qt', 'gallon', 'g', 'gal', 'ml', 'milliliter', 'millilitre', 'cc', 'mL', 'l', 'liter', 'litre', 'L', 'dl', 'deciliter', 'decilitre', 'dL', 'bulb', 'level', 'heaped', 'rounded', 'whole', 'pinch', 'medium', 'slice', 'pound', 'lb', '#', 'ounce', 'oz', 'mg', 'milligram', 'milligramme', 'g', 'gram', 'gramme', 'kg', 'kilogram', 'kilogramme', 'x', 'of', 'mm', 'millimetre', 'millimeter', 'cm', 'centimeter', 'centimetre', 'm', 'meter', 'metre', 'inch', 'in', 'milli', 'centi', 'deci', 'hecto', 'kilo']
    wordsToRemove = ['i', 'I', 'squeezed', 'each', 'unsalted', 'seedless', 'unpeeled', 'count', 'moon', 'andor', 'dice', 'bias', 'skin', 'attached', 'will', 'weigh', 'so', 'sweet', 'unsweetend', 'variety', 'kind', 'sold', 'swirl', 'shape', 'mixed', 'pulse', 'food', 'processor', 'julienned', 'cored', 'chopped', 'patted', 'minced', 'bitesize', 'smallmedium', 'skinned', 'at', 'thickest', 'preferably', 'center', 'about', 'loosely', 'emulsifying', 'coin', 'recipe', 'palm', 'full', 'plus','extra','for', 'garnish', 'follows', 'kept', 'neutral', 'only', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'mandoline', 'brand', 'fresh', 'a', 'bunch', 'and', 'clove', 'or', 'leaf',  'large', 'extra', 'sprig', 'ground', 'handful', 'free', 'small', 'range', 'from', 'dried', 'sustainable', 'peeled', 'higher', 'welfare', 'for', 'finely', 'freshly', 'sea', 'quality', 'ripe', 'few', 'piece', 'source', 'to', 'organic', 'flat', 'sliced', 'picked', 'the', 'stick', 'plain', 'plus', 'your', 'optional', 'serve', 'ask', 'natural', 'roughly', 'into', 'such', 'cut', 'good', 'grated', 'trimmed', 'oregano', 'powder', 'yellow', 'dusting', 'knob', 'frozen', 'on', 'deseeded', 'low', 'runny', 'cooked', 'streaky', 'nutmeg', 'sage', 'rasher', 'zest', 'pin', 'groundnut', 'breadcrumb', 'turmeric', 'halved', 'grating', 'stalk', 'light', 'tinned', 'dry', 'soft', 'rocket', 'bone', 'color', 'washed', 'skinless', 'leftover', 'splash', 'removed', 'dijon', 'thick', 'big', 'hot', 'drained', 'sized', 'english', 'dill', 'caper', 'raw', 'flake', 'cider', 'cayenne', 'tbsp', 'leg', 'pine', 'wild', 'if', 'fine', 'herb', 'almond', 'shoulder', 'cube', 'dressing', 'with', 'chunk', 'spice', 'thumb', 'new', 'little', 'punnet', 'peppercorn', 'shelled', 'saffron', 'other''chopped', 'salt', 'olive', 'taste', 'can', 'sauce', 'water', 'diced', 'package', 'italian', 'shredded', 'divided', 'all', 'purpose', 'crushed', 'juice', 'more', 'coriander', 'needed', 'thinly', 'boneless', 'half', 'thyme', 'cubed', 'cinnamon', 'cilantro', 'jar', 'seasoning', 'rosemary', 'extract', 'baking', 'beaten', 'heavy', 'seeded', 'tin', 'vanilla', 'uncooked', 'crumb', 'style', 'thin', 'nut', 'coarsely', 'spring', 'chili', 'cornstarch', 'strip', 'cardamom', 'rinsed', 'honey', 'cherry', 'root', 'quartered', 'head', 'softened', 'container', 'crumbled', 'frying', 'lean', 'cooking', 'roasted', 'warm', 'whipping', 'thawed', 'corn', 'pitted', 'sun', 'kosher', 'bite', 'toasted', 'lasagna', 'split', 'melted', 'degree', 'lengthwise', 'romano', 'packed', 'pod', 'anchovy', 'rom', 'prepared', 'juiced', 'fluid', 'floret', 'room', 'active', 'seasoned', 'mix', 'deveined', 'lightly', 'anise', 'thai', 'size', 'unsweetened', 'torn', 'wedge', 'sour', 'basmati', 'marinara', 'dark', 'temperature', 'garnish', 'bouillon', 'loaf', 'shell', 'reggiano', 'canola', 'parmigiano', 'round', 'canned', 'ghee', 'crust', 'long', 'broken', 'ketchup', 'bulk', 'cleaned', 'condensed', 'sherry', 'provolone', 'cold', 'soda', 'cottage', 'spray', 'tamarind', 'pecorino', 'shortening', 'part', 'bottle', 'sodium', 'cocoa', 'grain', 'french', 'roast', 'stem', 'link', 'firm', 'asafoetida', 'mild', 'dash', 'boiling']
    # wordsToRemove = ['only', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'roasted', 'and', 'split', 'in', 'half', 'peeled', 'I', 'aged', 'cut', 'into', 'bite-sized', 'pieces', 'woody', 'core', 'removed', 'finely', 'chopped', 'halved', 'with', 'skin', 'small', 'medium', 'sprigs', 'fresh', 'parts', 'scrubbed', 'washed', 'large', 'peeled', 'higher', 'welfare', 'for', 'sea', 'ripe', 'quality', 'to', 'organic', 'sliced', 'mandoline', 'picked', 'stick', 'plain']
    # The ingredient list is now a string so we need to turn it back into a list. We use ast.literal_eval
    if isinstance(ingreds, list):
        ingredients = ingreds
    elif pd.isna(ingreds) == True:
        ingredients = []
    else:
        ingredients = ast.literal_eval(ingreds)
    
    lemmatizer = WordNetLemmatizer()
    ingred_list = []
    for i in ingredients:
        punct = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        for letter in i:
            if letter in punct:
                i = i.replace(letter, "")
        # We split up with hyphens as well as spaces
        items = re.split(' |-', i)
        # Get rid of words containing non alphabet letters
        items = [word for word in items if word.isalpha()]
        # Turn everything to lowercase
        items = [word.lower() for word in items]
        # remove accents
        items = [unidecode.unidecode(word) for word in items] #''.join((c for c in unicodedata.normalize('NFD', items) if unicodedata.category(c) != 'Mn'))
        # Lemmatize words so we can compare words to measuring words
        items = [lemmatizer.lemmatize(word) for word in items]
        # Gets rid of measuring words/phrases, e.g. heaped teaspoon
        items = [word for word in items if word not in measures]
        # Get rid of common easy words
        items = [word for word in items if word not in wordsToRemove]
        if items:
            ingred_list.append(' '.join(items)) 
    ingred_list = " ".join(ingred_list)
    return ingred_list

if __name__ == "__main__":
    recipe_df = pd.read_csv(r"/Users/sahiti/Desktop/recipeRecommender/foodNetworkFull.csv")
    recipe_df['ingredientsParsed'] = recipe_df['ingredients'].apply(lambda x: ingredient_parser(x))
    df = recipe_df[['Recipe Urls', 'recipeName', 'ingredientsParsed']]
    df = recipe_df.dropna()
       
    df.to_csv(r"/Users/sahiti/Desktop/recipeRecommender/foodNetworkFullParsed.csv", index=False)