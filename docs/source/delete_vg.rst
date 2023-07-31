Removing volume group from IBM PowerHA Cluster using Ansible
============================================================

.. code-block:: yaml

   ---
   - name: test playbook - remove volume group
     hosts: node1
     gather_facts: false
     vars:
       - vg: vg01
       - lv: lvora
       - mountpoint: /ora
       - rg: rg_ora
     tasks:
       - name: remove shared volume group from resource group
         enfence.powerha_aix.vg:
           name: "{{ vg }}"
           rg: "{{ rg }}"
           state: rgremove
       - name: sync cluster config
         enfence.powerha_aix.cluster:
           name: cluster1
           fix: true
       - name: delete file system
         enfence.powerha_aix.fs:
           name: "{{ mountpoint }}"
           state: absent
       - name: delete shared volume group
         enfence.powerha_aix.vg:
           name: "{{ vg }}"
           state: absent
