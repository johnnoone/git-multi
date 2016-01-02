import os.path
from collections import namedtuple

Repository = namedtuple('Repository', 'name work_tree git_dir bare')


def prepare(name, work_tree=None, git_dir=None, bare=False):
    if bare:
        if not git_dir:
            git_dir = name
            if not name.endswith('.git'):
                git_dir += '.git'
    else:
        if not work_tree:
            work_tree = name
        if not git_dir:
            git_dir = os.path.join(work_tree, '.git')
    return Repository(name, work_tree, git_dir, bare)
