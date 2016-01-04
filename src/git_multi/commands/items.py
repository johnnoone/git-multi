import argparse
from git_multi.conf import Settings


def items(config_file):
    settings = Settings(config_file)
    for repo in settings.repositories:
        yield repo.name, repo


def main(config_file, args):
    parser = argparse.ArgumentParser(prog="git-multi list")
    args = parser.parse_args(args)
    for name, opts in items(config_file, **vars(args)):
        print('%:10s %s %s %s' % name, opts.work_tree, opts.git_dir, opts.bare)
