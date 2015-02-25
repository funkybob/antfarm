=========
Utilities
=========

Functional
==========

buffered_property
-----------------

This works much like Python's ``property`` built-in, except it will only call
the function once per instance, saving the result on the objects's \__dict__.

In subsequent accesses to the property, Python will discover the value in
\__dict__ first, and skip calling the property's \__get__.

In all other ways, this works as a normal class attribute.  Setting and del
work as expected.

By default, ``buffered_property`` will save the value to the name of the method
it decorators.  If you want to provide a buffered interface to a method, but keep
the method, you will need to pass the name argument:

.. code-block:: python

    def get_foo(self):
        ...

    foo = buffered_property(get_foo, name='foo')

