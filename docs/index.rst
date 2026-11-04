.. stinger-ipc documentation master file, created by Sphinx.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Stinger-IPC
===========

StingerIPC provides **inter-process communications (IPC)** between a server and
multiple clients running on the same or separate hosts.  It uses an MQTT server
to pass messages between processes, implementing several IPC patterns: signals,
commands, properties, and procedures.

Given a declarative description of an interface (a ``*.stinger.yaml`` file),
Stinger-IPC generates ready-to-use client and server code in multiple target
languages so that separate processes can communicate against a shared,
strongly-typed contract.

.. note::

   This project is in early stages of active development.  You should not use
   it in any of your projects yet — both because it doesn't have enough
   features to be useful, and because things may be broken in future updates.

.. toctree::
   :maxdepth: 2
   :caption: Contents

   usage
   architecture
   api

.. toctree::
   :maxdepth: 1
   :caption: Project links

   GitHub <https://github.com/stinger-ipc/stinger-ipc>
   PyPI <https://pypi.org/project/stinger-ipc/>

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
