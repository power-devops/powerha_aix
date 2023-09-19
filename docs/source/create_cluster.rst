Creating IBM PowerHA Cluster using Ansible
==========================================

.. code-block:: yaml

   ---
   - name: Create cluster
     hosts: all
     vars:
       nodes:
         - aix101
         - aix102
       nodes_ip:
         - 10.11.12.21
         - 10.11.12.22
     tasks:
       - name: Create /etc/cluster/rhosts
         ansible.builtin.copy:
           content: "{{ nodes_ip | join('\n') }}\n"
           dest: /etc/cluster/rhosts
           owner: root
           group: system
           mode: "0600"
         notify:
           - Restart clcomd
       - name: Flush handlers
         ansible.builtin.meta: flush_handlers
       - name: Create a cluster
         enfence.powerha_aix.cluster:
           name: cluster1
           state: present
           repos:
             - hdisk1
           nodes: "{{ nodes }}"
         when: inventory_hostname in groups['node1']
       - name: Start cluster
         enfence.powerha_aix.cluster:
           name: cluster1
           state: started
         when: inventory_hostname in groups['node1']
       - name: Add service label
         enfence.powerha_aix.service_ip:
           name: oracle
         when: inventory_hostname in groups['node1']
         notify: "Synchronize cluster"
       - name: Add application controller
         enfence.powerha_aix.appcontroller:
           name: ac_oracle
           start: /usr/local/bin/start_ora
           stop: /usr/local/bin/stop_ora
           mode: foreground
         when: inventory_hostname in groups['node1']
         notify: "Synchronize cluster"
       - name: Add resource group
         enfence.powerha_aix.rg:
           name: rg_oracle
           nodes: "{{ nodes }}"
           startup: OHN
           fallover: FNPN
           fallback: NFB
           service: ['oracle']
           application: ['ac_oracle']
           volgrp:
             - vg01
             - vg02
         when: inventory_hostname in groups['node1']
         notify: "Synchronize cluster"
       - name: Flush handlers
         ansible.builtin.meta: flush_handlers
         when: inventory_hostname in groups['node1']
       - name: Bring rg_oracle online
         enfence.powerha_aix.rg:
           name: rg_oracle
           state: started
         when: inventory_hostname in groups['node1']
   
     handlers:
       - name: Stop clcomd # noqa: no-changed-when
         ansible.builtin.command:
           cmd: stopsrc -s clcomd
         ignore_errors: true # noqa: ignore-errors
         listen: "Restart clcomd"
   
       - name: Wait 5 seconds...
         ansible.builtin.pause:
           seconds: 5
         listen: "Restart clcomd"
   
       - name: Start clcomd # noqa: no-changed-when
         ansible.builtin.command:
           cmd: startsrc -s clcomd
         listen: "Restart clcomd"
   
       - name: Synchronize cluster
         enfence.powerha_aix.cluster:
           name: cluster1
           fix: true
           state: synced
   
