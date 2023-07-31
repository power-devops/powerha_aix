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
        description:
            - the desired state of the volume group - C(present), C(absent).
            - additional states C(rgadd) and C(rgremove) to add and remove the volume group from a resource group.
        required: false
        type: str
        choices: [ present, absent, rgadd, rgremove ]
        default: present
    nodes:
        description:
          - list of nodes where volume group can be activated.
          - required if the state is C(present).
        required: false
        type: list
        elements: str
    type:
        description: volume group type.
        required: false
        type: str
        choices: [ original, big, scalable, legacy ]
        default: scalable
    volumes:
        description:
          - list of physical volumes to add into the volume group.
          - required if the state is C(present).
        required: false
        type: list
        elements: str
        aliases: [ physical_volumes, pv, pvs, volume ]
    rg:
        description:
            - resource group for the volume group.
            - required if state is C(rgadd) or C(rgremove).
        required: false
        type: str
        aliases: [ resource_group ]
    pp_size:
        description: size of the physical partition in MB.
        required: false
        type: int
        choices: [ 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024 ]
        aliases: [ ppart_size, ppsize, pp ]
    major:
        description: major number of the volume group device.
        required: false
        type: int
        aliases: [ major_number, number ]
    activate_on_restart:
        description: activate the volume group on system startup.
        required: false
        type: bool
    quorum:
        description: if the volume group must be automatically varied off after losing its quorum of physical volumes.
        required: false
        type: bool
        aliases: [ quorum_needed ]
    ltg:
        description: logical track group size.
        required: false
        type: int
        choices: [ 128, 256, 512, 1024 ]
        aliases: [ ltg_size ]
    migrate_failed_disks:
        description: .
        required: false
        type: str
        choices: [ 'false', one, pool, remove ]
    max_pp:
        description: maximum number of physical partitions in the volume group.
        required: false
        type: int
        choices: [ 32, 64, 128, 256, 512, 768, 1024 ]
        aliases: [ maxpp, max_physical_partitions ]
    max_lv:
        description: maximum number of logical volumes in the volume group.
        required: false
        type: int
        choices: [ 256, 512, 1024, 2048, 4096 ]
        aliases: [ maxlv, max_logical_volumes ]
    strict_mp:
        description:
            - enable mirror pool strictness on the volume group.
            - C(no) means disable mirror pool strictness.
            - C(yes) means mirror pools must be used.
            - C(super) means mirror pools will be enforced.
        required: false
        type: str
        choices: [ 'yes', 'no', super ]
        aliases: [ strict_mirror_pools ]
    mp:
        description: the name of the mirror pool.
        required: false
        type: str
        aliases: [ mirror_pool, mirror_pool_name ]
    critical:
        description: enable critical vg flag on the volume group.
        required: false
        type: bool
    encryption:
        description: enalbe LV encryption on the volume group
        required: false
        type: bool
        aliases: [ lv_encryption, enable_lv_encryption ]
    on_failure:
        description: action on failure of the critical volume group.
        required: false
        type: str
        choices: [ halt, notify, fence, stoprg, moverg ]
        aliases: [ failureaction, failure_action ]
    notify:
        description: script to call if the C(on_failure) action is C(notify).
        required: false
        type: path
        aliases: [ notify_method, notifymethod ]
    preferred_read:
        description: read preference to the copy of logical volumes.
        required: false
        type: str
        choices: [ roundrobin, favorcopy, siteaffinity ]
        aliases: [ lvm_preferred_read, prefered_read, lvm_prefered_read ]

author:
    - Andrey Klyachkin (@aklyachkin)
'''

EXAMPLES = r'''
# find a disk with LDEV 25B6 and create vg01 on it
- name: find disk for vg01
  enfence.powerha_aix.pv_info:
    ldev: 25B6
  register: hdisk
- name: stop if the hdisk is not found
  ansible.builtin.fail:
    msg: hdisk for the volume group is not found
  when: hdisk.pv | length == 0
- name: create shared volume group
  enfence.powerha_aix.vg:
    name: vg01
    nodes:
      - node1
      - node2
    volumes: "{{ hdisk.pv }}"
    rg: rg_oracle
# delete volume group vg01
- name: delete vg01
  enfence.powerha_aix.vg:
    name: vg01
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
    add_string, add_list, add_int, add_bool, check_powerha, parse_clmgrq_output, CLMGR)


def get_rg(module):
    rgopts = dict()
    cmd = "%s query resource_group %s" % (CLMGR, module.params['rg'])
    module.debug('Starting command: %s' % cmd)
    rc, stdout, stderr = module.run_command(cmd)
    if rc != 0:
        return rgopts, rc, stdout, stderr
    rgopts = parse_clmgrq_output(stdout)
    return rgopts, rc, stdout, stderr


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
    opts += add_string(module, 'type', 'type')
    opts += add_string(module, 'rg', 'resource_group')
    opts += add_string(module, 'migrate_failed_disks', 'migrate_failed_disks')
    opts += add_string(module, 'strict_mp', 'strict_mirror_pools')
    opts += add_string(module, 'mp', 'mirror_pool_name')
    opts += add_string(module, 'on_failure', 'failureaction')
    opts += add_string(module, 'notify', 'notifymethod')
    opts += add_string(module, 'preferred_read', 'lvm_preferred_read')
    opts += add_int(module, 'pp_size', 'ppart_size')
    opts += add_int(module, 'major', 'major_number')
    opts += add_int(module, 'ltg', 'ltg_size')
    opts += add_int(module, 'max_pp', 'max_physical_partitions')
    opts += add_int(module, 'max_lv', 'max_logical_volumes')
    opts += add_bool(module, 'activate_on_restart', 'activate_on_restart')
    opts += add_bool(module, 'quorum', 'quorum_needed')
    opts += add_bool(module, 'critical', 'critical')
    opts += add_bool(module, 'encryption', 'enable_lv_encryption')
    cmd = "%s %s" % (cmd, opts)
    module.debug('Starting command: %s' % cmd)
    return module.run_command(cmd)


def delete_vg(module):
    cmd = "%s delete volume_group %s" % (CLMGR, module.params['name'])
    module.debug('Starting command: %s' % cmd)
    return module.run_command(cmd)


def addrg_vg(module):
    rgopts, rc, stdout, stderr = get_rg(module)
    if rc != 0:
        return rc, stdout, stderr
    # get active vgs
    vglist = rgopts['VOLUME_GROUP'].split()
    vglist.append(module.params['name'])
    # modify rg
    cmd = "%s modify resource_group %s volume_group=%s" % (CLMGR, module.params['rg'], ','.join(vglist))
    module.debug('Starting command: %s' % cmd)
    return module.run_command(cmd)


def deleterg_vg(module):
    rgopts, rc, stdout, stderr = get_rg(module)
    if rc != 0:
        return rc, stdout, stderr
    vglist = rgopts['VOLUME_GROUP'].split()
    vglist.remove(module.params['name'])
    cmd = "%s modify resource_group %s volume_group=%s" % (CLMGR, module.params['rg'], ','.join(vglist))
    module.debug('Starting command: %s' % cmd)
    return module.run_command(cmd)


def run_module():
    module_args = dict(
        name=dict(type='str', required=True),
        state=dict(type='str', required=False, choices=['present', 'absent', 'rgadd', 'rgremove'], default='present'),
        nodes=dict(type='list', required=False, elements='str'),
        volumes=dict(type='list', required=False, elements='str', aliases=['physical_volumes', 'pv', 'pvs', 'volume']),
        type=dict(type='str', required=False, choices=['original', 'big', 'scalable', 'legacy'], default='scalable'),
        rg=dict(type='str', required=False, aliases=['resource_group']),
        pp_size=dict(type='int', required=False, choices=[1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024], aliases=['ppart_size', 'ppsize', 'pp']),
        major=dict(type='int', required=False, aliases=['major_number', 'number']),
        activate_on_restart=dict(type='bool', required=False),
        quorum=dict(type='bool', required=False, aliases=['quorum_needed']),
        ltg=dict(type='int', required=False, choices=[128, 256, 512, 1024], aliases=['ltg_size']),
        migrate_failed_disks=dict(type='str', required=False, choices=['false', 'one', 'pool', 'remove']),
        max_pp=dict(type='int', required=False, choices=[32, 64, 128, 256, 512, 768, 1024], aliases=['maxpp', 'max_physical_partitions']),
        max_lv=dict(type='int', required=False, choices=[256, 512, 1024, 2048, 4096], aliases=['maxlv', 'max_logical_volumes']),
        strict_mp=dict(type='str', required=False, choices=['no', 'yes', 'super'], aliases=['strict_mirror_pools']),
        mp=dict(type='str', required=False, aliases=['mirror_pool', 'mirror_pool_name']),
        critical=dict(type='bool', required=False),
        encryption=dict(type='bool', required=False, aliases=['lv_encryption', 'enable_lv_encryption']),
        on_failure=dict(type='str', required=False, choices=['halt', 'notify', 'fence', 'stoprg', 'moverg'], aliases=['failure_action', 'failureaction']),
        notify=dict(type='path', required=False, aliases=['notify_method', 'notifymethod']),
        preferred_read=dict(type='str', required=False, choices=['roundrobin', 'favorcopy', 'siteaffinity'],
                            aliases=['lvm_preferred_read', 'prefered_read', 'lvm_prefered_read'])
    )

    result = dict(
        changed=False,
        msg='No changes',
        rc=0
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[('state', 'present', ('nodes', 'volumes'))],
        required_by={
            'notify': 'critical',
            'on_failure': 'critical',
            'preferred_read': 'critical'
        }
    )

    module._debug = True
    module.debug('Starting enfence.powerha_aix.vg module')
    # check if we can run clmgr
    result = check_powerha(result)
    if result['rc'] == 1:
        module.fail_json(**result)

    if module.params['type'] is None or module.params['type'] == '':
        module.params['type'] = 'scalable'

    if module.params['max_pp'] is not None and module.params['type'] != 'scalable':
        result['msg'] = 'max_pp can be specified only volume group is of type scalable'
        module.fail_json(**result)

    if module.params['max_lv'] is not None and module.params['type'] != 'scalable':
        result['msg'] = 'max_lv can be specified only volume group is of type scalable'
        module.fail_json(**result)

    if module.params['strict_mp'] is not None and module.params['type'] != 'scalable':
        result['msg'] = 'strict_mp can be specified only volume group is of type scalable'
        module.fail_json(**result)

    if module.params['mp'] is not None and module.params['type'] != 'scalable':
        result['msg'] = 'mp can be specified only volume group is of type scalable'
        module.fail_json(**result)

    if module.params['rg'] is None and (module.params['state'] == 'rgadd' or module.params['state'] == 'rgremove'):
        result['msg'] = 'rg is required if state is rgadd or rgremove'
        module.fail_json(**result)

    if module.params['state'] is None or module.params['state'] == 'present':
        state, result['rc'], result['stdout'], result['stderr'], opts = get_vg(module)
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
        state, result['rc'], result['stdout'], result['stderr'], opts = get_vg(module)
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
    elif module.params['state'] == 'rgadd':
        state, result['rc'], result['stdout'], result['stderr'], opts = get_vg(module)
        if state == 'absent':
            result['msg'] = 'volume group does not exist'
            module.exit_json(**result)
        if 'RESOURCE_GROUP' in opts and module.params['rg'] in opts['RESOURCE_GROUP']:
            result['msg'] = 'volume group is already added into resource group'
            result['rc'] = 0
            module.exit_json(**result)
        result['changed'] = True
        if module.check_mode:
            result['msg'] = 'volume group will be added into resource group'
            module.exit_json(**result)
        result['rc'], result['stdout'], result['stderr'] = addrg_vg(module)
        if result['rc'] != 0:
            result['msg'] = 'adding volume group into resource group failed. see stderr for any error messages'
            module.exit_json(**result)
        result['msg'] = 'volume group is added into resource group'
    elif module.params['state'] == 'rgremove':
        state, result['rc'], result['stdout'], result['stderr'], opts = get_vg(module)
        if state == 'absent':
            result['msg'] = 'volume group does not exist'
            module.exit_json(**result)
        if 'RESOURCE_GROUP' not in opts or opts['RESOURCE_GROUP'] is None or module.params['rg'] not in opts['RESOURCE_GROUP']:
            result['msg'] = 'volume group is not in resource group'
            result['rc'] = 0
            module.exit_json(**result)
        result['changed'] = True
        if module.check_mode:
            result['msg'] = 'volume group will be removed from resource group'
            module.exit_json(**result)
        result['rc'], result['stdout'], result['stderr'] = deleterg_vg(module)
        if result['rc'] != 0:
            result['msg'] = 'removing volume group from resource group failed. see stderr for any error messages'
            module.exit_json(**result)
        result['msg'] = 'volume group is removed from resource group'
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
