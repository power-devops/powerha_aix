# IBM PowerHA SystemMirror for AIX Ansible collection

This collection enables PowerHA cluster management through Ansible on IBM AIX.
It is tested with IBM PowerHA 7.2.6 and 7.2.7 but should work with any PowerHA starting 7.2.1.

## Description

The collection contains modules to deploy and manage IBM PowerHA SystemMirror for IBM AIX.
There are also some basic roles to deploy simple two-node clusters with single resource group.

Using the collection you automate highly available deployments on IBM AIX for your applications.

## Requirements

- AIX 7.2 or AIX 7.3
- IBM PowerHA SystemMirror 7.2
- Packages are already installed:
  - bos.ahafs
  - bos.cluster.rte
  - bos.clvm
  - rsct.basic.rte
- Ansible 2.15
- Python 3.9

### Supported versions of PowerHA

We support all AIX and PowerHA versions which are officially supported by IBM. 

- [AIX lifecycle support information](https://www.ibm.com/support/pages/aix-support-lifecycle-information).
- [PowerHA lifecycle support information](https://www.ibm.com/support/pages/powerha-systemmirror-support-lifecycle-information).

## Installation

Before using this collection, you need to install it with the Ansible Galaxy command-line tool:
```bash
ansible-galaxy collection install enfence.powerha_aix
```

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:
```yaml
---
collections:
  - name: enfence.powerha_aix
```

Note that if you install the collection from Ansible Galaxy, it will not be upgraded automatically when you upgrade the `ansible` package. To upgrade the collection to the latest available version, run the following command:
```bash
ansible-galaxy collection install enfence.powerha_aix --upgrade
```

You can also install a specific version of the collection, for example, if you need to downgrade when something is broken in the latest version (please report an issue in this repository). Use the following syntax to install version `1.3.3`:

```bash
ansible-galaxy collection install enfence.powerha_aix:==1.3.3
```

See [using Ansible collections](https://docs.ansible.com/ansible/devel/user_guide/collections_using.html) for more details.

## Use cases

### Deploying PowerHA cluster

See example [`cluster_create.yml`](examples/cluster_create.yml) in examples subdirectory.

### Getting information about PowerHA clusters


```yaml
- name: Get PowerHA cluster information
  enfence.powerha_aix.ha_facts:

- name: Print cluster information
  ansible.builtin.debug:
    var: ansible_facts.powerha
```

### Stop and start a PowerHA cluster

```yaml
- name: Stop cluster
  enfence.powerha_aix.cluster:
    name: cluster1
    state: stopped
  tags:
    - stop

- name: Start cluster
  enfence.powerha_aix.cluster:
    name: cluster1
    state: started
  tags:
    - start
```

## Documentation

Documentation is available at:

- [Github Docs](https://power-devops.github.io/powerha_aix/)
- [Ansible Galaxy](https://galaxy.ansible.com/ui/repo/published/enfence/powerha_aix/docs/)
- [Red Hat Automation Hub](https://console.redhat.com/ansible/automation-hub/repo/published/enfence/powerha_aix/docs/)

If you already installed the collection you can read the documentation using ansible-doc:

```
ansible-doc -M ./collections/ansible_collections/enfence/powerha_aix/plugins/modules enfence.powerha_aix.cluster
```

### Modules

The following modules are available now:

* enfence.powerha_aix.appcontroller (Application Controller)
* enfence.powerha_aix.cluster (Cluster)
* enfence.powerha_aix.fc (File Collection)
* enfence.powerha_aix.fs (File System)
* enfence.powerha_aix.ha_facts (Information about current cluster configuration)
* enfence.powerha_aix.lv (Logical Volume)
* enfence.powerha_aix.mp (Mirror Pool)
* enfence.powerha_aix.pv_info (Information about Physical Volumes)
* enfence.powerha_aix.rg (Resource Group)
* enfence.powerha_aix.service_ip (Service IP)
* enfence.powerha_aix.vg (Volume Group)

More will come in the future.

### Roles

The following roles are available now:

* cluster_prepare (Prepare AIX to configure PowerHA cluster)
* cluster_create (Create simple dual-node PowerHA cluster on AIX)

### Examples

Look at [examples directory](examples/) for playbook examples using the collection.

Youtube [video](https://youtu.be/H5JvMAWcBTs) deploying a simple PowerHA dual-node cluster using the collection.

## Testing

The collection is tested with each new version of IBM PowerHA SystemMirror for AIX when it becomes available. 
Tests are performed in automated manner on IBM AIX 7.2 TL5 and 7.3 TL2 for several use cases:

- Deploying cluster
- Deploying resource group in a cluster
- Bringing resource group online
- Bringing resource group offline
- Adding a volume group to resource group
- Removing resource group
- Stopping cluster
- Starting cluster

## Certification

This collection is certified by Red Hat. It means you can download the collection from Ansible Automation Hub and it is fully
supported for Red Hat's Ansible Automation Platform customers.

## Release Notes and Roadmap

Summary of changes is available in [Changelog](https://github.com/power-devops/powerha_aix/blob/main/docs/source/changelog.rst).

Roadmap:

- add RG move
- add cluster filesystem size change
- introduce better idempotency in some modules

## Code of Conduct

We follow the [Ansible Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html) in all our interactions within this project.

If you encounter abusive behavior, please refer to the [policy violations](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html#policy-violations) section of the Code for information on how to raise a complaint.

## Contributions

Contributions are welcome. Open an issue or create a pull request.

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
