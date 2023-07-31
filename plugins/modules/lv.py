#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2023, eNFence GmbH (info@power-devops.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: lv

short_description: manage logical volumes in PowerHA cluster
version_added: "1.2.0"

description:
    - This module creates/deletes/changes logical_volume resource in PowerHA cluster.

options:
    name:
        description: name of the logical volume.
        required: true
        type: str
    state:
        description: the desired state of the logical volume - C(present), C(absent).
        required: false
        type: str
        choices: [ present, absent ]
        default: present
    vg:
        description: name of the volume group where the logical volume resides.
        required: true
        type: str
        aliases: [ volgrp, volume_group ]
    size:
        description: size of the logical volume. required if state is C(present).
        required: false
        type: int
    unit:
        description:
          - unit for the size of the logical volume.
          - the size will be rounded according to physical partition size in the volume group.
        required: false
        type: str
        choices: [ pp, mb, gb ]
        default: pp
    volumes:
        description: physical volumes where the logical volume should reside.
        required: false
        type: list
        elements: str
        aliases: [ physical_volumes, pv, pvs, volume ]
    type:
        description: type of the logical volumes.
        required: false
        type: str
        choices: [ jfs, jfs2, sysdump, paging, jfslog, jfs2log, aio_cache, boot ]
        default: jfs2
    position:
        description: position of the logical volume on the physical volume.
        required: false
        type: str
        choices: [ outer_middle, outer_edge, center, inner_middle, inner_edge ]
        aliases: [ pos ]
    pv_range:
        description: how to place the logical volume on physical volumes.
        required: false
        type: str
        choices: [ maximum, minimum ]
        aliases: [ pvrange, range ]
    max_pv:
        description: maximum number of physical volumes to use for the logical volume.
        required: false
        type: int
        aliases: [ max_pvs_for_new_alloc ]
    copies:
        description: number of copies of the logical volume.
        required: false
        type: int
        choices: [ 1, 2, 3 ]
        aliases: [ lpart_copies, lp_copies ]
    write_consistency:
        description: mode of write consistency.
        required: false
        type: str
        choices: [ active, passive, 'off' ]
    sep_pvs:
        description: Strict allocation policy.
        required: false
        type: str
        choices: [ 'yes', 'no', 'superstrict' ]
        aliases: [ separate_pvs, lparts_on_separate_pvs, lps_on_separate_pvs ]
    relocate:
        description: Reorganization relocation flag.
        required: false
        type: bool
    label:
        description: logical volume label.
        required: false
        type: str
    max_lp:
        description: maximum number of logical partitions in the logical volume.
        required: false
        type: int
        aliases: [ max_lps, max_lparts, maxlp ]
    bb_relocate:
        description: Bad-block relocation policy.
        required: false
        type: bool
        aliases: [ bad_block_relocation ]
    sched_policy:
        description: Scheduling policy when more than one logical partition is written.
        required: false
        type: str
        choices: [ parallel, sequential, parallel_sequential, parallel_round_robin ]
        aliases: [ scheduling_policy, schedpolicy, policy ]
    verify_writes:
        description: Sets the write-verify state for the logical volume.
        required: false
        type: bool
    alloc_map:
        description: Specifies the exact physical partitions to allocate.
        required: false
        type: path
        aliases: [ allocation_map ]
    stripe_size:
        description: Specifies the number of bytes per strip.
        required: false
        type: str
        choices: [ 4K, 8K, 16K, 32K, 64K, 128K, 256K, 512K, 1M, 2M, 4M, 8M, 16M, 32M, 64M, 128M ]
    serialize_io:
        description: Turns on/off serialization of overlapping I/Os.
        required: false
        type: bool
    first_block_available:
        description: The logical volume control block does not occupy the first block of the logical volume.
        required: false
        type: bool
    mp1:
        description: Specify a mirror pool for first copy.
        required: false
        type: str
        aliases: [ mirror_pool_1, first_copy_mirror_pool ]
    mp2:
        description: Specify a mirror pool for second copy.
        required: false
        type: str
        aliases: [ mirror_pool_2, second_copy_mirror_pool ]
    mp3:
        description: Specify a mirror pool for third copy.
        required: false
        type: str
        aliases: [ mirror_pool_3, third_copy_mirror_pool ]
    group:
        description: Specifies group ID for the logical volume special file.
        required: false
        type: str
    permissions:
        description: Specifies permissions (file modes) for the logical volume special file.
        required: false
        type: str
    node:
        description: Reference node.
        required: false
        type: str
    encryption:
        description: Enables the data encryption option in the logical volume.
        required: false
        type: bool
        aliases: [ lv_encryption, enable_lv_encryption ]
    auth_method:
        description: N/A.
        required: false
        type: str
        choices: [ keyserv, pks ]
    method_details:
        description: N/A.
        required: false
        type: str
    auth_method_name:
        description: N/A.
        required: false
        type: str

author:
    - Andrey Klyachkin (@aklyachkin)
'''

EXAMPLES = r'''
- name: create logical volume
  enfence.powerha_aix.lv:
    name: lvora
    vg: vg01
    size: 1
    unit: gb
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
    add_bool, add_list, add_int, add_string, check_powerha, parse_clmgrq_output, CLMGR)
import math


def calc_size(module):
    if module.params['unit'] == 'pp':
        return module.params['size']
    # recalc size in MB first
    size = module.params['size']
    if module.params['unit'] == 'gb':
        size = module.params['size'] * 1024
    # ppsize is in MB
    ppsize = int(get_vg(module)['PPART_SIZE'])
    module.debug('ppsize is %s' % ppsize)
    # recalc size in pps
    size = math.ceil(size / ppsize)
    return size


def get_vg(module):
    vgopts = dict()
    cmd = "%s query volume_group %s" % (CLMGR, module.params['vg'])
    module.debug('Starting command: %s' % cmd)
    rc, stdout, stderr = module.run_command(cmd)
    if rc != 0:
        return vgopts
    vgopts = parse_clmgrq_output(stdout)
    return vgopts


def get_lv(module):
    lvopts = dict()
    cmd = "%s query logical_volume %s" % (CLMGR, module.params['name'])
    module.debug('Starting command: %s' % cmd)
    rc, stdout, stderr = module.run_command(cmd)
    if rc != 0:
        return 'absent', rc, stdout, stderr, lvopts
    # Check for ERROR: in stderr
    # PowerHA 7.2.7 GA, rc == 0 even if the error is reported
    # ERROR: "lv01" does not appear to exist!
    if "ERROR:" in stderr:
        return 'absent', 1, stdout, stderr, lvopts
    vgopts = parse_clmgrq_output(stdout)
    return 'present', rc, stdout, stderr, lvopts


def add_lv(module):
    cmd = "%s add logical_volume %s" % (CLMGR, module.params['name'])
    opts = ""
    opts += add_string(module, 'vg', 'volume_group')
    if module.params['unit'] != 'pp':
        module.params['size'] = calc_size(module)
    opts += add_int(module, 'size', 'logical_partitions')
    opts += add_list(module, 'volumes', 'physical_volumes')
    opts += add_string(module, 'type', 'type')
    opts += add_string(module, 'position', 'position')
    opts += add_string(module, 'pv_range', 'pv_range')
    opts += add_string(module, 'write_consistency', 'write_consistency')
    opts += add_string(module, 'sep_pvs', 'lpars_on_separate_pvs')
    opts += add_string(module, 'label', 'label')
    opts += add_string(module, 'sched_policy', 'scheduling_policy')
    opts += add_string(module, 'alloc_map', 'allocation_map')
    opts += add_string(module, 'stripe_size', 'stripe_size')
    opts += add_string(module, 'mp1', 'first_copy_mirror_pool')
    opts += add_string(module, 'mp2', 'second_copy_mirror_pool')
    opts += add_string(module, 'mp3', 'third_copy_mirror_pool')
    opts += add_string(module, 'group', 'group')
    opts += add_string(module, 'permissions', 'permissions')
    opts += add_string(module, 'node', 'node')
    opts += add_string(module, 'auth_method', 'auth_method')
    opts += add_string(module, 'method_details', 'method_details')
    opts += add_string(module, 'auth_method_name', 'auth_method_name')
    opts += add_int(module, 'max_pv', 'max_pvs_for_new_alloc')
    opts += add_int(module, 'copies', 'lpart_copies')
    opts += add_int(module, 'max_lp', 'max_lparts')
    opts += add_bool(module, 'relocate', 'relocate')
    opts += add_bool(module, 'bb_relocate', 'bad_block_relocation')
    opts += add_bool(module, 'verify_writes', 'verify_writes')
    opts += add_bool(module, 'serialize_io', 'serialize_io')
    opts += add_bool(module, 'first_block_available', 'first_block_available')
    opts += add_bool(module, 'encryption', 'enable_lv_encryption')
    cmd = "%s %s" % (cmd, opts)
    module.debug('Starting command: %s' % cmd)
    return module.run_command(cmd)


def delete_lv(module):
    cmd = "%s delete logical_volume %s" % (CLMGR, module.params['name'])
    module.debug('Starting command: %s' % cmd)
    return module.run_command(cmd)


def run_module():
    module_args = dict(
        name=dict(type='str', required=True),
        state=dict(type='str', required=False, choices=['present', 'absent'], default='present'),
        vg=dict(type='str', required=True, aliases=['volgrp', 'volume_group']),
        size=dict(type='int', required=False),
        unit=dict(type='str', required=False, choices=['pp', 'mb', 'gb'], default='pp'),
        volumes=dict(type='list', required=False, elements='str', aliases=['physical_volumes', 'pv', 'pvs', 'volume']),
        type=dict(type='str', required=False, choices=['jfs', 'jfs2', 'sysdump', 'paging', 'jfslog', 'jfs2log', 'aio_cache', 'boot'], default='jfs2'),
        position=dict(type='str', required=False, choices=['outer_middle', 'outer_edge', 'center', 'inner_middle', 'inner_edge'], aliases=['pos']),
        pv_range=dict(type='str', required=False, choices=['maximum', 'minimum'], aliases=['pvrange', 'range']),
        max_pv=dict(type='int', required=False, aliases=['max_pvs_for_new_alloc']),
        copies=dict(type='int', required=False, choices=[1, 2, 3], aliases=['lpart_copies', 'lp_copies']),
        write_consistency=dict(type='str', required=False, choices=['active', 'passive', 'off']),
        sep_pvs=dict(type='str', required=False, choices=['yes', 'no', 'superstrict'],
                     aliases=['separate_pvs', 'lparts_on_separate_pvs', 'lps_on_separate_pvs']),
        relocate=dict(type='bool', required=False),
        label=dict(type='str', required=False),
        max_lp=dict(type='int', required=False, aliases=['max_lps', 'max_lparts', 'maxlp']),
        bb_relocate=dict(type='bool', required=False, aliases=['bad_block_relocation']),
        sched_policy=dict(type='str', required=False,
                          choices=['parallel', 'sequential', 'parallel_sequential', 'parallel_round_robin'],
                          aliases=['scheduling_policy', 'schedpolicy', 'policy']),
        verify_writes=dict(type='bool', required=False),
        alloc_map=dict(type='path', required=False, aliases=['allocation_map']),
        stripe_size=dict(type='str', required=False,
                         choices=['4K', '8K', '16K', '32K', '64K', '128K', '256K', '512K', '1M', '2M', '4M', '8M', '16M', '32M', '64M', '128M']),
        serialize_io=dict(type='bool', required=False),
        first_block_available=dict(type='bool', required=False),
        mp1=dict(type='str', required=False, aliases=['mirror_pool_1', 'first_copy_mirror_pool']),
        mp2=dict(type='str', required=False, aliases=['mirror_pool_2', 'second_copy_mirror_pool']),
        mp3=dict(type='str', required=False, aliases=['mirror_pool_3', 'third_copy_mirror_pool']),
        group=dict(type='str', required=False),
        permissions=dict(type='str', required=False),
        node=dict(type='str', required=False),
        encryption=dict(type='bool', required=False, aliases=['lv_encryption', 'enable_lv_encryption']),
        auth_method=dict(type='str', required=False, choices=['keyserv', 'pks']),
        method_details=dict(type='str', required=False),
        auth_method_name=dict(type='str', required=False)
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

    module._debug = True
    module.debug('Starting enfence.powerha_aix.lv module')

    # check if we can run clmgr
    result = check_powerha(result)
    if result['rc'] == 1:
        module.fail_json(**result)

    if module.params['unit'] is None or module.params['unit'] == '':
        module.params['unit'] = 'pp'

    if module.params['type'] is None or module.params['type'] == '':
        module.params['type'] = 'jfs2'

    if module.params['state'] is None or module.params['state'] == 'present':
        state, result['rc'], result['stdout'], result['stderr'], opts = get_lv(module)
        if state == 'present':
            result['msg'] = 'logical volume already exists'
            module.exit_json(**result)
        result['changed'] = True
        if module.check_mode:
            result['msg'] = 'logical volume will be created'
            module.exit_json(**result)
        result['rc'], result['stdout'], result['stderr'] = add_lv(module)
        if result['rc'] != 0:
            result['msg'] = 'creating logical volume failed. see stderr for any error messages'
            module.fail_json(**result)
        result['msg'] = 'logical volume created'
    elif module.params['state'] == 'absent':
        state, result['rc'], result['stdout'], result['stderr'], opts = get_lv(module)
        if state == 'absent':
            result['msg'] = 'logical volume does not exist'
            result['rc'] = 0
            module.exit_json(**result)
        result['changed'] = True
        if module.check_mode:
            result['msg'] = 'logical volume will be deleted'
            module.exit_json(**result)
        result['rc'], result['stdout'], result['stderr'] = delete_lv(module)
        if result['rc'] != 0:
            result['msg'] = 'deleting logical volume failed. see stderr for any error messages'
            module.fail_json(**result)
        result['msg'] = 'logical volume is deleted'
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
