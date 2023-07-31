.. _rg_module:


rg -- manage resource groups in PowerHA cluster
===============================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module creates or deletes resource group in PowerHA cluster.






Parameters
----------

  name (True, str, None)
    name of the resource group.


  nodes (False, list, None)
    list of the nodes where the resource group can be started. required if resource group is created.


  secnodes (False, list, None)
    secondary nodes

    added in 1.1.3


  sitepolicy (False, str, None)
    site policy

    added in 1.1.3


  startup (False, str, None)
    startup policy for the resource group. One of \ :literal:`OHN`\ , \ :literal:`OFAN`\ , \ :literal:`OAAN`\ , or \ :literal:`OUDP`\ .

    \ :literal:`OHN`\  - Online Home Node (default).

    \ :literal:`OFAN`\  - Online on First Available Node.

    \ :literal:`OAAN`\  - Online on All Available Nodes (concurrent).

    \ :literal:`OUDP`\  - Online Using Node Distribution Policy.


  fallover (False, str, None)
    fallover policy for the resource group. One of \ :literal:`FNPN`\ , \ :literal:`FUDNP`\ , or \ :literal:`BO`\ .

    \ :literal:`FNPN`\  - Fallover to Next Priority Node (default).

    \ :literal:`FUDNP`\  - Fallover Using Dynamic Node Priority.

    \ :literal:`BO`\  - Bring Offline (On Error Node Only).


  fallback (False, str, None)
    fallback policy for the resource group. One of \ :literal:`NFB`\ , or \ :literal:`FBHPN`\ .

    \ :literal:`NFB`\  - Never Fallback.

    \ :literal:`FBHPN`\  - Fallback to Higher Priority Node (default).


  prio_policy (False, str, None)
    node priority policy, if fallover set to FUDNP. One of \ :literal:`default`\ , \ :literal:`mem`\ , \ :literal:`disk`\ , \ :literal:`cpu`\ , \ :literal:`least`\ , \ :literal:`most`\ 

    \ :literal:`default`\  - next node in the nodes list.

    \ :literal:`mem`\  - node with most available memory.

    \ :literal:`disk`\  - node with least disk activity.

    \ :literal:`cpu`\  - node with most cpu cycles available.

    \ :literal:`least`\  - node where the dynamic node priority script returns the lowest value.

    \ :literal:`most`\  - node where the dynamic node priority script returns the highest value.

    added in 1.1.3


  prio_policy_script (False, path, None)
    path to script to determine the \ :literal:`prio\_policy`\ 

    added in 1.1.3


  prio_policy_timeout (False, int, None)
    added in 1.1.3


  service (False, list, None)
    list of service labels for the resource group.


  application (False, list, None)
    list of application controllers for the resource group.


  volgrp (False, list, None)
    list of volume groups for the resource group.


  tape (False, list, None)
    .


  forced_varyon (False, bool, None)
    .


  vg_auto_import (False, bool, None)
    .


  fs (False, list, None)
    .


  disk (False, list, None)
    .


  fs_before_ipaddr (False, bool, None)
    .


  wpar (False, str, None)
    .


  export_nfs (False, list, None)
    .


  export_nfs4 (False, list, None)
    .


  stable_storage_path (False, str, None)
    .


  nfs_network (False, str, None)
    .


  mount_nfs (False, list, None)
    .


  mirror_group (False, str, None)
    .


  fallback_at (False, str, None)
    .


  state (False, str, present)
    the desired state of the resource - \ :literal:`present`\ , \ :literal:`absent`\ , \ :literal:`started`\ , \ :literal:`stopped`\ .

    If the resource is already defined, it will not be changed.









Examples
--------

.. code-block:: yaml+jinja

    
    # create a new resource group
    - name: create a new resource group
      enfence.powerha_aix.rg:
        name: rg_oracle
        nodes:
          - node1
          - node2
        startup: OHN
        fallover: FNPN
        fallback: NFB
        service: [ 'serviceip' ]
        application: [ 'ac_ora' ]
        volgrp:
          - vg01
          - vg02
          - vg03
        state: present
    # bring resource group online
    - name: starting resource group
      enfence.powerha_aix.rg:
        name: rg_oracle
        state: started
    # bring resource group offline
    - name: stopping resource group
      enfence.powerha_aix.rg:
        name: rg_oracle
        state: stopped
    # delete an existing resource group
    - name: delete an existing resource group
      enfence.powerha_aix.rg:
        name: rg_oracle
        state: absent



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

