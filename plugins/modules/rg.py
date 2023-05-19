#!/usr/bin/python

# Copyright (c) 2023, eNFence GmbH (info@power-devops.com)
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
    startup:
        description: startup policy for the resource group. One of OHN, OFAN, OAAN, or OUDP.
        required: false
        type: str
    fallover:
        description: fallover policy for the resource group. One of FNPN, FUDNP, or BO.
        requried: false
        type: str
    fallback:
        description: fallback policy for the resource group. One of NFB, or FBHPN.
        required: false
        type: str
    service:
        description: list of service labels for the resource group.
        required: false
        type: list
    application:
        description: list of application controllers for the resource group.
        required: false
        type: list
    volgrp:
        description: list of volume groups for the resource group.
        required: false
        type: list
    state:
        description: the desired state of the resource - present, absent, started, stopped. If the resource is already defined, it will not be changed.
        default: present
        required: false
        type: str

author:
    - Andrey Klyachkin <info@power-devops.com>
'''

EXAMPLES = r'''
# create a new resource group
- name: create a new resource group
  powerdevops.powerha_aix.rg:
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
  powerdevops.powerha_aix.rg:
    name: rg_oracle
    state: started
# bring resource group offline
- name: stopping resource group
  powerdevops.powerha_aix.rg:
    name: rg_oracle
    state: stopped
# delete an existing resource group
- name: delete an existing resource group
  powerdevops.powerha_aix.rg:
    name: rg_oracle
    state: absent
'''

RETURN = r'''
# possible return values
'''

import os
from ansible.module_utils.basic import AnsibleModule, is_executable

CLMGR = '/usr/es/sbin/cluster/utilities/clmgr'


def get_rg(module):
    cmd = "%s query resource_group %s" % (CLMGR, module.params['name'])
    module.debug('Starting command: %s' % cmd)
    rc, stdout, stderr = module.run_command(cmd)
    if rc != 0:
        return 'absent', rc, stdout, stderr
    state = 'present'
    for line in stdout.splitlines():
        if line.startswith('STATE='):
            state = line.split('=')[1].strip('"').lower()
    return state, rc, stdout, stderr


def add_rg(module):
    cmd = "%s add resource_group %s" % (CLMGR, module.params['name'])
    opts = ""
    if 'startup' in module.params and module.params['startup'] != '':
        opts += " startup=%s" % module.params['startup']
    if 'fallover' in module.params and module.params['fallover'] != '':
        opts += " fallover=%s" % module.params['fallover']
    if 'fallback' in module.params and module.params['fallback'] != '':
        opts += " fallback=%s" % module.params['fallback']
    if 'nodes' in module.params and module.params['nodes'] is not None:
        oldopts = opts
        try:
            opts += ' nodes='
            for node in module.params['nodes']:
                opts += '%s,' % node
            opts = opts[:-1]
        except TypeError:
            opts = oldopts
    if 'service' in module.params and module.params['service'] is not None:
        oldopts = opts
        try:
            opts += ' service_label='
            for svc in module.params['service']:
                opts += '%s,' % svc
            opts = opts[:-1]
        except TypeError:
            opts = oldopts
    if 'application' in module.params and module.params['application'] is not None:
        oldopts = opts
        try:
            opts += ' applications='
            for app in module.params['application']:
                opts += '%s,' % app
            opts = opts[:-1]
        except TypeError:
            opts = oldopts
    if 'volgrp' in module.params and module.params['volgrp'] is not None:
        oldopts = opts
        try:
            opts += ' volume_group='
            for vg in module.params['volgrp']:
                opts += '%s,' % vg
            opts = opts[:-1]
        except TypeError:
            opts = oldopts
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
        message='No changes'
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # check if we can run clmgr
    if not os.path.exists(CLMGR):
        result['message'] = 'IBM PowerHA is not installed or clmgr is not found'
        module.fail_json(msg=result['message'], rc=1)

    if not is_executable(CLMGR):
        result['message'] = 'clmgr can not be executed by the current user'
        module.fail_json(msg=result['message'], rc=1)

    if module.params['state'] is None or module.params['state'] == 'present':
        state, result['rc'], result['stdout'], result['stderr'] = get_rg(module)
        if state != 'absent':
            result['message'] = 'resource group is already defined'
            module.exit_json(**result)
        result['changed'] = True
        if module.check_mode:
            result['message'] = 'resource group will be defined'
            module.exit_json(**result)
        result['rc'], result['stdout'], result['stderr'] = add_rg(module)
        if result['rc'] != 0:
            result['message'] = 'adding resource group to the cluster failed. see stderr for any error messages'
            module.fail_json(msg=result['message'], rc=result['rc'], result=result)
        result['message'] = 'resource group added to the cluster'
    elif module.params['state'] == 'absent':
        state, result['rc'], result['stdout'], result['stderr'] = get_rg(module)
        if state == 'absent':
            result['message'] = 'resource group is not defined'
            result['rc'] = 0
            module.exit_json(**result)
        result['changed'] = True
        if module.check_mode:
            result['message'] = 'resource group will be deleted'
            module.exit_json(**result)
        result['rc'], result['stdout'], result['stderr'] = delete_rg(module)
        if result['rc'] != 0:
            result['message'] = 'deleting resource group failed. see stderr for any error messages'
            module.fail_json(msg=result['message'], rc=result['rc'], result=result)
        result['message'] = 'resource group is deleted'
    elif module.params['state'] == 'started' or module.params['state'] == 'online':
        state, result['rc'], result['stdout'], result['stderr'] = get_rg(module)
        if state == 'absent':
            result['message'] = 'resource group is not defined'
            module.fail_json(msg=result['message'], rc=result['rc'], result=result)
        if state == 'online':
            result['message'] = 'resource group is already online'
            result['rc'] = 0
            module.exit_json(**result)
        result['changed'] = True
        if module.check_mode:
            result['message'] = 'resource group will be started'
            module.exit_json(**result)
        result['rc'], result['stdout'], result['stderr'] = start_rg(module)
        if result['rc'] != 0:
            result['message'] = 'starting resource group failed. see stderr for any error messages'
            module.fail_json(msg=result['message'], rc=result['rc'], result=result)
        result['message'] = 'resource group is started'
    elif module.params['state'] == 'stopped' or module.params['state'] == 'offline':
        state, result['rc'], result['stdout'], result['stderr'] = get_rg(module)
        if state == 'absent':
            result['message'] = 'resource group is not defined'
            module.fail_json(msg=result['message'], rc=result['rc'], result=result)
        if state == 'offline':
            result['message'] = 'resource group is already offline'
            result['rc'] = 0
            module.exit_json(**result)
        result['changed'] = True
        if module.check_mode:
            result['message'] = 'resource group will be stopped'
            module.exit_json(**result)
        result['rc'], result['stdout'], result['stderr'] = stop_rg(module)
        if result['rc'] != 0:
            result['message'] = 'stopping resource group failed. see stderr for any error messages'
            module.fail_json(msg=result['message'], rc=result['rc'], result=result)
        result['message'] = 'resource group is stopped'
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
