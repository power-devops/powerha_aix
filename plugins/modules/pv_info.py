#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2023, eNFence GmbH (info@power-devops.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: pv_info

short_description: find a suitable physical volume.
version_added: "1.2.0"

description:
    - this module searches for physical volumes according to the supplied attributes.
    - if the volumes are found, a dictionary with their names is returned.
    - otherwise an empty dictionary is returned.
    - physical volumes already assigned to volume groups or locked by LVM are not returned.

options:
    name:
        description:
            - name to find a suitable physical volumes.
            - it can be a regular expresion.
        required: false
        type: str
    pvid:
        description:
            - PVID of the physical volume to return.
        required: false
        type: str
    uuid:
        description:
            - UUID of the physical volumes to return.
        required: false
        type: str
    ldev:
        description:
            - LDEV or LUN ID of the physical volumes to return.
            - it can be a regular expresion.
        required: false
        type: str

author:
    - Andrey Klyachkin (@aklyachkin)
'''

EXAMPLES = r'''
# get a list of disks with LDEV 60050768019081D398000000000010D4
- name: get hdisk for LDEV 60050768019081D398000000000010D4
  enfence.powerha_aix.pv_info:
    ldev: 60050768019081D398000000000010D4
  register: hdisk
# get a list of free disks, not assigned to volume groups
- name: get a list of free disks
  enfence.powerha_aix.pv_info:
    name: "hdisk*"
  register: free_hdisk
# print the found hdisks
- name: print hdisk
  ansible.builtin.debug:
    var: free_hdisk.pv
'''

RETURN = r'''
# possible return values
pv:
    description: a list of found physical volumes
    type: list
    returned: always
changed:
    description: always False
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
import re


def get_lspv_output(stdout):
    pvs = list()
    for line in stdout.splitlines():
        s = line.split()
        pv = dict(name=s[0], pvid='', vg='', state='', udid='', uuid='')
        if s[1] != 'none':
            pv['pvid'] = s[1]
        if s[2] != 'None':
            pv['vg'] = s[2]
        if len(s) == 6:
            pv['state'] = s[3]
            pv['udid'] = s[4]
            pv['uuid'] = s[5]
        else:
            pv['udid'] = s[3]
            pv['uuid'] = s[4]
        pvs.append(pv)
    return pvs


def select_by_pvid(pvs, pvid):
    ret_pvs = list(filter(lambda p: p['pvid'] == pvid and p['state'] == '' and p['vg'] == '', pvs))
    return ret_pvs


def select_by_uuid(pvs, uuid):
    ret_pvs = list(filter(lambda p: p['uuid'] == uuid and p['state'] == '' and p['vg'] == '', pvs))
    return ret_pvs


def select_by_udid(pvs, udid):
    ret_pvs = list(filter(lambda p: re.search(udid, p['udid']) is not None and p['state'] == '' and p['vg'] == '', pvs))
    return ret_pvs


def select_by_name(pvs, name):
    ret_pvs = list(filter(lambda p: re.search(name, p['name']) is not None and p['state'] == '' and p['vg'] == '', pvs))
    return ret_pvs


def run_module():
    module_args = dict(
        name=dict(type='str', required=False),
        pvid=dict(type='str', required=False),
        uuid=dict(type='str', required=False),
        ldev=dict(type='str', required=False)
    )

    result = dict(
        pv=list(),
        changed=False,
        msg='No changes',
        rc=0,
        stdout='',
        stderr=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        mutually_exclusive=[('name', 'pvid', 'uuid', 'ldev')],
        required_one_of=[('name', 'pvid', 'uuid', 'ldev')]
    )

    if module.check_mode:
        result['msg'] = 'will search for physical volume'
        module.exit_json(**result)

    module.debug('Starting lspv -u')
    result['rc'], result['stdout'], result['stderr'] = module.run_command('lspv -u')
    if result['rc'] != 0:
        result['msg'] = 'error calling lspv. See stderr for error messages'
        module.exit_json(**result)

    pvs = get_lspv_output(result['stdout'])
    if len(pvs) == 0:
        result['msg'] = 'no disks found in lspv output'
        module.exit_json(**result)

    if module.params['name'] is not None and module.params['name'] != '':
        pvs = select_by_name(pvs, module.params['name'])
    if module.params['pvid'] is not None and module.params['pvid'] != '':
        pvs = select_by_pvid(pvs, module.params['pvid'])
    if module.params['uuid'] is not None and module.params['uuid'] != '':
        pvs = select_by_uuid(pvs, module.params['uuid'])
    if module.params['ldev'] is not None and module.params['ldev'] != '':
        pvs = select_by_udid(pvs, module.params['ldev'])

    if len(pvs) == 0:
        result['msg'] = 'no disks found according to the specified criteria'
        module.exit_json(**result)

    result['pv'] = list(map(lambda p: p['name'], pvs))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
