.. _ha_facts_module:


ha_facts -- Gather facts about PowerHA
======================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module gathers information about the current PowerHA installation and configuration.

File collection facts are not complete now. We are working on it.

Please don't use 'all' in subset unless you know what you are doing. It can take a very long time on large clusters!






Parameters
----------

  subset (False, list, all)
    subset of facts to return









Examples
--------

.. code-block:: yaml+jinja

    
    # get complete information about PowerHA cluster. It takes long time!
    - name: Get PowerHA information
      enfence.powerha_aix.ha_facts:
    # get information about defined PowerHA networks
    - name: Get PowerHA network information
      enfence.powerha_aix.ha_facts:
        subset: network



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

