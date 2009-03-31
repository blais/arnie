#!/usr/bin/env python
#
# Install script for arnie.
#

__author__ = "Martin Blais <blais@furius.ca>"

from distutils.core import setup

def read_version():
    try:
        return open('VERSION', 'r').readline().strip()
    except IOError, e:
        raise SystemExit(
            "Error: you must run setup from the root directory (%s)" % str(e))


# Include all files without having to create MANIFEST.in
def add_all_files(fun):
    import os, os.path
    from os.path import abspath, dirname, join
    def f(self):
        for root, dirs, files in os.walk('.'):
            if '.hg' in dirs: dirs.remove('.hg')
            self.filelist.extend(join(root[2:], fn) for fn in files
                                 if not fn.endswith('.pyc'))
        return fun(self)
    return f
from distutils.command.sdist import sdist
sdist.add_defaults = add_all_files(sdist.add_defaults)


setup(name="arnie",
      version=read_version(),
      description="Simple scripts for incremental backups to untrusted host.",
      long_description="""
Arnie is: a tremendously *simple* system for performing incremental backups to
remote untrusted hosts, with support for encrypted files on the remote host.
While our scripts are simple, we believe they are robust and are in active use
on the author's own servers, and we provide a comprehensive suite of tests to
prove it.
""",
      license="GNU GPL",
      author="Martin Blais",
      author_email="blais@furius.ca",
      url="http://furius.ca/arnie",
      scripts = ['bin/arnie-archive', 'bin/arnie-restore']
     )
