=====================================
  arnie: Simple Incremental Backups
=====================================

.. contents::
..
    1   Description
      1.1  Context
      1.2  Basic Functioning and Features
        1.2.1  Features
        1.2.2  Caution
    2   Documentation
    3   Download
    4   Installation and Packaging
    5   Testing
    6   Reporting Bugs
    7   Installation
      7.1  Dependencies
      7.2  Portability
    8   External Links
      8.1  Other Projects
    9   Copyright, License and Disclaimer
    10  Author

Description
===========

In a single sentence, arnie is: a tremendously *simple* system for performing
incremental backups to remote untrusted hosts, with support for encrypted files
on the remote host.  While our scripts are simple and recent, we believe they
are robust and are in active use on the author's own servers, and we provide a
comprehensive suite of tests to prove it.


Context
-------

Our goal is to provide a *very simple* and robust script to perform incremental
backups.

The original context for the creation of this program was that we had access to
a remote but untrusted online host with plenty of storage, where we wanted to
send backup archives of a source code repository.  We wanted incremental backups
in order to minimize bandwidth requirements, and we wanted the archive files to
be encrypted on the remote host (in case it gets broken into--it's untrusted).

We tried many other open source offerings for this problem, such as dar,
duplicity, hdup2, etc., but writing a few simple tests--*if you do not tests
your backups, you have no backups*--brought problems to the surface with most of
these systems, and more complex backup solutions like Amanda required more setup
time and work to setup than writing my own simplistic solution.

I suspect that the widespread availability of cheap online storage space
(e.g. IBackup) will make this simple scheme for backups attractive for many
other people.  This is why I provide this code as open source.


Basic Functioning and Features
------------------------------

The system consists in two self-contained Python scripts: the archiver
(``arnie-archive``) and the restorer (``arnie-restore``).

Essentially, the arnie archiver creates a tar archive with all the files that have
changed since the last backup.  The history of what had been previously backed
up is kept in a simple text file in the root of the archived directory
(``.arniehistory``), and the full list of files available at the moment of backup
is also included in the tar archive itself.  Optionally, the history file can be
stored in an alternate location (see options).

To archive, you typically run a command like this::

   arnie-archive /path/to/important-dir remotehost:/path/to/backups

The name of the archive file generated is output on stdout.  The date of the
backup archive is contained in the filename, so do not rename the file (there is
an option to select the prefix that the archive files are given).  To perform a
full backup, invoke the archive script with the ``--full`` option, or simply
delete the history file before running the archiver.

Restoring backups is similarly very simple: we open the latest tar archive, get
its list of necessary files to restore, and search backwards in time within all
the available archive files to find them.  To restore, you login to the remote
host (or fetch the archives locally) and run::

   arnie-restore /path/to/backups /path/to/restored-directory [<dir/file> ...]

The original archived directory will be restored to
``/path/to/restored-directory``.  After re-creating the files, the restore
script normally runs a verification of the MD5 sums of all the restored files,
so if something ever went wrong you will be notified at that point.  If you do
not want to restore the entire archive, you can specify the list of directories
or files to restore (specified directories will be restored recursively).

Note that if the backup files are encrypted, you will need to decrypt them
manually before running the restorer, for example::

   gpg --decrypt-files backup.*

The restorer will ignore encrypted files in the backups directory.

Features
~~~~~~~~

In addition, the following features are provided (see options):

- Automatically compress archives in gzip or bzip2 format;
- Automatically encrypt archives using a GnuPG key (specify the key Id or name);
- Automatically send the archive file to a remote host using scp.  This is just
  a convenience: alternatively you can capture the name of the archive and send
  it any way you like (ftp, other...);
- Tracks and restores permissions changes on directories and files;
- Works with empty directories;
- Works with symbolic links;
- An alternate location for the history file can be specified;
- Regexp patterns for excluding files in the backup can be provided;
- You can restore at any of the times the backups were made (the restore script
  has an option);
- The archives are simply stored as GNU tar files, so you can open them manually
  if so desired.

Caution
~~~~~~~

The arnie tools do *not* incrementally archive changes in user/group ids nor
access, modification or creation times (however, they could very easily be
modified to do so and I might do that at some point).  They do, however, track
permission changes, and obviously added files, deleted files, and file content
changes (the file comparison is carried out using a simple MD5 sum).

Also note that the incremental archives produced by these programs are not of
optimally minimal size, i.e. we do not store diffs, but rather we store entire
files when they change, and we do not track file location moves.  Therefore this
might not be a suitable solution if you have a large binary file from which only
a few blocks are changing between backups (the entire file will be backed up
every time).  Our solution is meant to work well on directories with many small
to intermediate size files (such as a CVS source code repository).


Documentation
=============

There is no special manual, the manual consists in this README file and the
``--help`` switch will provide ample details about invocation. Run the scripts
like this to get full details::

   arnie-archive --help

Other files:

- `CHANGES <CHANGES>`_ *(news, recent changes, history)*;
- `TODO <TODO>`_ *(future features, wishlist)*;
- `Design Notes (Internal Notes) <doc/arnie-design.html>`_;


Download
========

A Mercurial repository can be found at:

  http://github.com/blais/arnie


Installation and Packaging
==========================

Simply copy the ``arnie/bin/arnie-archive`` and ``arnie/bin/arnie-restore`` scripts to
``/usr/bin``.


Testing
=======

If you want to run the test suite, download the source code and see the
instructions under the ``test`` subdirectory (very simple, one Python script to
run).  In case you have a question, it should be extremely easy to add new tests
to the test code.


Reporting Bugs
==============

Send email to the author: Martin Blais <blais@furius.ca>.

If you would like to add new features, please contact the author for advice.
Please contribute your changes or additional test code back to the author, we
will be happy to include your changes if they are generic and could benefit
others.


Installation
============

Dependencies
------------

We have tried to minimize the dependencies of the arnie scripts in order to keep
them simple and working in as many environments as posarniele.

- Python 2.4 or greater;

- If you use encryption of the archives, you need to have GnuPG installed (the
  gpg executable);

- If you send files to a remote host from the archive script, you need to have
  the ssh and scp clients installed.

We invoke the client programs rather than use Python bindings for these last few
options, in order to avoid yet more dependencies.


Portability
-----------

We have not tested arnie under Windows yet, but there is no reason why it should
not work.  If you encounter problems or success using it on Windows, please let
me know via email.


External Links
==============

- `Official Homepage <http://furius.ca/arnie>`_
- `Freshmeat Application Index <http://freshmeat.net/projects/arnie>`_
- `Author's Homepage <http://furius.ca>`_

Other Projects
--------------

`Duplicity <http://duplicity.nongnu.org/>`_ is enjoying a recent
revival (2006-2007).  It uses librsync, so it is more efficient than
what arnie is doing (it needs not send entire files over to the remote
network).


Copyright, License and Disclaimer
=================================

Copyright (C) 2005  Martin Blais.  All Rights Reserved.
This code is distributed under the `GNU General Public License <COPYING>`_;

We are *NOT* responsible for any data loss resulting from the use of these
programs.  Please test your backups regularly, this is *YOUR* responsibility.
If you do not test your backups, you do *NOT* have backups.  Test the archive
and restore on the actual data that you will use it own as well.  If you don't
understand the importance of this, we suggest you do not use the software.


Author
======

Martin Blais <blais@furius.ca>
