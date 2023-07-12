#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2023, eNFence GmbH (info@power-devops.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: vg

short_description: manage volume_group resource in PowerHA cluster
version_added: "1.2.0"

description:
    - This module creates/deletes/changes volume_group resource in PowerHA cluster.
    - This module was added in 1.1.3.

options:
    name:
        description: name of the volume group.
        required: true
        type: str
    state:
        description: the desired state of the volume group - present, absent
        required: false
        type: str
        choices: [ present, absent ]
        default: present
    nodes:
        description: list of nodes where volume group can be activated
        required: true
        type: list
        elements: str
    volumes:
        description: list of physical volumes to add into the volume group
        required: true
        type: list
        elements: str
        aliases: [ physical_volumes, pv, pvs, volume ]

author:
    - Andrey Klyachkin (@aklyachkin)
'''

EXAMPLES = r'''
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
from ansible_collections.enfence.powerha_aix.plugins.module_utils.helpers import add_string, add_list, check_powerha, parse_clmgrq_output, CLMGR


def get_vg(module):
    vgopts = dict()
    cmd = "%s query volume_group %s" % (CLMGR, module.params['name'])
    module.debug('Starting command: %s' % cmd)
    rc, stdout, stderr = module.run_command(cmd)
    if rc != 0:
        return 'absent', rc, stdout, stderr, vgopts
    vgopts = parse_clmgrq_output(stdout)
    return 'present', rc, stdout, stderr, vgopts


def add_vg(module):
    cmd = "%s add volume_group %s" % (CLMGR, module.params['name'])
    opts = ""
    opts += add_list(module, 'nodes', 'nodes')
    opts += add_list(module, 'volumes', 'physical_volumes')
    cmd = "%s %s" % (cmd, opts)
    module.debug('Starting command: %s' % cmd)
    return module.run_command(cmd)


def delete_vg(module):
    cmd = "%s delete volume_group %s" % (CLMGR, module.params['name'])
    module.debug('Starting command: %s' % cmd)
    return module.run_command(cmd)


def run_module():
    module_args = dict(
        name=dict(type='str', required=True),
        state=dict(type='str', required=False, choices=['present', 'absent'], default='present'),
        nodes=dict(type='list', required=True, elements='str'),
        volumes=dict(type='list', required=True, elements='str', aliases=['physical_volumes', 'pv', 'pvs', 'volume']),
    )

    result = dict(
        changed=False,
        msg='No changes',
        rc=0
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # check if we can run clmgr
    result = check_powerha(result)
    if result['rc'] == 1:
        module.fail_json(**result)

    if module.params['state'] is None or module.params['state'] == 'present':
        state, result['rc'], result['stdout'], result['stderr'] = get_vg(module)
        if state == 'present':
            result['msg'] = 'volume group already exists'
            module.exit_json(**result)
        result['changed'] = True
        if module.check_mode:
            result['msg'] = 'volume group will be created'
            module.exit_json(**result)
        result['rc'], result['stdout'], result['stderr'] = add_vg(module)
        if result['rc'] != 0:
            result['msg'] = 'creating volume group failed. see stderr for any error messages'
            module.fail_json(**result)
        result['msg'] = 'volume group created'
    elif module.params['state'] == 'absent':
        state, result['rc'], result['stdout'], result['stderr'] = get_vg(module)
        if state == 'absent':
            result['msg'] = 'volume group does not exist'
            result['rc'] = 0
            module.exit_json(**result)
        result['changed'] = True
        if module.check_mode:
            result['msg'] = 'volume group will be deleted'
            module.exit_json(**result)
        result['rc'], result['stdout'], result['stderr'] = delete_vg(module)
        if result['rc'] != 0:
            result['msg'] = 'deleting volume group failed. see stderr for any error messages'
            module.fail_json(**result)
        result['msg'] = 'volume group is deleted'
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
