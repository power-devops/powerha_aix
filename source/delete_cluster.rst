Deleting IBM PowerHA Cluster using Ansible
==========================================

.. code-block:: yaml

   ---
   - name: Delete cluster
     hosts: all
     tasks:
       - name: Stop cluster
         enfence.powerha_aix.cluster:
           name: cluster1
           state: stopped
         when: inventory_hostname in groups['node1']
       - name: delete cluster
         enfence.powerha_aix.cluster:
           name: cluster1
           state: absent
         when: inventory_hostname in groups['node1']
