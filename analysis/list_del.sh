#!/bin/bash
cd '../scraping/spotify_data/playlist_tracks/user_curated'

if [ ! -d 'user_curated_del' ]; then
	mkdir '../user_curated_del'
fi

for d in */;
do 
	cd $d
	let count=0
	let lc=0
	let s_c=0
	for dir in */;
	do
		if [ -d $dir ]; then
			cd $dir
			for files in ./*.csv;
			do
				chmod u+r $files
				#line count (amount of songs added or removed)
				lc=`( wc -l <$files )`
				s_c=$(($lc+$s_c))
				
				#checking for playlists that never change (when count=30)
				#if [[ lc -eq 1 ]]; then
				#	let count++
				#fi

			done

		fi
		cd '..'
	done
	cd '..'
	if [[ $s_c -lt 50 ]]; then
		mv -v $d '../user_curated_del'
	fi
done
