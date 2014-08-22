# -*- coding: utf-8 -*-
from nose.plugins import Plugin
from .redisbox import RedisBox
import os

DEFAULT_PORT_ENVVAR = 'REDISBOX_PORT'


class RedisBoxPlugin(Plugin):

    """A nose plugin that sets up a sandboxed redis instance."""

    name = 'redisbox'

    def options(self, parser, env):
        super(RedisBoxPlugin, self).options(parser, env)
        parser.add_option(
            "--redisbox-bin",
            dest="bin",
            action="store",
            default=None,
            help="Optionally specify the path to the redisd executable.")
        parser.add_option(
            "--redisbox-port",
            action="store",
            dest="port",
            type="int",
            default=0,
            help="Optionally specify the port to run redis on.")
        parser.add_option(
            "--redisbox-dbpath",
            action="store",
            dest="dbpath",
            default=None,
            help=("Path to database files directory. Creates temporary "
                  "directory by default."))
        parser.add_option(
            "--redisbox-logfile",
            action="store",
            dest="logfile",
            default=None,
            help=("Optionally store the redis log here "
                  "(default is /dev/null)"))
        parser.add_option(
            "--redisbox-port-envvar",
            action="store",
            dest="port_envvar",
            default=DEFAULT_PORT_ENVVAR,
            help=("Which environment variable dynamic port number will be "
                  "exported to."))

    def configure(self, options, conf):
        super(RedisBoxPlugin, self).configure(options, conf)

        if not self.enabled:
            return

        self.redisbox = RedisBox(
            redisd_bin=options.bin, port=options.port or None,
            log_file=options.logfile, db_path=options.dbpath
        )

        self.port_envvar = options.port_envvar

    def begin(self):
        assert self.port_envvar not in os.environ, (
            '{} environment variable is already taken. Do you have other '
            'tests with redisbox running?'.format(self.port_envvar))

        self.redisbox.start()
        os.environ[self.port_envvar] = str(self.redisbox.port)

    def finalize(self, result):
        self.redisbox.stop()
        del os.environ[self.port_envvar]
