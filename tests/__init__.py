import os.path

here = os.path.dirname(os.path.abspath(__file__))
fixture_dir = os.path.join(here, 'fixtures')


def fixture(*paths):
    return os.path.join(fixture_dir, *paths)
