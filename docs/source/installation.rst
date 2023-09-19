Installation
============

Installing the Collection from Ansible Galaxy
---------------------------------------------

Before using this collection, you need to install it with the Ansible Galaxy command-line tool:

.. code-block:: sh

   $ ansible-galaxy collection install enfence.powerha_aix

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

.. code-block:: yaml

   ---
   collections:
     - name: enfence.powerha_aix

Note that if you install the collection from Ansible Galaxy, it will not be upgraded automatically when you upgrade the `ansible` package. To upgrade the collection to the latest available version, run the following command:

.. code-block:: sh

   $ ansible-galaxy collection install enfence.powerha_aix --upgrade

You can also install a specific version of the collection, for example, if you need to downgrade when something is broken in the latest version (please report an issue in this repository). Use the following syntax to install version `1.2.1`:

.. code-block:: sh

   $ ansible-galaxy collection install enfence.powerha_aix:==1.2.1
