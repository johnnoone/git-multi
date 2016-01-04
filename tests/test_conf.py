from git_multi.conf import ConfigLexer, ConfigParser, ConfigReader
from git_multi.repository import Repository


def test_lexer():
    lexer = ConfigLexer()
    output = lexer.lex('''
    [repository "foo"]
        work-tree = foo
        git-dir = foo/.git
        bare = false
    [repository "bar"]
        git-dir = bar.git
        bare = true
    ''')
    assert output == [
        ('repository "foo"', 'work-tree', ['foo']),
        ('repository "foo"', 'git-dir', ['foo/.git']),
        ('repository "foo"', 'bare', ['false']),
        ('repository "bar"', 'git-dir', ['bar.git']),
        ('repository "bar"', 'bare', ['true'])
    ]


def test_parser():
    parser = ConfigParser()
    output = parser.parse([
        ('repository "foo"', 'work-tree', ['foo']),
        ('repository "foo"', 'git-dir', ['foo/.git']),
        ('repository "foo"', 'bare', ['false']),
        ('repository "bar"', 'git-dir', ['bar.git']),
        ('repository "bar"', 'bare', ['true'])
    ])
    assert output == {
        'repositories': {
            Repository(name="foo",
                       work_tree='foo',
                       git_dir='foo/.git',
                       bare=False),
            Repository(name="bar",
                       work_tree=None,
                       git_dir='bar.git',
                       bare=True)
        }
    }


def test_reader():
    reader = ConfigReader()
    output = reader('''
    [repository "foo"]
        work-tree = foo
        git-dir = foo/.git
        bare = false
    [repository "bar"]
        git-dir = bar.git
        bare = true
    ''')
    assert output == {
        'repositories': {
            Repository(name="foo",
                       work_tree='foo',
                       git_dir='foo/.git',
                       bare=False),
            Repository(name="bar",
                       work_tree=None,
                       git_dir='bar.git',
                       bare=True)
        }
    }
