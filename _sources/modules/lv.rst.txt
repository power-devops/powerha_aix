.. _lv_module:


lv -- manage logical volumes in PowerHA cluster
===============================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module creates/deletes/changes logical\_volume resource in PowerHA cluster.






Parameters
----------

  name (True, str, None)
    name of the logical volume.


  state (False, str, present)
    the desired state of the logical volume - \ :literal:`present`\ , \ :literal:`absent`\ .


  vg (True, str, None)
    name of the volume group where the logical volume resides.


  size (False, int, None)
    size of the logical volume. required if state is \ :literal:`present`\ .


  unit (False, str, pp)
    unit for the size of the logical volume.

    the size will be rounded according to physical partition size in the volume group.


  volumes (False, list, None)
    physical volumes where the logical volume should reside.


  type (False, str, jfs2)
    type of the logical volumes.


  position (False, str, None)
    position of the logical volume on the physical volume.


  pv_range (False, str, None)
    how to place the logical volume on physical volumes.


  max_pv (False, int, None)
    maximum number of physical volumes to use for the logical volume.


  copies (False, int, None)
    number of copies of the logical volume.


  write_consistency (False, str, None)
    mode of write consistency.


  sep_pvs (False, str, None)
    Strict allocation policy.


  relocate (False, bool, None)
    Reorganization relocation flag.


  label (False, str, None)
    logical volume label.


  max_lp (False, int, None)
    maximum number of logical partitions in the logical volume.


  bb_relocate (False, bool, None)
    Bad-block relocation policy.


  sched_policy (False, str, None)
    Scheduling policy when more than one logical partition is written.


  verify_writes (False, bool, None)
    Sets the write-verify state for the logical volume.


  alloc_map (False, path, None)
    Specifies the exact physical partitions to allocate.


  stripe_size (False, str, None)
    Specifies the number of bytes per strip.


  serialize_io (False, bool, None)
    Turns on/off serialization of overlapping I/Os.


  first_block_available (False, bool, None)
    The logical volume control block does not occupy the first block of the logical volume.


  mp1 (False, str, None)
    Specify a mirror pool for first copy.


  mp2 (False, str, None)
    Specify a mirror pool for second copy.


  mp3 (False, str, None)
    Specify a mirror pool for third copy.


  group (False, str, None)
    Specifies group ID for the logical volume special file.


  permissions (False, str, None)
    Specifies permissions (file modes) for the logical volume special file.


  node (False, str, None)
    Reference node.


  encryption (False, bool, None)
    Enables the data encryption option in the logical volume.


  auth_method (False, str, None)
    N/A.


  method_details (False, str, None)
    N/A.


  auth_method_name (False, str, None)
    N/A.









Examples
--------

.. code-block:: yaml+jinja

    
    - name: create logical volume
      enfence.powerha_aix.lv:
        name: lvora
        vg: vg01
        size: 1
        unit: gb



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

