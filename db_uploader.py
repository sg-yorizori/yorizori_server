# -----------for independent execution------------
import os
import argparse
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()
# ------------------------------------------------

import csv
import ast
from recipe.models import Recipe, Ingred
from tqdm import tqdm

def write_to_db(file):
    with open(file, encoding='utf-8-sig') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader, None)
        for row in tqdm(csvreader):
            try:
                recipe, _ = Recipe.objects.get_or_create(
                    title=row[0],
                    main_img=row[1],
                    ingred_amount=row[3],
                    steps=row[4],
                    step_img=row[5],
                    views=row[6],
                    writer=row[7]
                )
                ingreds_str = row[2]
                ingreds = ast.literal_eval(ingreds_str)
                ingreds = map(str.lower, ingreds)
                ingreds = list(set(ingreds))
                for ingred_name in ingreds:
                    ingred, _ = Ingred.objects.get_or_create(name=ingred_name)
                    recipe.ingreds.add(ingred)
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