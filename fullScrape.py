import pandas as pd 
import time
from FNScrapeClass import FoodNetwork

# reads in the csv containing each recipe's url
recipeDf = pd.read_csv("/Users/sahiti/Desktop/recipeRecommender/foodNetworkRecipeUrls.csv")

# list of recipe attributes we want to scrape - name and ingredients
attributes = ['recipeName', 'ingredients']

# for each url (i), add the attribute data to the i-th row
temp = pd.DataFrame(columns = attributes)
for i in range(62000, 62500):
    url = recipeDf['Recipe Urls'][i]
    recipe_scraper = FoodNetwork(url)
    temp.loc[i] = [getattr(recipe_scraper, attrib)() for attrib in attributes]
    if i % 100 == 0:
        print("Recipe " + str(i) + " completed")
    # time.sleep(2)

# put all the data into the same dataframe
temp['Recipe Urls'] = recipeDf['Recipe Urls']
columns = ['Recipe Urls'] + attributes
temp = temp[columns]

FoodNetworkDf = temp

FoodNetworkDf.to_csv(r"/Users/sahiti/Desktop/recipeRecommender/foodNetworkFull1.csv", index = False)