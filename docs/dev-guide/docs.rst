.. _docs_guidelines:

*******************
Documentation Rules
*******************

Overview
========

All code must be documented and we follow these style conventions described here:

* `numpydoc <https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard>`_

We recommend familiarizing yourself with this style.

Referring to other code
-----------------------

To link to other methods, classes, or modules in your repo you have to use backticks, for example:

.. code-block:: rst

    `solarnet_metadata.schema.attribute_template`

generates a link like this: `solarnet_metadata.schema.attribute_template`.

Other packages can also be linked via
`intersphinx <http://www.sphinx-doc.org/en/master/ext/intersphinx.html>`_:

.. code-block:: rst

    `numpy.mean`

will return this link: `numpy.mean`.
This works for Python, Numpy and Astropy (full list is in :file:`docs/conf.py`).

With Sphinx, if you use ``:func:`` or ``:meth:``, it will add closing brackets to the link.
If you get the wrong pre-qualifier, it will break the link, so we suggest that you double check if what you are linking is a method or a function.

.. code-block:: rst

    :class:`numpy.mean()`
    :meth:`numpy.mean()`
    :func:`numpy.mean()`

will return two broken links ("class" and "meth") but "func" will work.

Project-specific Rules
----------------------

* For **all** RST files, we enforce a one sentence per line rule and ignore the line length.


Sphinx
======

All of the documentation (like this page) is built by `Sphinx <https://www.sphinx-doc.org/en/stable/>`_, which is a tool especially well-suited for documenting Python projects.
Sphinx works by parsing files written using a `a Mediawiki-like syntax <http://docutils.sourceforge.net/docs/user/rst/quickstart.html>`_ called `reStructuredText <http://docutils.sourceforge.net/rst.html>`_.
It can also parse markdown files.
In addition to parsing static files of reStructuredText, Sphinx can also be told to parse code comments.
In fact, in addition to what you are reading right now, the `Python documentation <https://www.python.org/doc/>`_ was also created using Sphinx.

Usage and Building the documentation
------------------------------------

All of the documentation is contained in the "docs" folder and code documentation strings.
Sphinx builds documentation iteratively, only adding things that have changed.
For more information on how to use Sphinx, consult the `Sphinx documentation <http://www.sphinx-doc.org/en/stable/contents.html>`_.

HTML
^^^^

To build the html documentation locally use the following command, in the root directory run::

    $ sphinx-build docs docs/_build/html -W -b html

This will generate HTML documentation in the "docs/_build/html" directory.
You can open the "index.html" file to browse the final product.

PDF
^^^

To build the pdf documentation locally use the follownig command, in the root directory run::

    $ sphinx-build docs docs/_build/pdf -W -b pdf

This will generate HTML documentation in the "docs/_build/html" directory.
You can open the "index.html" file to browse the final product.
