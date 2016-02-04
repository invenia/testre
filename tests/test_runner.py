"""
Tests for the runner
"""
from nose.tools import assert_equals, assert_raises
import rethinkdb


def test_basic():
    """
    run a db temporarily
    """
    from testre.runner import run

    with run() as the_port:
        port = the_port

        connection = rethinkdb.connect(port=port)

        result = rethinkdb.db('test').table_create('testre').run(connection)
        assert_equals(result['tables_created'], 1)

    with assert_raises(rethinkdb.ReqlDriverError):
        connection = rethinkdb.connect(port=port)

    # a new connection should happen on a new db
    with run(port=port) as the_port:
        assert_equals(port, the_port)

        connection = rethinkdb.connect(port=port)

        assert_equals(rethinkdb.db('test').table_list().run(connection), [])

    with assert_raises(rethinkdb.ReqlDriverError):
        connection = rethinkdb.connect(port=port)


def test_copied_data():
    """
    db with copied data
    """
    from testre.runner import run
    from testre.temporary import temporary_directory

    with temporary_directory() as tempdir:
        with run(path=tempdir, port=11111) as port:
            assert_equals(port, 11111)

            original = rethinkdb.connect(port=port)

            result = rethinkdb.db('test').table_create('testre').run(original)
            assert_equals(result['tables_created'], 1)

        # we now have a non-empty db to copy
        with run(data_directory=tempdir, port=11112):
            copy = rethinkdb.connect(port=11112)

            assert_equals(
                rethinkdb.db('test').table_list().run(copy),
                ['testre']
            )

            result = rethinkdb.db('test').table_create('table2').run(copy)
            assert_equals(result['tables_created'], 1)

        # we did an actual copy, right
        with run(path=tempdir, port=11111):
            original = rethinkdb.connect(port=11111)

            assert_equals(
                rethinkdb.db('test').table_list().run(original),
                ['testre']
            )

            # while we're here, might as well connect to a bound port
            with assert_raises(OSError):
                with run(port=11111):
                    raise AssertionError

            # everything still cool?
            assert_equals(
                rethinkdb.db('test').table_list().run(original),
                ['testre']
            )
