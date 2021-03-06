import subprocess
import shutil
import os
import jinja2

class TaskHandler(object):
    """
    Actions to configure the local node as described by role configuration file
    :param attributes: dict of attributes including template variables
    """

    def __init__(self, runbook, roles_dir):
        self.attributes = runbook['attributes']
        self.templates_dir = '{}/templates'.format(roles_dir)
        self.jinja_environmenent = jinja2.Environment(loader=jinja2.FileSystemLoader(self.templates_dir))
        self.roles_dir = roles_dir


    def handle_task(self, task):
        if task['action'] == 'commands':
            output = ""
            for command in task['commands']:
                try:
                    output += self.run_command(command)
                except Exception as e:
                    raise e
            return output

        elif task['action'] == 'file':
                output = self.copy_file(source=task['source'], destination=task['destination'], owner=task['owner'],
                                        group=task['group'], mode=task['mode'])
                return output
        elif task['action'] == 'template':
                output = self.copy_template_to_file(source=task['source'],
                                                    destination=task['destination'], attributes=self.attributes)
                return output


    def run_command(self, command):
        try:
            output = subprocess.check_output(command, universal_newlines=True, shell=True, timeout=60)
        except subprocess.CalledProcessError:
            raise
        except subprocess.TimeoutExpired:
            raise
        return '<- {}'.format(output)


    def copy_file(self, source, destination, owner='root', group='root', mode='640'):
        '''
        :param source: location of file relative to repo root
        :param destination: full path to destination on local fs
        :return: 0 if success else exception
        '''
        path = '{}/files/{}'.format(self.roles_dir, source)
        shutil.copyfile(path, destination)
        shutil.chown(destination, user=owner, group=group)
        os.chmod(destination, mode)
        return '<- Copied {} to {}'.format(source, destination)

    def copy_template_to_file(self, source, destination, attributes):
        template = self.jinja_environmenent.get_template(source)
        with open(destination, 'w') as f:
            f.write(template.render(attributes=attributes))
        return '<- wrote file from template: {}'.format(destination)
