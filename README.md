Testre
======

A library for writing test cases against a temporary rethinkdb database.

Prerequisites
-------------

This should go without saying, but to run a rethinkdb server, you will need to have rethinkdb installed on your machine. Follow the instructions on their [website](http://rethinkdb.com/) for details.

Install
-------

Testre is available on pypi:
```sh
>pip install testre
```

It can also be installed directly:
```sh
>git clone https://github.com/invenia/testre
>cd testre
>python setup.py install
```

Usage
-----
Testre will run a rethinkdb server in a temporary directory, automatically stopping the process and cleaning up after you're done (or in case of an exception).

Basic usage:
```python
from testre import run_rethink

with run_rethink() as port:
    ...
```

You can pass the `port` argument to have the server listen on a specific port:
```python
with run_rethink(port=YOUR_PORT):
    ...
```

If testre cannot bind to a port it will clean itself up and then throw an `OSError`.

### Data ###
Sometimes you want to run tests against a database that has data in it. Testre provides to different ways to do this based on your needs.

If your tests don't modify the database, you can run directly on that database by passing a `pathlib.Path` to the `rethink_data` directory using the `path` argument.

If you are going to be making changes, a better option is to pass that directory as the first positional argument. Instead of running on that data directly, testre will copy that data and run on the copy. That way you can run all the tests your heart desires without worrying about breaking anything:
```python
with run_rethink(PATH_TO_YOUR_DATA) as port:
    ...
```

Should I Just Use This to Run my Rethinkdb Server All the Time?
---------------------------------------------------------------

No.

License
-------

Testre is available under the Mozilla Public License version 2.0.
