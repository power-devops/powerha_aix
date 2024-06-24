Examples
========

The **IBM PowerHA SystemMirror for AIX collection** contains some `examples`_ to help you to start automating PowerHA.

All examples are tested with the inventory file like:

.. code-block:: ini

   [node1]
   aix101

   [node2]
   aix102

Additional documentation:

* `Automating IBM PowerHA cluster deployment on AIX with Ansible`_

.. _examples: https://github.com/power-devops/powerha_aix/tree/main/examples

.. _Automating IBM PowerHA cluster deployment on AIX with Ansible: https://www.linkedin.com/pulse/automating-ibm-powerha-cluster-deployment-aix-ansible-klyachkin/

.. toctree::
   :maxdepth: 1
   :caption: Playbook Examples:

   create_cluster
   delete_cluster
   create_vg
   delete_vg
   move_rg
