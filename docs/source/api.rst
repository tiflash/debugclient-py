.. _api:

=============
API Reference
=============

.. py:module:: debugclient

The `debugclient` module provides two classes for interacting with a
`DebugServer-js`_ instance:

    | :ref:`DebugServer <debugserver>`
    | :ref:`DebugSession <debugsession>`

.. warning::

   You should not instantiate the :py:class:`DebugSession` class
   directly. Instead use the :py:meth:`DebugServer.open_session` command to obtain a
   handle to a DebugSession object.

.. toctree::
    :maxdepth: 5
    :hidden:

    api/debugserver
    api/debugsession

.. _DebugServer-js: https://github.com/tiflash/debugserver-js
