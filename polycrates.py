#!/usr/bin/python
import sys
import os
import re
from subprocess import *

if sys.platform == "linux" or sys.platform == "linux2":
		def showInvalidArgError():
			print "This script takes a single directory for its arguments."
		convert_path = '/usr/local/bin/convert'
		def showIMError():
			print "ImageMagick was not found in %s." % convert_path
elif sys.platform == "darwin":
		def showInvalidArgError():
			call("""osascript -e 'tell app "Finder" to display dialog "You must drop a folder onto this application."'""", shell=True)
		convert_path = '/usr/local/bin/convert'
		def showIMError():
			call("""osascript -e 'tell app "Finder" to display dialog "You must first install ImageMagick to use this application."'""", shell=True)
elif sys.platform == "win32":
		def showInvalidArgError():
			call('Msg * "You must drop a folder onto this application."', shell=True)
		convert_path = 'C:\Windows\System32\convert.exe'
		def showIMError():
			call('Msf * "You must first install ImageMagick to use this application."', shell=True)

def isKnownIMVersion(v):
	return v >= '6.8.3-3'

#Checking arguments
if len(sys.argv) != 2 or not os.path.isdir(sys.argv[1]):
	showInvalidArgError()
	sys.exit(1)

#Checking for ImageMagick
if not os.path.exists(convert_path):
	showIMError()
	sys.exit(1)

#Checking ImageMagick Version
im_version = check_output(['convert', '-version']).split(' ')[2]
if not isKnownIMVersion(im_version):
	print "Warning: version %s is not known to work with this script." % im_version

#Setting up directories
src_dir = sys.argv[1].rstrip('\\/')
pres_dir = src_dir + '_presentation'
upload_dir= src_dir + '_upload'

if not os.path.isdir(pres_dir):
	os.mkdir(pres_dir)

if not os.path.isdir(upload_dir):
	os.mkdir(upload_dir)

#Pulling apart the layers
for f in os.listdir(src_dir):
	if len(f) < 4 or f[-4:] != '.psd':
			continue
	root = f[:-4]
	call(['convert', os.path.join(src_dir,f), os.path.join(pres_dir,root + '_tmp_%02d.png')])
	prev = os.path.join(pres_dir, root + '_01.png')
	call(['convert', '-background', 'white', os.path.join(pres_dir, root + '_tmp_01.png'), prev])

	os.remove(os.path.join(pres_dir, root + '_tmp_00.png'))
	os.remove(os.path.join(pres_dir, root + '_tmp_01.png'))

	N = sum( 1 for t in os.listdir(pres_dir) if re.match(root + '_tmp_[0-9][0-9].png', t) )

	if N == 0:
		continue

	for j in range(2 , N+2):
		now = os.path.join(pres_dir, root+'_%02d.png' % j)
		tmp = os.path.join(pres_dir, root + '_tmp_%02d.png' % j)
		call(['convert', prev, tmp , '-composite', now])
		os.remove(tmp)
		prev = now 

#Creating smaller files for upload
for f in os.listdir(pres_dir):
		if len(f) < 4 or f[-4:] != '.png':
			continue
		call(['convert', os.path.join(pres_dir, f), '-resize', '25%', os.path.join(upload_dir,f)])
