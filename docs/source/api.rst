.. _api:

=============
API Reference
=============

.. py:module:: debugclient

The :py:mod:`debugclient` module provides two classes for interacting with a
`debugserver-js`_ instance:

    | :ref:`DebugServer <debugserver>`
    | :ref:`DebugSession <debugsession>`

.. warning::

   You should not instantiate the :py:class:`DebugSession` class
   directly. Instead use the :py:meth:`DebugServer.open_session` command to obtain a
   handle to a :py:class:`DebugSession` object.

.. toctree::
    :maxdepth: 5
    :hidden:

    api/debugserver
    api/debugsession

.. _debugserver-js: https://github.com/tiflash/debugserver-js
.. _debugclient-py: https://github.com/tiflash/debugclient-py
