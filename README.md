# IBM PowerHA SystemMirror for AIX Ansible collection

This collection enables PowerHA cluster management through Ansible on IBM AIX.
It is tested with IBM PowerHA 7.2.6 and 7.2.7 but should work with any PowerHA starting 7.2.1.

## Prerequisites

- AIX 7.2 or AIX 7.3
- IBM PowerHA SystemMirror 7.2
- Packages are already installed:
  - bos.ahafs
  - bos.cluster.rte
  - bos.clvm
  - rsct.basic.rte
- Ansible 2.13
- Python 3.9

## Supported versions

We support all AIX and PowerHA versions which are officially supported by IBM. 

- [AIX lifecycle support information](https://www.ibm.com/support/pages/aix-support-lifecycle-information).
- [PowerHA lifecycle support information](https://www.ibm.com/support/pages/powerha-systemmirror-support-lifecycle-information).

## Documentation

Documentation is available at https://power-devops.github.io/powerha_aix/.

If you already installed the collection you can read the documentation using ansible-doc:

```
ansible-doc -M ./collections/ansible_collections/enfence/powerha_aix/plugins/modules enfence.powerha_aix.cluster
```

## Modules

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

## Roles

The following roles are available now:

* cluster_prepare (Prepare AIX to configure PowerHA cluster)
* cluster_create (Create simple dual-node PowerHA cluster on AIX)

## Using the collection

### Installing the Collection from Ansible Galaxy

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

You can also install a specific version of the collection, for example, if you need to downgrade when something is broken in the latest version (please report an issue in this repository). Use the following syntax to install version `1.2.1`:

```bash
ansible-galaxy collection install enfence.powerha_aix:==1.2.1
```

### Examples

Look at examples directory for playbook examples using the collection.

## Certification

This collection is certified by Red Hat. It means you can download the collection from Ansible Automation Hub and it is fully
supported for Red Hat's Ansible Automation Platform customers.

## Changes

Summary of changes is available in [Changelog](https://github.com/power-devops/powerha_aix/blob/main/docs/source/changelog.rst).

## Code of Conduct

We follow the [Ansible Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html) in all our interactions within this project.

If you encounter abusive behavior, please refer to the [policy violations](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html#policy-violations) section of the Code for information on how to raise a complaint.

## Contributions

Contributions are welcome. Open an issue or create a pull request.

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
