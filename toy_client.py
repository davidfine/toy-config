# Inputs: Console arguments - name of role, logging level.
# External classes: TaskHandler
# Actions: Git pull role repo, apply actions in runbook.yml to local system (command, file, template)
# Output: Log to file. Configuration changes are made to local system.

import git
import yaml
import argparse
import logging
import os
import sys
import TaskHandler


def apply_full(roles_dir):
    returncode = 0
    LOGGER.info('-> Applying full configuration')
    runbook = role_file_parser('{}/runbook.yml'.format(roles_dir), 'all')
    task_handler = TaskHandler.TaskHandler(runbook=runbook, roles_dir=roles_dir)
    for task in runbook['tasks']:
        LOGGER.info('-> Starting Task: {}'.format(task['name']))
        LOGGER.debug('>>> {}'.format(task))
        try:
            output = task_handler.handle_task(task)
            LOGGER.info(output)
        except Exception as e:
            LOGGER.warn(e)
            returncode = 1
    return returncode


def start_logging(verbose):
    logger = logging.getLogger('ToyClient')
    logging_filehandler = logging.FileHandler('/var/log/toy-client.log')
    logging_streamhandler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    logging_filehandler.setFormatter(formatter)
    logging_streamhandler.setFormatter(formatter)
    logger.addHandler(logging_filehandler)
    logger.addHandler(logging_streamhandler)
    logger.setLevel(logging.DEBUG) if verbose else logger.setLevel(logging.INFO)
    logger.info('-> Started logging')
    return logger


def update_repo(url, directory):
    """
    :param url: git url
    :param directory: destination for the repo
    :return:
    """
    try:
        if os.path.isdir(directory):
            g = git.cmd.Git(directory)
            g.pull()
        else:
            git.Repo.clone_from(url, directory)
    except Exception as e:
        LOGGER.warn(e)


def role_file_parser(rolefile, section):
    """
    :param rolefile: a YAML file
    :param section: selects 'attributes', 'tasks', 'comments', 'runbook_name', or 'all'
    :return: dict of a portion of rolefile
    """
    with open(rolefile) as yamlfile:
        parsed = yaml.load(yamlfile)
    if section == 'all':
        return parsed
    if section == 'tasks':
        return parsed['tasks']
    if section == 'attributes':
        return parsed['attributes']


def main(args):
    role = args.role
    ROLES_DIR = '/tmp/{}'.format(role)
    git_url = 'https://github.com/davidfine/toy-role.git'
    try:
        update_repo(git_url, ROLES_DIR)
    except Exception as e:
        return e

    try:
        returncode = apply_full(ROLES_DIR)

    except Exception as e:
        return e
    return returncode


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Configure local system based on Role')
    argparser.add_argument('--role', required=True, help='name of git repo with runbook and files.')
    argparser.add_argument('--verbose', action='store_true', help='set log level to debug')
    ARGS = argparser.parse_args()

    LOGGER = start_logging(ARGS.verbose)

    sys.exit(main(ARGS))