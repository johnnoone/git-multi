from .repository import Repository
from .shell import Command
import os.path
try:
    from configparser import RawConfigParser, DuplicateSectionError
except:
    from ConfigParser import RawConfigParser, DuplicateSectionError


class Settings:

    def __init__(self, config_file=None):
        self.config = RawConfigParser()
        if os.path.isfile(config_file):
            self.config.read(config_file)
        self.config_file = config_file

    def save(self):
        with open(self.config_file, 'w') as file:
            self.config.write(file)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.save()

    @property
    def cwd(self):
        return os.path.dirname(self.config_file)

    @property
    def repositories(self):
        for section in self.config.sections():
            if section.startswith('repository '):
                name = section[12:-1]
                opts = {'work_tree': None,
                        'git_dir': None,
                        'bare': None}
                if self.config.has_option(section, 'work-tree'):
                    opts['work_tree'] = self.config.get(section, 'work-tree')
                if self.config.has_option(section, 'git-dir'):
                    opts['git_dir'] = self.config.get(section, 'git-dir')
                if self.config.has_option(section, 'bare'):
                    opts['bare'] = self.config.getboolean(section, 'bare')
                yield Repository(name, **opts)

    def add_repository(self, repo):
        section = 'repository "%s"' % repo.name
        try:
            self.config.add_section(section)
        except DuplicateSectionError:
            for opt, val in self.config.items(section):
                self.config.remove_option(section, opt)
        if repo.work_tree:
            self.config.set(section, 'work-tree', repo.work_tree)
        self.config.set(section, 'git-dir', repo.git_dir)
        self.config.set(section, 'bare', 'true' if repo.bare else 'false')

    def Command(self, cmd, **kwargs):
        cwd = os.path.join(self.cwd, kwargs.pop('cwd', '.'))
        return Command(cmd, cwd=cwd, **kwargs)
