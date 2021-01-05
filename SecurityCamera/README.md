# Security Camera Scripts
About: These scripts were created to backup the security footage from the "improvised security camera system" in our inventory room to Google Drive.
This "improvised security camera system" was created by... you guessed it - yours truly.
Anyway, I needed to have all of this footage backed up in case the computer that was hosting the footage crashed or something of that sort.

How It Works:
This was all able to be done utilizing the rclone API. The rclone_backup.sh is being initialized by a crontab each night at 23:50.
The script goes through the DVR's directory on the computer and shuffles them around until they're on Google Drive.
network_check.sh was created to verify that the laptop that was doing the backup was connected to the network as it would regularly drop connection - it's NO LONGER IN USE as we just got an ethernet cable to resolve the issue
The network_check.sh would ping Google to verify that there was an internet connection. If it wasn't able to ping Google successfully, it would reconnect the wifi and email me the new ip address.
If you're curious to know more about the "imporvised security camera system" feel free to shoot me an email at millerlm012@gmail!

Future Upgrades:
- having a dedicated email address for rclone to use when backing up to Google Drive - currently it's using my work email
