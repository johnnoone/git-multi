#!/usr/bin/env python

import argparse
import git_multi
import pkg_resources


def _registered_commands(group='git_multi.commands'):
    registered_commands = pkg_resources.iter_entry_points(group=group)
    return dict((c.name, c) for c in registered_commands)


def dispatch(args):
    registered_commands = _registered_commands()
    parser = argparse.ArgumentParser(prog="git-multi")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s version {0}".format(git_multi.__version__),
    )

    parser.add_argument(
        '--config-file',
        default='.multi.cfg'
    )
    parser.add_argument(
        "command",
        choices=registered_commands.keys(),
    )
    parser.add_argument(
        "args",
        help=argparse.SUPPRESS,
        nargs=argparse.REMAINDER,
    )

    ns = parser.parse_args(args)
    main = registered_commands[ns.command].load()
    main(ns.config_file, ns.args)
