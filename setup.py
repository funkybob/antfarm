from setuptools import setup, find_packages

setup(
    name='antfarm',
    version='0.0.2',
    description='An ultra-light-weight web framework',
    author='Curtis Maloney',
    author_email='curtis@tinbrain.net',
    url='http://github.com/funkybob/antfarm',
    keywords=['wsgi'],
    packages = find_packages(exclude=('tests*',)),
    zip_safe=False,
    classifiers = [
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
