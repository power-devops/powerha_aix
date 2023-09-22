.. _fc_module:


fc -- manage file\_collection resource in PowerHA cluster
=========================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module creates/deletes/changes file\_collection resource in PowerHA cluster.






Parameters
----------

  name (True, str, None)
    name of the file collection.


  state (False, str, present)
    the desired state of the file collection - \ :literal:`present`\ , \ :literal:`absent`\ .


  files (False, list, None)
    list of files to be synchronized between cluster nodes.


  description (False, str, None)
    description of the file collection.


  sync_with_cluster (False, bool, None)
    if \ :emphasis:`true`\ , the file collection will be automatically synchronized during cluster synchronization.


  sync_when_changed (False, bool, None)
    if \ :emphasis:`true`\ , the file collection will be checked for changes automatically by the cluster.

    if the cluster detects changes on the files in the collection, they will be automatically propagated to other nodes.









Examples
--------

.. code-block:: yaml+jinja

    
    # create file collection
    - name: file collection profiles
      enfence.powerha_aix.fc:
        name: profiles
        sync_when_changed: true
        sync_with_cluster: true
        files:
          - /home/sapadm/.profile
          - /home/sapadm/.login
          - /home/sapadm/.sapenv.sh
          - /home/sapadm/.dbenv.sh
    # manually synchronize collection
    - name: synchronize profiles fc
      enfence.powerha_aix.fc:
        name: profiles
        state: synced
    # delete file collection
    - name: delete file collection profiles
      enfence.powerha_aix.fc:
        name: profiles
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

