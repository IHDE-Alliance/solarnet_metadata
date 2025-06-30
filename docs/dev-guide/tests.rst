.. _testing:

******************
Testing Guidelines
******************

This section describes the testing framework and format standards for tests.
Here we have heavily adapted the `Astropy version <https://docs.astropy.org/en/latest/development/testguide.html>`_, and **it is worth reading that link.**

The testing framework used by this repository is the `pytest`_ framework, accessed through the ``pytest`` command.

.. _pytest: https://pytest.org/en/latest/

.. note::

    The ``pytest`` project was formerly called ``py.test``, and you may
    see the two spellings used interchangeably.

Writing tests
=============

``pytest`` has the following `test discovery rules <https://pytest.org/en/latest/goodpractices.html#conventions-for-python-test-discovery>`_::

 * ``test_*.py`` or ``*_test.py`` files
 * ``Test`` prefixed classes (without an ``__init__`` method)
 * ``test_`` prefixed functions and methods

We use the first one for our test files, ``test_*.py`` and we suggest that developers follow this.

A rule of thumb for unit testing is to have at least one unit test per public function.

Where to put tests
------------------

Each package should include a suite of unit tests, covering as many of the public methods/functions as possible.
These tests should be included inside each package, e.g::

    solarnet_metadata/tests/

"tests" directories should contain an ``__init__.py`` file so that the tests can be imported.

.. _doctests:

doctests
--------

Code examples in the documentation will also be run as tests and this helps to validate that the documentation is accurate and up to date.
We use the same system as Astropy, so for information on writing doctests see the astropy `documentation <https://docs.astropy.org/en/latest/development/testguide.html#writing-doctests>`_.

You do not have to do anything extra in order to run any documentation tests.
Within our ``setup.cfg`` file we have set default options for ``pytest``, such that you only need to run::

    $ pytest <rst to test>

to run any documentation test.

Bugs Testing
------------

In addition to writing unit tests new functionality, it is also a good practice to write a unit test each time a bug is found, and submit the unit test along with the fix for the problem.
This way we can ensure that the bug does not re-emerge at a later time.
