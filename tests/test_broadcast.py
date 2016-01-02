import pytest
from git_multi.commands import broadcast
import textwrap


@pytest.mark.xfail
def test_broadcast(tmpdir):
    config_file = tmpdir.join('multi.cfg')
    config_file.write(textwrap.dedent('''\
    [repository "foo"]
        work-tree = foo
        git-dir = foo/.git
        bare = false
    [repository "bar"]
        git-dir = bar.git
        bare = true
    '''))
    for name, res in broadcast(config_file.strpath, ['init']):
        print(name)
        print('stdout:')
        print(res.stdout.decode('utf-8'))
        print('stderr:')
        print(res.stderr.decode('utf-8'))
    assert False
