from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import random
import requests
import os
from datetime import datetime

from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

# Add this near the top of your file, after imports
print("Current working directory:", os.getcwd())

# Define the absolute path to the database
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'recipes.db')

# Update the configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

# Add this print statement to see where the database will be created
print(f"Database will be created at: {db_path}")

db = SQLAlchemy(app)

# Get API key from environment variable
SPOONACULAR_API_KEY = os.environ.get('SPOONACULAR_API_KEY')

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.String(500), nullable=False)
    instructions = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'ingredients': self.ingredients.split(','),
            'instructions': self.instructions
        }

class CachedApiRecipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(db.String(50), unique=True)
    data = db.Column(db.Text)  # Store JSON response
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

def init_db():
    with app.app_context():
        db.create_all()
        # Add some sample recipes if the database is empty
        if Recipe.query.count() == 0:
            sample_recipes = [
                Recipe(
                    name="Pasta with Tomato Sauce",
                    ingredients="pasta,tomatoes,garlic,olive oil,basil",
                    instructions="1. Cook pasta according to package instructions\n2. Sauté garlic in olive oil\n3. Add tomatoes and simmer\n4. Toss with pasta and fresh basil"
                ),
                Recipe(
                    name="Simple Stir Fry",
                    ingredients="rice,vegetables,soy sauce,garlic,ginger",
                    instructions="1. Cook rice\n2. Stir fry vegetables with garlic and ginger\n3. Add soy sauce\n4. Serve over rice"
                ),
                Recipe(
                    name="Basic Omelette",
                    ingredients="eggs,butter,cheese,vegetables",
                    instructions="1. Beat eggs\n2. Melt butter in pan\n3. Add eggs and cook\n4. Add fillings and fold"
                ),
                # New recipes that use eggs, beans, avocado, coconut oil, onions
                Recipe(
                    name="Avocado & Egg Breakfast Bowl",
                    ingredients="eggs,avocado,beans,onions,salt,pepper",
                    instructions="1. Fry eggs in a pan\n2. Warm beans in a pot\n3. Dice onions and avocado\n4. Combine all ingredients in a bowl\n5. Season with salt and pepper"
                ),
                Recipe(
                    name="Mexican-Style Eggs",
                    ingredients="eggs,beans,avocado,onions,tomatoes,cilantro",
                    instructions="1. Sauté diced onions until translucent\n2. Add beans and warm through\n3. Scramble eggs into the mixture\n4. Serve topped with sliced avocado and cilantro"
                ),
                Recipe(
                    name="Coconut Oil Fried Eggs with Avocado",
                    ingredients="eggs,coconut oil,avocado,salt,pepper",
                    instructions="1. Heat coconut oil in a pan\n2. Fry eggs to desired doneness\n3. Serve with sliced avocado\n4. Season with salt and pepper"
                )
            ]
            for recipe in sample_recipes:
                db.session.add(recipe)
            db.session.commit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_recipe', methods=['POST'])
def get_recipe():
    available_ingredients = request.json.get('ingredients', [])
    available_ingredients = [ing.lower().strip() for ing in available_ingredients]
    
    # Try to get recipes from API first
    api_recipes = get_recipes_from_api(available_ingredients)
    
    if api_recipes:
        # Return a random recipe from API results
        selected_recipe = random.choice(api_recipes)
        return jsonify(selected_recipe)
    
    # Fallback to local database if API fails or returns no results
    all_recipes = Recipe.query.all()
    possible_recipes = []
    
    for recipe in all_recipes:
        recipe_ingredients = [ing.lower().strip() for ing in recipe.ingredients.split(',')]
        matching_ingredients = sum(1 for ing in recipe_ingredients if ing in available_ingredients)
        if matching_ingredients / len(recipe_ingredients) >= 0.6:
            possible_recipes.append(recipe)
    
    if possible_recipes:
        selected_recipe = random.choice(possible_recipes)
        return jsonify(selected_recipe.to_dict())
    else:
        return jsonify({'error': 'No recipes found with available ingredients'}), 404

def get_recipes_from_api(ingredients):
    try:
        # Join ingredients with commas for the API
        ingredients_param = ','.join(ingredients)
        
        # Make request to Spoonacular API
        url = "https://api.spoonacular.com/recipes/findByIngredients"
        params = {
            'apiKey': SPOONACULAR_API_KEY,
            'ingredients': ingredients_param,
            'number': 5,  # Number of recipes to return
            'ranking': 2,  # 1 = maximize used ingredients, 2 = minimize missing ingredients
            'ignorePantry': True  # Ignore common ingredients like salt, oil
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            recipes_data = response.json()
            
            # If we got recipes, get detailed instructions for each
            formatted_recipes = []
            
            for recipe in recipes_data:
                # Get recipe details including instructions
                recipe_id = recipe['id']
                details_url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
                details_params = {
                    'apiKey': SPOONACULAR_API_KEY,
                    'includeNutrition': False
                }
                
                details_response = requests.get(details_url, params=details_params)
                
                if details_response.status_code == 200:
                    details = details_response.json()
                    
                    # Extract ingredients
                    ingredients_list = [item['name'] for item in recipe['usedIngredients']]
                    ingredients_list.extend([item['name'] for item in recipe['missedIngredients']])
                    
                    # Format instructions
                    instructions = ""
                    if details.get('instructions'):
                        instructions = details['instructions']
                    elif details.get('analyzedInstructions'):
                        steps = []
                        for instruction in details['analyzedInstructions']:
                            for step in instruction['steps']:
                                steps.append(f"{step['number']}. {step['step']}")
                        instructions = "\n".join(steps)
                    
                    formatted_recipe = {
                        'id': recipe['id'],
                        'name': recipe['title'],
                        'ingredients': ingredients_list,
                        'instructions': instructions,
                        'image': recipe['image']
                    }
                    
                    formatted_recipes.append(formatted_recipe)
            
            return formatted_recipes
        
        return []
    
    except Exception as e:
        print(f"API Error: {e}")
        return []

if __name__ == '__main__':
    init_db()
    app.run(debug=True) 