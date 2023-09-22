#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2023, eNFence GmbH (info@power-devops.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: fc

short_description: manage file_collection resource in PowerHA cluster
version_added: "1.3.0"

description:
    - This module creates/deletes/changes file_collection resource in PowerHA cluster.

options:
    name:
        description: name of the file collection.
        required: true
        type: str
    state:
        description:
            - the desired state of the file collection - C(present), C(absent).
        required: false
        type: str
        choices: [ present, absent, synced ]
        default: present
    files:
        description:
          - list of files to be synchronized between cluster nodes.
        required: false
        type: list
        elements: str
    description:
        description: description of the file collection.
        required: false
        type: str
        aliases: [ desc, descr ]
    sync_with_cluster:
        description:
            - if I(true), the file collection will be automatically synchronized during cluster synchronization.
        required: false
        type: bool
    sync_when_changed:
        description:
            - if I(true), the file collection will be checked for changes automatically by the cluster.
            - if the cluster detects changes on the files in the collection, they will be automatically propagated to other nodes.
        required: false
        type: bool

author:
    - Andrey Klyachkin (@aklyachkin)
'''

EXAMPLES = r'''
# create file collection
- name: file collection profiles
  enfence.powerha_aix.fc:
    name: profiles
    sync_when_changed: true
    sync_with_cluster: true
    files:
      - /home/sapadm/.profile
      - /home/sapadm/.login
      - /home/sapadm/.sapenv.sh
      - /home/sapadm/.dbenv.sh
# manually synchronize collection
- name: synchronize profiles fc
  enfence.powerha_aix.fc:
    name: profiles
    state: synced
# delete file collection
- name: delete file collection profiles
  enfence.powerha_aix.fc:
    name: profiles
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
    add_string, add_list, add_bool, check_powerha, parse_clmgrq_output, CLMGR)


def get_fc(module):
    mpopts = dict()
    cmd = "%s query file_collection %s" % (CLMGR, module.params['name'])
    module.debug('Starting command: %s' % cmd)
    rc, stdout, stderr = module.run_command(cmd)
    if rc != 0:
        return 'absent', rc, stdout, stderr, mpopts
    fcopts = parse_clmgrq_output(stdout)
    return 'present', rc, stdout, stderr, fcopts


def add_fc(module):
    cmd = "%s add file_collection %s" % (CLMGR, module.params['name'])
    opts = ""
    opts += add_list(module, 'files', 'files')
    opts += add_string(module, 'description', 'description')
    opts += add_bool(module, 'sync_with_cluster', 'sync_with_cluster')
    opts += add_bool(module, 'sync_when_changed', 'sync_when_changed')
    cmd = "%s %s" % (cmd, opts)
    module.debug('Starting command: %s' % cmd)
    return module.run_command(cmd)


def delete_fc(module):
    cmd = "%s delete file_collection %s" % (CLMGR, module.params['name'])
    module.debug('Starting command: %s' % cmd)
    return module.run_command(cmd)


def sync_fc(module):
    cmd = "%s sync file_collection %s" % (CLMGR, module.params['name'])
    module.debug('Starting command: %s' % cmd)
    return module.run_command(cmd)


def run_module():
    module_args = dict(
        name=dict(type='str', required=True),
        state=dict(type='str', required=False, choices=['present', 'absent', 'synced'], default='present'),
        files=dict(type='list', required=False, elements='str'),
        description=dict(type='str', required=False, aliases=['desc', 'descr']),
        sync_with_cluster=dict(type='bool', required=False),
        sync_when_changed=dict(type='bool', required=False)
    )

    result = dict(
        changed=False,
        msg='No changes',
        rc=0
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[
            ('state', 'present', ('files', )),
        ],
    )

    module.debug('Starting enfence.powerha_aix.fc module')
    # check if we can run clmgr
    result = check_powerha(result)
    if result['rc'] == 1:
        module.fail_json(**result)

    if module.params['state'] is None or module.params['state'] == 'present':
        state, result['rc'], result['stdout'], result['stderr'], opts = get_fc(module)
        if state == 'present':
            result['msg'] = 'file collection already exists'
            module.exit_json(**result)
        result['changed'] = True
        if module.check_mode:
            result['msg'] = 'file collection will be created'
            module.exit_json(**result)
        result['rc'], result['stdout'], result['stderr'] = add_fc(module)
        if result['rc'] != 0:
            result['msg'] = 'creating file collection failed. see stderr for any error messages'
            module.fail_json(**result)
        result['msg'] = 'mirror pool created'
    elif module.params['state'] == 'synced':
        state, result['rc'], result['stdout'], result['stderr'], opts = get_fc(module)
        if state == 'absent' and not module.check_mode:
            result['msg'] = 'file collection does not exist'
            module.exit_json(**result)
        result['changed'] = True
        if module.check_mode:
            if state == 'absent':
                result['msg'] = 'file collection will be deleted (assuming it was created before)'
            else:
                result['msg'] = 'file collection will be deleted'
            module.exit_json(**result)
        result['rc'], result['stdout'], result['stderr'] = sync_fc(module)
        if result['rc'] != 0:
            result['msg'] = 'synchronizing file collection failed. see stderr for any error messages'
            module.fail_json(**result)
        result['msg'] = 'file collection is synchronized'
    elif module.params['state'] == 'absent':
        state, result['rc'], result['stdout'], result['stderr'], opts = get_fc(module)
        if state == 'absent':
            result['msg'] = 'file collection does not exist'
            result['rc'] = 0
            module.exit_json(**result)
        result['changed'] = True
        if module.check_mode:
            result['msg'] = 'file collection will be deleted'
            module.exit_json(**result)
        result['rc'], result['stdout'], result['stderr'] = delete_fc(module)
        if result['rc'] != 0:
            result['msg'] = 'deleting file collection failed. see stderr for any error messages'
            module.fail_json(**result)
        result['msg'] = 'file collection is deleted'
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
