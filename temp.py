import git
import os
import yaml
from TaskHandler import TaskHandler
import logging
from jinja2 import Environment, FileSystemLoader, Template


def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)
    env = Environment(loader=FileSystemLoader(path))
    template = env.get_template(filename)
    print(template)
    return template.render(context)

context = {
    'firstname': 'John',
    'lastname': 'Doe'
}

result = render('/src/toy-role/templates/test.txt', context)
print(result)
'''

def render_template(source, destination, attributes):
    template = jinja2.Environment(loader=jinja2.FileSystemLoader(source)
    ).get_template(filename).render(attributes)

def role_file_parser(rolefile, section):

    with open(rolefile) as yamlfile:
        parsed = yaml.load(yamlfile)
    if section == 'all':
        return parsed
    if section == 'tasks':
        return parsed['tasks']
    if section == 'attributes':
        return parsed['attributes']
    else:
        return 0

attributes = role_file_parser('/src/toy-role/runbook.yml', 'attributes')

apply_template('/src/toy-role/templates/test_template.txt', destination='/tmp/test_template.txt', attributes=attributes)
'''

'''
ATTRIBUTES = 'attributes!!'
ATTRIBUTES2 = "attributes2"
run_book = role_file_parser('/src/toy-config/test_rolefile.yml', 'all')
task = run_book['tasks'][0]
print(task)

handler = TaskHandler(run_book)
output = handler.copy_file(source=task['source'], destination=task['destination'], owner=task['owner'],
                                        group=task['group'], mode=task['mode'])
print(output)

def role_file_parser(rolefile):

    with open(rolefile) as yamlfile:
        tasks = yaml.load(yamlfile)['tasks']
    return tasks

def start_logging():
    logger = logging.getLogger('ToyClient')
    hdlr = logging.FileHandler('/var/log/toy-client.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)
    logger.info("started logging")
    return logger

def test_logging():
    logger.info('test passed')

#tasks = role_file_parser(rolefile)['tasks']


def route(task):
    pass

for task in tasks:
    if task['action'] == 'commands':
        for command in task['commands']:
            print(command)
            output = action.run_command(command)
            print(output)
    elif task['action'] == 'file':
            output = action.copy_file(source=task['source'], destination=task['destination'])
            print(output)
    elif task['action'] == 'template':
            output = action.copy_template_to_file(source=task['source'], destination=task['destination'])
            print(output)



tasks = role_file_parser(rolefile)
print(tasks)
for task in tasks:
    print(task)
    action.handle_task(task)

'''
