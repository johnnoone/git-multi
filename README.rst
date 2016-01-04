git-multi
=========

This repository implements ``git-multi`` command.

It allows to broadcast a bunch of commands to many repositories at once.

Register git repositories::

    git multi register foo
    git multi register bar --bare
    git multi register baz --git-dir bar.git

Initialize missing repositories::

    git multi init

Broadcast commands::

    git multi -- log --name-status HEAD^..HEAD
