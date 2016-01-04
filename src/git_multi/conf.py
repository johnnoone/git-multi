from collections import defaultdict
from .repository import Repository
from .shell import Command
import os.path
import textwrap


class ConfigLexer:

    def lex(self, data):
        data = textwrap.dedent(data.strip('\n'))
        output, section, block = [], '', ''
        for line in data.splitlines(True):
            if line.startswith('['):
                block = self.drain_block(section, block, output)
                section = line.strip()[1:-1]
                continue
            else:
                block += line
        else:
            block = self.drain_block(section, block, output)
        return output

    __call__ = lex

    def drain_block(self, section, block, output):
        if block:
            block = textwrap.dedent(block)
            key, values = '', []
            for line in block.splitlines():
                if not line.strip():
                    continue

                if key and line[0] in (' ', '\t'):
                    # it must be a value
                    values.append(line.strip())
                    pass
                if '=' in line:
                    if key:
                        output.append((section, key, values))
                        values = []
                    key, _, val = line.partition('=')
                    key = key.strip()
                    val = val.strip()
                    if val:
                        values.append(val)
            if key:
                output.append((section, key, values))
                values = []
        return ''


class ConfigParser:

    def parse_repository(self, key, values, repository):
        if key == 'work-tree':
            repository['work_tree'] = values[-1]
        elif key == 'git-dir':
            repository['git_dir'] = values[-1]
        elif key == 'bare':
            repository['bare'] = values[-1] == 'true'
        else:
            raise ValueError('unknown option %s' % key)

    def parse(self, data):
        repositories = defaultdict(lambda: {
            'work_tree': None,
            'git_dir': None,
            'bare': None
        })
        for section, key, values in data:
            if section.startswith('repository '):
                name = section[12:-1]
                repository = repositories[name]
                self.parse_repository(key, values, repository)

            else:
                raise ValueError('unknown section %s' % section)

        repositories = {Repository(name, **opts)
                        for name, opts in repositories.items()}
        return {
            'repositories': repositories
        }

    __call__ = parse


class ConfigReader:

    def __init__(self):
        self.lexer = ConfigLexer()
        self.parser = ConfigParser()

    def read(self, data):
        data = self.lexer(data)
        data = self.parser(data)
        return data

    def read_from_filename(self, filename):
        with open(filename) as file:
            data = file.read()
            return self.read(data)
        return data

    __call__ = read


class ConfigWriter:

    def write(self, conf):

        def clean(value):
            if value is True:
                return 'true'
            if value is False:
                return 'false'
            if value is None:
                return 'null'
            return value

        buf = ''
        for repository in conf['repositories']:
            buf += '[repository "%s"]\n' % repository.name
            if repository.work_tree is not None:
                buf += '\twork-tree = %s\n' % repository.work_tree
            if repository.git_dir is not None:
                buf += '\tgit-dir = %s\n' % repository.git_dir
            if repository.bare is not None:
                buf += '\tbare = %s\n' % clean(repository.bare)
        return buf
    __call__ = write

    def write_into_filename(self, filename, conf):
        with open(filename, 'w') as file:
            data = self.write(conf)
            file.write(data)


class Settings:

    def __init__(self, config_file=None):
        self._reader = ConfigReader().read_from_filename
        self._writer = ConfigWriter().write_into_filename
        self._config = {'repositories': set()}
        if os.path.isfile(config_file):
            self._config = self._reader(config_file)
        self.config_file = config_file

    def save(self):
        self._writer(self.config_file, self._config)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.save()

    @property
    def cwd(self):
        return os.path.dirname(self.config_file)

    @property
    def repositories(self):
        return self._config['repositories']

    def Command(self, *cmd, **kwargs):
        cwd = os.path.join(self.cwd, kwargs.pop('cwd', '.'))
        return Command(*cmd, cwd=cwd, **kwargs)
