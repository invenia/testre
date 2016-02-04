"""
The actual rethink runner
"""
from contextlib import contextmanager
from logging import getLogger
from shutil import copytree
from subprocess import Popen, check_call, CalledProcessError, PIPE

from testre.temporary import temporary_directory


@contextmanager
def run(data_directory=None, port=28015, path=None, logger=None):
    """
    Temporarily run a rethink database

    data_directory: (optional, None) If given the path to a
        rethinkdb_data directory to duplicate and use.
    port: (optional, 28015) The port to run the database on.
    path: (optional, None) The location to store the data directory. If
        not given, a temporary directory will be used. If your tests
        involve writing to the database, you should instead use
        data_directory as it will guarantee your testing database
        remains in a pristine state.
    logger: (optional, None) The name of the logger to use.
    """
    with temporary_directory() as tempdir:
        if data_directory:
            if path:
                raise ValueError('cannot add data to existing path')

            path = tempdir / 'rethinkdb_data'
            copytree(str(data_directory), str(path))
        elif path is None:
            path = tempdir

        # we want an empty log file so it is easier to parse. Make
        # our own log file
        logfile = tempdir / 'log_file'

        pidfile = tempdir / 'pidfile'

        try:
            # The reason we are using Popen instead of check_call here
            # is that the call writes some output to stdout and we don't
            # want that text to pollute our process' stdout. Sadly,
            # subprocess doesn't provide a clean way to /dev/null output
            # without using Popen directly.
            process = Popen(
                (
                    'rethinkdb',
                    '--no-http-admin',
                    '--no-update-check',
                    '--daemon',
                    '--directory',
                    str(path),
                    '--pid-file',
                    str(pidfile),
                    '--driver-port',
                    str(port),
                    '--log-file',
                    str(logfile)
                ),
                stdout=PIPE
            )
            process.communicate()

            if process.returncode != 0:
                raise OSError("Could not start rethinkdb")

            getLogger(logger).info("rethinkdb running on {}".format(port))

            # wait for the log file to be generated
            while not logfile.exists():
                pass

            # don't yield until the db can receive connections
            available = False

            while not available:
                with logfile.open() as f_in:
                    for line in f_in:
                        if 'Listening for client driver' in line:
                            available = True
                            break
                        elif 'error: TCP socket creation failed' in line:
                            # The pidfile briefly exists while the
                            # daemon cleans itself up. pypy is fast
                            # enough that we may actually attempt to
                            # kill it in the finally clause. This will
                            # cause an error. We can't just skip that
                            # exists check in the finally as we then may
                            # get into a race condition between rethink
                            # shutting down and tempdir being deleted.
                            while pidfile.exists():
                                pass

                            raise OSError("Could not bind to port")

            yield port
        finally:
            # only try to kill the process if it exists.
            if pidfile.exists():
                with pidfile.open() as f_in:
                    pid = f_in.read()

                    try:
                        check_call(('kill', pid))
                    except CalledProcessError:
                        getLogger(logger).exception(
                            "could not kill process: {}".format(pid)
                        )

                        raise
                    else:
                        # we need to wait for the process to actually
                        # die or else there will be a race condition on
                        # the pidfile when deleting the temporary
                        # directory
                        running = True

                        while running:
                            # Popen because we want to silence the stderr
                            # message that pid doesn't exist. It is the
                            # entire reason we are running this command
                            # in the first place
                            process = Popen(('kill', '-0', pid), stderr=PIPE)
                            process.communicate()

                            running = (process.returncode == 0)

                        getLogger(logger).info("rethinkdb process ended")
            else:
                getLogger(logger).info("no rethinkdb running")
