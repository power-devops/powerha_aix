.. _cluster_module:


cluster -- manage PowerHA cluster
=================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module creates/deletes/starts or stops a PowerHA cluster. Depending on the state different set of attributes are required.






Parameters
----------

  name (True, str, None)
    name of the cluster.


  state (True, str, None)
    the desired state of the cluster - present, absent, started, stopped, synced


  nodes (False, list, None)
    list of nodes to be in the cluster. used only when the cluster is created


  repos (False, list, None)
    list of repository disks. used only when the cluster is created


  type (False, str, nsc)
    type of the cluster. used only when the cluster is created

    added in 1.1.1


  heartbeat (False, str, unicast)
    hearbeat type for the cluster. used only when the cluster is created

    added in 1.1.1


  clusterip (False, str, None)
    cluster ip for heartbeating.


  fix (False, bool, None)
    automatically fix errors during synchronization


  fc_sync_interval (False, int, None)
    .


  rg_settling_time (False, int, None)
    .


  max_event_time (False, int, None)
    .


  max_rg_processing_time (False, int, None)
    .


  daily_verification (False, bool, None)
    .


  verification_node (False, str, None)
    .


  verification_debugging (False, bool, None)
    .


  heartbeat_frequency (False, str, None)
    .


  grace_period (False, str, None)
    .


  site_policy_failure_action (False, str, None)
    .


  site_policy_notify_method (False, path, None)
    .


  site_heartbeat_cycle (False, str, None)
    .


  site_grace_period (False, str, None)
    .


  temp_hostname (False, str, None)
    .


  lpm_policy (False, str, None)
    .


  heartbeat_frequency_during_lpm (False, int, None)
    .


  network_failure_detection_time (False, int, None)
    .


  caa_auto_start_dr (False, bool, None)
    .


  caa_repos_mode (False, str, None)
    .


  caa_config_timeout (False, int, None)
    .


  lvm_preferred_read (False, str, None)
    .


  crit_daemon_restart_grace_period (False, int, None)
    .


  skip_event_processing_manage_node (False, bool, None)
    .


  caa_pvm_watchdog_timer (False, str, None)
    .


  when (False, str, None)
    Taking the cluster online or offline, should be it done only \ :emphasis:`now`\ , at \ :emphasis:`restart`\  or \ :emphasis:`both`\  - now and at restart.

    Can be used only if \ :literal:`state`\  \ :emphasis:`started`\  or \ :emphasis:`stopped`\ .


  manage (False, str, None)
    What to do with resource groups if the cluser is going online or offline.

    Can be used only if \ :literal:`state`\  \ :emphasis:`started`\  or \ :emphasis:`stopped`\ .

    If \ :literal:`state`\  is \ :emphasis:`started`\  the following values are possible - \ :emphasis:`auto`\ , \ :emphasis:`manual`\ , \ :emphasis:`delayed`\ .

    If \ :literal:`state`\  is \ :emphasis:`stopped`\  the following values are possible - \ :emphasis:`offline`\ , \ :emphasis:`move`\ , \ :emphasis:`unmanage`\ .


  broadcast (False, bool, None)
    Broadcast information about changing cluster state to all logged in users.

    Can be used only if \ :literal:`state`\  \ :emphasis:`started`\  or \ :emphasis:`stopped`\ .


  timeout (False, int, None)
    Number of seconds to wait till the operation completes.

    Can be used only if \ :literal:`state`\  \ :emphasis:`started`\  or \ :emphasis:`stopped`\ .


  caa (False, bool, None)
    Should CAA be started prior to the cluster start or stopped after cluster stop.

    Can be used only if \ :literal:`state`\  \ :emphasis:`started`\  or \ :emphasis:`stopped`\ .









Examples
--------

.. code-block:: yaml+jinja

    
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



Return Values
-------------

changed (always, bool, )
  set to true if the resource was changed


msg (always, str, )
  error and informational messages


rc (always, int, )
  return code of the last executed command


stdout (always, str, )
  standard output of the last executed command


stderr (always, str, )
  standard error of the last executed command





Status
------





Authors
~~~~~~~

- Andrey Klyachkin (@aklyachkin)

