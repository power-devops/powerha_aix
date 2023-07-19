#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2023, eNFence GmbH (info@power-devops.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: fs

short_description: manage file_system resource in PowerHA cluster
version_added: "1.2.0"

description:
    - This module creates/deletes/changes file_system resource in PowerHA cluster.
    - This module was added in 1.2.0.

options:
    name:
        description: name (mount point) of the file system.
        required: true
        type: str
        aliases: [ mount, mountpoint, mount_point ]
    state:
        description: the desired state of the file system - C(present), C(absent).
        required: false
        type: str
        choices: [ present, absent ]
        default: present
    vg:
        description:
            - volume group where the file system must be created.
            - required if I(lv) is not specified and state is C(present).
        required: false
        type: str
        aliases: [ volume_group, volumegroup ]
    lv:
        description:
            - logical volume where the file system must be created.
            - required if I(vg) is not specified and state is C(present).
        required: false
        type: str
        aliases: [ lvol, logical_volume ]
    type:
        description:
            - file system type.
            - C(jfs2) and C(enhanced) are aliases.
            - C(jfs) and (standard) are aliases.
            - C(compressed) is C(jfs) filesytem with compression enabled. I(fragment_size) must be 2048 or less.
            - C(large) is large file enabled C(jfs) filesystem. I(fragment_size) must be 4096.
        required: false
        type: str
        choices: [ jfs2, enhanced, jfs, standard, compressed, large ]
        default: jfs2
    size:
        description:
          - size of the future file system.
          - required if the state is C(present) and I(lv) is not specified.
        required: false
        type: int
        aliases: [ units ]
    unit:
        description:
            - which unit is used to specify I(size) of the filesystem.
            - required if I(size) is specified.
        required: false
        type: str
        choices: [ mb, gb, block ]
        aliases: [ size_per_unit ]
    perm:
        description: permissions on the file system.
        required: false
        type: str
        choices: [ rw, ro ]
        aliases: [ perms, permissions, permission ]
    options:
        description: file system options.
        required: false
        type: str
        choices: [ "nodev", "nosuid", "nodev,nosuid" ]
    disk_accounting:
        description: enables accounting on the file system.
        required: false
        type: bool
    block_size:
        description: jfs2 block size in bytes.
        required: false
        type: int
        choices: [ 512, 1024, 2048, 4096 ]
        default: 4096
    fragment_size:
        description:
            - jfs fragment size in bytes.
            - by default jfs uses I(4096) bytes fragments.
            - the module sets C(fragment_size) to I(4096) by default if you specify C(type): I(large) and no C(fragment_size).
            - the module sets C(fragment_size) to I(2048) by default if you specify C(type): I(compressed) and no C(fragment_size).
        required: false
        type: int
        choices: [ 512, 1024, 2048, 4096 ]
    bytes_per_inode:
        description: number of bytes per i-node for jfs filesytem.
        required: false
        type: int
        choices: [ 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072 ]
    alloc_group_size:
        description: allocation group size in megabytes for jfs filesytem.
        required: false
        type: int
        choices: [ 8, 16, 32, 64 ]
    log:
        description:
            - logical volume for jfs/jfs2 log.
            - use C(INLINE) if you want to use jfs2 inline logs.
        required: false
        type: str
        aliases: [ lv_for_log ]
        default: INLINE
    ea_format:
        description: specifies the format is used to store jfs2 extended attributes.
        required: false
        type: str
        choices: [ v1, v2 ]
        aliases: [ eaformat, ext_attr_format ]
    quota:
        description: type of quotas that can be enabled on jfs2 filesytem.
        required: false
        type: str
        choices: [ "no", all, user, group ]
        aliases: [ enable_quota_mgmt ]
    efs:
        description: enable Encyrpted File System (EFS) on jfs2.
        required: false
        type: bool

author:
    - Andrey Klyachkin (@aklyachkin)
'''

EXAMPLES = r'''
# create JFS2 filesytem on existing logical volume with INLINE jfs2log.
- name: create /ora filesystem
  enfence.powerha_aix.fs:
    name: /ora
    lv: lvora
# delete an existing file system.
- name: delete /ora file system
  enfence.powerha_aix.fs:
    name: /ora
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
import math


def calc_log_size(fssize, unit):
    # log size must be in MB. convert fs size into MB
    if unit == 'gb':
        fssize = fssize * 1024
    elif unit == 'block':
        fssize = int(fssize * 512 / 1048576)
    # jfs2 minimum size is 16MB
    if fssize < 16:
        return 0
    # standard log size is 0.4 of fs size
    logsize = math.ceil(fssize / 100 * 0.4)
    # max log size is 2047 MB
    if logsize > 2047:
        logsize = 2047
    # log size can't be > 10% of fs size
    if logsize > (fssize / 10):
        logsize = int(fssize / 10)
    return logsize


def get_lv(module):
    lvopts = dict()
    if module.params['lv'] is None or module.params['lv'] == '':
        return lvopts
    cmd = "%s query logical_volume %s" % (CLMGR, module.params['lv'])
    module.debug('Starting command: %s' % cmd)
    rc, stdout, stderr = module.run_command(cmd)
    if rc != 0 or ("ERROR:" in stderr):
        return lvopts
    lvopts = parse_clmgrq_output(stdout)
    return lvopts


def get_fs(module):
    fsopts = dict()
    cmd = "%s query file_system %s" % (CLMGR, module.params['name'])
    module.debug('Starting command: %s' % cmd)
    rc, stdout, stderr = module.run_command(cmd)
    if rc != 0:
        return 'absent', rc, stdout, stderr, fsopts
    fsopts = parse_clmgrq_output(stdout)
    return 'present', rc, stdout, stderr, fsopts


def add_fs(module):
    logsize = 0
    if module.params['log'].upper() == 'INLINE':
        if module.params['size'] is not None:
            logsize = calc_log_size(module.params['size'], module.params['unit'])
        else:
            size = int(get_lv(module)['SIZE'])
            logsize = calc_log_size(size, 'mb')
    if module.params['unit'] == 'mb':
        module.params['unit'] = 'megabytes'
    elif module.params['unit'] == 'gb':
        module.params['unit'] = 'gigabytes'
    else:
        module.params['unit'] = '512bytes'
    cmd = "%s add file_system %s" % (CLMGR, module.params['name'])
    opts = ""
    opts += add_string(module, 'vg', 'volume_group')
    opts += add_string(module, 'lv', 'logical_volume')
    opts += add_string(module, 'type', 'type')
    opts += add_string(module, 'unit', 'size_per_unit')
    opts += add_string(module, 'perm', 'permissions')
    opts += add_string(module, 'options', 'options')
    opts += add_string(module, 'log', 'lv_for_log')
    opts += add_string(module, 'ea_format', 'ext_attr_format')
    opts += add_string(module, 'quota', 'quota')
    if logsize != 0:
        opts += ' %s=%d' % ('inline_log_size', logsize)
    opts += add_int(module, 'size', 'units')
    opts += add_int(module, 'block_size', 'block_size')
    opts += add_int(module, 'fragment_size', 'fragment_size')
    opts += add_int(module, 'bytes_per_inode', 'bytes_per_inode')
    opts += add_int(module, 'alloc_group_size', 'alloc_group_size')
    opts += add_bool(module, 'disk_accounting', 'disk_accounting')
    opts += add_bool(module, 'efs', 'efs')
    cmd = "%s %s" % (cmd, opts)
    module.debug('Starting command: %s' % cmd)
    return module.run_command(cmd)


def delete_fs(module):
    cmd = "%s delete file_system %s" % (CLMGR, module.params['name'])
    module.debug('Starting command: %s' % cmd)
    return module.run_command(cmd)


def run_module():
    module_args = dict(
        name=dict(type='str', required=True, aliases=['mount', 'mount_point', 'mountpoint']),
        state=dict(type='str', required=False, choices=['present', 'absent'], default='present'),
        vg=dict(type='str', required=False, aliases=['volume_group', 'volumegroup']),
        lv=dict(type='str', required=False, aliases=['lvol', 'logical_volume']),
        type=dict(type='str', required=False, choices=['jfs2', 'enhanced', 'jfs', 'standard', 'compressed', 'large'], default='jfs2'),
        size=dict(type='int', required=False, aliases=['units']),
        unit=dict(type='str', required=False, choices=['mb', 'gb', 'block'], aliases=['size_per_unit']),
        perm=dict(type='str', required=False, choices=['rw', 'ro'], aliases=['perms', 'permissions', 'permission']),
        options=dict(type='str', required=False, choices=['nodev', 'nosuid', 'nodev,nosuid']),
        disk_accounting=dict(type='bool', required=False),
        block_size=dict(type='int', required=False, choices=[512, 1024, 2048, 4096], default=4096),
        fragment_size=dict(type='int', required=False, choices=[512, 1024, 2048, 4096]),
        bytes_per_inode=dict(type='int', required=False, choices=[512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072]),
        alloc_group_size=dict(type='int', required=False, choices=[8, 16, 32, 64]),
        log=dict(type='str', required=False, aliases=['lv_for_log'], default='INLINE'),
        ea_format=dict(type='str', required=False, choices=['v1', 'v2'], aliases=['eaformat', 'ext_attr_format']),
        quota=dict(type='str', required=False, choices=['no', 'all', 'user', 'group'], aliases=['enable_quota_mgmt']),
        efs=dict(type='bool', required=False)
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
    module.debug('Starting enfence.powerha_aix.fs module')
    # check if we can run clmgr
    result = check_powerha(result)
    if result['rc'] == 1:
        module.fail_json(**result)

    # parameter checking
    if module.params['type'] is None or module.params['type'] == '':
        module.params['type'] = 'enhanced'

    if module.params['type'] == 'jfs2':
        module.params['type'] = 'enhanced'
    elif module.params['type'] == 'jfs':
        module.params['type'] = 'standard'

    if module.params['vg'] is not None and module.params['lv'] is not None:
        result['msg'] = 'vg and lv cannot be specified at the same time. If you want to create file system on existing lv, omit vg name.'
        module.fail_json(**result)

    if module.params['vg'] is not None and module.params['size'] is None:
        result['msg'] = 'size must be specified if a new logical volume is created for the file system.'
        module.fail_json(**result)

    if module.params['type'] == 'enhanced':
        for opt in ('fragment_size', 'bytes_per_inode', 'alloc_group_size'):
            if module.params[opt] is not None:
                result['msg'] = '%s cannot be used with jfs2 filesystems' % opt
                module.fail_json(**result)
        if module.params['block_size'] is None:
            module.params['block_size'] = 4096
        if module.params['log'] is None:
            module.params['log'] = 'INLINE'

    if module.params['type'] == 'standard':
        for opt in ('block_size', 'ea_format', 'quota', 'efs'):
            if module.params[opt] is not None:
                result['msg'] = '%s cannot be used with jfs filesystems' % opt
                module.fail_json(**result)

    if module.params['type'] == 'compressed':
        if module.params['fragment_size'] is None:
            module.params['fragment_size'] = 2048
        elif module.params['fragment_size'] > 2048:
            result['msg'] = 'fragment_size must be 2048 or less for compressed jfs filesystem'
            module.fail_json(**result)

    if module.params['type'] == 'large':
        if module.params['fragment_size'] is None:
            module.params['fragment_size'] = 4096
        elif module.params['fragment_size'] != 4096:
            result['msg'] = 'fragment_size must be 4096 for large file enabled jfs filesystem'
            module.fail_json(**result)

    if module.params['state'] is None or module.params['state'] == 'present':
        state, result['rc'], result['stdout'], result['stderr'], opts = get_fs(module)
        if state == 'present':
            result['msg'] = 'file system already exists'
            module.exit_json(**result)
        result['changed'] = True
        if module.check_mode:
            result['msg'] = 'file system will be created'
            module.exit_json(**result)
        result['rc'], result['stdout'], result['stderr'] = add_fs(module)
        if result['rc'] != 0:
            result['msg'] = 'creating file system failed. see stderr for any error messages'
            module.fail_json(**result)
        result['msg'] = 'file system created'
    elif module.params['state'] == 'absent':
        state, result['rc'], result['stdout'], result['stderr'], opts = get_fs(module)
        if state == 'absent':
            result['msg'] = 'file system does not exist'
            result['rc'] = 0
            module.exit_json(**result)
        result['changed'] = True
        if module.check_mode:
            result['msg'] = 'file system will be deleted'
            module.exit_json(**result)
        result['rc'], result['stdout'], result['stderr'] = delete_fs(module)
        if result['rc'] != 0:
            result['msg'] = 'deleting file system failed. see stderr for any error messages'
            module.fail_json(**result)
        result['msg'] = 'file system is deleted'
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
