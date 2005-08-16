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
