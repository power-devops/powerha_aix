#!/usr/bin/python

# Copyright (c) 2023, eNFence GmbH (info@power-devops.com)
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
        description: name of the service ip label. the name must be resolvable by using /etc/hosts.
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
    state:
        description: the desired state of the resource - present or absent. If the resource is already defined, it will not be changed.
        default: present
        required: false
        type: str

author:
    - Andrey Klyachkin <info@power-devops.com>
'''

EXAMPLES = r'''
# create a new service ip label
- name: create a new service ip label
  powerdevops.powerha_aix.service_ip:
    name: clusterip
    state: present
# delete an existing service ip
- name: delete an existing service ip label
  powerdevops.powerha_aix.service_ip:
    name: clusterip
    state: absent
'''

RETURN = r'''
# possible return values
'''

from ansible.module_utils.basic import AnsibleModule, is_executable
import os

CLMGR='/usr/es/sbin/cluster/utilities/clmgr'

def get_cluster_ip(module):
    cmd = "%s query service_ip %s" % (CLMGR, module.params['name'])
    module.debug('Starting command: %s' % cmd)
    rc, stdout, stderr = module.run_command(cmd)
    if rc != 0:
        return 'absent', rc, stdout, stderr
    return 'present', rc, stdout, stderr

def add_cluster_ip(module):
    cmd = "%s add service_ip %s" % (CLMGR, module.params['name'])
    opts = ""
    if 'network' in module.params and module.params['network'] != '':
        opts += " network=%s" % module.params['network']
    if 'netmask' in module.params and module.params['netmask'] != '':
        opts += " netmask=%s" % module.params['netmask']
    cmd = "%s %s" % (cmd, opts)
    module.debug('Starting command: %s' % cmd)
    return module.run_command(cmd)

def delete_cluster_ip(module):
    cmd = "%s delete service_ip %s" % (CLMGR, module.params['name'])
    module.debug('Starting command: %s' % cmd)
    return module.run_command(cmd)

def run_module():
    module_args = dict(
        name = dict(type='str', required=True),
        state = dict(type='str', required=False, choices=['present', 'absent'], default='present'),
        network = dict(type='str', required=False, default='net_ether_01'),
        netmask = dict(type='str', required=False)
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
        result['message']='IBM PowerHA is not installed or clmgr is not found'
        module.fail_json(msg=result['message'], rc=1)

    if not is_executable(CLMGR):
        result['message']='clmgr can not be executed by the current user'
        module.fail_json(msg=result['message'], rc=1)

    if module.params['state'] == None or module.params['state'] == 'present':
        state, result['rc'], result['stdout'], result['stderr'] = get_cluster_ip(module)
        if state == 'present':
            result['message']='servce ip is already defined'
            module.exit_json(**result)
        result['changed']=True
        if module.check_mode:
            result['message']='service ip will be defined'
            module.exit_json(**result)
        result['rc'], result['stdout'], result['stderr'] = add_cluster_ip(module)
        if result['rc'] != 0:
            result['message']='adding service ip to the cluster failed. see stderr for any error messages'
            module.fail_json(msg=result['message'], rc=result['rc'], result=result)
        result['message']='service ip added to the cluster'
    elif module.params['state'] == 'absent':
        state, result['rc'], result['stdout'], result['stderr'] = get_cluster_ip(module)
        if state == 'absent':
            result['message']='servce ip is not defined'
            result['rc']=0
            module.exit_json(**result)
        result['changed']=True
        if module.check_mode:
            result['message']='service ip will be deleted'
            module.exit_json(**result)
        result['rc'], result['stdout'], result['stderr'] = delete_cluster_ip(module)
        if result['rc'] != 0:
            result['message']='deleting service ip failed. see stderr for any error messages'
            module.fail_json(msg=result['message'], rc=result['rc'], result=result)
        result['message']='service ip is deleted'
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()

