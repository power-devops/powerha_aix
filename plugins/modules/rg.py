#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2023, eNFence GmbH (info@power-devops.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: rg

short_description: manage resource groups in PowerHA cluster
version_added: "1.0.0"

description: This module creates or deletes resource group in PowerHA cluster.

options:
    name:
        description: name of the resource group.
        required: true
        type: str
    nodes:
        description: list of the nodes where the resource group can be started. required if resource group is created.
        required: false
        type: list
        elements: str
    startup:
        description: startup policy for the resource group. One of OHN, OFAN, OAAN, or OUDP.
        required: false
        type: str
        choices: [ OHN, OFAN, OAAN, OUDP ]
        aliases: [ start ]
    fallover:
        description: fallover policy for the resource group. One of FNPN, FUDNP, or BO.
        required: false
        type: str
        choices: [ FNPN, FUDNP, BO ]
    fallback:
        description: fallback policy for the resource group. One of NFB, or FBHPN.
        required: false
        type: str
        choices: [ NFB, FBHPN ]
    service:
        description: list of service labels for the resource group.
        required: false
        type: list
        elements: str
        aliases: [ service_ip, service_label ]
    application:
        description: list of application controllers for the resource group.
        required: false
        type: list
        elements: str
        aliases: [ app, applications ]
    volgrp:
        description: list of volume groups for the resource group.
        required: false
        type: list
        elements: str
        aliases: [ vg, volume_group ]
    state:
        description: the desired state of the resource - present, absent, started, stopped. If the resource is already defined, it will not be changed.
        default: present
        required: false
        type: str
        choices: [ present, absent, started, stopped, online, offline ]

author:
    - Andrey Klyachkin (@aklyachkin)
'''

EXAMPLES = r'''
# create a new resource group
- name: create a new resource group
  enfence.powerha_aix.rg:
    name: rg_oracle
    nodes:
      - node1
      - node2
    startup: OHN
    fallover: FNPN
    fallback: NFB
    service: [ 'serviceip' ]
    application: [ 'ac_ora' ]
    volgrp:
      - vg01
      - vg02
      - vg03
    state: present
# bring resource group online
- name: starting resource group
  enfence.powerha_aix.rg:
    name: rg_oracle
    state: started
# bring resource group offline
- name: stopping resource group
  enfence.powerha_aix.rg:
    name: rg_oracle
    state: stopped
# delete an existing resource group
- name: delete an existing resource group
  enfence.powerha_aix.rg:
    name: rg_oracle
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
from ansible_collections.enfence.powerha_aix.plugins.module_utils.helpers import add_list, add_string, check_powerha, parse_clmgrq_output, CLMGR


def get_rg(module):
    rgopts = dict()
    cmd = "%s query resource_group %s" % (CLMGR, module.params['name'])
    module.debug('Starting command: %s' % cmd)
    rc, stdout, stderr = module.run_command(cmd)
    if rc != 0:
        return 'absent', rc, stdout, stderr, rgopts
    state = 'present'
    rgopts = parse_clmgrq_output(stdout)
    if 'STATE' in rgopts and rgopts['STATE'] != "":
        state = rgopts['STATE'].lower()
    return state, rc, stdout, stderr, rgopts


def add_rg(module):
    cmd = "%s add resource_group %s" % (CLMGR, module.params['name'])
    opts = ""
    opts += add_string(module, 'startup', 'startup')
    opts += add_string(module, 'fallover', 'fallover')
    opts += add_string(module, 'fallback', 'fallback')
    opts += add_list(module, 'nodes', 'nodes')
    opts += add_list(module, 'service', 'service_label')
    opts += add_list(module, 'application', 'applications')
    opts += add_list(module, 'volgrp', 'volume_group')
    cmd = "%s %s" % (cmd, opts)
    module.debug('Starting command: %s' % cmd)
    return module.run_command(cmd)


def delete_rg(module):
    cmd = "%s delete resource_group %s" % (CLMGR, module.params['name'])
    module.debug('Starting command: %s' % cmd)
    return module.run_command(cmd)


def start_rg(module):
    cmd = "%s online resource_group %s" % (CLMGR, module.params['name'])
    module.debug('Starting command: %s' % cmd)
    return module.run_command(cmd)


def stop_rg(module):
    cmd = "%s offline resource_group %s" % (CLMGR, module.params['name'])
    module.debug('Starting command: %s' % cmd)
    return module.run_command(cmd)


def run_module():
    module_args = dict(
        name=dict(type='str', required=True),
        state=dict(type='str', required=False, choices=['present', 'absent', 'started', 'stopped', 'online', 'offline'], default='present'),
        nodes=dict(type='list', required=False, elements='str'),
        startup=dict(type='str', required=False, choices=['OHN', 'OFAN', 'OAAN', 'OUDP'], aliases=['start']),
        fallover=dict(type='str', required=False, choices=['FNPN', 'FUDNP', 'BO']),
        fallback=dict(type='str', required=False, choices=['NFB', 'FBHPN']),
        service=dict(type='list', required=False, elements='str', aliases=['service_ip', 'service_label']),
        application=dict(type='list', required=False, elements='str', aliases=['app', 'applications']),
        volgrp=dict(type='list', required=False, elements='str', aliases=['vg', 'volume_group'])
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
        state, result['rc'], result['stdout'], result['stderr'] = get_rg(module)
        if state != 'absent':
            result['msg'] = 'resource group is already defined'
            module.exit_json(**result)
        result['changed'] = True
        if module.check_mode:
            result['msg'] = 'resource group will be defined'
            module.exit_json(**result)
        result['rc'], result['stdout'], result['stderr'] = add_rg(module)
        if result['rc'] != 0:
            result['msg'] = 'adding resource group to the cluster failed. see stderr for any error messages'
            module.fail_json(**result)
        result['msg'] = 'resource group added to the cluster'
    elif module.params['state'] == 'absent':
        state, result['rc'], result['stdout'], result['stderr'] = get_rg(module)
        if state == 'absent':
            result['msg'] = 'resource group is not defined'
            result['rc'] = 0
            module.exit_json(**result)
        result['changed'] = True
        if module.check_mode:
            result['msg'] = 'resource group will be deleted'
            module.exit_json(**result)
        result['rc'], result['stdout'], result['stderr'] = delete_rg(module)
        if result['rc'] != 0:
            result['msg'] = 'deleting resource group failed. see stderr for any error messages'
            module.fail_json(**result)
        result['message'] = 'resource group is deleted'
    elif module.params['state'] == 'started' or module.params['state'] == 'online':
        state, result['rc'], result['stdout'], result['stderr'] = get_rg(module)
        if state == 'absent':
            result['msg'] = 'resource group is not defined'
            module.fail_json(**result)
        if state == 'online':
            result['msg'] = 'resource group is already online'
            result['rc'] = 0
            module.exit_json(**result)
        result['changed'] = True
        if module.check_mode:
            result['msg'] = 'resource group will be started'
            module.exit_json(**result)
        result['rc'], result['stdout'], result['stderr'] = start_rg(module)
        if result['rc'] != 0:
            result['msg'] = 'starting resource group failed. see stderr for any error messages'
            module.fail_json(**result)
        result['msg'] = 'resource group is started'
    elif module.params['state'] == 'stopped' or module.params['state'] == 'offline':
        state, result['rc'], result['stdout'], result['stderr'] = get_rg(module)
        if state == 'absent':
            result['msg'] = 'resource group is not defined'
            module.fail_json(**result)
        if state == 'offline':
            result['msg'] = 'resource group is already offline'
            result['rc'] = 0
            module.exit_json(**result)
        result['changed'] = True
        if module.check_mode:
            result['msg'] = 'resource group will be stopped'
            module.exit_json(**result)
        result['rc'], result['stdout'], result['stderr'] = stop_rg(module)
        if result['rc'] != 0:
            result['msg'] = 'stopping resource group failed. see stderr for any error messages'
            module.fail_json(**result)
        result['msg'] = 'resource group is stopped'
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
