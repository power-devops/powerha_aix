# Copyright (c) 2023, eNFence GmbH (info@power-devops.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
from ansible.module_utils.basic import is_executable

__metaclass__ = type

import os

CLMGR = '/usr/es/sbin/cluster/utilities/clmgr'


def check_powerha(result):
    result['rc'] = 0
    result['msg'] = ''

    if not os.path.exists(CLMGR):
        result['msg'] = 'IBM PowerHA is not installed or clmgr is not found'
        result['rc'] = 1
        return result

    if not is_executable(CLMGR):
        result['msg'] = 'clmgr can not be executed by the current user'
        result['rc'] = 1
        return result

    return result


def parse_clmgrq_output(stdout):
    opts = dict()
    for line in stdout.splitlines():
        if '=' in line:
            opt, value = line.split('=')
            value = value.strip('"')
            if value != "":
                opts[opt] = value
    return opts
