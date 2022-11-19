from json import loads
import os
OUTPUT_DIR = 'output'
f = open('config.json')
configs = loads(f.read())
br = '\n'


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
            # print(enum)
        properties += f'''
  {field['name']}:
    type: {field['type']}
    description: {field['name']} of {config['name']} {br+enum if enum != "" else ""}
    example: {field['example']}
'''
        if field['required']:
            required_fields += f'  - {field["name"]}\n'
    f = open('templates/schema.template')
    template = f.read()
    f.close()

    template = template.replace('%REQUIRED_FIELDS%', required_fields)
    template = template.replace('%PROPERTIES%', properties)
    print(template)
    f = open(f'{SCHEMA_DIR}/{object["name"]}.yaml', 'w')
    f.write(template)
    f.close()


for config in configs:
    create_schema(config)
