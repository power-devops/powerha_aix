.. _fs_module:


fs -- manage file\_system resource in PowerHA cluster
=====================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module creates/deletes/changes file\_system resource in PowerHA cluster.

This module was added in 1.2.0.






Parameters
----------

  name (True, str, None)
    name (mount point) of the file system.


  state (False, str, present)
    the desired state of the file system - \ :literal:`present`\ , \ :literal:`absent`\ .


  vg (False, str, None)
    volume group where the file system must be created.

    required if \ :emphasis:`lv`\  is not specified and state is \ :literal:`present`\ .


  lv (False, str, None)
    logical volume where the file system must be created.

    required if \ :emphasis:`vg`\  is not specified and state is \ :literal:`present`\ .


  type (False, str, jfs2)
    file system type.

    \ :literal:`jfs2`\  and \ :literal:`enhanced`\  are aliases.

    \ :literal:`jfs`\  and (standard) are aliases.

    \ :literal:`compressed`\  is \ :literal:`jfs`\  filesytem with compression enabled. \ :emphasis:`fragment\_size`\  must be 2048 or less.

    \ :literal:`large`\  is large file enabled \ :literal:`jfs`\  filesystem. \ :emphasis:`fragment\_size`\  must be 4096.


  size (False, int, None)
    size of the future file system.

    required if the state is \ :literal:`present`\  and \ :emphasis:`lv`\  is not specified.


  unit (False, str, None)
    which unit is used to specify \ :emphasis:`size`\  of the filesystem.

    required if \ :emphasis:`size`\  is specified.


  perm (False, str, None)
    permissions on the file system.


  options (False, str, None)
    file system options.


  disk_accounting (False, bool, None)
    enables accounting on the file system.


  block_size (False, int, 4096)
    jfs2 block size in bytes.


  fragment_size (False, int, None)
    jfs fragment size in bytes.

    by default jfs uses \ :emphasis:`4096`\  bytes fragments.

    the module sets \ :literal:`fragment\_size`\  to \ :emphasis:`4096`\  by default if you specify \ :literal:`type`\ : \ :emphasis:`large`\  and no \ :literal:`fragment\_size`\ .

    the module sets \ :literal:`fragment\_size`\  to \ :emphasis:`2048`\  by default if you specify \ :literal:`type`\ : \ :emphasis:`compressed`\  and no \ :literal:`fragment\_size`\ .


  bytes_per_inode (False, int, None)
    number of bytes per i-node for jfs filesytem.


  alloc_group_size (False, int, None)
    allocation group size in megabytes for jfs filesytem.


  log (False, str, INLINE)
    logical volume for jfs/jfs2 log.

    use \ :literal:`INLINE`\  if you want to use jfs2 inline logs.


  ea_format (False, str, None)
    specifies the format is used to store jfs2 extended attributes.


  quota (False, str, None)
    type of quotas that can be enabled on jfs2 filesytem.


  efs (False, bool, None)
    enable Encyrpted File System (EFS) on jfs2.









Examples
--------

.. code-block:: yaml+jinja

    
    # create JFS2 filesytem on existing logical volume with INLINE jfs2log.
    - name: create /ora filesystem
      enfence.powerha_aix.fs:
        name: /ora
        lv: lvora
    # delete an existing file system.
    - name: delete /ora file system
      enfence.powerha_aix.fs:
        name: /ora
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

