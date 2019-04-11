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

"""This module contains base REST classes for constructing identity v1
servlets, which are just proxied to the same URL on identity servers.
"""

import logging
import re

from synapse.api.urls import IDENTITY_PREFIX

logger = logging.getLogger(__name__)


def identity_path_patterns(path_regex, releases=(0,), include_in_unstable=True):
    """Creates a regex compiled path with the correct identity path prefix.

    Args:
        path_regex (str): The regex string to match. This should NOT have a ^
        as this will be prefixed.
    Returns:
        SRE_Pattern
    """
    return [re.compile("^" + IDENTITY_PREFIX + path_regex)]
