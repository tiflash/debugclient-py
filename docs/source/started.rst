.. _started:

===============
Getting Started
===============

Requirements
============

`debugserver-js`_
    dsclient-py is designed to interact with `debugserver-js`_ therefore you'll
    need to have the `debugserver-js`_ `installed <https://debugserver-js.readthedocs.io/en/latest/started.html#install>`_ and
    an instance `running <https://debugserver-js.readthedocs.io/en/latest/started.html#launch>`_ to connect to.

`Code Composer Studio`_
    Texas Instrument's eclipse based IDE which includes `DSS`_ (required by `debugserver-js`_)

Install
=======

PyPi:

::

    pip install dsclient


Source:

::

    git clone https://github.com/tiflash/dsclient-py
    cd dsclient-py
    pip install .

.. External Links
.. _debugserver-js: https://github.com/tiflash/debugserver-js
.. _Code Composer Studio: http://www.ti.com/tool/CCSTUDIO
.. _DSS: http://software-dl.ti.com/ccs/esd/documents/users_guide/sdto_dss_handbook.html
