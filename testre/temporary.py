from contextlib import contextmanager
from tempfile import mkdtemp

from pathlib import Path


# This function exists because tempfile.TemporaryDirectory wasn't added
# until 3.2 and 2.7 support is desired (read: required). Since a custom
# version needs to be made anyway, that version is used even in places
# where tempfile.TemporaryDirectory is available.
@contextmanager
def temporary_directory():
    """
    Create a temporary directory that will be emptied and deleted on
    context manager exit. Returns the string path to the directory.
    """
    temp = Path(mkdtemp())

    try:
        yield temp
    finally:
        remove_directory(temp)


def remove_directory(path):
    """
    Recursively delete a directory.
    """
    for subpath in path.iterdir():
        if subpath.is_dir():
            remove_directory(subpath)
        else:
            subpath.unlink()

    path.rmdir()
