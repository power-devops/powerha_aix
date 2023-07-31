.. _appcontroller_module:


appcontroller -- manage application\_controller resource in PowerHA cluster
===========================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module creates or deletes application\_controller resource in PowerHA cluster.






Parameters
----------

  name (True, str, None)
    name of the application controller.


  start (False, path, None)
    path to the start script. the attribute is required if application controller is created.


  stop (False, path, None)
    path to the stop script. the attribute is required if application controller is created.


  mode (False, str, background)
    mode of starting scripts. background or foreground. by default background.


  monitors (False, list, None)
    application monitors.

    added in 1.1.3


  cpumon (False, bool, None)
    enable or disable CPU monitoring. By default is disabled.

    added in 1.1.3


  cpuproc (False, path, None)
    full path of the application binary to monitor.

    added in 1.1.3


  cpuintvl (False, int, None)
    interval in minutes to monitor cpu usage by the process. valid values are 1 to 120.

    added in 1.1.3


  state (False, str, present)
    the desired state of the resource - present or absent. If the resource is already defined, it will not be changed.









Examples
--------

.. code-block:: yaml+jinja

    
    # create a new application controller
    - name: create a new application controller
      enfence.powerha_aix.appcontroller:
        name: ac_oracle
        start: /usr/local/bin/start_ora
        stop: /usr/local/bin/stop_ora
        mode: foreground
        state: present
    # delete an existing application controller
    - name: delete an existing application controller
      enfence.powerha_aix.appcontroller:
        name: ac_oracle
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

