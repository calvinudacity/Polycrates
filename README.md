# Polycrates
===============

Polycrates is an python script that separates and stacks the layers of PSD files into separate png files.  It takes a folder srcdir as its single argument, and for each PSD file f in the folder, it generates a sequence of png files of the form $f_01.png, $f_02.png, … $f_$N.png, where N is the number of layers in $f.psd.  It then places these files in a folder $srcdir_presentation.  It also resizes these files to 25% of the original size and places them in a folder $srcdir_upload.

Suppose that a file Images/A.psd has 4 layers and a file Images/B.psd has 2 layers.  The running the script on the folder Images will produce create a folder Images_presentation

	Images_presentation/
		A_01.png
		A_02.png
		A_03.png
		A_04.png
		B_01.png
		B_02.png

and a parallel folder Images_upload with the smaller images.

## MacOS Installation
The script depends on python and the ImageMagick library.  Python is installed by default on MacOS.

### Installing ImageMagick on MacOS
First, test to see if you have ImageMagick's command line tools already.  Typing

    $ which convert

in the Terminal should give the path to an executable (often in /usr/local/bin but sometimes in a user's diretory).  To confirm that this is the correct convert executable, type

    $ convert logo: logo.gif
    $ open logo.gif
which should open an image of a wizard.

If this fails, then install ImageMagick with [Homebrew](http://brew.sh/).  To install Homebrew itself run in the Terminal

	$ ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"

If you haven't already, you should also run

	$ sudo brew doctor
	
Assuming that everything went okay, you may then install ImageMagick with

	$ sudo brew install imagemagick


### Creating a Droplet on MacOS
To convert the script to a droplet in Finder

1. Open Automator from the Applications folder
2. Choose Workflow for the type of Document
3. Drag "Run Shell Script" (under Utilities) from the Actions Menu to the workflow.
4. Change the "Pass input" selector to "as arguments."
5. Copy and paste the contents of polycrates.pys to replace the default script.
6. Save and choose Application as the file format.

## Windows Installation
The script depends on pythonwin32 and the ImageMagick library.

### Installing Python on Windows
Download [pywin32](http://sourceforge.net/projects/pywin32/files/pywin32/) (python extension for windows), choosing the latest version for python 2.7.

To confirm that python was installed properly, type

	python --version

in the cmd window, which should give the version (e.g. Python 2.7.2).

### Installing ImageMagick on Windows
To test if ImageMagick is installed already, type in a cmd window

    $ convert logo: logo.gif
    $ imdisplay logo.gif

which should display an image of a wizard.

If this fails, then download the latest binary release from [here](http://imagemagick.org/script/binary-releases.php#windows).  Repeat the test above.

### Creating a Droplet on Windows
Simply copy the file polycrates.py to the desired location and add shortcuts to suite the user needs.  With pywin32 installed, Windows should recognize the file an a python script from the .py suffix.

## Contact
Please direct equations to Charles Brubaker at cb@udacity.com.








