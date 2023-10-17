import requests
from bs4 import BeautifulSoup
import numpy as np
import json

# use this class to loop over every recipe in allRecipesDf (all Food Network Urls)
headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"}

class FoodNetwork():
    def __init__(self, url):
        self.url = url 
        self.soup = BeautifulSoup(requests.get(url, headers=headers).content, 'html.parser')
    
    # locates recipe's name
    def recipeName(self):
        # some urls may not be recipe urls, so to avoid errors we use try/except 
        try:
            data = json.loads(self.soup.find('script', type = 'application/ld+json').text)
            return(data[0]['name'])
        except: 
            return np.nan

    # creates vector containing recipe ingredients
    def ingredients(self):
        try:
            data = json.loads(self.soup.find('script', type = 'application/ld+json').text)
            return(data[0]['recipeIngredient'])
        except:
            return np.nan
            