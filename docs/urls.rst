==============
URL Dispatcher
==============

Included is a Django-esque URL dispatcher view.

.. code-block:: python

    from functools import partial

    from antfarm.views import urls

    from myapp import views

    view = urls.url_dispatcher(
        (r'^/$', views.index),
        (r'^/(?P<slug>[-\w]+)/$', views.blog_detail),
        (r'^/(?P<slug>[-\w]+)/up/$', partial(views.blog_vote, direction=1)),
        (r'^/(?P<slug>[-\w]+)/$', partial(views.blog_vote, direction=-1)),
    )

    application = App(root_view=view)

.. note::

   Unlike Django, the initial / on the url is not automatically removed. To get
   a more django feel, you can include a pattern like this:

   .. code-block:: python

      root_url = urls.url_dispatcher(
          (r'^/', root)
      )

A view can raise a ``antfarm.urls.KeepLooking`` exception to tell the
dispatcher to continue scanning.

urls_dispather.register
-----------------------

You can dynamically add patterns to a urls_dispatcher by calling the instances
``register`` method:

.. code-block:: python

   urls = url_dispatcher(....)

   urls.register(pattern, view)

Additionally, you can decorate your views to add them to the url_dispatcher.

.. code-block:: python

   urls = url_dispatcher()

   @urls.register(pattern)
   def view(request...):

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

Customising Not Found
=====================

To control what response is given when no match is found for a pattern, you can
sub-class url_dispatcher.  Override ``handle_not_found`` method.

.. code-block:: python

   class my_url_dispatcher(url_dispatcher):
       def handle_not_found(self, request):
           return http.NotFound("Could not find a page for %s" % request.path)
