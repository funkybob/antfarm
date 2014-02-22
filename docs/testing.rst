=======
Testing
=======

Running tests
-------------

A test suite using the standard library's ``unittest`` package exists in
the ``tests`` directory of the git repository, it can be run from the root
of the repository via::

    python tests

To run only the tests in a specific file, you may do::

    python tests/<filename>.py

To generate a `coverage`_ report for the test suite::

    coverage run tests/__main__.py

Once the coverage data is generated, you can `report on it`_ using your
preferred output method.

.. _coverage: http://nedbatchelder.com/code/coverage/
.. _report on it: http://nedbatchelder.com/code/coverage/cmd.html#cmd-reporting

Writing tests
-------------

New tests should either be added to the appropriate test file, if it already
exists, or to a new file in the ``tests`` directory, whose name is prefixed with
``test_``::

    tests/test_<thing_to_test>.py

Test **classes** should be written such that they subclass ``unittest.TestCase``
and are named with a ``Test`` suffix::

    from unittest import TestCase

    class ThingTest(TestCase):
        pass

Individual test **methods** should be named and numbered like so::

    class ThingTest(TestCase):
        def test_001_function_description():
            pass

        def test_002_another_function_description():
            pass

Finally, to allow individual test files to be without the rest of the suite,
the file should end with the following ``if`` statement::

    from unittest import main

    if __name__ == '__main__':
        main()

