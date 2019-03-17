#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Console script for tghs."""

import argparse
import configparser
import logging
import os
import sys

import appdirs
from github import Github
from trello import TrelloClient

from tghs.synchronizer import TrelloGitHubSynchronizer

LOGGER = logging.getLogger(__name__)


def _hello(args):
    print('Hello World!')


def _parse_args():
    parser = argparse.ArgumentParser(description='Trello Github Sync Command Line Interface')

    parser.add_argument('-c', '--config', help='Path to custom configuration file')
    parser.add_argument('-p', '--profile', help='Profile to use')
    parser.add_argument('projects', nargs='*', help='Names of the projects to process')

    return parser.parse_args()


def read_config(args):
    if args.config:
        config_file = args.config
    else:
        config_dir = appdirs.user_config_dir('tghs')
        config_file = os.path.join(config_dir, 'profiles', 'default.conf')

    conf = configparser.ConfigParser(interpolation=None)
    conf.optionxform = str    # Prevent lowercase keys

    if not os.path.isfile(config_file):
        raise FileNotFoundError("File {} not found".format(config_file))

    conf.read(config_file)

    return conf


def sync(config, projects):
    auth = config['auth']
    board = config['trello']['board']
    github_config = config['github']

    if not projects:
        projects = github_config.keys()
    else:
        for project in projects:
            if project not in github_config.keys():
                raise ValueError("Unknown project: {}".format(project))

    github = Github(auth['GITHUB_TOKEN'])
    trello = TrelloClient(
        api_key=auth['TRELLO_KEY'],
        api_secret=auth['TRELLO_SECRET'],
        token=auth['TRELLO_OAUTH_TOKEN'],
        token_secret=auth['TRELLO_OAUTH_SECRET']
    )

    tghs = TrelloGitHubSynchronizer(github, trello, board)

    for project in projects:
        repo = github_config[project]
        tghs.sync(repo, project)


def main():
    args = _parse_args()

    config = read_config(args)

    try:
        sync(config, args.projects)
        return 0
    except Exception as e:
        print(e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
