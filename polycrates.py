#!/usr/bin/python

import sys
import os
import re
import ctypes
from subprocess import *

if sys.platform == "linux" or sys.platform == "linux2":
    def showInvalidArgError():
        print "This script takes a single directory for its arguments."
    convert_path = '/usr/local/bin/convert'
    convert_cmd = convert_path
    def showIMError():
        print "ImageMagick was not found in %s." % convert_path
    def showIMVersionWarning(version):
        print "ImageMagick version %s has not been tested." % version
elif sys.platform == "darwin":
    def showInvalidArgError():
        call("""osascript -e 'tell app "Finder" to display dialog "You must drop a folder onto this application."'""", shell=True)
    convert_path = '/usr/local/bin/convert'
    convert_cmd = convert_path
    def showIMError():
        call("""osascript -e 'tell app "Finder" to display dialog "You must first install ImageMagick to use this application."'""", shell=True)
    def showIMVersionWarning(version):
        call("""osascript -e 'tell app "Finder" to display dialog "ImageMagick version %s has not been tested." % version'""" % version, shell=True)
elif sys.platform == "win32":
    def showInvalidArgError():
        MessageBox = ctypes.windll.user32.MessageBoxA
        MessageBox(None, 'You must drop a folder onto this application.', 'Error:', 0)
    convert_path = [x for x in check_output('where convert').splitlines() if 'ImageMagick' in x].pop()
    convert_cmd = convert_path
    def showIMError():
        MessageBox = ctypes.windll.user32.MessageBoxA
        MessageBox(None, 'You must drop a folder onto this application.', 'Error:', 0)
    def showIMVersionWarning(version):
        MessageBox = ctypes.windll.user32.MessageBoxA
        MessageBox(None, "ImageMagick version %s has not been tested." % version, 'Warning:', 0)
            

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
im_version = check_output([convert_cmd, '-version']).split(' ')[2]
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
	call([convert_cmd, os.path.join(src_dir,f), os.path.join(pres_dir,root + '_tmp_%02d.png')])
	prev = os.path.join(pres_dir, root + '_01.png')
	call([convert_cmd, '-flatten', os.path.join(pres_dir, root + '_tmp_01.png'), prev])

	os.remove(os.path.join(pres_dir, root + '_tmp_00.png'))
	os.remove(os.path.join(pres_dir, root + '_tmp_01.png'))

	N = sum( 1 for t in os.listdir(pres_dir) if re.match(root + '_tmp_[0-9][0-9].png', t) )

	if N == 0:
		continue

	for j in range(2 , N+2):
		now = os.path.join(pres_dir, root+'_%02d.png' % j)
		tmp = os.path.join(pres_dir, root + '_tmp_%02d.png' % j)
		call([convert_cmd, prev, tmp , '-composite', now])
		os.remove(tmp)
		prev = now 

#Creating smaller files for upload
for f in os.listdir(pres_dir):
		if len(f) < 4 or f[-4:] != '.png':
			continue
		call([convert_cmd, os.path.join(pres_dir, f), '-resize', '25%', os.path.join(upload_dir,f)])