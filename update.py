# import ruamel.yaml

# file_name = '../test-1/data.yaml'
# config, ind, bsi = ruamel.yaml.util.load_yaml_guess_indent(open(file_name))

# names = config['names']
# names[0] = '1.2.3.4'
# names[0] = 'Username'
# names[0] = 'Password'

# yaml = ruamel.yaml.YAML()
# yaml.indent(mapping = ind, sequence = ind, offset = bsi)
# with open('output.yaml', 'w') as fp:
#    yaml.dump(config, fp)

# import yaml

# with open("../test-1/data.yaml", "r") as stream:
#     try:
#         print(yaml.safe_load(stream))
#     except yaml.YAMLError as exc:
#         print(exc)

# -*- coding: utf-8 -*-
import yaml
import io

# Define data
data = {
    'names': [
        '1', 
        '2', 
        '3', 
        '4',
        '5',
        '6',
        '7',
        '8',
        '9',
        'A',
        'B',
        'C',
        'D',
        'E',
        'F',
        'G',
        'H',
        'S',
        'T',
        'U',
        'V',
        'W',
        'X',
        'Y',
        'Z',
        'up_arrow',
        'down_arrow',
        'right_arrow',
        'left_arrow',
        'yellow_circle',
        'bullseye' 
    ],
    'nc': '31',
    'train': 'mdpimages-1/train/images',
    'val' : 'mdpimages-1/valid/images'
}

# Write YAML file
with io.open('./mdpimages-1/data.yaml', 'w', encoding='utf8') as outfile:
    yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)

# Read YAML file
with open("./mdpimages-1/data.yaml", 'r') as stream:
    data_loaded = yaml.safe_load(stream)

print(data == data_loaded)