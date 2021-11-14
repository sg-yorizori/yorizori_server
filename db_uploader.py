# -----------for independent execution------------
import os
import argparse
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()
# ------------------------------------------------

import csv
import ast
from users.models import User
from recipe.models import Recipe, Ingredients, Steps
from tqdm import tqdm

def write_to_db(file):
    with open(file, encoding='utf-8-sig') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader, None)
        for row in tqdm(csvreader):
            try:
                recipe, _ = Recipe.objects.get_or_create(
                    title=row[0],
                    thumbnail=row[1],
                    # writer : row[2]
                    # ingredients : row[3] >> unit(ingrd_id, unit)
                    # steps : row[4]
                    views=row[5],
                )
                # ------------writer------------
                recipe.writer = User.objects.get(pk=0)
                # ------------ingredients------------
                ingrds_str = row[3]
                ingrds = ast.literal_eval(ingrds_str)     # str convert to python format
                '''
                ingreds = map(str.lower, ingreds)           # to lower case
                ingreds = list(set(ingreds))
                for ingred_name in ingreds:
                    ingred, _ = Ingredients.objects.get_or_create(name=ingred_name)#TODO manytomany field
                    recipe.ingredients.add(ingred)
                '''
                for each_ingrd, each_unit in ingrds:
                    ingrd, _ = Ingredients.get_or_create(ingredient=each_ingrd)
                    unit, _ = Unit.objects.get_or_create(ingrd_id=ingrd.pk, recipe_id=recipe.id, unit=each_unit)
                    recipe.units.add(unit)

                # ------------steps------------
                steps_str = row[4]
                steps = ast.literal_eval(steps_str)  # str convert to python format
                for step in steps:
                    step, _ = Steps.objects.create(num=step[0], contents=step[1], img=step[2])
                    recipe.steps.add(step)

            except Exception as e:
                    print(e)

def validate_file(f):
    if not os.path.exists(f):
        # Argparse uses the ArgumentTypeError to give a rejection message like:
        # error: argument input: x does not exist
        raise argparse.ArgumentTypeError("{0} does not exist".format(f))
    return f

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_path', type=validate_file,
                        help='input csv file path')
    args = parser.parse_args()
    print('saving [' + args.csv_path + '] to [db.sqlite3]...')

    write_to_db(args.csv_path)