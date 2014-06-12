========
Cookbook
========

Below are some common patterns that have proven productive in using Antfarm.

Middleware
==========

It's easy to write "Middleware" style views, which do some work before or after
other views.

.. code-block:: python

   class middleware(object):
       def __init__(self, view):
           self.view

       def __call__(self, request, *args, **kwargs):
           # Work before
           try:
               return self.view(request, *args, **kwargs)
           except ...:
               # Catch errors
           finally:
               # Work after _always_


    application = App(root_view = middleware(normalview))

Selective Middleware
====================

An idea which resurfaces frequently in the Django community is one of applying
middleware to a sub-set of the URL tree.  The only existing solution is to
apply a decorator to all the views [tedious and error prone] or to complicate
the middleware with ways to denote what it is to apply to.

In Antfarm, this problem is trivially solved, since middleware are just views
which wrap views.

A simple example is making some URLs password protected, but not others.

.. code-block:: python

    private_urls = url_dispatcher(
        (r'^$', views.user_list),
        (r'^(?P<user_id>\d+)/$', views.user_detail),
    )

    root_urls = url_dispatcher(
        (r'^/$', views.index),
        (r'^/login/$', views.login),
        (r'^/users/', login_required(private_urls)),
    )


