==================
Django equivalents
==================

Documented here are antfarm equivalents to Django idioms.

Middleware
==========

The need for middleware is obviated by the fact everything is a view.  If you
want to hook in something to do work before matching a view, before calling a
view, or on the way out, you can just wrap that view in your own view.

This was a pattern proposed in Django also, to help disambiguate which
middleware methods are called when, but it has not been included yet as it is
too much of a backward-incompatible burden.

Further to this approach, it now becomes much simpler to selectively implement
middleware, as you can wrap only the views or dispatcher paths you choose.

URL Patterns
============

There is a Django-style URL dispatcher view included in views/urls.py

There is currently no support for named url patterns or reversing urls.
