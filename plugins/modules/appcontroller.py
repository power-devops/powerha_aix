#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2023, eNFence GmbH (info@power-devops.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

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
        aliases: [ startscript, start_script ]
    stop:
        description: path to the stop script. the attribute is required if application controller is created.
        required: false
        type: path
        aliases: [ stopscript, stop_script ]
    mode:
        description: mode of starting scripts. background or foreground. by default background.
        required: false
        type: str
        choices: [ foreground, background ]
        default: background
        aliases: [ startupmode, startup_mode ]
    monitors:
        description:
            - application monitors.
            - added in 1.1.3
        required: false
        type: list
        elements: str
        aliases: [ monitor ]
    cpumon:
        description:
            - enable or disable CPU monitoring. By default is disabled.
            - added in 1.1.3
        required: false
        type: bool
        aliases: [ 'cpu_usage_monitor', 'usage_monitor', 'cpu_monitor' ]
    cpuproc:
        description:
            - full path of the application binary to monitor.
            - added in 1.1.3
        required: false
        type: path
        aliases: [ 'cpu_usage_process', 'process_to_monitor_cpu_usage', 'cpu_usage_monitor_process', 'usage_process', 'cpu_process' ]
    cpuintvl:
        description:
            - interval in minutes to monitor cpu usage by the process. valid values are 1 to 120.
            - added in 1.1.3
        required: false
        type: int
        aliases: [ 'cpu_usage_interval', 'cpu_usage_monitor_interval', 'usage_interval', 'cpu_interval' ]
    state:
        description: the desired state of the resource - present or absent. If the resource is already defined, it will not be changed.
        default: present
        required: false
        type: str
        choices: [ present, absent ]

author:
    - Andrey Klyachkin (@aklyachkin)
'''

EXAMPLES = r'''
# create a new application controller
- name: create a new application controller
  enfence.powerha_aix.appcontroller:
    name: ac_oracle
    start: /usr/local/bin/start_ora
    stop: /usr/local/bin/stop_ora
    mode: foreground
    state: present
# delete an existing application controller
- name: delete an existing application controller
  enfence.powerha_aix.appcontroller:
    name: ac_oracle
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
from ansible_collections.enfence.powerha_aix.plugins.module_utils.helpers import add_bool, add_list, add_string, check_powerha, parse_clmgrq_output, CLMGR


def get_ac(module):
    acopts = dict()
    cmd = "%s query application_controller %s" % (CLMGR, module.params['name'])
    module.debug('Starting command: %s' % cmd)
    rc, stdout, stderr = module.run_command(cmd)
    if rc != 0:
        return 'absent', rc, stdout, stderr, acopts
    acopts = parse_clmgrq_output(stdout)
    return 'present', rc, stdout, stderr, acopts


def add_ac(module):
    cmd = "%s add application_controller %s" % (CLMGR, module.params['name'])
    opts = ""
    opts += add_string(module, 'start', 'startscript')
    opts += add_string(module, 'stop', 'stopscript')
    opts += add_string(module, 'mode', 'startup_mode')
    opts += add_list(module, 'monitors', 'monitors')
    opts += add_bool(module, 'cpumon', 'cpu_usage_monitor')
    opts += add_string(module, 'cpuproc', 'process_to_monitor_cpu_usage')
    opts += add_string(module, 'cpuintvl', 'cpu_usage_monitor_interval')
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
        mode=dict(type='str', required=False, choices=['foreground', 'background'], default='background', aliases=['startup_mode', 'startupmode']),
        monitors=dict(type='list', required=False, elements='str', aliases=['monitor']),
        cpumon=dict(type='bool', required=False, aliases=['cpu_usage_monitor', 'usage_monitor', 'cpu_monitor']),
        cpuproc=dict(type='path', required=False,
                     aliases=['cpu_usage_process', 'process_to_monitor_cpu_usage', 'cpu_usage_monitor_process', 'usage_process', 'cpu_process']),
        cpuintvl=dict(type='int', required=False,
                      aliases=['cpu_usage_interval', 'cpu_usage_monitor_interval', 'usage_interval', 'cpu_interval'])
    )

    result = dict(
        changed=False,
        msg='No changes',
        rc=0
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        mutually_exclusive=[('monitors', 'cpumon'), ('monitors', 'cpuproc'), ('monitors', 'cpuintvl')],
        required_together=[('cpumon', 'cpuproc', 'cpuintvl')]
    )

    # check if we can run clmgr
    result = check_powerha(result)
    if result['rc'] == 1:
        module.fail_json(**result)

    if module.params['cpuintvl'] is not None:
        if module.params['cpuintvl'] < 1 or module.params['cpuintvl'] > 120:
            result['msg'] = 'CPU usage monitoring interval can be between 1 and 120 minutes'
            result['rc'] = 1
            module.fail_json(**result)

    if module.params['state'] is None or module.params['state'] == 'present':
        state, result['rc'], result['stdout'], result['stderr'], opts = get_ac(module)
        if state == 'present':
            result['msg'] = 'application controller is already defined'
            module.exit_json(**result)
        result['changed'] = True
        if module.check_mode:
            result['msg'] = 'application controller will be defined'
            module.exit_json(**result)
        result['rc'], result['stdout'], result['stderr'] = add_ac(module)
        if result['rc'] != 0:
            result['msg'] = 'adding application controller to the cluster failed. see stderr for any error messages'
            module.fail_json(**result)
        result['message'] = 'application controller added to the cluster'
    elif module.params['state'] == 'absent':
        state, result['rc'], result['stdout'], result['stderr'], opts = get_ac(module)
        if state == 'absent':
            result['msg'] = 'application controller is not defined'
            result['rc'] = 0
            module.exit_json(**result)
        result['changed'] = True
        if module.check_mode:
            result['msg'] = 'application controller will be deleted'
            module.exit_json(**result)
        result['rc'], result['stdout'], result['stderr'] = delete_ac(module)
        if result['rc'] != 0:
            result['msg'] = 'deleting application controller failed. see stderr for any error messages'
            module.fail_json(**result)
        result['msg'] = 'application controller is deleted'
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
