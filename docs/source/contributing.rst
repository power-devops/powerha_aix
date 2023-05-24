Contributing to the collection
==============================

Thank you for your interest in our **IBM PowerHA SystemMirror for AIX Ansible collection** ☺️

There are many ways in which you can participate in the project, for example:

* `Report and verify bugs and help with solving issues`_.
* `Submit and review patches`_.

.. _Report and verify bugs and help with solving issues: https://github.com/power-devops/powerha_aix/issues
.. _Submit and review patches: https://github.com/power-devops/powerha_aix/pulls

Development Guide for IBM PowerHA SystemMirror for AIX Ansible Collection
-------------------------------------------------------------------------

**IBM PowerHA SystemMirror for AIX Ansible collection** is a set of Ansible modules for interacting with IBM PowerHA SystemMirror for AIX. In order to test your contributions you must have access to IBM AIX and have license to run IBM PowerHA on it.

We use Github for the collection's development. Patches are submitted as pull requests through `Github`_.

.. _Github: https://github.com/power-devops/powerha_aix/pulls

Branches
^^^^^^^^

We use ``main`` branch for development. If you want to submit a pull request, fork the repository, create a new branch and add your changes into your new branch.

Naming
^^^^^^

* This collection is named ``powerdevops.powerha_aix``. There is no need for further namespace prefixing.
* Name new module according to PowerHA resources or similar, that every user of the collection can understand which type of PowerHA resource is configured using the module.

Interface
^^^^^^^^^

* If you need to return some additional information to the user, use ``msg`` field.
* If you call external utilities, provide ``stdout`` and ``stderr`` fields with the output from the utilities.
* If there is was failure, ``rc`` field must be set to non-zero value.
* Module results have to be documented in ``RETURN`` docstring.
* Module must have documentation and examples.

Coding Guidelines
^^^^^^^^^^^^^^^^^

* Modules should
  * be idempotent (not being idempotent requires a solid reason),
  * return whether something has ``changed``,
  * support ``check mode``,
* ``*_info`` modules never raise exceptions when resources cannot be found. When resources cannot be found, then a ``*_info`` module returns an empty list instead. 
* ``EXAMPLES`` docstring in modules (and Ansible's own modules) consist of a list of tasks. They do not contain YAML directives end marker line (``---``) and do not define playbooks (e.g. ``hosts`` keyword). They shall be simple, e.g. do not do fancy loops, heavy use of variables or use Ansible directives for no apparent reason such as ignore_errors or register.
* Use module option names which match attribute names used in PowerHA. You may use aliases if you want to provide shorter or more clear attribute names.

Testing
^^^^^^^

* Modules have to be tested with ansible-test sanity checking.
* Before submitting patches, you must test your contributions on IBM AIX with PowerHA.


