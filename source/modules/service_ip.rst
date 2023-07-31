.. _service_ip_module:


service_ip -- manage service\_ip resource in PowerHA cluster
============================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module creates/deletes/changes service\_ip resource in PowerHA cluster.






Parameters
----------

  name (True, str, None)
    name of the service ip label. the name must be resolvable by using \ :literal:`/etc/hosts`\ .


  network (False, str, net_ether_01)
    name of the cluster network, where the service ip should be placed.


  netmask (False, str, None)
    netmask for the service ip.

    prefix and netmask are mutually exclusive.


  prefix (False, int, None)
    bit prefix for the service ip.

    prefix and netmask are mutually exclusive.


  site (False, str, None)
    site of the service ip.

    added in 1.1.1


  state (False, str, present)
    the desired state of the resource - \ :literal:`present`\  or \ :literal:`absent`\ .

    If the resource is already defined, it will not be changed.









Examples
--------

.. code-block:: yaml+jinja

    
    # create a new service ip label
    - name: create a new service ip label
      enfence.powerha_aix.service_ip:
        name: clusterip
        state: present
    # delete an existing service ip
    - name: delete an existing service ip label
      enfence.powerha_aix.service_ip:
        name: clusterip
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

