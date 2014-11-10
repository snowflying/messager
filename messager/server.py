#!/usr/bin/env python
#encoding: utf-8

import eventlet
import logging
import sys
import time
import signal

from oslo.config import cfg
from messager import topics
from messager.common import rpc
from messager.common.rpc import dispatcher as rpc_dispatcher

CONF = cfg.CONF
LOG = logging.getLogger(__name__)

server_opts = [
        cfg.StrOpt('host_ip',
                   default='0.0.0.0'),
]

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
        return 'messager-callfunc'


class AMQPConsumerServer(object):

    def __init__(self, agent_name, agent_host):
        self.serializer = None
        self.consumers = [[agent_name, False],
                          ['%s.%s' % (agent_name, agent_host), False]]

        self.manager = Manager()
        self.setup_rpc()
        self.run_daemon_loop = True
        self.handle_signal()

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
        LOG.info("Starting the messager Service ...")
        if self.run_daemon_loop:
            self._done = eventlet.event.Event()
            self._done.wait()
        else:
            pass

    def clean_exchanges_queues(self):
        pass

    def handle_signal(self):
        self._set_signals_handler(self._handle_signal)

    def _handle_signal(self, signo, frame):
        LOG.info('Catch the signal %s to stop AMQPConsumerServer ...' % str(signo))
        self.run_daemon_loop = False
        self.connection.close()
        self.clean_exchanges_queues()

        # Allow the process to be killed again and die from natural causes
        self._set_signals_handler(signal.SIG_DFL)

    def _set_signals_handler(self, handler):
        signal.signal(signal.SIGTERM, handler)
        signal.signal(signal.SIGINT, handler)



def main():
    eventlet.monkey_patch()
    CONF.register_opts(server_opts)
    CONF(project='messager', version='1.0')
    if CONF.log_file:
        logging.config.fileConfig(CONF.log_file, disable_existing_loggers=False)
    else:
        logging.basicConfig(stream=sys.stderr, level=logging.INFO)

    server = AMQPConsumerServer(topics.DAOLI_AGENT, CONF.host_ip)
    server.daemon_loop()

if __name__ == '__main__':
    sys.exit(main())
