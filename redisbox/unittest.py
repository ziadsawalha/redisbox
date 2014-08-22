# -*- coding: utf-8 -*-
from __future__ import absolute_import
from unittest import TestCase
import os

try:
    import redis
except ImportError:
    raise ImportError('`redis` is required for RedisTestCase')


class RedisTestCase(TestCase):
    """A base for Redis DB driven test cases. Provides
    :class:`redis.StrictRedis` instance in :attribute:`redis_client`
    and has a :method:`flushall` helper method for database cleanup.

    It is expected that tests are run from `nose` with `--with-redisbox` flag
    that brings up a sandboxed instance of Redis.
    """
    __redis_client = None

    @property
    def redis_client(self):
        """Returns an instance of :class:`redis.StrictRedis` connected
        to RedisBox database instance.
        """
        if not self.__redis_client:
            try:
                port = int(os.getenv('REDISBOX_PORT'))
                self.__redis_client = redis.StrictRedis(port=port)
            except (TypeError, redis.errors.ConnectionFailure):
                raise RuntimeError(
                    'Seems that RedisBox is not running. ' +
                    'Do you run nosetests with --with-redisbox flag?')

        return self.__redis_client

    def flushall(self, drop=True):
        """Delete all data.

        A typical use is call this method in :func:`unittest.TestCase.tearDown`
        to have a clean database for every test case method.

        .. code-block:: python

        def tearDown(self):
            super(self, MyTestCase).tearDown()
            self.flushall()
        """

        self.redis_client.flushall()
