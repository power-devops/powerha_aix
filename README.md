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

## Certifications

This collection is NOT certified by Red Hat. But yes, we plan to do it one day.

## Contributions

Contributions are welcome. Open an issue or create a pull request.
