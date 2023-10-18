# Copyright (c) 2023, eNFence GmbH (info@power-devops.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.enfence.powerha_aix.plugins.module_utils.helpers import (
    parse_clmgrq_output, CLMGR)


def get_pha_version(module):
    version = {}
    cmd = "/usr/es/sbin/cluster/utilities/halevel -s"
    module.debug('Starting command: %s' % cmd)
    rc, stdout, stderr = module.run_command(cmd)
    if rc != 0:
        return version, rc, stdout, stderr
    version['version'] = stdout.split()[0]
    version['sp'] = stdout.split()[1]
    version['full_version'] = stdout.strip()
    if version['sp'] == 'GA':
        version['sp'] = ''
    return version, rc, stdout, stderr


def _get_rsc(module, rsc):
    res = []
    cmd = "%s query %s" % (CLMGR, rsc)
    module.debug('Starting command: %s' % cmd)
    rc, stdout, stderr = module.run_command(cmd)
    if rc != 0:
        return res, rc, stdout, stderr
    res = stdout.split()
    return res, rc, stdout, stderr


def _get_attrs(module, rsc, name):
    attrs = dict()
    cmd = "%s query %s %s" % (CLMGR, rsc, name)
    module.debug('Starting command: %s' % cmd)
    rc, stdout, stderr = module.run_command(cmd)
    if rc != 0:
        return attrs, rc, stdout, stderr
    attrs = parse_clmgrq_output(stdout)
    return attrs, rc, stdout, stderr


# APPLICATION CONTROLLER
def get_pha_apps(module):
    return _get_rsc(module, 'application_controller')


def get_pha_app_attrs(module, item):
    return _get_attrs(module, 'application_controller', item)


# CLUSTER
def get_pha_cluster(module):
    a, rc, stdout, stderr = _get_attrs(module, 'cluster', '')
    return [a['CLUSTER_NAME']], rc, stdout, stderr


def get_pha_cluster_attrs(module, item):
    return _get_attrs(module, 'cluster', item)


# FILE COLLECTION
def get_pha_filecolls(module):
    return _get_rsc(module, 'file_collection')


def get_pha_filecoll_attrs(module, item):
    return _get_attrs(module, 'file_collection', item)


# FILE SYSTEMS
def get_pha_filesystems(module):
    return _get_rsc(module, 'file_system')


def get_pha_filesystem_attrs(module, item):
    return _get_attrs(module, 'file_system', item)


# LOGICAL VOLUMES
def get_pha_lvols(module):
    return _get_rsc(module, 'logical_volume')


def get_pha_lvol_attrs(module, item):
    return _get_attrs(module, 'logical_volume', item)


# MIRROR POOLS
def get_pha_mpools(module):
    return _get_rsc(module, 'mirror_pool')


def get_pha_mpool_attrs(module, item):
    return _get_attrs(module, 'mirror_pool', item)


# NETWORK
def get_pha_networks(module):
    return _get_rsc(module, 'network')


def get_pha_network_attrs(module, item):
    return _get_attrs(module, 'network', item)


# RESOURCE GROUP
def get_pha_rgs(module):
    return _get_rsc(module, 'resource_group')


def get_pha_rg_attrs(module, item):
    return _get_attrs(module, 'resource_group', item)


# SERVICE IP
def get_pha_sips(module):
    return _get_rsc(module, 'service_ip')


def get_pha_sip_attrs(module, item):
    return _get_attrs(module, 'service_ip', item)


# VOLUME GROUP
def get_pha_vgs(module):
    return _get_rsc(module, 'volume_group')


def get_pha_vg_attrs(module, item):
    return _get_attrs(module, 'volume_group', item)
