.. _appcontroller_module:


appcontroller -- manage application_controller resource in PowerHA cluster
==========================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module creates or deletes application_controller resource in PowerHA cluster.






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


  state (False, str, present)
    the desired state of the resource - present or absent. If the resource is already defined, it will not be changed.









Examples
--------

.. code-block:: yaml+jinja

    
    # create a new application controller
    - name: create a new application controller
      powerdevops.powerha_aix.appcontroller:
        name: ac_oracle
        start: /usr/local/bin/start_ora
        stop: /usr/local/bin/stop_ora
        mode: foreground
        state: present
    # delete an existing application controller
    - name: delete an existing application controller
      powerdevops.powerha_aix.appcontroller:
        name: ac_oracle
        state: absent





Status
------





Authors
~~~~~~~

- Andrey Klyachkin (@aklyachkin)

