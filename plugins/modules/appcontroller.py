#!/usr/bin/python

# Copyright (c) 2023, eNFence GmbH (info@power-devops.com)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: appcontroller

short_description: manage application_controller resource in PowerHA cluster
version_added: "1.0.0"

description: This module creates or deletes application_controller resource in PowerHA cluster. 

options:
    name:
        description: name of the application controller.
        required: true
        type: str
    start:
        description: path to the start script. the attribute is required if application controller is created.
        required: false
        type: path
    stop:
        description: path to the stop script. the attribute is required if application controller is created.
        required: false
        type: path
    mode:
        description: mode of starting scripts. background or foreground. by default background.
        requried: false
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
# create a new application controller
- name: create a new application controller
  powerdevops.powerha_aix.appcontroller:
    name: ac_oracle
    start: /usr/local/bin/start_ora
    stop: /usr/local/bin/stop_ora
    mode: foreground
    state: present
# delete an existing application controller
- name: delete an existing application controller
  powerdevops.powerha_aix.appcontroller:
    name: ac_oracle
    state: absent
'''

RETURN = r'''
# possible return values
'''

import os
from ansible.module_utils.basic import AnsibleModule, is_executable

CLMGR = '/usr/es/sbin/cluster/utilities/clmgr'


def get_ac(module):
    cmd = "%s query application_controller %s" % (CLMGR, module.params['name'])
    module.debug('Starting command: %s' % cmd)
    rc, stdout, stderr = module.run_command(cmd)
    if rc != 0:
        return 'absent', rc, stdout, stderr
    return 'present', rc, stdout, stderr


def add_ac(module):
    cmd = "%s add application_controller %s" % (CLMGR, module.params['name'])
    opts = ""
    if 'start' in module.params and module.params['start'] != '':
        opts += " startscript=%s" % module.params['start']
    if 'stop' in module.params and module.params['stop'] != '':
        opts += " stopscript=%s" % module.params['stop']
    if 'mode' in module.params and module.params['mode'] != '':
        opts += " startup_mode=%s" % module.params['mode']
    cmd = "%s %s" % (cmd, opts)
    module.debug('Starting command: %s' % cmd)
    return module.run_command(cmd)


def delete_ac(module):
    cmd = "%s delete application_controller %s" % (CLMGR, module.params['name'])
    module.debug('Starting command: %s' % cmd)
    return module.run_command(cmd)


def run_module():
    module_args = dict(
        name=dict(type='str', required=True),
        state=dict(type='str', required=False, choices=['present', 'absent'], default='present'),
        start=dict(type='path', required=False, aliases=['startscript', 'start_script']),
        stop=dict(type='path', required=False, aliases=['stopscript', 'stop_script']),
        mode=dict(type='str', required=False, choices=['foreground', 'background'], default='background', aliases=['startup_mode', 'startupmode'])
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
        result['message'] = 'IBM PowerHA is not installed or clmgr is not found'
        module.fail_json(msg=result['message'], rc=1)

    if not is_executable(CLMGR):
        result['message'] = 'clmgr can not be executed by the current user'
        module.fail_json(msg=result['message'], rc=1)

    if module.params['state'] is None or module.params['state'] == 'present':
        state, result['rc'], result['stdout'], result['stderr'] = get_ac(module)
        if state == 'present':
            result['message'] = 'application controller is already defined'
            module.exit_json(**result)
        result['changed'] = True
        if module.check_mode:
            result['message'] = 'application controller will be defined'
            module.exit_json(**result)
        result['rc'], result['stdout'], result['stderr'] = add_ac(module)
        if result['rc'] != 0:
            result['message'] = 'adding application controller to the cluster failed. see stderr for any error messages'
            module.fail_json(msg=result['message'], rc=result['rc'], result=result)
        result['message'] = 'application controller added to the cluster'
    elif module.params['state'] == 'absent':
        state, result['rc'], result['stdout'], result['stderr'] = get_ac(module)
        if state == 'absent':
            result['message'] = 'application controller is not defined'
            result['rc'] = 0
            module.exit_json(**result)
        result['changed'] = True
        if module.check_mode:
            result['message'] = 'application controller will be deleted'
            module.exit_json(**result)
        result['rc'], result['stdout'], result['stderr'] = delete_ac(module)
        if result['rc'] != 0:
            result['message'] = 'deleting application controller failed. see stderr for any error messages'
            module.fail_json(msg=result['message'], rc=result['rc'], result=result)
        result['message'] = 'application controller is deleted'
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()

