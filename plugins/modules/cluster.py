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
    clusterip:
        description: cluster ip for heartbeating.
        required: false
        type: str
        aliases: [ cluster_ip ]
    fix:
        description: automatically fix errors during synchronization
        required: false
        type: bool
    fc_sync_interval:
        description: .
        required: false
        type: int
    rg_settling_time:
        description: .
        required: false
        type: int
    max_event_time:
        description: .
        required: false
        type: int
    max_rg_processing_time:
        description: .
        required: false
        type: int
    daily_verification:
        description: .
        required: false
        type: bool
    verification_node:
        description: .
        required: false
        type: str
    verification_debugging:
        description: .
        required: false
        type: bool
    heartbeat_frequency:
        description: .
        required: false
        type: str
    grace_period:
        description: .
        required: false
        type: str
    site_policy_failure_action:
        description: .
        required: false
        type: str
        choices: [ fallover, notify ]
    site_policy_notify_method:
        description: .
        required: false
        type: path
    site_heartbeat_cycle:
        description: .
        required: false
        type: str
    site_grace_period:
        description: .
        required: false
        type: str
    temp_hostname:
        description: .
        required: false
        type: str
        choices: [ allow, disallow ]
    lpm_policy:
        description: .
        required: false
        type: str
        choices: [ manage, unmanage ]
    heartbeat_frequency_during_lpm:
        description: .
        required: false
        type: int
    network_failure_detection_time:
        description: .
        required: false
        type: int
    caa_auto_start_dr:
        description: .
        required: false
        type: bool
    caa_repos_mode:
        description: .
        required: false
        type: str
        choices: [ assert, event ]
    caa_config_timeout:
        description: .
        required: false
        type: int
    lvm_preferred_read:
        description: .
        required: false
        type: str
        choices: [ roundrobin, favorcopy, siteaffinity ]
    crit_daemon_restart_grace_period:
        description: .
        required: false
        type: int
    skip_event_processing_manage_node:
        description: .
        required: false
        type: bool
    caa_pvm_watchdog_timer:
        description: .
        required: false
        type: str
        choices: [disable, dump_restart, hard_reset, hard_power_off ]
    when:
        description:
            - Taking the cluster online or offline, should be it done only I(now), at I(restart) or I(both) - now and at restart.
            - Can be used only if C(state) I(started) or I(stopped).
        required: false
        type: str
        choices: [ now, restart, both ]
    manage:
        description:
            - What to do with resource groups if the cluser is going online or offline.
            - Can be used only if C(state) I(started) or I(stopped).
            - If C(state) is I(started) the following values are possible - I(auto), I(manual), I(delayed).
            - If C(state) is I(stopped) the following values are possible - I(offline), I(move), I(unmanage).
        required: false
        type: str
        choices: [ auto, manual, delayed, offline, move, unmanage ]
    broadcast:
        description:
            - Broadcast information about changing cluster state to all logged in users.
            - Can be used only if C(state) I(started) or I(stopped).
        required: false
        type: bool
    timeout:
        description:
            - Number of seconds to wait till the operation completes.
            - Can be used only if C(state) I(started) or I(stopped).
        required: false
        type: int
    caa:
        description:
            - Should CAA be started prior to the cluster start or stopped after cluster stop.
            - Can be used only if C(state) I(started) or I(stopped).
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
- name: bring cluster apps in unmanaged state
  enfence.powerha_aix.cluster:
    name: cluster1
    state: stopped
    manage: unmanage
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
    add_list, add_string, add_int, add_bool, check_powerha, parse_clmgrq_output, CLMGR)


def is_caa_started(module):
    rc, stdout, stderr = module.run_command("lscluster -i")
    if rc == 0:
        return True
    return False


def start_caa(module):
    rc, stdout, stderr = module.run_command("/usr/sbin/clctrl -start -a")


def get_cluster_state(module):
    clusteropts = dict()
    cmd = "%s query cluster %s" % (CLMGR, module.params['name'])
    module.debug('Starting command: %s' % cmd)
    rc, stdout, stderr = module.run_command(cmd)
    if rc != 0:
        return 'absent', rc, stdout, stderr, clusteropts
    # check for other states, like started or stopped
    state = 'present'
    clusteropts = parse_clmgrq_output(stdout)
    if 'STATE' in clusteropts and clusteropts['STATE'] != "":
        state = clusteropts['STATE'].lower()
    return state, rc, stdout, stderr, clusteropts


def create_cluster(module):
    opts = module.params['name']
    opts += add_list(module, 'nodes', 'nodes')
    opts += add_list(module, 'repos', 'repositories')
    opts += add_string(module, 'type', 'type')
    opts += add_string(module, 'heartbeat', 'heartbeat_type')
    opts += add_string(module, 'clusterip', 'cluster_ip')
    opts += add_string(module, 'verification_node', 'verification_node')
    opts += add_string(module, 'heartbeat_frequency', 'heartbeat_frequency')
    opts += add_string(module, 'grace_period', 'grace_period')
    opts += add_string(module, 'site_policy_failure_action', 'site_policy_failure_action')
    opts += add_string(module, 'site_policy_notify_method', 'site_policy_notify_method')
    opts += add_string(module, 'site_heartbeat_cycle', 'site_heartbeat_cycle')
    opts += add_string(module, 'site_grace_period', 'site_grace_period')
    opts += add_string(module, 'temp_hostname', 'temp_hostname')
    opts += add_string(module, 'lpm_policy', 'lpm_policy')
    opts += add_string(module, 'caa_repos_mode', 'caa_repos_mode')
    opts += add_string(module, 'lvm_preferred_read', 'lvm_preferred_read')
    opts += add_string(module, 'caa_pvm_watchdog_timer', 'caa_pvm_watchdog_timer')
    opts += add_int(module, 'fc_sync_interval', 'fc_sync_interval')
    opts += add_int(module, 'rg_settling_time', 'rg_settling_time')
    opts += add_int(module, 'max_event_time', 'max_event_time')
    opts += add_int(module, 'max_rg_processing_time', 'max_rg_processing_time')
    opts += add_int(module, 'heartbeat_frequency_during_lpm', 'heartbeat_frequency_during_lpm')
    opts += add_int(module, 'network_failure_detection_time', 'network_failure_detection_time')
    opts += add_int(module, 'caa_config_timeout', 'caa_config_timeout')
    opts += add_int(module, 'crit_daemon_restart_grace_period', 'crit_daemon_restart_grace_period')
    opts += add_bool(module, 'daily_verification', 'daily_verification')
    opts += add_bool(module, 'verification_debugging', 'verification_debugging')
    opts += add_bool(module, 'caa_auto_start_dr', 'caa_auto_start_dr')
    opts += add_bool(module, 'skip_event_processing_manage_node', 'skip_event_processing_manage_node')
    cmd = "%s add cluster %s" % (CLMGR, opts)
    module.debug('Starting command: %s' % cmd)
    return module.run_command(cmd)


def delete_cluster(module):
    cmd = "%s delete cluster NODES=ALL" % CLMGR
    module.debug('Starting command: %s' % cmd)
    return module.run_command(cmd)


def start_cluster(module):
    opts = ''
    opts += add_string(module, 'when', 'when')
    opts += add_string(module, 'manage', 'manage')
    opts += add_bool(module, 'caa', 'start_caa')
    opts += add_bool(module, 'broadcast', 'broadcast')
    opts += add_bool(module, 'fix', 'fix')
    cmd = "%s online cluster clinfo=false force=true %s" % (CLMGR, opts)
    module.debug('Starting command: %s' % cmd)
    return module.run_command(cmd)


def stop_cluster(module):
    opts = ''
    opts += add_string(module, 'when', 'when')
    opts += add_string(module, 'manage', 'manage')
    opts += add_bool(module, 'caa', 'stop_caa')
    opts += add_bool(module, 'broadcast', 'broadcast')
    cmd = "%s offline cluster %s" % (CLMGR, opts)
    module.debug('Starting command: %s' % cmd)
    return module.run_command(cmd)


def sync_cluster(module):
    if not is_caa_started(module):
        # CAA is not started, we can't sync
        start_caa(module)
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
        heartbeat=dict(type='str', required=False, choices=['unicast', 'multicast'], default='unicast'),
        clusterip=dict(type='str', required=False, aliases=['cluster_ip']),
        fc_sync_interval=dict(type='int', required=False),
        rg_settling_time=dict(type='int', required=False),
        max_event_time=dict(type='int', required=False),
        max_rg_processing_time=dict(type='int', required=False),
        daily_verification=dict(type='bool', required=False),
        verification_node=dict(type='str', required=False),
        verification_debugging=dict(type='bool', required=False),
        heartbeat_frequency=dict(type='str', required=False),
        grace_period=dict(type='str', required=False),
        site_policy_failure_action=dict(type='str', choices=['fallover', 'notify'], required=False),
        site_policy_notify_method=dict(type='path', required=False),
        site_heartbeat_cycle=dict(type='str', required=False),
        site_grace_period=dict(type='str', required=False),
        temp_hostname=dict(type='str', choices=['allow', 'disallow'], required=False),
        lpm_policy=dict(type='str', choices=['manage', 'unmanage'], required=False),
        heartbeat_frequency_during_lpm=dict(type='int', required=False),
        network_failure_detection_time=dict(type='int', required=False),
        caa_auto_start_dr=dict(type='bool', required=False),
        caa_repos_mode=dict(type='str', choices=['assert', 'event'], required=False),
        caa_config_timeout=dict(type='int', required=False),
        lvm_preferred_read=dict(type='str', choices=['roundrobin', 'favorcopy', 'siteaffinity'], required=False),
        crit_daemon_restart_grace_period=dict(type='int', required=False),
        skip_event_processing_manage_node=dict(type='bool', required=False),
        caa_pvm_watchdog_timer=dict(type='str', choices=['disable', 'dump_restart', 'hard_reset', 'hard_power_off'], required=False),
        when=dict(type='str', choices=['now', 'restart', 'both'], required=False),
        manage=dict(type='str', choices=['offline', 'move', 'unmanage', 'auto', 'manual', 'delayed'], required=False),
        broadcast=dict(type='bool', required=False),
        timeout=dict(type='int', required=False),
        caa=dict(type='bool', required=False)
    )

    result = dict(
        changed=False,
        msg='No changes',
        rc=0
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_by={
            'clusterip': 'heartbeat'
        }
    )

    # check if we can run clmgr
    result = check_powerha(result)
    if result['rc'] == 1:
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
