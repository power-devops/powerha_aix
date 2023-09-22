#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2023, eNFence GmbH (info@power-devops.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: mp

short_description: manage mirror_pool resource in PowerHA cluster
version_added: "1.3.0"

description:
    - This module creates/deletes/changes mirror_pool resource in PowerHA cluster.

options:
    name:
        description: name of the mirror pool.
        required: true
        type: str
    state:
        description:
            - the desired state of the mirror pool - C(present), C(absent).
        required: false
        type: str
        choices: [ present, absent ]
        default: present
    volume_group:
        description:
          - name of the volume group.
          - required if the state is C(present) and no C(volumes) are specified.
        required: false
        type: str
        aliases: [ vg ]
    volumes:
        description:
          - list of disks to be in the mirror pool.
          - required if the state is C(present) and no C(volume_group) is specified.
        required: false
        type: list
        elements: str
        aliases: [ physical_volumes, pv, pvs, volume, disks ]
    mode:
        description: mode of mirroring - synchronous or asynchronous.
        required: false
        type: str
        choices: [ sync, async ]
        default: sync
    async_cache_lv:
        description:
            - logical volume to cache data if C(mode) is I(async).
            - required if C(mode) is I(async).
        required: false
        type: str
        aliases: [ cache_lv, cachelv, cache ]
    async_cache_hw_mark:
        description:
            - specifies the I/O-cache high watermark.
            - the value is the percent of I/O cache size.
            - the default value is 100%.
        required: false
        type: int
        aliases: [ cache_hw_mark, hwmark, hw_mark ]

author:
    - Andrey Klyachkin (@aklyachkin)
'''

EXAMPLES = r'''
# create mirror pools for vg01
- name: mirror pool mp1
  enfence.powerha_aix.mp:
    name: mp1
    vg: vg01
    volumes:
      - hdisk1
      - hdisk2
- name: mirror pool mp2
  enfence.powerha_aix.mp:
    name: mp2
    vg: vg02
    volumes:
      - hdisk3
      - hdisk4
# delete mirror pool mp1 from volume group vg01
- name: delete mirror pool mp1
  enfence.powerha_aix.mp:
    name: mp1
    vg: vg01
    state: absent
'''

RETURN = r'''
# possible return values
changed:
    description: set to true if the resource was changed
    type: bool
    returned: always
msg:
    description: error and informational messages
    type: str
    returned: always
rc:
    description: return code of the last executed command
    type: int
    returned: always
stdout:
    description: standard output of the last executed command
    type: str
    returned: always
stderr:
    description: standard error of the last executed command
    type: str
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.enfence.powerha_aix.plugins.module_utils.helpers import (
    add_string, add_list, add_int, check_powerha, parse_clmgrq_output, CLMGR)


def get_mp(module):
    mpopts = dict()
    cmd = "%s query mirror_pool %s" % (CLMGR, module.params['name'])
    module.debug('Starting command: %s' % cmd)
    rc, stdout, stderr = module.run_command(cmd)
    if rc != 0:
        return 'absent', rc, stdout, stderr, mpopts
    mpopts = parse_clmgrq_output(stdout)
    return 'present', rc, stdout, stderr, mpopts


def add_mp(module):
    cmd = "%s add mirror_pool %s" % (CLMGR, module.params['name'])
    opts = ""
    opts += add_list(module, 'volumes', 'physical_volumes')
    opts += add_string(module, 'volume_group', 'volume_group')
    opts += add_string(module, 'mode', 'mode')
    opts += add_string(module, 'async_cache_lv', 'async_cache_lv')
    opts += add_int(module, 'async_cache_hw_mark', 'async_cache_hw_mark')
    cmd = "%s %s" % (cmd, opts)
    module.debug('Starting command: %s' % cmd)
    return module.run_command(cmd)


def delete_mp(module):
    opts = ""
    opts += add_list(module, 'volumes', 'physical_volumes')
    opts += add_string(module, 'volume_group', 'volume_group')
    cmd = "%s delete mirror_pool %s %s" % (CLMGR, module.params['name'], opts)
    module.debug('Starting command: %s' % cmd)
    return module.run_command(cmd)


def run_module():
    module_args = dict(
        name=dict(type='str', required=True),
        state=dict(type='str', required=False, choices=['present', 'absent'], default='present'),
        volume_group=dict(type='str', required=False, aliases=['vg']),
        volumes=dict(type='list', required=False, elements='str', aliases=['physical_volumes', 'pv', 'pvs', 'volume', 'disks']),
        mode=dict(type='str', required=False, choices=['sync', 'async'], default='sync'),
        async_cache_lv=dict(type='str', required=False, aliases=['cache_lv', 'cachelv', 'cache']),
        async_cache_hw_mark=dict(type='int', required=False, aliases=['cache_hw_mark', 'hw_mark', 'hwmark'])
    )

    result = dict(
        changed=False,
        msg='No changes',
        rc=0
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_one_of=[
            ('volume_group', 'volumes'),
        ],
        required_if=[
            ('mode', 'async', ('async_cache_lv', 'async_cache_hw_mark')),
        ],
    )

    module.debug('Starting enfence.powerha_aix.mp module')
    # check if we can run clmgr
    result = check_powerha(result)
    if result['rc'] == 1:
        module.fail_json(**result)

    if module.params['state'] is None or module.params['state'] == 'present':
        state, result['rc'], result['stdout'], result['stderr'], opts = get_mp(module)
        if state == 'present':
            result['msg'] = 'mirror pool already exists'
            module.exit_json(**result)
        result['changed'] = True
        if module.check_mode:
            result['msg'] = 'mirror pool will be created'
            module.exit_json(**result)
        result['rc'], result['stdout'], result['stderr'] = add_mp(module)
        if result['rc'] != 0:
            result['msg'] = 'creating mirror pool failed. see stderr for any error messages'
            module.fail_json(**result)
        result['msg'] = 'mirror pool created'
    elif module.params['state'] == 'absent':
        state, result['rc'], result['stdout'], result['stderr'], opts = get_mp(module)
        if state == 'absent':
            result['msg'] = 'mirror pool does not exist'
            result['rc'] = 0
            module.exit_json(**result)
        result['changed'] = True
        if module.check_mode:
            result['msg'] = 'mirror pool will be deleted'
            module.exit_json(**result)
        result['rc'], result['stdout'], result['stderr'] = delete_mp(module)
        if result['rc'] != 0:
            result['msg'] = 'deleting mirror pool failed. see stderr for any error messages'
            module.fail_json(**result)
        result['msg'] = 'mirror pool is deleted'
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
