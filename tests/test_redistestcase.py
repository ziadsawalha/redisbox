# -*- coding: utf-8 -*-
from redisbox.unittest import RedisTestCase


class RedisTestCaseTestCase(RedisTestCase):

    @classmethod
    def setUpClass(cls):
        # intentionally created class based method.
        pass

    def setUp(self):
        self.client = self.redis_client
        self.client.set('test', {'foo': 'bar'})

    def tearDown(self):
        self.flushall()

    def test_one_record(self):
        self.assertEquals(
            1, len(self.client.keys()),
            'Data expected to be purged in tearDown'
        )

    def test_one_record_once_again(self):
        self.assertEquals(
            1, len(self.client.keys()),
            'Data expected to be purged in tearDown'
        )
