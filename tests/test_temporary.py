"""
Tests for the temporary_directory function
"""
from nose.tools import assert_true, assert_false, assert_raises


def test_empty():
    """
    Empty temporary directory
    """
    from testre.temporary import temporary_directory

    with temporary_directory() as tempdir:
        temp = tempdir

        assert_true(temp.exists())

    assert_false(temp.exists())


def test_non_empty():
    """
    Temporary directory with files
    """
    from testre.temporary import temporary_directory

    with temporary_directory() as tempdir:
        temp = tempdir

        assert_true(temp.exists())

        for filename in ('foo', 'bar', 'baz'):
            filepath = temp / filename

            with filepath.open('w') as f_out:
                f_out.write(u"It's a file!")

            assert_true(filepath.exists())

    assert_false(temp.exists())


def test_nested():
    """
    Nested temporary directories
    """
    from testre.temporary import temporary_directory

    with temporary_directory() as tempdir:
        temp = tempdir

        assert_true(temp.exists())

        directory = temp / 'alpha'

        directory.mkdir()

        for filename in ('bravo', 'beta', 'getti'):
            filepath = directory / filename

            with filepath.open('w') as f_out:
                f_out.write(u'content')

            assert_true(filepath.exists())

    assert_false(temp.exists())


def test_exception():
    """
    An exception during temporary directory
    """
    from testre.temporary import temporary_directory

    class CustomException(Exception):
        """
        You know, for testing
        """

    with assert_raises(CustomException):
        with temporary_directory() as tempdir:
            temp = tempdir

            assert_true(temp.exists())

            for filename in ('foo', 'bar', 'baz'):
                filepath = temp / filename

                with filepath.open('w') as f_out:
                    f_out.write(u'read me')

                assert_true(filepath.exists())

            raise CustomException

    assert_false(temp.exists())
