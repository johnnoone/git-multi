from git_multi.commands import init
import textwrap


def test_init(tmpdir):
    config_file = tmpdir.join('multi.cfg')
    config_file.write(textwrap.dedent('''\
    [repository "foo"]
        work-tree = foo
        git-dir = foo/.git
        bare = false
    [repository "bar"]
        work-tree = bar
        bare = false
    [repository "baz"]
        work-tree = baz
        git-dir = baz.git
        bare = false
    [repository "qux"]
        git-dir = qux.git
        bare = true
    '''))
    for name, res in init(config_file.strpath):
        assert res.returncode == 0
