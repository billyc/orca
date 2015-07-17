from __future__ import print_function

import subprocess

# Install setuptools if not installed.
try:
    import setuptools
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()

from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
from setuptools.command.sdist import sdist


# these make sure the js distribution bundle is created and
# up-to-date when creating distribution packages.
def build_js_bundle():
    print('Building JS bundle')
    subprocess.check_call(['./bin/build_js_bundle.sh'])


class sdist_(sdist):
    def run(self):
        build_js_bundle()
        sdist.run(self)


class build_py_(build_py):
    def run(self):
        build_js_bundle()
        build_py.run(self)

# read README as the long description
with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
    name='orca',
    version='1.2dev',
    description='A pipeline orchestration tool with Pandas support',
    long_description=long_description,
    author='Synthicity',
    author_email='mdavis@synthicity.com',
    license='BSD',
    url='https://github.com/synthicity/orca',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: BSD License'
    ],
    packages=find_packages(exclude=['*.tests']),
    package_data={
        'orca': [
            'server/static/css/*',
            'server/static/js/dist/*',
            'server/templates/*']
    },
    install_requires=[
        'pandas >= 0.13.1',
        'tables >= 3.1.0',
        'toolz >= 0.7.0',
        'zbox >= 1.2'
    ],
    extras_require={
        'server': ['flask >= 0.10', 'pygments >= 2.0', 'six >= 1.9.0']
    },
    entry_points={
        'console_scripts': [
            'orca-server = orca.server.server:main [server]'
        ]
    },
    cmdclass={
        'build_py': build_py_,
        'sdist': sdist_
    }
)
