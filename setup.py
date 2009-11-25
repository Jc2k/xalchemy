#!/usr/bin/env python

import os
from glob import glob
from distutils.core import Command, setup
from unittest import TextTestRunner, TestLoader


class Test(Command):

    user_options = []

    def initialize_options(self):
        self._tests_dir = os.path.join(os.getcwd(), "tests")

    def finalize_options(self):
        pass

    def get_tests(self):
        for test in glob(os.path.join(self._tests_dir, "*.py")):
            if test != '__init__.py':
                name, ext = os.path.splitext(os.path.basename(test))
                yield name

    def run(self):
        tests = TestLoader().loadTestsFromNames([
            'tests.%s' % name for name in self.get_tests()
            ])
        runner = TextTestRunner(verbosity = 1)
        runner.run(tests)


setup(
    name='xquery',
    version='0.1',
    description='Xquery abstraction playground',
    author='John Carr',
    author_email='john.carr@unrouted.co.uk',
    packages=['xquery'],
    cmdclass = {'test': Test}
    )
