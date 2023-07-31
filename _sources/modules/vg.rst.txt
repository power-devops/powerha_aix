.. _vg_module:


vg -- manage volume\_group resource in PowerHA cluster
======================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module creates/deletes/changes volume\_group resource in PowerHA cluster.

This module was added in 1.1.3.






Parameters
----------

  name (True, str, None)
    name of the volume group.


  state (False, str, present)
    the desired state of the volume group - \ :literal:`present`\ , \ :literal:`absent`\ .

    additional states \ :literal:`rgadd`\  and \ :literal:`rgremove`\  to add and remove the volume group from a resource group.


  nodes (False, list, None)
    list of nodes where volume group can be activated.

    required if the state is \ :literal:`present`\ .


  type (False, str, scalable)
    volume group type.


  volumes (False, list, None)
    list of physical volumes to add into the volume group.

    required if the state is \ :literal:`present`\ .


  rg (False, str, None)
    resource group for the volume group.

    required if state is \ :literal:`rgadd`\  or \ :literal:`rgremove`\ .


  pp_size (False, int, None)
    size of the physical partition in MB.


  major (False, int, None)
    major number of the volume group device.


  activate_on_restart (False, bool, None)
    activate the volume group on system startup.


  quorum (False, bool, None)
    if the volume group must be automatically varied off after losing its quorum of physical volumes.


  ltg (False, int, None)
    logical track group size.


  migrate_failed_disks (False, str, None)
    .


  max_pp (False, int, None)
    maximum number of physical partitions in the volume group.


  max_lv (False, int, None)
    maximum number of logical volumes in the volume group.


  strict_mp (False, str, None)
    enable mirror pool strictness on the volume group.

    \ :literal:`no`\  means disable mirror pool strictness.

    \ :literal:`yes`\  means mirror pools must be used.

    \ :literal:`super`\  means mirror pools will be enforced.


  mp (False, str, None)
    the name of the mirror pool.


  critical (False, bool, None)
    enable critical vg flag on the volume group.


  encryption (False, bool, None)
    enalbe LV encryption on the volume group


  on_failure (False, str, None)
    action on failure of the critical volume group.


  notify (False, path, None)
    script to call if the \ :literal:`on\_failure`\  action is \ :literal:`notify`\ .


  preferred_read (False, str, None)
    read preference to the copy of logical volumes.









Examples
--------

.. code-block:: yaml+jinja

    
    # find a disk with LDEV 25B6 and create vg01 on it
    - name: find disk for vg01
      enfence.powerha_aix.pv_info:
        ldev: 25B6
      register: hdisk
    - name: stop if the hdisk is not found
      ansible.builtin.fail:
        msg: hdisk for the volume group is not found
      when: hdisk.pv | length == 0
    - name: create shared volume group
      enfence.powerha_aix.vg:
        name: vg01
        nodes:
          - node1
          - node2
        volumes: "{{ hdisk.pv }}"
        rg: rg_oracle
    # delete volume group vg01
    - name: delete vg01
      enfence.powerha_aix.vg:
        name: vg01
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

