import argparse
import os.path
from git_multi.conf import Settings


def init(config_file):
    settings = Settings(config_file)

    procs = []
    for repo in settings.repositories:
        work_tree, git_dir, bare = repo.work_tree, repo.git_dir, repo.bare
        if bare:
            cmd = ['git', 'init', '--bare', git_dir]
        elif git_dir and git_dir != os.path.join(work_tree, '.git'):
            cmd = ['git', 'init', '--separate-git-dir', git_dir, work_tree]
        else:
            cmd = ['git', 'init', work_tree]
        procs.append((repo.name, settings.Command(*cmd)))
    for name, proc in procs:
        proc.wait()
        yield name, proc.result


def main(config_file, args):
    parser = argparse.ArgumentParser(prog="git-multi init")
    args = parser.parse_args(args)
    init(config_file, **vars(args.args))
