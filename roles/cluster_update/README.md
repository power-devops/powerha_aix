# Role: cluster_update

## Description

This role updates PowerHA SystemMirror software on AIX 7.2 or AIX 7.3. It brings your cluster in unmanaged mode
and updates software consequently on both nodes and then starts the cluster software again.

You must have PowerHA SystemMirror filesets. You can download them from IBM ESS or IBM FixCentral sites.

The role is part of [PowerHA SystemMirror for AIX collection](https://power-devops.github.io/powerha_aix).

## Prerequisites

- IBM AIX 7.2 or IBM AIX 7.3
- IBM PowerHA SystemMirror for AIX 7.2.X
- Ansible 2.13 or newer
- Python 3.9

## Variables

| Name | Type | Default | Description |
| ---- | ---- | ------- | ----------- |
| update_type | str | copy | Where to find PowerHA updates. `copy` - local on Ansible controller, `nfs` - mount from NFS server, `nim` - lpp_source on NIM server. |
| source | path | `/pha_update` | Path to PowerHA installation filesets. If *update_type* == `copy,` it is local path on Ansible controller node. If *update_type* == `nfs`, it is NFS share like `server:/pha_update`. If *update_type* == `nim`, it is lpp_source on the NIM server. |
| nodes | array of dict | [] | Cluster nodes. Each item must have two fields: `name` for node's name and `ip` for IP address of the node. |
| cluster_name | str | cluster1 | Name of the cluster. |

## Example

```yaml
---
- name: Update PowerHA on AIX
  hosts: all
  become: true
  gather_facts: false

  roles:
    - role: cluster_update
      nodes:
        - { name: "node1", ip: "10.0.0.11" }
        - { name: "node2", ip: "10.0.0.12" }
```

## License

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.


## Author

Andrey Klyachkin (@aklyachkin)
