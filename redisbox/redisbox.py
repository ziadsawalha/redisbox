# -*- coding: utf-8 -*-

import copy
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time

from .utils import find_executable, get_free_port

REDIS_SERVER_BIN = 'redis-server'
DEFAULT_ARGS = [
    # No need to talk outside of this box
    '--bind', 'localhost',
    # Drop dead clients
    '--tcp-keepalive', '10',
    # Default to a single database
    '--databases', '1',
    # Don't save to file
    '--save', '""',
    '--appendfsync', 'no',
    # No need for many clients
    '--maxclients', '8',
    # Just a few MB
    '--maxmemory', '10485760',
    # No logging needed
    '--loglevel', 'warning'
]
STARTUP_TIME = 0.4
START_CHECK_ATTEMPTS = 200


class RedisBox(object):
    def __init__(self, redisd_bin=None, port=None, log_file=None, db_path=None):

        self.redisd_bin = redisd_bin or find_executable(REDIS_SERVER_BIN)
        assert self.redisd_bin, (
            'Could not find "{}" in system PATH. Make sure you have Redis '
            'installed.'.format(REDIS_SERVER_BIN))

        self.port = port or get_free_port()
        self.log_file = log_file or os.devnull
        self.db_path = db_path

        if self.db_path:
            if os.path.exists(self.db_path) and os.path.isfile(self.db_path):
                raise AssertionError('DB path should be a directory, but it '
                                     'is a file.')

        self.process = None
        self._db_path_is_temporary = False

    def start(self):
        """Start Redis.

        Returns `True` if instance has been started or
        `False` if it could not start.
        """
        if self.db_path:
            if not os.path.exists(self.db_path):
                os.mkdir(self.db_path)
            self._db_path_is_temporary = False
        else:
            self.db_path = tempfile.mkdtemp()
            self._db_path_is_temporary = True

        args = copy.copy(DEFAULT_ARGS)
        args.insert(0, self.redisd_bin)

        args.extend(['--dir', self.db_path])
        args.extend(['--port', str(self.port)])
        args.extend(['--logfile', self.log_file])

        self.process = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        return self._wait_till_started()

    def stop(self):
        if not self.process:
            return

        # Not sure if there should be more checks for
        # other platforms.
        if sys.platform == 'darwin':
            self.process.kill()
        else:
            os.kill(self.process.pid, 9)
        self.process.wait()

        if self._db_path_is_temporary:
            shutil.rmtree(self.db_path)
            self.db_path = None

        self.process = None

    def running(self):
        return self.process is not None

    def client(self):
        import redis
        return redis.StrictRedis(port=self.port)

    def _wait_till_started(self):
        attempts = 0
        while self.process.poll() is None and attempts < START_CHECK_ATTEMPTS:
            attempts += 1
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                try:
                    sock.connect(('localhost', int(self.port)))
                    return True
                except (IOError, socket.error):
                    time.sleep(0.25)
            finally:
                sock.close()

        self.stop()
        return False
