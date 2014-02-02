.. antfarm documentation master file, created by
   sphinx-quickstart on Sat Feb  1 21:54:44 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Ant Farm
========

Overview
--------

Antfarm is an ultra-light weight WSGI web framework.

Essentially, it wraps the WSGI call structure, providing helpful wrappers for
common needs.

You create an App instance, with a root view.  A "view" is a function which
accepts a ``Request`` instance, and returns a ``Response``.

QuickStart
----------

.. code-block:: python

    from antfarm import App, Response

    application = App(root_view = lambda r: Respone('Hello World!'))


Contents:
---------


.. toctree::
   :maxdepth: 2

   urls
   example


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

