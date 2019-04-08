=======
Testing
=======

This directory contains all necessary files for running the tests

Setting up Test Environment
===========================

To setup your testing environment, you'll need at least one device to run
tests on. Below are the devices supported out of the box that include resources
for testing (if you want to run tests on a device not listed below, you'll need
to provide similar resources for that device. See `tests/resources/cc13x0 <resources/cc13x0>`_ for an
example)

- `cc1310/cc1350 <resources/cc13x0/README.rst>`_


Steps
-----

1. Edit the file `tests/env.cfg <env.cfg>`_

   a. Enter the full path to your ccs installation under ``ccs``
   b. Enter the required device information (see `tests/resources/cc13x0/README.rst <resources/cc13x0/README.rst>`_
      for what's required)


2. From the top level repo directory (``cd ../``):

   a. Configure the test setup

       | ``make configure``

   b. Run tests

      | ``make test``
