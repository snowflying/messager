# Copyright (c) 2013 OpenStack Foundation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import eventlet
from messager import topics
from messager.common import log as logging
from messager.common.rpc import proxy

LOG = logging.getLogger(__name__)


class ClientProducerAPI(proxy.RpcProxy):
    BASE_RPC_API_VERSION = '1.0'

    def __init__(self, topic=topics.DAOLI_AGENT):
        super(ClientProducerAPI, self).__init__(
            topic=topic, default_version=self.BASE_RPC_API_VERSION)

    def _notification_host(self, context, mode, method, payload, host):
        if host == None:
            _topic = '%s' % topics.DAOLI_AGENT
        else:
            _topic = '%s.%s' % (topics.DAOLI_AGENT, host)

        if mode == 'cast':
            self.cast(context, self.make_msg(method,
                                             payload=payload),
                      topic=_topic)
        elif mode == 'call':
            result = self.call(context, self.make_msg(method,
                                                      payload=payload),
                               topic=_topic)
            print result
        else:
            pass

    def notifier(self, name, method, mode, context=None, host=None):
        self._notification_host(context, mode,
                                method,
                                {'name': name},
                                host)

eventlet.monkey_patch()
ClientNotifyAPI = ClientProducerAPI()


### TEST RPC client interface ####
ClientNotifyAPI.notifier('xuecheng', 'callfunc', 'call', host='192.168.10.9')
# ClientNotifyAPI.notifier('xuecheng', 'callfunc', 'call')
# ClientNotifyAPI.notifier('xuecheng', 'castfunc', 'cast', host='192.168.10.9')
# ClientNotifyAPI.notifier('xuecheng', 'castfunc', 'cast')
