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
    },
    cmdclass=versioneer.get_cmdclass()
)
