========
Examples
========

A simple way to run any of these examples is with gunicorn:

.. code-block:: sh

    gunicorn -b localhost:8000 test:application


Hello World!
============

.. code-block:: python

    import antfarm

    def index(request):
        return antfarm.Response('Hello World!')

    application = antfarm.App(root_view=index)


Simple URL routing
==================

.. code-block:: python

    import antfarm
    from antfarm.urls import URL, url_dispatcher

    def index(request):
        return antfarm.Response('Index')

    def detail(request, user_pk):
        return antfarm.Response('You asked for %s' % user_pk)

    application = antfarm.App(
        root_view = url_dispatcher(
            (r'^/$', index),
            (r'^/details/(?P<user_pk>\d+)/$', detail),
        )
    )

