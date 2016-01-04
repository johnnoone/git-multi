import argparse
from git_multi.repository import prepare
from git_multi.conf import Settings


def register(config_file, repo):
    with Settings(config_file) as settings:
        settings.repositories.add(repo)


def main(config_file, args):
    parser = argparse.ArgumentParser(prog="git-multi register")
    parser.add_argument('name')
    parser.add_argument('--work-tree')
    parser.add_argument('--git-dir')
    parser.add_argument('--bare', action='store_true')
    args = parser.parse_args(args)
    repo = prepare(**vars(args))
    register(config_file, *repo)
