#!/bin/bash

src_dir=${1%%/}

if [ $# != 1 ] || [ ! -d $src_dir ]; then
	osascript -e 'tell app "Finder" to display dialog "You must drop a folder onto this application."'
	exit 1
fi

if [ -z $(which convert) ]; then
	osascript -e 'tell app "Finder" to display dialog "You must first install ImageMagick to use this application."'
	exit 1
fi

im_version=$(convert -version | grep "Version:" | cut -d' ' -f 3)
if [[ $im_version != 6.8.3-3 ]]; then
	osascript -e 'tell app "Finder" to display dialog "Warning: This script has only been tested with ImageMagick 6.8.3-3.  Script will proceed."'
fi

export PATH=/usr/local/bin:"$PATH"

pres_dir=${src_dir}_presentation
upload_dir=${src_dir}_upload

if [ ! -d $pres_dir ]; then
	mkdir $pres_dir
fi

if [ ! -d $upload_dir ]; then
	mkdir $upload_dir
fi

#For each file in the src
for i in $(ls $src_dir)
	do
		if [ "${i: -4}" != ".psd" ]; then
			continue
		fi
		root=${i%.psd}
		convert ${src_dir}/${i} ${pres_dir}/${root}_tmp_%02d.png
		convert -background white ${pres_dir}/${root}_tmp_01.png ${pres_dir}/${root}_01.png

		rm ${pres_dir}/${root}_tmp_0[0-1].png

		N=$(ls $pres_dir | grep ${root}_tmp_ | wc -l | tr -d ' ')

		if [ $N == "0" ]; then
			continue
		fi

		prev=01
		for j in $(seq -f %02g 2 $[${N}+1])
			do
				convert ${pres_dir}/${root}_${prev}.png ${pres_dir}/${root}_tmp_${j}.png -composite ${pres_dir}/${root}_${j}.png
				rm ${pres_dir}/${root}_tmp_${j}.png
				prev=${j}
			done

done

#For each file in the pres_dir
for i in $(ls $pres_dir)
	do
		root=${i%.png}
		if [ "${i: -4}" != ".png" ]; then
			continue
		fi
		convert ${pres_dir}/${root}.png -resize 25% ${upload_dir}/${root}.png
done
