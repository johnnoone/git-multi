import argparse
from git_multi.conf import Settings


def broadcast(config_file, args):
    settings = Settings(config_file)

    procs = {}
    for repo in settings.repositories:
        cwd = repo.git_dir if repo.bare else repo.work_tree
        procs[repo.name] = settings.Command(['git'] + args, cwd=cwd)
    for name, proc in procs.items():
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
