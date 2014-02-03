=========
Utilities
=========

Decorators
==========

The ``With`` class
------------------

This is primarily for wrapping views with context managers.

.. code-block:: python

    from antfarm.utils import With

    @With(session_manager)
    def user_detail(request, ...)

Or, in a url_dispatcher:

.. code-block:: python

    urls = url_dispatcher([
        (r'^/user/$', With(session_manager)(user_detail)),
    ])

Internally the wrapping function will be called passed the request, and any
positional or keyword arguments passed to the constructor.  It is expected to
yield an updated request object.

Calling the above view is equivalent to:

.. code-block:: python

    with session_manager(request) as request:
        return user_detail(request, *args, **kwargs)

Since everything is a view, you can apply a context manager to dispatchers,
also:

.. code-block:: python

    App(
        root_view = With(session_manager)(url_dispatcher([
            ...
        ]))
    )


Functional
==========

buffered_property
-----------------

This works much like Python's ``property`` build-in, except it will only call
the function once per instance, saving the result on the objects's \__dict__.

In subsequent accesses to the property, Python will discover the value in
\__dict__ first, and skip calling the property's __get__.

In all other ways, this works as a normal class attribute.  Setting and del
work as expected.

By default, ``buffered_property`` will save the value to the name of the method
it decorats.  If you want to provide a buffered interface to a method, but keep
the method, you will need to pass the name argument:

.. code-block:: python

    def get_foo(self):
        ...

    foo = buffered_property(get_foo, name='foo')

