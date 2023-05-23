# IBM PowerHA SystemMirror for AIX Ansible collection

This collection enable PowerHA cluster management through Ansible on IBM AIX.
It is tested with IBM PowerHA 7.2.7 but should work with any PowerHA starting 7.2.1.

## Prerequisites

- AIX 7.2 or AIX 7.3
- IBM PowerHA SystemMirror 7.2
- Packages are already installed:
  - bos.ahafs
  - bos.cluster.rte
  - bos.clvm
  - rsct.basic.rte

## Documentation

Documentation is available at https://power-devops.github.io/powerha_aix/.

If you already installed the collection you can read the documentation using ansible-doc:

```
ansible-doc -M ./collections/ansible_collections/powerdevops/powerha_aix/plugins/modules powerdevops.powerha_aix.cluster
```

## Modules

The following modules are available now:

* powerdevops.powerha_aix.appcontroller
* powerdevops.powerha_aix.cluster
* powerdevops.powerha_aix.rg
* powerdevops.powerha_aix.service_ip

More will come in the future.

## Using the collection

### Installing the Collection from Ansible Galaxy

Before using this collection, you need to install it with the Ansible Galaxy command-line tool:
```bash
ansible-galaxy collection install powerdevops.powerha_aix
```

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:
```yaml
---
collections:
  - name: powerdevops.powerha_aix
```

Note that if you install the collection from Ansible Galaxy, it will not be upgraded automatically when you upgrade the `ansible` package. To upgrade the collection to the latest available version, run the following command:
```bash
ansible-galaxy collection install powerdevops.powerha_aix --upgrade
```

You can also install a specific version of the collection, for example, if you need to downgrade when something is broken in the latest version (please report an issue in this repository). Use the following syntax to install version `1.0.0`:

```bash
ansible-galaxy collection install powerdevops.powerha_aix:==1.0.0
```

### Examples

Look at examples directory for playbook examples using the collection.

## Certification

This collection is NOT certified by Red Hat. But yes, we plan to do it one day.

## Code of Conduct

We follow the [Ansible Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html) in all our interactions within this project.

If you encounter abusive behavior, please refer to the [policy violations](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html#policy-violations) section of the Code for information on how to raise a complaint.

## Contributions

Contributions are welcome. Open an issue or create a pull request.

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
