#!/usr/bin/env python

from setuptools import setup
import versioneer

setup(
    name='git-multi',
    version=versioneer.get_version(),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'git-multi=git_multi.cli:main'
        ],
        'git_multi.commands': [
            'register = git_multi.commands.register:main',
            'list = git_multi.commands.items:main',
            'init = git_multi.commands.init:main',
            '-- = git_multi.commands.dispatch:main',
        ],
    },
    cmdclass=versioneer.get_cmdclass()
)
