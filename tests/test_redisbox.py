# -*- coding: utf-8 -*-
import os
import shutil
import tempfile
import unittest

import redis

from redisbox import RedisBox
from redisbox.nose_plugin import DEFAULT_PORT_ENVVAR


class TestRedisBox(unittest.TestCase):

    def test_nose_plugin_exports_envvar(self):
        self.assertTrue(DEFAULT_PORT_ENVVAR in os.environ)

    def test_can_run_redis(self):
        box = RedisBox()
        box.start()

        db_path = box.db_path

        self.assertTrue(box.running())
        self.assertIsNotNone(box.port)

        client = box.client()
        self.assertTrue(client.ping())

        box.stop()

        self.assertFalse(box.running())
        self.assertRaises(redis.ConnectionError, client.ping)
        self.assertFalse(os.path.exists(db_path))

    def test_keep_db_path(self):
        db_path = tempfile.mkdtemp()
        box = RedisBox(db_path=db_path)
        box.start()
        box.stop()

        self.assertTrue(os.path.exists(db_path))
        shutil.rmtree(db_path)


if __name__ == "__main__":
    unittest.main()
