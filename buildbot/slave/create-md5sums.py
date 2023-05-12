#!/usr/bin/env python3

import prepare
import hashlib, sys, os

path = prepare.TMP_BASE
suffixes = sys.argv[3:] # config + branch are used in prepare.py
suffix = ".md5"

def hashfile(filename, blocksize=4096):
	hasher = hashlib.md5()
	f = open(filename, "rb")
	buf = f.read(blocksize)
	while len(buf) > 0:
		hasher.update(buf)
		buf = f.read(blocksize)
	return hasher.hexdigest()

def createhash(filename, md5):
	with open(md5, 'wb') as f:
		hexdigest = hashfile(filename)
		line = f"{hexdigest} {os.path.basename(filename)}"
		f.write(str.encode(line))
	return hexdigest

def verify(fn, md5):
	f = open(md5, "rb").read().decode("utf-8")
	hexdigest, filename = f.split(" ", 1)
	if filename != os.path.basename(fn):
		print(f"Invalid file: {filename} {fn}")
		return False, ""
	h = hashfile(fn)
	return h == hexdigest, h

def handlefile(f, suffixes, suffix):
	if f.endswith(suffix):
		return
	basename = os.path.basename(f)

	skip = not any(basename.endswith(s) for s in suffixes)
	if skip: return

	md5file = f + suffix
	if os.path.isfile(md5file):
		res, h = verify(f, md5file)
		print(f"Verifying {h}: {f} - {res}")
	else:
		h = createhash(f, md5file)
		print(f"Creating {h}: {md5file}")


for root, directories, filenames in os.walk(path):
	for filename in filenames:
		handlefile(os.path.join(root, filename), suffixes, suffix)

