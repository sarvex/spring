#!/usr/bin/env python3

import prepare
import os, subprocess, sys, shutil


CMAKEPARAM=[]
if 'CMAKEPARAM' in os.environ:
	CMAKEPARAM=os.environ['CMAKEPARAM'].split(" ")

CMAKEBIN = os.environ.get('CMAKEBIN', 'cmake')
print(f"Creating BUILDDIR: {prepare.BUILDDIR}")
if not os.path.isdir(prepare.BUILDDIR):
	os.makedirs(prepare.BUILDDIR)

basedir = os.path.join(prepare.BUILDDIR, 'base')
if os.path.isdir(basedir):
	print(f"erasing old base content... {basedir}")
	shutil.rmtree(basedir)

print(
	f"configuring {prepare.SOURCEDIR} with {CMAKEBIN} {CMAKEPARAM + sys.argv[3:]} in {prepare.BUILDDIR}"
)
subprocess.call([CMAKEBIN] + CMAKEPARAM + sys.argv[3:] + [prepare.SOURCEDIR], cwd=prepare.BUILDDIR)
subprocess.call([prepare.MAKE, "generateSources", "-j1"], cwd=prepare.BUILDDIR)

