from pianopy import __version__


def test_version():
    major, minor, bugfix = __version__.split('.')
    assert int(major) >= 0
    assert int(minor) >= 0
    assert int(bugfix) > 0
