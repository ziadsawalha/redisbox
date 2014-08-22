Redis Box
---------

Redis Box helps starting and stopping a sandboxed Redis instance
from within a Python process. The Redis instance is run with a
temporary directory to store any files and is configured to
be as lightweight as possible. It will choose a free port on localhost,
so it will not interfere with default Redis processes.
It is primarily expected to be used in unit tests and for prototyping concepts.

A typical use of a Redis Box:

```python
from redisbox import RedisBox

box = RedisBox()
box.start()

client = box.client() # redis client
assert client.ping()

# do stuff with Redis

box.stop()
client.ping()  # Raises error
```

Nose
----

Redis Box comes with a Nose plugin which is automatically installed.
If used as a plugin, port of the running instance will be exported
in environment variable `REDISBOX_PORT`. This name can be overridden
in settings.

The plugin exposes several configuration options. To see them, run:

    nosetests --help

The options you are interested in start with `--redisbox-`.

Unit tests
----------

For an easy unit tests integration there is a `RedisTestCase` class
inherited from `unittest.TestCase`. It assumes tests are run from `nosetests`
with `--with-redisbox` flag. `RedisTestCases` provides a `redis` client
connected to the sandboxed redis instance and a `purge_database` helper
to clean up the database after every test:

```python
from redisbox.unittest import RedisTestCase

class MyTest(RedisTestCase):
    def setUp(self):
        deploy_fixtures(self.redis_client)

    def tearDown(self):
        self.purge_database()
```

Installation
------------

Get it from PyPi:

    pip install redisbox

Get it from GitHub:

    pip install https://github.com/ziadsawalha/redisbox.git



Authors
=======

 Ziad Sawalha


Thanks
------

RedisBox is based on mongobox by Roman Kalyakin.

For a list of contributors see `AUTHORS.md`.
