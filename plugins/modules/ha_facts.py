#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2023, eNFence GmbH (info@power-devops.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: ha_facts

short_description: Gather facts about PowerHA
version_added: "1.3.0"

description:
- This module gathers information about the current PowerHA installation and configuration.
- File collection facts are not complete now. We are working on it.
- Please don't use 'all' in subset unless you know what you are doing. It can take a very long time on large clusters!

options:
    subset:
        description: subset of facts to return
        required: false
        type: list
        elements: str
        choices: [ all, appcontroller, cluster, fc, fs, lv, mp, network, rg, service_ip, vg ]
        default: all

author:
    - Andrey Klyachkin (@aklyachkin)
'''

EXAMPLES = r'''
# get complete information about PowerHA cluster. It takes long time!
- name: Get PowerHA information
  enfence.powerha_aix.ha_facts:
# get information about defined PowerHA networks
- name: Get PowerHA network information
  enfence.powerha_aix.ha_facts:
    subset: network
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
from ansible_collections.enfence.powerha_aix.plugins.module_utils.helpers import check_powerha
from ansible_collections.enfence.powerha_aix.plugins.module_utils.getters import (
    get_pha_version,
    get_pha_app_attrs,
    get_pha_apps,
    get_pha_cluster,
    get_pha_cluster_attrs,
    get_pha_filecoll_attrs,
    get_pha_filecolls,
    get_pha_filesystem_attrs,
    get_pha_filesystems,
    get_pha_lvol_attrs,
    get_pha_lvols,
    get_pha_mpool_attrs,
    get_pha_mpools,
    get_pha_network_attrs,
    get_pha_networks,
    get_pha_rg_attrs,
    get_pha_rgs,
    get_pha_sip_attrs,
    get_pha_sips,
    get_pha_vg_attrs,
    get_pha_vgs)


def get_facts(module, get_rsc_func, get_attr_func):
    info = []
    rsc, rc, stdout, stderr = get_rsc_func(module)
    for r in rsc:
        i, rc, stdout, stderr = get_attr_func(module, r)
        info = info + [{r: i}]
    return info, rc, stdout, stderr


def app_facts(module):
    return get_facts(module, get_pha_apps, get_pha_app_attrs)


def cluster_facts(module):
    return get_facts(module, get_pha_cluster, get_pha_cluster_attrs)


def fc_facts(module):
    return get_facts(module, get_pha_filecolls, get_pha_filecoll_attrs)


def fs_facts(module):
    return get_facts(module, get_pha_filesystems, get_pha_filesystem_attrs)


def lv_facts(module):
    return get_facts(module, get_pha_lvols, get_pha_lvol_attrs)


def mp_facts(module):
    return get_facts(module, get_pha_mpools, get_pha_mpool_attrs)


def network_facts(module):
    return get_facts(module, get_pha_networks, get_pha_network_attrs)


def rg_facts(module):
    return get_facts(module, get_pha_rgs, get_pha_rg_attrs)


def sip_facts(module):
    return get_facts(module, get_pha_sips, get_pha_sip_attrs)


def vg_facts(module):
    return get_facts(module, get_pha_vgs, get_pha_vg_attrs)


def run_module():
    module_args = dict(
        subset=dict(type='list', elements='str', required=False,
                    choices=['all', 'appcontroller', 'cluster', 'fc', 'fs', 'lv', 'mp', 'network', 'rg', 'service_ip', 'vg'],
                    default='all')
    )

    result = dict(
        changed=False,
        msg='No changes',
        rc=0,
        ansible_facts={}
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    ha_facts = {}

    # check if we can run clmgr
    result = check_powerha(result)
    if result['rc'] == 1:
        ha_facts['status'] = 'not installed'
        result['rc'] = 0
        result['ansible_facts'] = dict(powerha=ha_facts)
        module.exit_json(**result)

    ha_facts['version'], result['rc'], result['stdout'], result['stderr'] = get_pha_version(module)

    if 'appcontroller' in module.params['subset'] or 'all' in module.params['subset']:
        ha_facts['appcontrollers'], result['rc'], result['stdout'], result['stderr'] = app_facts(module)

    if 'cluster' in module.params['subset'] or 'all' in module.params['subset']:
        ha_facts['cluster'], result['rc'], result['stdout'], result['stderr'] = cluster_facts(module)

    if 'fc' in module.params['subset'] or 'all' in module.params['subset']:
        ha_facts['file_collections'], result['rc'], result['stdout'], result['stderr'] = fc_facts(module)

    if 'fs' in module.params['subset'] or 'all' in module.params['subset']:
        ha_facts['filesystems'], result['rc'], result['stdout'], result['stderr'] = fs_facts(module)

    if 'lv' in module.params['subset'] or 'all' in module.params['subset']:
        ha_facts['lvols'], result['rc'], result['stdout'], result['stderr'] = lv_facts(module)

    if 'mp' in module.params['subset'] or 'all' in module.params['subset']:
        ha_facts['mirror_pools'], result['rc'], result['stdout'], result['stderr'] = mp_facts(module)

    if 'network' in module.params['subset'] or 'all' in module.params['subset']:
        ha_facts['networks'], result['rc'], result['stdout'], result['stderr'] = network_facts(module)

    if 'service_ip' in module.params['subset'] or 'all' in module.params['subset']:
        ha_facts['service_ips'], result['rc'], result['stdout'], result['stderr'] = sip_facts(module)

    if 'rg' in module.params['subset'] or 'all' in module.params['subset']:
        ha_facts['resource_groups'], result['rc'], result['stdout'], result['stderr'] = rg_facts(module)

    if 'vg' in module.params['subset'] or 'all' in module.params['subset']:
        ha_facts['volume_groups'], result['rc'], result['stdout'], result['stderr'] = vg_facts(module)

    result['ansible_facts'] = dict(powerha=ha_facts)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
