import argparse
from git_multi.conf import Settings
from git_multi import alias


def broadcast(config_file, args):
    settings = Settings(config_file)

    procs = []
    for repo in settings.repositories:
        cmd = ['git'] + alias.expand(*args)
        cwd = repo.git_dir if repo.bare else repo.work_tree
        procs.append((repo.name, settings.Command(*cmd, cwd=cwd)))
    for name, proc in procs:
        proc.wait()
        yield name, proc.result


def main(config_file, args):
    parser = argparse.ArgumentParser(prog="git-multi --")
    parser.add_argument(
        "args",
        help=argparse.SUPPRESS,
        nargs=argparse.REMAINDER,
    )
    args = parser.parse_args(args)
    broadcast(config_file, **vars(args.args))
