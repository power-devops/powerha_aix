#!/usr/bin/python

# Copyright (c) 2023, eNFence GmbH (info@power-devops.com)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: cluster

short_description: manage PowerHA cluster
version_added: "1.0.0"

description: This module creates/deletes/starts or stops a PowerHA cluster. Depending on the state different set of attributes are required. 

options:
    name:
        description: name of the cluster.
        required: true
        type: str
    state:
        description: the desired state of the cluster - present, absent, started, stopped, synced
        required: true
        type: str
    nodes:
        description: list of nodes to be in the cluster. used only when the cluster is created
        required: false
        type: list
    repos:
        description: list of repository disks. used only when the cluster is created
        required: false
        type: list
    fix:
        description: automatically fix errors during synchronization
        required: false
        type: bool

author: 
    - Andrey Klyachkin <info@power-devops.com>
'''

EXAMPLES = r'''
# create a new cluster if it doesn't exist
- name: create a new cluster
  powerdevops.powerha_aix.cluster:
    name: cluster1
    state: present
    nodes:
      - node1
      - node2
    repos:
      - hdisk2
      - hdisk3
- name: delete an existing cluster
  powerdevops.powerha_aix.cluster:
    name: cluster1
    state: absent
- name: start cluster
  powerdevops.powerha_aix.cluster:
    name: cluster1
    state: started
- name: stop cluster
  powerdevops.powerha_aix.cluster:
    name: cluster1
    state: stopped
- name: synchronize cluster
  powerdevops.powerha_aix.cluster:
    name: cluster1
    fix: true
    state: synced
'''

RETURN = r'''
# possible return values
'''

from ansible.module_utils.basic import AnsibleModule, is_executable
import os

CLMGR='/usr/es/sbin/cluster/utilities/clmgr'

def get_cluster_state(module):
    cmd = "%s query cluster %s" % (CLMGR, module.params['name'])
    module.debug('Starting command: %s' % cmd)
    rc, stdout, stderr = module.run_command(cmd)
    if rc != 0:
        return 'absent', rc, stdout, stderr
    # check for other states, like started or stopped
    state='present'
    for line in stdout.splitlines():
        if line.startswith('STATE='):
            state=line.split('=')[1].strip('"').lower()
    return state, rc, stdout, stderr

def create_cluster(module):
    opts = module.params['name']
    # check nodes
    if 'nodes' in module.params:
        oldopts = opts
        try:
            opts += ' NODES='
            for node in module.params['nodes']:
                opts += '%s,' % node
            opts = opts[:-1]
        except TypeError:
            opts = oldopts
    # check repos
    if 'repos' in module.params:
        oldopts = opts
        try:
            opts += ' REPOSITORIES='
            for repo in module.params['repos']:
                opts += '%s,' % repo
            opts = opts[:-1]
        except TypeError:
            opts = oldopts
    cmd = "%s add cluster %s" % (CLMGR, opts)
    module.debug('Starting command: %s' % cmd)
    return module.run_command(cmd)

def delete_cluster(module):
    cmd = "%s delete cluster NODES=ALL" % CLMGR
    module.debug('Starting command: %s' % cmd)
    return module.run_command(cmd)

def start_cluster(module):
    cmd = "%s online cluster when=now manage=auto broadcast=false clinfo=false force=true fix=yes start_caa=yes" % CLMGR
    module.debug('Starting command: %s' % cmd)
    return module.run_command(cmd)

def stop_cluster(module):
    cmd = "%s offline cluster when=now manage=offline broadcast=false stop_caa=no" % CLMGR
    module.debug('Starting command: %s' % cmd)
    return module.run_command(cmd)

def sync_cluster(module):
    cmd = "%s sync cluster" % CLMGR
    if 'fix' in module.params and module.params['fix'] == True:
        cmd = "%s force=yes fix=yes" % cmd
    module.debug('Starting command: %s' % cmd)
    return module.run_command(cmd)

def run_module():
    module_args = dict(
        name = dict(type='str', required=True),
        state = dict(type='str', required=True, choices=['present', 'absent', 'started', 'stopped', 'synced']),
        nodes = dict(type='list', required=False, elements='str'),
        repos = dict(type='list', required=False, elements='str', aliases=['repositories','repo','repository']),
        fix = dict(type='bool', required=False)
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

    # check state and possible attributes
    if module.params['state'] == 'present':
        state, result['rc'], result['stdout'], result['stderr'] = get_cluster_state(module)
        if state != 'absent':
            result['message']='cluster already exists'
            module.exit_json(**result)
        if module.check_mode:
            result['message']='cluster will be created'
            module.exit_json(**result)
        result['rc'], result['stdout'], result['stderr'] = create_cluster(module)
        if rc != 0:
            result['message']='cluster creation failed. see stderr for any error messages'
            module.fail_json(msg=result['message'], rc=result['rc'], result=result)
        result['changed']=True
        module.exit_json(**result)
    elif module.params['state'] == 'absent':
        state, result['rc'], result['stdout'], result['stderr'] = get_cluster_state(module)
        if state == 'absent':
            result['message']='cluster does not exist'
            reuslt['rc']=0
            module.exit_json(**result)
        if module.check_mode:
            result['message']='cluster will be deleted'
            module.exit_json(**result)
        result['rc'], result['stdout'], result['stderr'] = delete_cluster(module)
        if result['rc'] != 0:
            result['message']='cluster deletion failed. see stderr for any error messages'
            module.fail_json(msg=result['message'], rc=result['rc'], result=result)
        result['changed']=True
        module.exit_json(**result)
    elif module.params['state'] == 'started':
        state, result['rc'], result['stdout'], result['stderr'] = get_cluster_state(module)
        if state == 'absent':
            result['message']='cluster does not exist'
            module.fail_json(msg=result['message'], rc=result['rc'], result=result)
        if state == 'stable':
            result['message']='cluster is already started'
            module.exit_json(**result)
        if module.check_mode:
            result['message']='cluster will start'
            module.exit_json(**result)
        result['changed']=True
        if state == 'not_configured':
            result['rc'], result['stdout'], result['stderr'] = sync_cluster(module)
            if result['rc'] != 0:
                result['message']='cluster sync is failed. see stderr for any error messages'
                module.fail_json(msg=result['message'], rc=result['rc'], result=result)
        result['rc'], result['stdout'], result['stderr'] = start_cluster(module)
        if result['rc'] != 0:
            result['message']='cluster is not started. see stderr for any error messages'
            module.fail_json(msg=result['message'], rc=result['rc'], result=result)
    elif module.params['state'] == 'stopped':
        state, result['rc'], result['stdout'], result['stderr'] = get_cluster_state(module)
        if state == 'absent':
            result['message']='cluster does not exist'
            module.fail_json(msg=result['message'], rc=result['rc'], result=result)
        if state == 'offline':
            result['message']='cluster is already stopped'
            module.exit_json(**result)
        if module.check_mode:
            result['message']='cluster will start'
            module.exit_json(**result)
        result['changed']=True
        result['rc'], result['stdout'], result['stderr'] = stop_cluster(module)
        if result['rc'] != 0:
            result['message']='cluster is not stopped. see stderr for any error messages'
            module.fail_json(msg=result['message'], rc=result['rc'], result=result)
    elif module.params['state'] == 'synced':
        state, result['rc'], result['stdout'], result['stderr'] = get_cluster_state(module)
        if state == 'absent':
            result['message']='cluster does not exist'
            module.fail_json(msg=result['message'], rc=result['rc'], result=result)
        if module.check_mode:
            result['message']='cluster will sync'
            module.exit_json(**result)
        result['changed']=True
        result['rc'], result['stdout'], result['stderr'] = sync_cluster(module)
        if result['rc'] != 0:
            result['message']='cluster is not synced. see stderr for any error messages'
            module.fail_json(msg=result['message'], rc=result['rc'], result=result)
        
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
