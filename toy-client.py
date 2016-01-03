

### Inputs: name of role, location of github repo, switch for full update

### Actions: Git pull role file, apply actions in it to local host (command, file, template)

### Output: Log to file

__author__ = 'dfine'

from jinja2 import Environment, FileSystemLoader
from configobj import ConfigObj
import git
import argparse
import subprocess
import logging
import os

### Setup Argparse
argparser = argparse.ArgumentParser(description = "Configure local system based on Role and Environment")
argparser.add_argument('--role', required=True, help='github account and repo containing config. Example: davidfine/toy-config')
#argparser.add_argument('--environment', required=False, default='prod' help='github account and repo containing config. Example: davidfine/toy-config')
argparser.add_argument('--update', action='store_true', help= "update only items changed in most recent git push")
args = argparser.parse_args()
print args

### Globals
ROLE = args.role
ENVIRONMENT = 'prod'
TEMPLATE_ENV = Environment(loader=FileSystemLoader('roles/{0}/templates'.format(ROLE)))
ATTRIBUTES = ConfigObj('roles/{0})/variables/{1}'.format(ROLE, ENVIRONMENT))
REPO = git.Repository("/src/{0}".format(ROLE))


### Setup Logging
logger = logging.getLogger('ToyClient')
hdlr = logging.FileHandler('/var/log/toy-client.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)
logger.info("started logging")


def apply_full():
    ''' Run all actions in role configuration file '''


def apply_updates():
    ''' Run only parts that have changed'''

def role_file_parser(rolefile):
    ''' Yeild one configuration action per line of role file
    :param rolefile:
    :return: Yeild actions appropriate for config_actions()
    '''
class config_actions(object):
    ''' Actions to configure the local node as described by role configuration file
    '''
    def __init__(self):
        pass


    def run_script(self, script):
        '''
        :param script: shell command followed by argument(s)
        :return: stdout, stderr from shell
        '''


    def copy_file(self, source, destination):
        '''
        :param source: location of file relative to repo root
        :param destination: full path to destination on local fs
        :return: 0 if success else exception
        '''


    def copy_template_to_file(self, source, ATTRIBUTES):
        '''
        :param source: template path relative to repo root
        :param ATTRIBUTES: attributes dict, global
        :return: 0 if success else exception
        '''
        template = TEMPLATE_ENV.get_template(source)
        path = '/%s' % source
        with open(path, 'w') as file:
            file.write(template.render(ATTRIBUTES=ATTRIBUTES))
            print("wrote file %s" % path)


###
def changed_files(REPO):
    '''
    :param REPO: http url of Role repo
    :return: list of files which have changed between last two pushes
    '''
    commits_list = list(REPO.iter_commits())
    changed_files = []
    changed_files.append([ x.a_path for x in commits_list[0].diff(commits_list[1]) if x.a_path not in changed_files ])
    changed_files.append([ x.b_path for x in commits_list[0].diff(commits_list[1]) if x.b_path not in changed_files ])
    return changed_files


if __name__ == '__main__':
    if args.update:
        apply_updates()
    else:
        apply_full()
