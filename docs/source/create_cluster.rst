Creating IBM PowerHA Cluster using Ansible
==========================================

.. code-block:: yaml

   ---
   - name: test playbook - create cluster
     hosts: all
     tasks:
       - name: create /etc/cluster/rhosts
         ansible.builtin.copy:
           content: "10.11.12.21\n10.11.12.22\n"
           dest: /etc/cluster/rhosts
           owner: root
           group: system
           mode: 0600
         register: rh_result
       - name: start clcomd
         ansible.builtin.shell:
           cmd: startsrc -s clcomd
         when: rh_result.changed
       - name: wait two sec...
         ansible.builtin.pause:
           seconds: 5
         when: rh_result.changed
       - name: create a cluster
         powerdevops.powerha_aix.cluster:
           name: cluster1
           state: present
           repos:
             - hdisk1
           nodes:
             - node1
             - node2
       - name: start cluster
         powerdevops.powerha_aix.cluster:
           name: cluster1
           state: started
       - name: add service label
         powerdevops.powerha_aix.service_ip:
           name: oracle
         register: sl_added
       - name: add application controller
         powerdevops.powerha_aix.appcontroller:
           name: ac_oracle
           start: /usr/local/bin/start_ora
           stop: /usr/local/bin/stop_ora
           mode: foreground
         register: ac_added
       - name: add resource group
         powerdevops.powerha_aix.rg:
           name: rg_oracle
           nodes:
             - node1
             - node2
           startup: OHN
           fallover: FNPN
           fallback: NFB
           service: ['oracle']
           application: ['ac_oracle']
           volgrp:
             - vg01
             - vg02
             - vg03
         register: rg_added
       - name: sync cluster config
         powerdevops.powerha_aix.cluster:
           name: cluster1
           fix: true
           state: synced
         when: sl_added.changed or ac_added.changed or rg_added.changed
       - name: bring rg_oracle online
         powerdevops.powerha_aix.rg:
           name: rg_oracle
           state: started
