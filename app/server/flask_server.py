import os
import sys
import json
from .search_products import procces_recipes, sort_json
from .import2neoj4 import _create_order_node, _create_menu_node, similar_products_node, _get_user_menu


# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from flask import Flask, jsonify,request
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
#CORS(app)  # Enable CORS for all routes

def test_neo4j():
    with open('exported_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

@app.route('/', methods=['GET'])
def index():
    
    # En el landing page poner similitud de recetas
    recomended_products=similar_products_node()
    sort_json(recomended_products)

    if len!=0:
        return jsonify({"message":recomended_products})
    else:
        return jsonify({"message":""})

@app.route('/api/submit-text', methods=['POST', 'OPTIONS'])
def generate_response():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    data = request.json   
    user_text = data.get('text', '').strip() 
    
    #recipes_json =  procces_recipes(user_text)
    
    # For testing
    # That is the respond I'm waiting for
    recipes_json = test_neo4j()
    sort_json(recipes_json)
    
    recipes = {"message": recipes_json}
    return jsonify(recipes)


@app.route('/api/buy', methods=['POST', 'OPTIONS'])
def order_purchased():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
        
    if request.method == 'POST':
        data = request.json 
        order = data.get('items', [])
    
        _create_order_node(user_session='David', order=order)

        if not order:
            return jsonify({"error": "No hay productos para comprar."}), 400

    return jsonify({}), 200
    

@app.route('/api/save-recipe',methods=['POST','OPTIONS'])
def save_user_recipe():
    if request.method=='POST':
        data=request.json
        recipe = data.get('recipe',[])

        
        #_create_menu_node(user_session="David",recipe=recipe)

    return jsonify({}), 200

@app.route('/api/my-recipes',methods=['GET'])
def get_my_recipes():
    if request.method=='GET':

        user_menus = _get_user_menu("David")

        return jsonify({"message":user_menus})

if __name__ == '__main__':
    app.run(debug=True)
