from setuptools import setup, find_packages

import os
from subprocess import call
from setuptools import Command
from distutils.command.build_ext import build_ext as _build_ext
from setuptools.command.bdist_egg import bdist_egg as _bdist_egg
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel


class build_frontend(Command):
    """ A command class to run `frontendbuild.sh` """
    description = 'build front-end JavaScript and CSS'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        call(['./frontendbuild.sh'],
             cwd=os.path.dirname(os.path.abspath(__file__)))


class build_ext(_build_ext):
    """ A build_ext subclass that adds build_frontend """
    def run(self):
        self.run_command('build_frontend')
        _build_ext.run(self)


class bdist_egg(_bdist_egg):
    """ A bdist_egg subclass that runs build_frontend """
    def run(self):
        self.run_command('build_frontend')
        _bdist_egg.run(self)


class bdist_wheel(_bdist_wheel):
    """ A bdist_wheel subclass that runs build_frontend """
    def run(self):
        self.run_command('build_frontend')
        _bdist_wheel.run(self)

setup(
    name="regulations",
    version="2.0.0",
    packages=find_packages(),
    include_package_data=True,
    cmdclass={
        'build_frontend': build_frontend,
        'build_ext': build_ext,
        'bdist_egg': bdist_egg,
        'bdist_wheel': bdist_wheel,
    },
    install_requires=[
        'django==1.8',
        'lxml',
        'requests'
    ],
    classifiers=[
        'License :: Public Domain',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication'
    ]
)
