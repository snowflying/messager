#!/usr/bin/env python
#encoding: utf-8

import eventlet
import logging
import traceback
import sys
import time
import signal

from oslo.config import cfg

from daolicloud.common import rpc
from daolicloud.common.rpc import dispatcher as rpc_dispatcher

CONF = cfg.CONF
NAME = 'daolicloud'
LOG = logging.getLogger(__name__)


class Manager(object):
    RPC_API_VERSION = '1.0'

    def __init__(self, *args, **kwargs):
        super(Manager, self).__init__(*args, **kwargs)
        pass

    def castfunc(self, *args, **kwargs):
        print kwargs, args
        print 'hello world'

    def callfunc(self, *args, **kwargs):
        print 'callfunc ...'
        return 'daolicloud-callfunc'



class AMQPServer(object):

    def __init__(self, *args, **kwargs):
        self.serializer = None
        self.consumers = [[NAME, False], ['%s.%s' % (NAME, '192.168.10.9'), False]]
        self.manager = Manager()
        self.setup_rpc()
        self.run_daemon_loop = True

    def setup_rpc(self):
        self.dispatcher = rpc_dispatcher.RpcDispatcher([self.manager],
                                                       self.serializer)

        self.connection = self.create_consumers(self.dispatcher,
                                                self.consumers)

    def create_consumers(self, dispatcher, consumers):
        """Create service RPC consumers.

        :param dispatcher: The dispatcher to process the incoming messages.
        :param topic_details: A list of topics. Each topic has a name, an
                              boolean entry for fanout using.

        :returns: A common Connection.
        """

        connection = rpc.create_connection(new=True)
        for item in consumers:
            connection.create_consumer(item[0], dispatcher, fanout=item[1])

        connection.consume_in_thread()
        return connection

    def daemon_loop(self):
        LOG.info("Starting the daolicloud Service ...")
        if self.run_daemon_loop:
            self.done = eventlet.event.Event()
            self.done.wait()
        else:
            self.connection.close()

    def _handle_sigterm(self, signum, frame):
        LOG.info("Service caught SIGTERM, quitting daemon loop.")
        self.run_daemon_loop = False


def main():
    eventlet.monkey_patch()
    CONF(project='daolicloud')
    if CONF.log_file:
       logging.config.fileConfig(CONF.log_file, disable_existing_loggers=False)
    else:
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)

    Server = AMQPServer()
    signal.signal(signal.SIGTERM, Server._handle_sigterm)
    Server.daemon_loop()

if __name__ == '__main__':
    sys.exit(main())
