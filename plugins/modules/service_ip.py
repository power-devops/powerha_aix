#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2023, eNFence GmbH (info@power-devops.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: service_ip

short_description: manage service_ip resource in PowerHA cluster
version_added: "1.0.0"

description: This module creates/deletes/changes service_ip resource in PowerHA cluster.

options:
    name:
        description: name of the service ip label. the name must be resolvable by using C(/etc/hosts).
        required: true
        type: str
    network:
        description: name of the cluster network, where the service ip should be placed.
        default: net_ether_01
        required: false
        type: str
    netmask:
        description: netmask for the service ip.
        required: false
        type: str
    site:
        description:
            - site of the service ip.
            - added in 1.1.1
        required: false
        type: str
    state:
        description:
            - the desired state of the resource - C(present) or C(absent).
            - If the resource is already defined, it will not be changed.
        default: present
        required: false
        type: str
        choices: [ present, absent ]

author:
    - Andrey Klyachkin (@aklyachkin)
'''

EXAMPLES = r'''
# create a new service ip label
- name: create a new service ip label
  enfence.powerha_aix.service_ip:
    name: clusterip
    state: present
# delete an existing service ip
- name: delete an existing service ip label
  enfence.powerha_aix.service_ip:
    name: clusterip
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

import os
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.enfence.powerha_aix.plugins.module_utils.helpers import check_powerha, parse_clmgrq_output, CLMGR


def get_cluster_ip(module):
    ipopts = dict()
    cmd = "%s query service_ip %s" % (CLMGR, module.params['name'])
    module.debug('Starting command: %s' % cmd)
    rc, stdout, stderr = module.run_command(cmd)
    if rc != 0:
        return 'absent', rc, stdout, stderr, ipopts
    ipopts = parse_clmgrq_output(stdout)
    return 'present', rc, stdout, stderr, ipopts


def add_cluster_ip(module):
    cmd = "%s add service_ip %s" % (CLMGR, module.params['name'])
    opts = ""
    if 'network' in module.params and module.params['network'] != '':
        opts += " network=%s" % module.params['network']
    if 'netmask' in module.params and module.params['netmask'] != '':
        opts += " netmask=%s" % module.params['netmask']
    if 'site' in module.params and module.params['site'] != '':
        opts += " site=%s" % module.params['site']
    cmd = "%s %s" % (cmd, opts)
    module.debug('Starting command: %s' % cmd)
    return module.run_command(cmd)


def delete_cluster_ip(module):
    cmd = "%s delete service_ip %s" % (CLMGR, module.params['name'])
    module.debug('Starting command: %s' % cmd)
    return module.run_command(cmd)


def run_module():
    module_args = dict(
        name=dict(type='str', required=True),
        state=dict(type='str', required=False, choices=['present', 'absent'], default='present'),
        network=dict(type='str', required=False, default='net_ether_01'),
        netmask=dict(type='str', required=False),
        site=dict(type='str', required=False)
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
        state, result['rc'], result['stdout'], result['stderr'] = get_cluster_ip(module)
        if state == 'present':
            result['msg'] = 'servce ip is already defined'
            module.exit_json(**result)
        result['changed'] = True
        if module.check_mode:
            result['msg'] = 'service ip will be defined'
            module.exit_json(**result)
        result['rc'], result['stdout'], result['stderr'] = add_cluster_ip(module)
        if result['rc'] != 0:
            result['msg'] = 'adding service ip to the cluster failed. see stderr for any error messages'
            module.fail_json(**result)
        result['msg'] = 'service ip added to the cluster'
    elif module.params['state'] == 'absent':
        state, result['rc'], result['stdout'], result['stderr'] = get_cluster_ip(module)
        if state == 'absent':
            result['msg'] = 'servce ip is not defined'
            result['rc'] = 0
            module.exit_json(**result)
        result['changed'] = True
        if module.check_mode:
            result['msg'] = 'service ip will be deleted'
            module.exit_json(**result)
        result['rc'], result['stdout'], result['stderr'] = delete_cluster_ip(module)
        if result['rc'] != 0:
            result['msg'] = 'deleting service ip failed. see stderr for any error messages'
            module.fail_json(**result)
        result['msg'] = 'service ip is deleted'
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
