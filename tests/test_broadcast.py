import textwrap
from git_multi.commands import broadcast, init


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
    for name, res in init(config_file.strpath):
        assert res.returncode == 0
    for name, res in broadcast(config_file.strpath, ['log']):
        assert res.returncode == 128, 'no commit'
