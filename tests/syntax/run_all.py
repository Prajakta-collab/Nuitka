#!/usr/bin/env python
#
#     Copyright 2012, Kay Hayen, mailto:kayhayen@gmx.de
#
#     Python test originally created or extracted from other peoples work. The
#     parts and resulting tests are too small to be protected and therefore
#     is in the public domain.
#
#     If you submit Kay Hayen patches to this in either form, you automatically
#     grant him a copyright assignment to the code, or in the alternative a BSD
#     license to the code, should your jurisdiction prevent this. Obviously it
#     won't affect code that comes to him indirectly or code you don't submit to
#     him.
#
#     This is to reserve my ability to re-license the official code at any time,
#     to put it into public domain or under PSF.
#
#     Please leave the whole of this copyright notice intact.
#

from __future__ import print_function

import os, sys, subprocess, tempfile, shutil

# Go its own directory, to have it easy with path knowledge.
os.chdir( os.path.dirname( os.path.abspath( __file__ ) ) )

search_mode = len( sys.argv ) > 1 and sys.argv[1] == "search"

start_at = sys.argv[2] if len( sys.argv ) > 2 else None

if start_at:
    active = False
else:
    active = True

if "PYTHON" not in os.environ:
    os.environ[ "PYTHON" ] = "python"

version_output = subprocess.check_output(
    [ os.environ[ "PYTHON" ], "--version" ],
    stderr = subprocess.STDOUT
)

python_version = version_output.split()[1]

os.environ[ "PYTHONPATH" ] = os.getcwd()

print( "Using concrete python", python_version )

for filename in sorted( os.listdir( "." ) ):
    if not filename.endswith( ".py" ) or filename == "run_all.py":
        continue

    path = filename

    if not active and start_at in ( filename, path ):
        active = True

    extra_flags = [ "expect_failure" ]

    if active:
        result = subprocess.call(
            "%s %s %s silent %s" % (
                sys.executable,
                os.path.join( "..", "..", "bin", "compare_with_cpython" ),
                path,
                " ".join( extra_flags )
            ),
            shell = True
        )

        if result == 2:
            sys.stderr.write( "Interruped, with CTRL-C\n" )
            sys.exit( 2 )

        if result != 0 and search_mode:
            print("Error exit!", result)
            sys.exit( result )
    else:
        print("Skipping", filename)
