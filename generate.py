from json import loads
import os
OUTPUT_DIR = 'output'
f = open('config.json')
configs = loads(f.read())
br = '\n'


def get_template(name):
    f = open(f'templates/{name}.template')
    template = f.read()
    f.close()
    return template


def write_data(data, file):
    f = open(file, 'w')
    f.write(data)
    f.close()


def create_schema(object):
    SCHEMA_DIR = f'{OUTPUT_DIR}/schemas'
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    if not os.path.exists(SCHEMA_DIR):
        os.makedirs(SCHEMA_DIR)
    required_fields = ""
    properties = ""
    for field in config['fields']:
        enum = ''
        if field.get('enum') is not None:
            enum += '    enum:'
            for item in field.get('enum'):
                enum += f'\n      - {item}'
        properties += f'''
  {field['name']}:
    type: {field['type']}
    description: {field['name']} of {config['name']} {br+enum if enum != "" else ""}
    example: {field['example']}
'''
        if field['required']:
            required_fields += f'  - {field["name"]}\n'
    template = get_template('schema')
    template = template.replace('%REQUIRED_FIELDS%', required_fields)
    template = template.replace('%PROPERTIES%', properties)
    write_data(template, f'{SCHEMA_DIR}/{object["name"]}.yaml')


def create_path(object):
    PATH_DIR = f'{OUTPUT_DIR}/paths'
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    if not os.path.exists(PATH_DIR):
        os.makedirs(PATH_DIR)
    object_name = object['name']
    capital_object_name = object['name'].capitalize()
    template = get_template('path')
    template = template.replace('%OBJECT_NAME%', object_name)
    template = template.replace('%CAPITAL_OBJECT_NAME%', capital_object_name)
    write_data(template, f'{PATH_DIR}/{object["name"]}.yaml')


for config in configs:
    create_schema(config)
    create_path(config)