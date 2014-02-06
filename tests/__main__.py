
import unittest
import os.path

if __name__ == '__main__':
    HERE = os.path.dirname(__file__)

    loader = unittest.loader.TestLoader()
    suite = loader.discover(HERE)
    result = unittest.result.TestResult()

    suite.run(result)

    print('Ran {} tests.'.format(result.testsRun))
    print('{} errors, {} failed, {} skipped'.format(
        len(result.errors),
        len(result.failures),
        len(result.skipped),
    ))
    result.printErrors()
