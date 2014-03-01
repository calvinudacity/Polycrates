# Polycrates
===============

Polycrates is an bash script intended to be used on MacOS that separates and stacks the layers of PSD files into separate png files.  It takes a folder srcdir as its single argument, and for each PSD file f in the folder, it generates a sequence of png files of the form $f_01.png, $f_02.png, … $f_$N.png, where N is the number of layers in f.psd.  It then places these files in a folder $srcdir_presentation.  It also resizes these files to 25% of the original size and places them in a folder $srcdir_upload.

Suppose that a file Images/A.psd has 4 layers and a file Images/B.psd has 2 layers.  The running the script on the folder Images will produce create a folder Images_presentation

	Images_presentation/
		A_01.png
		A_02.png
		A_03.png
		A_04.png
		B_01.png
		B_02.png

and a parallel folder Images_upload with the smaller images.

## Creating a Droplet
To convert the script to a droplet in Finder

1. Open Automator from the Applications folder
2. Choose Workflow for the type of Document
3. Drag "Run Shell Script" (under Utilities) from the Actions Menu to the workflow.
4. Change the "Pass input" selector to "as arguments."
5. Save and choose Application as the file format.

## Dependencies
The script uses [ImageMagick](http://imagemagick.org/).  It has only been tested with version 6.8.3-3 and will display a warning if it finds another version.

ImageMagick may be installed with [Homebrew](http://brew.sh/).  To install Homebrew itself run in the Terminal

	ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"
	
If you haven't already, you should also run

	sudo brew doctor
	
Assuming that everything went okay, you may then install ImageMagick with

	sudo brew install imagemagick

## Contact
Please direct equations to Charles Brubaker at cb@udacity.com.








