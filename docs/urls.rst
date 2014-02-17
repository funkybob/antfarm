==============
URL Dispatcher
==============

Included is a Django-esque URL dispatcher view.

.. code-block:: python

    from functools import partial

    from antfarm import urls

    from myapp import views

    view = urls.url_dispatcher(
        (r'^/$', views.index),
        (r'^/(?P<slug>[-\w]+)/$', views.blog_detail),
        (r'^/(?P<slug>[-\w]+)/up/$', partial(views.blog_vote, direction=1)),
        (r'^/(?P<slug>[-\w]+)/$', partial(views.blog_vote, direction=-1)),
    )

    application = App(root_view=view)

.. note::

    Unlike Django, the initial / on the url is not automatically removed.

A view can raise a ``antfarm.urls.KeepLooking`` exception to tell the
dispatcher to continue scanning.

Nesting patterns
================

The currently unmatched portion of the path is stashed on the Request object as
``remaining_path``, so ``url_dispatcher`` views can be nested.

.. code-block:: python

    inner_patterns = url_dispatcher(
        ...
    )

    root_view = url_dispatcher(
        ...
        (r'^/inner/', inner_patterns),
    )

