from json import loads
import os, sys
project_root = ""
if len(sys.argv) > 1:
    project_root = sys.argv[1]
OUTPUT_DIR = f'{project_root}/output'
f = open(f'{project_root}/config.json')
configs = loads(f.read())
f.close()
f = open(f'{project_root}/project_config.json')
project_configs = loads(f.read())
f.close()
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

    template = get_template('path_id')
    template = template.replace('%OBJECT_NAME%', object_name)
    template = template.replace('%CAPITAL_OBJECT_NAME%', capital_object_name)
    write_data(template, f'{PATH_DIR}/{object["name"]}_id.yaml')


def create_responses():
    template = get_template('response')
    write_data(template, f'{OUTPUT_DIR}/response.yaml')


def create_swagger_file(configs):
    servers = ""
    for server in project_configs['servers']:
        servers += f'  - url: {server["url"]}\n'
        servers += f'    description: {server["description"]}\n'
    paths = ""
    for config in configs:
        paths += f'\n  /{config["name"]}/:'
        paths += f'\n    $ref: ./paths/{config["name"]}.yaml'
        paths += f'\n  /{config["name"]}/{{id}}:'
        paths += f'\n    $ref: ./paths/{config["name"]}_id.yaml'
    template = get_template('swagger-ui')
    template = template.replace('%PROJECT_NAME%', project_configs['name'])
    template = template.replace('%EMAIL%', project_configs['email'])
    template = template.replace('%SERVERS%', servers)
    template = template.replace('%PATHS%', paths)
    write_data(template, f'{OUTPUT_DIR}/swagger-ui.yaml')


for config in configs:
    create_schema(config)
    create_path(config)
create_responses()
create_swagger_file(configs)
