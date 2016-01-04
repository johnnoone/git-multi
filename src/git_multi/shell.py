from subprocess import Popen, PIPE
from collections import namedtuple

Result = namedtuple('Result', 'cmd stdout stderr returncode')


class Command:

    def __init__(self, *cmd, **kwargs):
        self.cmd = cmd
        self.kwargs = kwargs
        kwargs.setdefault('stdout', PIPE)
        kwargs.setdefault('stderr', PIPE)
        self.proc = Popen(cmd, **kwargs)

    @property
    def poll(self):
        return self.proc.poll

    def wait(self):
        # TODO implement timeout... (python3.3 feature)
        return self.proc.wait()

    @property
    def stdout(self):
        return self.proc.stdout

    @property
    def stderr(self):
        return self.proc.stderr

    @property
    def returncode(self):
        return self.proc.returncode

    @property
    def ok(self):
        if self.proc.returncode is not None:
            return self.proc.returncode is True

    @property
    def result(self):
        if self.poll is not None:
            return Result(self.cmd,
                          self.stdout.read(),
                          self.stderr.read(),
                          self.returncode)
