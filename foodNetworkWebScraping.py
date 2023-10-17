import requests
from bs4 import BeautifulSoup
import pandas as pd

# Food Network recipes
# All Food Network recipe pages (A-Z)
baseUrl = 'https://www.foodnetwork.com/recipes/recipes-a-z/'
allFoodNetworkUrls = []
alphabet = ['123', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'xyz']

for letter in alphabet:
    if letter == '123':
        for num in range(2):
            allFoodNetworkUrls.append(baseUrl + letter + '/p/' + str(num + 1))
    elif letter == 'a':
        for num in range(17):
            allFoodNetworkUrls.append(baseUrl + letter + '/p/' + str(num + 1))
    elif letter == 'b':
        for num in range(48):
            allFoodNetworkUrls.append(baseUrl + letter + '/p/' + str(num + 1))
    elif letter == 'c':
        for num in range(81):
            allFoodNetworkUrls.append(baseUrl + letter + '/p/' + str(num + 1))
    elif letter == 'd':
        for num in range(10):
            allFoodNetworkUrls.append(baseUrl + letter + '/p/' + str(num + 1))
    elif letter == 'e':
        for num in range(9):
            allFoodNetworkUrls.append(baseUrl + letter + '/p/' + str(num + 1))
    elif letter == 'f':
        for num in range(21):
            allFoodNetworkUrls.append(baseUrl + letter + '/p/' + str(num + 1))
    elif letter == 'g':
        for num in range(36):
            allFoodNetworkUrls.append(baseUrl + letter + '/p/' + str(num + 1))
    elif letter == 'h':
        for num in range(18):
            allFoodNetworkUrls.append(baseUrl + letter + '/p/' + str(num + 1))
    elif letter == 'i':
        for num in range(7):
            allFoodNetworkUrls.append(baseUrl + letter + '/p/' + str(num + 1))
    elif letter == 'j':
        for num in range(5):
            allFoodNetworkUrls.append(baseUrl + letter + '/p/' + str(num + 1))
    elif letter == 'k':
        for num in range(6):
            allFoodNetworkUrls.append(baseUrl + letter + '/p/' + str(num + 1))
    elif letter == 'l':
        for num in range(16):
            allFoodNetworkUrls.append(baseUrl + letter + '/p/' + str(num + 1))
    elif letter == 'm':
        for num in range(30):
            allFoodNetworkUrls.append(baseUrl + letter + '/p/' + str(num + 1))
    elif letter == 'n':
        for num in range(6):
            allFoodNetworkUrls.append(baseUrl + letter + '/p/' + str(num + 1))
    elif letter == 'o':
        for num in range(10):
            allFoodNetworkUrls.append(baseUrl + letter + '/p/' + str(num + 1))
    elif letter == 'p':
        for num in range(45):
            allFoodNetworkUrls.append(baseUrl + letter + '/p/' + str(num + 1))
    elif letter == 'q':
        for num in range(3):
            allFoodNetworkUrls.append(baseUrl + letter + '/p/' + str(num + 1))
    elif letter == 'r':
        for num in range(27):
            allFoodNetworkUrls.append(baseUrl + letter + '/p/' + str(num + 1))
    elif letter == 's':
        for num in range(77):
            allFoodNetworkUrls.append(baseUrl + letter + '/p/' + str(num + 1))
    elif letter == 't':
        for num in range(28):
            allFoodNetworkUrls.append(baseUrl + letter + '/p/' + str(num + 1))
    elif letter == 'u':
        for num in range(2):
            allFoodNetworkUrls.append(baseUrl + letter + '/p/' + str(num + 1))
    elif letter == 'v':
        for num in range(7):
            allFoodNetworkUrls.append(baseUrl + letter + '/p/' + str(num + 1))
    elif letter == 'w':
        for num in range(12):
            allFoodNetworkUrls.append(baseUrl + letter + '/p/' + str(num + 1))
    elif letter == 'xyz':
        for num in range(4):
            allFoodNetworkUrls.append(baseUrl + letter + '/p/' + str(num + 1))

allRecipesDf = pd.DataFrame() 
# Initializing DataFrame to store the scraped URLs
scrapedRecipesDf = pd.DataFrame() 

for foodNetworkUrl in allFoodNetworkUrls:
    page = requests.get(foodNetworkUrl)
    # BeautifulSoup enables to find the elements/tags in a webpage
    soup = BeautifulSoup(page.text, "html.parser")

    # Selecting all the 'a' tags (URLs) present in the webpage and extracting their 'href' attribute
    recipeUrls = pd.Series([a.get("href") for a in soup.find_all("a")])

    recipeUrls = recipeUrls[(recipeUrls.str.count("-") > 0) 
                            & (recipeUrls.str.contains("/recipes/") == True)
                            & (recipeUrls.str.contains("/recipes-a-z/") == False)
                            & (recipeUrls.str.contains("trending-eats") == False)
                            & (recipeUrls.str.contains("/packages/") == False)
                            & (recipeUrls.str.contains("/ree-drummond/") == False)
                            & (recipeUrls.str.contains("food-network-kitchen-s-best-recipes") == False)
                            & (recipeUrls.str.endswith("recipes/") == False)].unique()

    # DataFrame to store the scraped URLs
    df = pd.DataFrame({'Recipe Urls': recipeUrls})
    df['Recipe Urls'] = "https:" + df['Recipe Urls'].astype('str')
    # Appending 'df' to a main DataFrame 'init_urls_df'
    recipeUrlsDf = scrapedRecipesDf.append(df).copy()
    allRecipesDf = pd.concat([allRecipesDf, df])
    print(foodNetworkUrl)

allRecipesDf.to_csv(r"/Users/sahiti/Desktop/recipeRecommender/foodNetworkRecipeUrls.csv", 
sep="\t", index=False)