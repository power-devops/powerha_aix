# Role: cluster_prepare

## Description

This role prepares AIX 7.2 or AIX 7.3 for cluster configuration. It installs required software packages, configure
```/etc/hosts```, cluster communications daemon (clcomd), and copies application start/stop-scripts to all nodes
in the cluster.

The role doesn't support NIM for now. All filesets to install must be available local on the nodes.

The role is part of [PowerHA SystemMirror for AIX collection](https://power-devops.github.io/powerha_aix).

## Prerequisites

- IBM AIX 7.2 or IBM AIX 7.3
- IBM PowerHA SystemMirror for AIX 7.2.X
- Ansible 2.13 or newer
- Python 3.9

## Variables

| Name | Type | Default | Description |
| ---- | ---- | ------- | ----------- |
| powerha_source | path | /phainst/installp/ppc | Path to PowerHA installation filesets. |
| powerha_filesets | str | cluster.es.server cluster.es.client | PowerHA filesets to install. |
| aix_source | path | /usr/sys/inst.images | Path to AIX installation filesets. |
| aix_filesets | str | bos.ahafs bos.cluster.rte bos.clvm rsct.basic.rte | AIX filesets to install. |
| nodes | array of dict | [] | Cluster nodes. Each time must have two fields: `name` for node's name and `ip` for IP address of the node. |
| service | array of dict | [] | Service IP labels. Each item must have two fields: `name` for the service label and `ip`for IP address of the service label. |
| app | dict | see below | Application controller resource in PowerHA clsuter. |

### app variable

```
app:
  name: "ac_ora" 		# name of the application controller
  start: "start_app.sh" 	# script to start the application
  stop: "stop_app.sh"		# script to stop the application
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
