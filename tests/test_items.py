from . import fixture
from git_multi.commands import items


def test_read():
    config_file = fixture('config.cfg')

    with open(config_file) as file:
        data = file.read()
    print(data)
    opts = dict(items(config_file))
    assert 'foo' in opts
    assert 'bar' in opts
    assert opts['foo'].work_tree == 'foo'
    assert opts['foo'].git_dir == 'foo/.git'
    assert opts['foo'].bare is False
    assert opts['bar'].work_tree is None
    assert opts['bar'].git_dir == 'bar.git'
    assert opts['bar'].bare is True
