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


  fix (False, bool, None)
    automatically fix errors during synchronization









Examples
--------

.. code-block:: yaml+jinja

    
    # create a new cluster if it doesn't exist
    - name: create a new cluster
      powerdevops.powerha_aix.cluster:
        name: cluster1
        state: present
        nodes:
          - node1
          - node2
        repos:
          - hdisk2
          - hdisk3
    - name: delete an existing cluster
      powerdevops.powerha_aix.cluster:
        name: cluster1
        state: absent
    - name: start cluster
      powerdevops.powerha_aix.cluster:
        name: cluster1
        state: started
    - name: stop cluster
      powerdevops.powerha_aix.cluster:
        name: cluster1
        state: stopped
    - name: synchronize cluster
      powerdevops.powerha_aix.cluster:
        name: cluster1
        fix: true
        state: synced



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

