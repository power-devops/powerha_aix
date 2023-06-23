#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2023, eNFence GmbH (info@power-devops.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

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
        choices: [ present, absent, started, stopped, synced ]
    nodes:
        description: list of nodes to be in the cluster. used only when the cluster is created
        required: false
        type: list
        elements: str
    repos:
        description: list of repository disks. used only when the cluster is created
        required: false
        type: list
        elements: str
        aliases: [ repo, repository, repositories ]
    type:
        description:
            - type of the cluster. used only when the cluster is created
            - added in 1.1.1
        required: false
        type: str
        choices: [ nsc, sc, lc ]
        default: nsc
    heartbeat:
        description:
            - hearbeat type for the cluster. used only when the cluster is created
            - added in 1.1.1
        required: false
        type: str
        choices: [ unicast, multicast ]
        default: unicast
    fix:
        description: automatically fix errors during synchronization
        required: false
        type: bool

author:
    - Andrey Klyachkin (@aklyachkin)
'''

EXAMPLES = r'''
# create a new cluster if it doesn't exist
- name: create a new cluster
  enfence.powerha_aix.cluster:
    name: cluster1
    state: present
    nodes:
      - node1
      - node2
    repos:
      - hdisk2
      - hdisk3
- name: delete an existing cluster
  enfence.powerha_aix.cluster:
    name: cluster1
    state: absent
- name: start cluster
  enfence.powerha_aix.cluster:
    name: cluster1
    state: started
- name: stop cluster
  enfence.powerha_aix.cluster:
    name: cluster1
    state: stopped
- name: synchronize cluster
  enfence.powerha_aix.cluster:
    name: cluster1
    fix: true
    state: synced
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
from ansible.module_utils.basic import AnsibleModule, is_executable

CLMGR = '/usr/es/sbin/cluster/utilities/clmgr'


def get_cluster_state(module):
    clusteropts = dict()
    cmd = "%s query cluster %s" % (CLMGR, module.params['name'])
    module.debug('Starting command: %s' % cmd)
    rc, stdout, stderr = module.run_command(cmd)
    if rc != 0:
        return 'absent', rc, stdout, stderr, clusteropts
    # check for other states, like started or stopped
    state = 'present'
    for line in stdout.splitlines():
        if '=' in line:
            opt, value = line.split('=')
            value = value.strip('"')
            if opt == 'STATE':
                state = value.lower()
            if value != "":
                clusteropts[opt] = value
    return state, rc, stdout, stderr, clusteropts


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
    # check type
    if 'type' in module.params:
        opts += ' TYPE=%s' % module.params['type']
    if 'heartbeat' in module.params:
        opts += ' HEARTBEAT_TYPE=%s' % module.params['heartbeat']
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
    if 'fix' in module.params and module.params['fix']:
        cmd = "%s force=yes fix=yes" % cmd
    module.debug('Starting command: %s' % cmd)
    return module.run_command(cmd)


def run_module():
    module_args = dict(
        name=dict(type='str', required=True),
        state=dict(type='str', required=True, choices=['present', 'absent', 'started', 'stopped', 'synced']),
        nodes=dict(type='list', required=False, elements='str'),
        repos=dict(type='list', required=False, elements='str', aliases=['repositories', 'repo', 'repository']),
        fix=dict(type='bool', required=False),
        type=dict(type='str', required=False, choices=['nsc', 'sc', 'lc'], default='nsc'),
        heartbeat=dict(type='str', required=False, choices=['unicast', 'multicast'], default='unicast')
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
    if not os.path.exists(CLMGR):
        result['msg'] = 'IBM PowerHA is not installed or clmgr is not found'
        result['rc'] = 1
        module.fail_json(**result)

    if not is_executable(CLMGR):
        result['msg'] = 'clmgr can not be executed by the current user'
        result['rc'] = 1
        module.fail_json(**result)

    # check if we should change cluster's state
    state, result['rc'], result['stdout'], result['stderr'], clopts = get_cluster_state(module)
    if module.params['state'] == 'absent' and state == 'absent':
        result['msg'] = 'cluster does not exist'
        result['rc'] = 0
        module.exit_json(**result)
    if module.params['state'] == 'started' and state == 'stable':
        result['msg'] = 'cluster is already started'
        module.exit_json(**result)
    if module.params['state'] == 'stopped' and state == 'offline':
        result['msg'] = 'cluster is already stopped'
        module.exit_json(**result)
    if module.params['state'] == 'present' and state != 'absent':
        # TODO: we need to check options if we should change anything on the cluster
        result['msg'] = 'cluster already exists'
        module.exit_json(**result)

    # create a new cluster
    if module.params['state'] == 'present':
        if module.check_mode:
            result['msg'] = 'cluster will be created'
            module.exit_json(**result)
        result['rc'], result['stdout'], result['stderr'] = create_cluster(module)
        if result['rc'] != 0:
            result['msg'] = 'cluster creation failed. see stderr for any error messages'
            module.fail_json(**result)
        result['changed'] = True
        module.exit_json(**result)

    # delete an existing cluster
    if module.params['state'] == 'absent':
        if module.check_mode:
            result['msg'] = 'cluster will be deleted'
            module.exit_json(**result)
        result['rc'], result['stdout'], result['stderr'] = delete_cluster(module)
        if result['rc'] != 0:
            result['msg'] = 'cluster deletion failed. see stderr for any error messages'
            module.fail_json(**result)
        result['changed'] = True
        module.exit_json(**result)

    if module.params['state'] == 'started':
        if state == 'absent' and not module.check_mode:
            result['msg'] = 'cluster does not exist'
            module.fail_json(**result)
        if module.check_mode:
            if state == 'absent':
                result['msg'] = 'cluster will start assuming it was created in some earlier task'
            else:
                result['msg'] = 'cluster will start'
            module.exit_json(**result)
        if state == 'not_configured' or state == 'unknown':
            # if cluster is not configured, we should force fixing all possible errors
            module.params['fix'] = True
            result['rc'], result['stdout'], result['stderr'] = sync_cluster(module)
            if result['rc'] != 0:
                result['msg'] = 'cluster sync is failed. see stderr for any error messages'
                module.fail_json(**result)
            result['changed'] = True
        result['rc'], result['stdout'], result['stderr'] = start_cluster(module)
        if result['rc'] != 0:
            result['msg'] = 'cluster is not started. see stderr for any error messages'
            module.fail_json(**result)
        result['changed'] = True
        module.exit_json(**result)

    if module.params['state'] == 'stopped':
        if state == 'absent' and not module.check_mode:
            result['msg'] = 'cluster does not exist'
            module.fail_json(**result)
        if module.check_mode:
            if state == 'absent':
                result['msg'] = 'cluster will stop assuming it was created in some earlier task'
            else:
                result['msg'] = 'cluster will stop'
            module.exit_json(**result)
        result['rc'], result['stdout'], result['stderr'] = stop_cluster(module)
        if result['rc'] != 0:
            result['msg'] = 'cluster is not stopped. see stderr for any error messages'
            module.fail_json(**result)
        result['changed'] = True
        module.exit_json(**result)

    if module.params['state'] == 'synced':
        if state == 'absent' and not module.check_mode:
            result['msg'] = 'cluster does not exist'
            module.fail_json(**result)
        if module.check_mode:
            if state == 'absent':
                result['msg'] = 'cluster will sync assuming it was created in some earlier task'
            else:
                result['msg'] = 'cluster will sync'
            module.exit_json(**result)
        result['rc'], result['stdout'], result['stderr'] = sync_cluster(module)
        if result['rc'] != 0:
            result['msg'] = 'cluster is not synced. see stderr for any error messages'
            module.fail_json(**result)
        result['changed'] = True
        module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
