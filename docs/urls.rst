==============
URL Dispatcher
==============

Included is a Django-esque URL dispatcher view.

.. code-block:: python

    from antfarm import urls

    from myapp import views

    view = urls.url_dispatcher([
        (r'^/$', views.index),
        (r'^/(?P<slug>[-\w]+)/$', views.blog_detail),
        (r'^/(?P<slug>[-\w]+)/up/$', views.blog_vote, {'direction': 1}),
        (r'^/(?P<slug>[-\w]+)/$', views.blog_vote, {'direction': -1}),
    ])


    application = App(root_view=view)

