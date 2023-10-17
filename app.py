from flask import Flask, jsonify, request
import word2vecReccomendations
import json, requests, pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity  
from ingredient_parser import ingredient_parser
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
app = Flask(__name__)
import secrets
foo = secrets.token_urlsafe(16)
app.secret_key = foo

class ingredientsForm(FlaskForm):
    ingredients = StringField('Input your ingredients:', description = "Use only a space to separate the ingredients", validators=[DataRequired()])
    submit = SubmitField('Submit')



@app.route('/', methods=['GET', 'POST'])
def index():
    form = ingredientsForm()
    ingredients = form.ingredients.data
    return redirect( url_for('actor', id=id) )

HELLO_HTML = """
     <html><body>
         <h1>Welcome!</h1>
         <p>Please add some ingredients to the url to receive recipe recommendations.
            You can do this by appending "/recipe?ingredients= Pasta Tomato ..." to the current url.
         <br>Click <a href="/recipe?ingredients= pasta tomato onion">here</a> for an example when using the ingredients: pasta, tomato and onion.
     </body></html>
     """

@app.route('/recipe', methods=["GET"])
def recommend_recipe():
    ingredients = request.args.get('ingredients')   
    recipe = word2vecReccomendations.get_recs(ingredients)
    
    response = {}
    count = 0
    for index, row in recipe.iterrows():
        response[count] = {
            'recipe': str(row['recipe']),
            'score': str(row['score']),
            'ingredients': str(row['ingredients']),
            'url': str(row['url'])
        }
        count += 1
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
