import os
import json
from argparse import ArgumentParser
from caseconverter import pascalcase, snakecase

GENERATION_TYPE_CATEGORIES = [
    'entityTypeVariables', 'shops', 'animationTypes', 'states', 'projectileTypes', 'itemTypes', 'music',
    'sound', 'unitTypes', 'variables', 'attributeTypes', 'playerTypes', 'playerTypeVariables'
]

parser = ArgumentParser(
    description='Turn a modd.io game json file into python')
parser.add_argument('json_file', help='The exported game json file')


def generate_game_variables():
    args = parser.parse_args()
    json_file = args.json_file
    if not json_file or not json_file.endswith('.json'):
        parser.error(f'{json_file} is not a valid file')

    game_dict = None
    with open(json_file, 'rt') as game_file:
        game_dict = json.loads(game_file.read())
    if game_dict is None or game_dict.get('data') is None:
        parser.error(f'{json_file} contains invalid content')
    game_name = snakecase(game_dict.get('title'))
    game_dict = game_dict.get('data')

    if not os.path.isdir(f'{game_name}/'):
        os.mkdir(f'{game_name}/')
    with open(f'{game_name}/game.py', 'w') as game_file:
        content = ''
        import_classes = []
        for category in GENERATION_TYPE_CATEGORIES:
            current_dict = game_dict.get(category)
            class_name = f"{pascalcase(category)}{'s' if category[-1] != 's' else ''}"
            content += f'\n\nclass {class_name}():\n'
            obj_ids = game_dict.get(category, {}).keys()
            if len(obj_ids) == 0:
                content += '\tpass\n'
                continue
            type_name = pascalcase(
                category).removesuffix('s') if 'variable' not in category.lower() else 'Variable'
            if type_name not in import_classes:
                import_classes.append(type_name)
            for obj_id in obj_ids:
                obj_name = current_dict.get(obj_id).get('name')
                obj_name = obj_name if obj_name is not None else obj_id
                content += ''.join(
                    [f"\t{snakecase(obj_name).upper()} = {type_name}('{obj_id}') \n"])
        content = (
            f"from pymodd.functions import {', '.join([class_name for class_name in import_classes])}\n"
            f'{content}'
        )
        game_file.write(content)
        print('Game project successfuly created/updated')

    with open(f'{game_name}/scripts.py', 'w') as scripts_file:
        scripts_file.write(
            "from pymodd.actions import *\nfrom pymodd.functions import *\nfrom pymodd.script import Script, Trigger, write_to_output\n\nfrom game import *\n\n\n# write game scripts here")


def main():
    generate_game_variables()


if __name__ == '__main__':
    main()
