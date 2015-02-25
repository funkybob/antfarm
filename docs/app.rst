=============
The App class
=============

The root of Antfarm is the ``antfarm.Ant`` class.

.. class:: App(root_view, \**kwargs)

   .. attribute:: root_view

      This provides the view to call to handle all requests.

      Any extra kwargs will be stored on self.

Each Antfarm application is an App instance.  Its configuration is passed to
the constructor, and the instance is a callable complying with the WSGI
interface (PEP3333).
