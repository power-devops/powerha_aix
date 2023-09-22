.. _mp_module:


mp -- manage mirror\_pool resource in PowerHA cluster
=====================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module creates/deletes/changes mirror\_pool resource in PowerHA cluster.






Parameters
----------

  name (True, str, None)
    name of the mirror pool.


  state (False, str, present)
    the desired state of the mirror pool - \ :literal:`present`\ , \ :literal:`absent`\ .


  volume_group (False, str, None)
    name of the volume group.

    required if the state is \ :literal:`present`\  and no \ :literal:`volumes`\  are specified.


  volumes (False, list, None)
    list of disks to be in the mirror pool.

    required if the state is \ :literal:`present`\  and no \ :literal:`volume\_group`\  is specified.


  mode (False, str, sync)
    mode of mirroring - synchronous or asynchronous.


  async_cache_lv (False, str, None)
    logical volume to cache data if \ :literal:`mode`\  is \ :emphasis:`async`\ .

    required if \ :literal:`mode`\  is \ :emphasis:`async`\ .


  async_cache_hw_mark (False, int, None)
    specifies the I/O-cache high watermark.

    the value is the percent of I/O cache size.

    the default value is 100%.









Examples
--------

.. code-block:: yaml+jinja

    
    # create mirror pools for vg01
    - name: mirror pool mp1
      enfence.powerha_aix.mp:
        name: mp1
        vg: vg01
        volumes:
          - hdisk1
          - hdisk2
    - name: mirror pool mp2
      enfence.powerha_aix.mp:
        name: mp2
        vg: vg02
        volumes:
          - hdisk3
          - hdisk4
    # delete mirror pool mp1 from volume group vg01
    - name: delete mirror pool mp1
      enfence.powerha_aix.mp:
        name: mp1
        vg: vg01
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

