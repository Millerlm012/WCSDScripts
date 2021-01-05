# Variables
today=$(date +"%Y_%m_%d")
today_with_time=$(date +"%Y_%m_%d_%T")

# Navigates to rm-108 directory under current user directory
cd ~/Documents/videos

# Create directory named current date YYYY/MM/DD
mkdir $today

# if statement
if ls Video* >/dev/null 2>&1;
then

	# List all video files in the videos directory and saves it to a txt file with current date & time
	ls Video* > files_uploaded_$today_with_time.txt

	# Move all video files into current date directory
	mv *.mov ~/Documents/videos/$today
	mv *.txt ~/Documents/videos/$today

	# Change working directory to today directory
	cd ~/Documents/videos/$today

	# counts how many files are in the videos directory and saves it to a textfile
	ls | wc -l > count_uploaded_$today_with_time.txt

	# Move current date directory into rm-108
	mv ~/Documents/videos/$today ~/Documents/rm-108/

	# Change working directory to rm-108
	cd ~/Documents/rm-108

	# Use rclone to move all videos and log files to google-drive:rm-108
	/usr/local/Cellar/rclone/1.53.2/bin/rclone move /Users/localadmin/Documents/rm-108 google-drive:rm-108

	# Remove leftover folders as rclone keeps original directory
	rm -rf $today

else
  	# If no video files recorded, create txt file indicating no files uploaded with current date and time
	echo "No files to upload_$today_with_time" > ~/Documents/videos/$today/Log_$today.txt

	# Move all text files into current date directory
	mv *.txt ~/Documents/videos/$today

	# Change working directory to today directory
	cd ~/Documents/videos/$today

	# counts how many files are in the videos directory and saves it to a textfile
	ls | wc -l > count_uploaded_$today_with_time.txt

	# Move current date direction into rm-108
	mv ~/Documents/videos/$today ~/Documents/rm-108/

	# Change working directory to rm-108 directory
	cd ~/Documents/rm-108

  	# Use rclone to upload log files to google-drive:rm-108
 	/usr/local/Cellar/rclone/1.53.2/bin/rclone move /Users/localadmin/Documents/rm-108 google-drive:rm-108

  	# Remove leftover folders as rclone keeps original directory
	rm -rf $today
fi
