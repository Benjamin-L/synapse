# -*- coding: utf-8 -*-
# Copyright 2019 New Vector Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import logging

from twisted.internet import defer

from synapse.api.errors import SynapseError
from synapse.handlers.identity import IdentityHandler
from synapse.http.servlet import RestServlet
from synapse.utils.dictutils import assert_params_in_dict

from ._base import identity_path_patterns

logger = logging.getLogger(__name__)


class IdentityLookupServlet(RestServlet):
    PATTERNS = identity_path_patterns("/lookup")

    def __init__(self, hs):
        super(IdentityLookupServlet, self).__init__()

        self.config = hs.config
        self.auth = hs.get_auth()
        self.identity_handler = IdentityHandler(hs)

    @defer.inlineCallbacks
    def on_GET(self, request):
        """Proxy a /_matrix/identity/api/v1/lookup request to an identity
        server
        """
        yield self.auth.get_user_by_req(request, allow_guest=True)

        if not self.config.enable_3pid_lookup:
            raise SynapseError(
                403,
                "Looking up third-party identifiers is denied from this server"
            )

        # Extract query parameters
        query_params = request.args
        assert_params_in_dict(query_params, ["medium", "address"])

        # Retrieve address and medium from the request parameters
        medium = query_params["medium"]
        address = query_params["address"]

        # TODO: Either get this from the request or from the config file
        is_server = "vector.im"

        # Proxy the request to the identity server
        ret = yield self.identity_handler.lookup_3pid(is_server, medium, address)
        defer.returnValue((200, ret))


def register_servlets(hs, http_server):
    IdentityLookupServlet(hs).register(http_server)
