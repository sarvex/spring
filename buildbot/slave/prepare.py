# This file is included by the other shell scripts to set up some variables.
# Each of the scripts (including this) gets 2 arguments: <config> <branch>

# It sets the following variables:
# - CONFIG   : configuration (default, debug, syncdebug, etc.)
# - BRANCH   : branch (master, etc.)
# - CONFIG_  : $CONFIG wrapped in [] or empty if CONFIG=default
# - BRANCH_  : $BRANCH wrapped in {} or empty if BRANCH=master
# - REV      : output of `git describe --tags'
# - SOURCEDIR: absolute path to the source directory
# - BUILDDIR : absolute path to the build directory
# - TMP_BASE : folder for temporary work items
# - TMP_PATH : $TMP_BASE/$CONFIG/$BRANCH/$REV
# - VERSION_ : version string, unsafe, may include special characters
# - VERSION  : sanitized version string, suitable for filenames

# Quit on error.

import os, sys, subprocess, tempfile


if len(sys.argv) < 2:
	print(f"Please run with {sys.argv[0]} <config> <branch>")
	exit(1)


print(sys.argv)
CONFIG=sys.argv[1]
BRANCH=sys.argv[2]

REV=subprocess.check_output(["git", "describe", "--abbrev=7", "--tags"], universal_newlines=True).strip()
SOURCEDIR=os.getcwd()
BUILDDIR=os.path.join(os.getcwd(), "build", CONFIG)
TMP_BASE=os.path.join(tempfile.gettempdir(), "spring")
TMP_PATH=os.path.join(TMP_BASE, CONFIG, BRANCH, REV)

if 'OUTPUTDIR' in os.environ:
	TMP_PATH=os.path.join(TMP_PATH, os.environ['OUTPUTDIR'])

CONFIG_ = '' if CONFIG == "default" else f"[{CONFIG}]"
BRANCH_ = '' if BRANCH == "master" else "{%s}" % (BRANCH)
VERSION_ = f"{CONFIG_}{BRANCH_}{REV}"
for char in "<>:\"/\\|?*":
	VERSION_=VERSION_.replace(char,'')

print(f"Detected VERSION_: {VERSION_}")

if 'MAKE' in os.environ:
	MAKE=os.environ['MAKE']
else:
	print("MAKE isn't set, using 'make' as default")
	MAKE="make"

