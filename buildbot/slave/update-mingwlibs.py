#!/usr/bin/env python

import os, subprocess, shutil
import prepare

MINGWLIBS_PATH = os.environ.get("MINGWLIBS_PATH", "vclibs")
print(f'MINGWLIBS_PATH={MINGWLIBS_PATH}')

assert(len(MINGWLIBS_PATH) > 0)

if not os.path.isdir(MINGWLIBS_PATH):
	print("cloning mingwlibs git-repo...")
	subprocess.call(["git", "clone", "git://github.com/spring/vclibs14.git", MINGWLIBS_PATH])
else:
	process = subprocess.Popen(["git", "fetch"], cwd=MINGWLIBS_PATH, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr = process.communicate()
	output = stdout + stderr
	print(output)
	if len(output) > 0:
		print(f"removing builddir {prepare.BUILDDIR} (mingwlibs updated)")
		shutil.rmtree(prepare.BUILDDIR)
		subprocess.call(["git","clean", "-f", "-d"], cwd=MINGWLIBS_PATH)
		subprocess.call(["git","reset", "--hard", "origin/master"], cwd=MINGWLIBS_PATH)

