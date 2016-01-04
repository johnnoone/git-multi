from .shell import Command
import shlex


def expand(command, *args):
    """Expands git alias
    """
    proc = Command('git', 'config', 'alias.%s' % command)
    if proc.wait() == 0:
        return shlex.split(proc.stdout) + args
    return [command] + list(args)
