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

# from daolicloud.common import constants
import eventlet
from daolicloud import topics
# from daolicloud.common import utils
# from daolicloud import manager
from daolicloud.common import log as logging
from daolicloud.common.rpc import proxy
# from daolicloud.plugins.common import constants as service_constants


LOG = logging.getLogger(__name__)


class ClientNotifyAPI(proxy.RpcProxy):
    BASE_RPC_API_VERSION = '1.0'

    def __init__(self, topic=topics.DAOLI_AGENT):
        super(ClientNotifyAPI, self).__init__(
            topic=topic, default_version=self.BASE_RPC_API_VERSION)

    def _notification_host(self, context, mode, method, payload, host):
        if mode == 'cast':
            self.cast(
                context, self.make_msg(method,
                                       payload=payload),
                topic='%s.%s' % (topics.DAOLI_AGENT, host))
        elif mode == 'call':
            result = self.call(
                        context, self.make_msg(method,
                                               payload=payload),
                        topic='%s.%s' % (topics.DAOLI_AGENT, host))
            print '2' * 20
            print result


    def notifier(self, name, host, method, mode, context=None):
        self._notification_host(context, mode,
                                method,
                                {'name': name},
                                host)

eventlet.monkey_patch()
ClientNotifyAPI = ClientNotifyAPI()
# ClientNotifyAPI.notifier('xuecheng', '192.168.10.9', 'callfunc', 'call')
ClientNotifyAPI.notifier('xuecheng', '192.168.10.9', 'castfunc', 'cast')
