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
    node:
        description:
            - Name of a target node where the resource group must be moved to.
            - Required if resource group's state is C(moved) and no target site is defined.
        required: false
        type: str
        aliases: [ target_node ]
    secnodes:
        description:
            - secondary nodes
            - added in 1.1.3
        required: false
        type: list
        elements: str
        aliases: [ secondary_nodes, secondarynodes ]
    site:
        description:
            - Name of a target site where the resource group must be moved to.
            - Required if resource group's state is C(moved) and no target node is defined.
        required: false
        type: str
        aliases: [ target_site ]
    sitepolicy:
        description:
            - site policy
            - added in 1.1.3
        required: false
        type: str
        choices: [ ignore, primary, either, both ]
        aliases: [ site_policy ]
    startup:
        description:
            - startup policy for the resource group. One of C(OHN), C(OFAN), C(OAAN), or C(OUDP).
            - C(OHN) - Online Home Node (default).
            - C(OFAN) - Online on First Available Node.
            - C(OAAN) - Online on All Available Nodes (concurrent).
            - C(OUDP) - Online Using Node Distribution Policy.
        required: false
        type: str
        choices: [ OHN, OFAN, OAAN, OUDP ]
        aliases: [ start ]
    fallover:
        description:
            - fallover policy for the resource group. One of C(FNPN), C(FUDNP), or C(BO).
            - C(FNPN) - Fallover to Next Priority Node (default).
            - C(FUDNP) - Fallover Using Dynamic Node Priority.
            - C(BO) - Bring Offline (On Error Node Only).
        required: false
        type: str
        choices: [ FNPN, FUDNP, BO ]
    fallback:
        description:
            - fallback policy for the resource group. One of C(NFB), or C(FBHPN).
            - C(NFB) - Never Fallback.
            - C(FBHPN) - Fallback to Higher Priority Node (default).
        required: false
        type: str
        choices: [ NFB, FBHPN ]
    prio_policy:
        description:
            - node priority policy, if fallover set to FUDNP. One of C(default), C(mem), C(disk), C(cpu), C(least), C(most)
            - C(default) - next node in the nodes list.
            - C(mem) - node with most available memory.
            - C(disk) - node with least disk activity.
            - C(cpu) - node with most cpu cycles available.
            - C(least) - node where the dynamic node priority script returns the lowest value.
            - C(most) - node where the dynamic node priority script returns the highest value.
            - added in 1.1.3
        required: false
        type: str
        choices: [ default, mem, disk, cpu, least, most ]
        aliases: [ node_priority_policy, priority_policy, priopolicy ]
    prio_policy_script:
        description:
            - path to script to determine the C(prio_policy)
            - added in 1.1.3
        required: false
        type: path
        aliases: [ node_priority_policy_script, priority_policy_script ]
    prio_policy_timeout:
        description:
            - added in 1.1.3
        required: false
        type: int
        aliases: [ node_priority_policy_timeout, priority_policy_timeout ]
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
    tape:
        description: .
        required: false
        type: list
        elements: str
        aliases: [ shared_tape, shared_tape_resources ]
    forced_varyon:
        description: .
        required: false
        type: bool
    vg_auto_import:
        description: .
        required: false
        type: bool
    fs:
        description: .
        required: false
        type: list
        elements: str
        aliases: [ filesystem, filesystems ]
    disk:
        description: .
        required: false
        type: list
        elements: str
        aliases: [ disks ]
    fs_before_ipaddr:
        description: .
        required: false
        type: bool
    wpar:
        description: .
        required: false
        type: str
        aliases: [ wpar_name ]
    export_nfs:
        description: .
        required: false
        type: list
        elements: str
        aliases: [ export_fs, export_filesystem ]
    export_nfs4:
        description: .
        required: false
        type: list
        elements: str
        aliases: [ export_fs4, export_fs_v4, export_filesystem_v4 ]
    stable_storage_path:
        description: .
        required: false
        type: str
    nfs_network:
        description: .
        required: false
        type: str
    mount_nfs:
        description: .
        required: false
        type: list
        elements: str
        aliases: [ mount_fs, mount_filesystem ]
    mirror_group:
        description: .
        required: false
        type: str
    fallback_at:
        description: .
        required: false
        type: str
    state:
        description:
            - the desired state of the resource - C(present), C(absent),
              C(started), C(stopped), C(moved).
            - If the resource is already defined, it will not be changed.
        default: present
        required: false
        type: str
        choices: [ present, absent, started, stopped, online, offline, moved ]

author:
    - Andrey Klyachkin (@aklyachkin)
'''

EXAMPLES = r'''
# create a new resource group
- name: Create a new resource group
  enfence.powerha_aix.rg:
    name: rg_oracle
    nodes:
      - node1
      - node2
    startup: OHN
    fallover: FNPN
    fallback: NFB
    service: ['serviceip']
    application: ['ac_ora']
    volgrp:
      - vg01
      - vg02
      - vg03
    state: present

# bring resource group online
- name: Start resource group
  enfence.powerha_aix.rg:
    name: rg_oracle
    state: started

# bring resource group offline
- name: Stop resource group
  enfence.powerha_aix.rg:
    name: rg_oracle
    state: stopped

# delete an existing resource group
- name: Delete an existing resource group
  enfence.powerha_aix.rg:
    name: rg_oracle
    state: absent

# move resource group to another node
- name: Move resource group to another node
  enfence.powerha_aix.rg:
    name: rg_oracle
    target_node: node2
    state: moved
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
from ansible_collections.enfence.powerha_aix.plugins.module_utils.helpers import add_list, add_string, add_bool, check_powerha, parse_clmgrq_output, CLMGR


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
    opts += add_string(module, 'sitepolicy', 'site_policy')
    opts += add_string(module, 'prio_policy', 'node_priority_policy')
    opts += add_string(module, 'prio_policy_script', 'node_priority_policy_script')
    opts += add_string(module, 'prio_policy_timeout', 'node_priority_policy_timeout')
    opts += add_string(module, 'wpar', 'wpar_name')
    opts += add_string(module, 'stable_storage_path', 'stable_storage_path')
    opts += add_string(module, 'nfs_network', 'nfs_network')
    opts += add_string(module, 'mirror_group', 'mirror_group')
    opts += add_string(module, 'fallback_at', 'fallback_at')
    opts += add_list(module, 'nodes', 'nodes')
    opts += add_list(module, 'secnodes', 'secondarynodes')
    opts += add_list(module, 'service', 'service_label')
    opts += add_list(module, 'application', 'applications')
    opts += add_list(module, 'volgrp', 'volume_group')
    opts += add_list(module, 'tape', 'shared_tape_resources')
    opts += add_list(module, 'fs', 'filesystem')
    opts += add_list(module, 'disk', 'disk')
    opts += add_list(module, 'export_nfs', 'export_filesystem')
    opts += add_list(module, 'export_nfs4', 'export_filesystem_v4')
    opts += add_list(module, 'mount_nfs', 'mount_filesystem')
    opts += add_bool(module, 'forced_varyon', 'forced_varyon')
    opts += add_bool(module, 'vg_auto_import', 'vg_auto_import')
    opts += add_bool(module, 'fs_before_ipaddr', 'fs_before_ipaddr')
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


def move_rg(module):
    cmd = "%s move resource_group"
    opts = ""
    if module.params['site'] is None:
        opts += add_string(module, 'node', 'node')
    else:
        opts += add_string(module, 'site', 'site')
    cmd = "%s %s" % (cmd, opts)
    module.debug('Starting command: %s' % cmd)
    return module.run_command(cmd)


def run_module():
    module_args = dict(
        name=dict(type='str', required=True),
        state=dict(type='str', required=False, choices=['present', 'absent', 'started', 'stopped', 'online', 'offline', 'moved'], default='present'),
        nodes=dict(type='list', required=False, elements='str'),
        node=dict(type='str', required=False, aliases=['target_node']),
        secnodes=dict(type='list', required=False, elements='str', aliases=['secondary_nodes', 'secondarynodes']),
        sitepolicy=dict(type='str', required=False, choices=['ignore', 'primary', 'either', 'both'], aliases=['site_policy']),
        site=dict(type='str', required=False, aliases=['target_site']),
        startup=dict(type='str', required=False, choices=['OHN', 'OFAN', 'OAAN', 'OUDP'], aliases=['start']),
        fallover=dict(type='str', required=False, choices=['FNPN', 'FUDNP', 'BO']),
        fallback=dict(type='str', required=False, choices=['NFB', 'FBHPN']),
        prio_policy=dict(type='str', required=False,
                         choices=['default', 'mem', 'cpu', 'disk', 'least', 'most'],
                         aliases=['priority_policy', 'node_priority_policy', 'priopolicy']),
        prio_policy_script=dict(type='path', required=False,
                                aliases=['node_priority_policy_script', 'priority_policy_script']),
        prio_policy_timeout=dict(type='int', required=False,
                                 aliases=['node_priority_policy_timeout', 'priority_policy_timeout']),
        service=dict(type='list', required=False, elements='str', aliases=['service_ip', 'service_label']),
        application=dict(type='list', required=False, elements='str', aliases=['app', 'applications']),
        volgrp=dict(type='list', required=False, elements='str', aliases=['vg', 'volume_group']),
        tape=dict(type='list', required=False, elements='str', aliases=['shared_tape', 'shared_tape_resources']),
        forced_varyon=dict(type='bool', required=False),
        vg_auto_import=dict(type='bool', required=False),
        fs=dict(type='list', required=False, elements='str', aliases=['filesystem', 'filesystems']),
        disk=dict(type='list', required=False, elements='str', aliases=['disks']),
        fs_before_ipaddr=dict(type='bool', required=False),
        wpar=dict(type='str', required=False, aliases=['wpar_name']),
        export_nfs=dict(type='list', required=False, elements='str', aliases=['export_fs', 'export_filesystem']),
        export_nfs4=dict(type='list', required=False, elements='str', aliases=['export_fs4', 'export_fs_v4', 'export_filesystem_v4']),
        stable_storage_path=dict(type='str', required=False),
        nfs_network=dict(type='str', required=False),
        mount_nfs=dict(type='list', required=False, elements='str', aliases=['mount_fs', 'mount_filesystem']),
        mirror_group=dict(type='str', required=False),
        fallback_at=dict(type='str', required=False)
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
        state, result['rc'], result['stdout'], result['stderr'], opts = get_rg(module)
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
        state, result['rc'], result['stdout'], result['stderr'], opts = get_rg(module)
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
        state, result['rc'], result['stdout'], result['stderr'], opts = get_rg(module)
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
        state, result['rc'], result['stdout'], result['stderr'], opts = get_rg(module)
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
    elif module.params['state'] == 'moved':
        if module.params['site'] is None and module.params['node'] is None:
            result['msg'] = 'either target node or target site must be specified'
            module.fail_json(**result)
        state, result['rc'], result['stdout'], result['stderr'], opts = get_rg(module)
        if state == 'absent':
            result['msg'] = 'resource group is not defined'
            module.fail_json(**result)
        if state == 'offline':
            result['msg'] = 'resource group is offline. If you want to move it to another node, start it there.'
            module.fail_json(**result)
        if module.params['site'] is None:
            target = 'node %s' % module.params['node']
        else:
            target = 'site %s' % module.params['site']
        if module.check_mode:
            result['msg'] = 'resource group will be moved to %s' % (target)
            module.exit_json(**result)
        result['rc'], result['stdout'], result['stderr'] = move_rg(module)
        if result['rc'] != 0:
            result['msg'] = 'moving resource group to %s failed. see stderr for any error messages' % (target)
            module.fail_json(**result)
        result['msg'] = 'resource group is moved to %s' % (target)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
