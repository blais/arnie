#!/usr/bin/env python
"""
Exhibit a bug with a check in the tarfile library.
"""
import os, os.path, tempfile, tarfile, shutil

# create a new directory and cd to it
ndir = tempfile.mkdtemp()
os.chdir(ndir)

# delete this new directory
os.rmdir(ndir)

# at this point, we are in a directory that does not exist anymore.
# running abspath on a file located in cwd will fail, e.g.
try:
    os.path.abspath('localfile')
    assert False
except OSError:
    pass

# create some file to archive
fno, fname = tempfile.mkstemp()
os.write(fno, 'sijdsjdsjdsjdsduwhdewu hwue whuw hew hw heu hwe hweuwehwheihw')
os.close(fno)

# let's try opening a tarfile in an existing temp dir and adding files to it.
tar = tarfile.open('/tmp/backup.tar', 'w')
assert tar.name == '/tmp/backup.tar'
tar.add(fname)

# ok, this works...

# now let's do the same with gzopen
tar = tarfile.open('/tmp/backup.tar', 'w:gz')
print tar.name  # oops, should be erroneously pring backup.tar and fail next
tar.add(fname)
