# Role: cluster_create

## Description

This role creates a simple dual-node PowerHA cluster with one resource group on IBM AIX.

The role is part of [PowerHA SystemMirror for AIX collection](https://power-devops.github.io/powerha_aix).

## Prerequisites

- IBM AIX 7.2 or IBM AIX 7.3
- IBM PowerHA SystemMirror for AIX 7.2.X
- Ansible 2.13 or newer
- Python 3.9

## Inventory requirements

Hosts where PowerHA cluster will be created must be in one of two groups:

- node1
- node2

The hosts from `node1` group will be primary nodes in the cluster.

```toml
[node1]
aix11
aix21
aix31

[node2]
aix12
aix22
aix32
```

## Variables

| Name | Type | Default | Description |
| ---- | ---- | ------- | ----------- |
| cluster_name | str | cluster1 | Name of PowerHA cluster. |
| caarepo_luns | array of str | [00000000000000000000000000000000] | LDEV to create CAA repository. |
| nodes | array of dict | [] | Cluster nodes. Each time must have two fields: `name` for node's name and `ip` for IP address of the node. |
| service | array of dict | [] | Service IP labels. Each item must have two fields: `name` for the service label and `ip`for IP address of the service label. |
| app | dict | see below | Application controller resource in PowerHA clsuter. |
| rg | dict | see below | Resource group resource in PowerHA cluster. |

### app variable

```yaml
app:
  name: "ac_ora" 		# name of the application controller
  start: "start_app.sh" 	# script to start the application
  stop: "stop_app.sh"		# script to stop the application
```

### rg variable

```yaml
rg:
  name: "rg_oracle"		# name of the resource group
  startup: "OHN"		# startup policy of the resource group
  fallover: "FNPN"		# fallover policy of the resource group
  fallback: "NFB"		# fallback policy of the resource group
```

## Example

```yaml
---
- name: Prepare AIX to configure PowerHA cluster
  hosts: all
  become: true
  gather_facts: false

  roles:
    - role: cluster_prepare
      nodes:
        - { name: "node1", ip: "10.0.0.11" }
        - { name: "node2", ip: "10.0.0.12" }
      service:
        - { name: "cluster", ip: "10.0.0.10" }
```

## License

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.


## Author

Andrey Klyachkin (@aklyachkin)
