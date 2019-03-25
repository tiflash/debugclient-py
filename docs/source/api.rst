.. _api:

=============
API Reference
=============

The `debugclient` module provides two classes for interacting with a
`DebugServer`_:

    1. :ref:`DebugServer <debugserver>`
    2. :ref:`DebugSession <debugsession>`

.. warning::

   You should not instantiate the :ref:`DebugSession <debugsession>` class
   directly. Instead use the DebugServer.open_session() command to obtain a
   handle to a DebugSession object.

.. toctree::
    :maxdepth: 5
    :hidden:

    api/debugserver
    api/debugsession

.. _DebugServer: https://github.com/tiflash/debugserver-js
