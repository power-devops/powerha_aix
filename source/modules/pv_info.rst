.. _pv_info_module:


pv_info -- find a suitable physical volume.
===========================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

this module searches for physical volumes according to the supplied attributes.

if the volumes are found, a list with their names is returned.

otherwise an empty list is returned.

physical volumes already assigned to volume groups or locked by LVM are not returned.






Parameters
----------

  name (False, str, None)
    name to find a suitable physical volumes.

    it can be a regular expresion.


  pvid (False, str, None)
    PVID of the physical volume to return.


  uuid (False, str, None)
    UUID of the physical volumes to return.


  ldev (False, str, None)
    LDEV or LUN ID of the physical volumes to return.

    it can be a regular expresion.









Examples
--------

.. code-block:: yaml+jinja

    
    # get a list of disks with LDEV 60050768019081D398000000000010D4
    - name: get hdisk for LDEV 60050768019081D398000000000010D4
      enfence.powerha_aix.pv_info:
        ldev: 60050768019081D398000000000010D4
      register: hdisk
    # get a list of free disks, not assigned to volume groups
    - name: get a list of free disks
      enfence.powerha_aix.pv_info:
        name: "hdisk*"
      register: free_hdisk
    # print the found hdisks
    - name: print hdisk
      ansible.builtin.debug:
        var: free_hdisk.pv



Return Values
-------------

pv (always, list, )
  a list of found physical volumes


changed (always, bool, )
  always False


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

