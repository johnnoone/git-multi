from tempfile import NamedTemporaryFile
from git_multi.commands import register
from git_multi.repository import prepare


def test_write_implicite():
    tmpfile = NamedTemporaryFile()

    register(tmpfile.name, prepare('foo'))
    with open(tmpfile.name) as file:
        data = file.read()
    assert '[repository "foo"]' in data
    assert 'work-tree = foo' in data
    assert 'git-dir = foo/.git' in data
    assert 'bare = false' in data


def test_write_bare():
    tmpfile = NamedTemporaryFile()

    register(tmpfile.name, prepare('bar', bare=True))
    with open(tmpfile.name) as file:
        data = file.read()
    assert '[repository "bar"]' in data
    assert 'git-dir = bar.git' in data
    assert 'bare = true' in data


def test_write_explicite():
    tmpfile = NamedTemporaryFile()

    register(tmpfile.name, prepare('baz', bare=False, work_tree='qux'))
    with open(tmpfile.name) as file:
        data = file.read()
    assert '[repository "baz"]' in data
    assert 'work-tree = qux' in data
    assert 'git-dir = qux/.git' in data
    assert 'bare = false' in data
