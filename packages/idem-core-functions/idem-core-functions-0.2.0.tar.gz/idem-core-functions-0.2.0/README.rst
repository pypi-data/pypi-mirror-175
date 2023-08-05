===================
idem-core-functions
===================

.. image:: https://img.shields.io/badge/made%20with-pop-teal
   :alt: Made with pop, a Python implementation of Plugin Oriented Programming
   :target: https://pop.readthedocs.io/

.. image:: https://img.shields.io/badge/made%20with-python-yellow
   :alt: Made with Python
   :target: https://www.python.org/

.. note::
    Idem plugin with set of common functions that can be executed with exec.run state.

About
=====

Idem plugin with built-in functions

What is POP?
------------

This project is built with `pop <https://pop.readthedocs.io/>`__, a Python-based
implementation of *Plugin Oriented Programming (POP)*. POP seeks to bring
together concepts and wisdom from the history of computing in new ways to solve
modern computing problems.

For more information:

* `Intro to Plugin Oriented Programming (POP) <https://pop-book.readthedocs.io/en/latest/>`__
* `pop-awesome <https://gitlab.com/saltstack/pop/pop-awesome>`__
* `pop-create <https://gitlab.com/saltstack/pop/pop-create/>`__

Getting Started
===============

Prerequisites
-------------

* Python 3.7+
* git *(if installing from source, or contributing to the project)*

Installation
------------

.. note::

   If wanting to contribute to the project, and setup your local development
   environment, see the ``CONTRIBUTING.rst`` document in the source repository
   for this project.

If wanting to use ``idem-core-functions``, you can do so from source.

Install from source
+++++++++++++++++++

.. code-block:: bash

   # clone repo
   git clone git@<your-project-path>/idem-core-functions.git
   cd idem-core-functions

   # Setup venv
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e .

Usage
=====
This Idem plugin functions can be executed with exec.run state that can then be used with other idem plugin like idem-aws, idem-k8s etc as arg-binding.

Setup
-----------------
After installation, the idem-core-functions execution modules will be accessible to the pop `hub`.

For more information:

* `Intro to Plugin Oriented Programming (POP) <https://pop-book.readthedocs.io/en/latest/>`__
* `pop hub <https://pop-book.readthedocs.io/en/latest/main/hub.html#>`__

You are ready to use idem-core-functions!!!

Exec Module
-----------
Exec modules can be run from SLS using the "exec.run" state. The return from the exec module is put in the state's "new_state", so it can be used in arg_binding. The desired state of a resource can be specified in sls file.
The "core.encoding.base64encode" to apply Base64 encoding to a string.
The "core.encoding.base64decode" takes a string containing a Base64 character sequence and returns the original string.
The "core.conversion.to_json" to serialize an object to a string of JSON
The "core.collection.distinct" to return a new list with any duplicate elements removed for a given list.
The "core.collection.flatten" to eplaces any elements that are lists with a flattened sequence of the list for a given list.
The "core.collection.element" to retrieve a single element from a list.
The "core.collection.length" to  determine the length of a given list, map, or string.

Request Syntax:

..  code:: sls


    [Idem-state-name]:
      exec.run:
        - path: core.encoder.base64.encode
        - kwargs:
            data: test-user-name:test-password


    [Idem-state-name]:
      exec.run:
        - path: core.encoder.base64.decode
        - kwargs:
            encoded_data: dGVzdC11c2VyLW5hbWU6dGVzdC1wYXNzd29yZA==

    [Idem-state-name]:
      exec.run:
        - path: core.conversion.to_json
        - kwargs:
            data: '{
              "cluster_name":  "idem-eks-test",
              "region": "ap-south-1",
            }'

    [Idem-state-name]:
      exec.run:
        - path: core.encryption.gpg.encrypt
        - kwargs:
            data: test-data-for-encryption

Examples Usage:

..  code:: sls

        vault_generic_secret.example-creds.search:
          vault.secrets.kv_v1.secret.search:
            - path: "example/projects.registry.example.com"

        idem.core.encoder.base64.encode.test-2:
          exec.run:
            - path: core.encoder.base64.encode
            - kwargs:
                data: "${vault.secrets.kv_v1.secret:vault_generic_secret.example-creds.search:data:user}:${vault.secrets.kv_v1.secret:vault_generic_secret.example-creds.search:data:pass}"

        kubernetes_secret.registry-secret-example:
          k8s.core.v1.secret.present:
            - resource_id: {{ params.get('kubernetes_secret.registry-secret-example') }}
            - metadata:
                name: "registrysecret-example"
            - string_data:
                ".dockerconfigjson": |+
                                     {
                                       "auths": {
                                         "projects.registry.example.com": {
                                           "auth": "${exec:idem.core.b64Encode.test-2:data}"
                                         }
                                       }
                                     }
            - type: "kubernetes.io/dockerconfigjson"

        idem.core.encryption.gpg.encrypt.test-1:
          exec.run:
            - path: core.encryption.gpg.encrypt
            - kwargs:
                data: test-data-for-encryption

It can be specified from command line when calling exec module as below

.. code:: bash

     idem exec exec.core.encoding.base64encode data=sample-data
     idem exec exec.core.encoding.base64decode encoded_data=dGVzdC11c2VyLW5hbWU6dGVzdC1wYXNzd29yZA==

Current Supported exec functions
++++++++++++++++++++++++++++++++++

core
"""""""""""""
* conversion
* collection
* encoder
* encryption
