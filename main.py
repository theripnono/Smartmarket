from llm.generate_recipes import generate_recipes
from neo4j import GraphDatabase
import neo4j
from dotenv import dotenv_values
import json
import ast

config = dotenv_values(".conf")

URI = config['URI']
AUTH = ast.literal_eval(config['AUTH'])

#recipes = generate_recipes()

recipes =[
            {'receta': 'Tortilla de patatas',
            'ingredientes': [
                {'categoria': 'Huevos grandes', 'qty': 4, 'unit': 'unidades'},
                {'categoria': 'Cebolla y ajo', 'qty': 1, 'unit': 'unidad'},
                {'categoria': 'Aceite de oliva virgen y virgen extra', 'qty': 100, 'unit': 'ml'},
                {'categoria': 'Sal y bicarbonato', 'qty': 1, 'unit': 'pizca'},
            ]
            }
        ]


def export_json(df:object)->object:

    """
    df estructure example:
                                            name            brand  ...  cantidad      unit
       0                          Huevos L docena    Gorrotxategi  ...         4  unidades
       1                 Huevos L de suelo docena            Dagu  ...         4  unidades
       2                      Huevos L 1/2 docena              BM  ...         4  unidades
       3                      Huevos L 1/2 docena    Gorrotxategi  ...         4  unidades
       4                 Huevos euskolabel decena     Eusko Label  ...         4  unidades
       5                          Huevos L docena              BM  ...         4  unidades
       6  Cebolla ecológica en malla (1 kg aprox)             ...  ...         1    unidad
       7                Cebolla tubo (1 kg aprox)             ...  ...         1    unida
    """
    # Agrupar el DataFrame por 'receta'
    recetas_json = []
    grouped = df.groupby('receta')
     # Iterar sobre los grupos
    for receta, group in grouped:
        receta_dict = {
            'receta': receta,
            'ingredientes': []
        }

        # Iterar sobre cada fila del grupo
        for _, row in group.iterrows():
            ingrediente = {
                'name': row['name'],
                'brand': row['brand'],
                'cantidad': row['cantidad'],
                'unit': row['unit']
            }
            receta_dict['ingredientes'].append(ingrediente)
        
        # Añadir el diccionario de la receta a la lista final
        recetas_json.append(receta_dict)

    return recetas_json

try:
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()

        records_df = driver.execute_query(
            "UNWIND $recipes as receta "
            "UNWIND receta.ingredientes as ingrediente "
            "MATCH (c:Category {category: ingrediente.categoria})--(p:Product) "
            "RETURN p.product_name as name, "
            "p.product_brand as brand, "
            "p.product_price_centAmount as price,"
            "receta.receta as receta,"
            "ingrediente.qty as cantidad,"
            "ingrediente.unit as unit"
                    
            , recipes=recipes
            , database_="neo4j"
            , result_transformer_=neo4j.Result.to_df
        )
      
except Exception as e:
    print('Oups! something goes wrong, please check: ')
    print({e})


export_json(records_df)