

### Inputs: name of role, location of github repo, switch for full update

### Actions: Git pull role file, apply actions in it to local host (command, file, template)

### Output: Log to file

__author__ = 'dfine'

from jinja2 import Environment, FileSystemLoader
import git
import yaml
import argparse
import subprocess
import logging
import os
import TaskHandler


def apply_full(ROLES_DIR):
    print('roles_dir:{}'.format(ROLES_DIR))
    runbook = role_file_parser('{}/runbook.yml'.format(ROLES_DIR), 'all')
    print('runbook:{}'.format(runbook))
    task_handler = TaskHandler.TaskHandler(runbook=runbook, roles_dir=ROLES_DIR)
    update_repo(GIT_URL, ROLES_DIR)
    for task in runbook['tasks']:
        output = task_handler.handle_task(task)
        LOGGER.info(output)


def start_logging():
    logger = logging.getLogger('ToyClient')
    hdlr = logging.FileHandler('/var/log/toy-client.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)
    logger.info("started logging")
    return logger


def update_repo(url, dir):
    ''' Pull repo, or clone if doens't exist '''
    print(url, dir)
    try:
        if os.path.isdir(dir):
            g = git.cmd.Git(dir)
            g.pull()
        else:
            git.Repo.clone_from(url, dir)
    except Exception as e:
        LOGGER.warn(e)
        print(e)


def role_file_parser(rolefile, section):
    '''
    :param rolefile: a YAML file
    :return: dict of a portion of rolefile
    '''
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


def apply_updates(ROLE):
    ''' Run only parts that have changed'''


if __name__ == '__main__':

    argparser = argparse.ArgumentParser(description = "Configure local system based on Role and Environment")
    argparser.add_argument('--role', required=True, help='github account and repo containing config. Example: davidfine/toy-config')
    argparser.add_argument('--update', action='store_true', help= "update only items changed in most recent git push")
    args = argparser.parse_args()

    ### Globals
    LOGGER = start_logging()
    ROLE = args.role
    ROLES_DIR = '/tmp/{}'.format(ROLE)
    GIT_URL = 'https://github.com/davidfine/toy-role.git'
    print(GIT_URL)
    update_repo(GIT_URL, ROLES_DIR)

    LOGGER.info('Applying full configuration')
    apply_full(ROLES_DIR)

