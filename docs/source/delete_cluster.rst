Deleting IBM PowerHA Cluster using Ansible
==========================================

.. code-block:: yaml

   ---
   - name: test playbook - delete cluster
     hosts: all
     tasks:
       - name: stop cluster
         powerdevops.powerha_aix.cluster:
           name: cluster1
           state: stopped
       - name: delete cluster
         powerdevops.powerha_aix.cluster:
           name: cluster1
           state: absent
