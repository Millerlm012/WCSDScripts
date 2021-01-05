# DESCRIPTION: Verifies computer is connected to network

host="www.google.com"
x=0

ping -c1 "$host" &> /dev/null

# if computer pings the address and 0 packet loss - all is well
if [ $? -eq 0 ]; then

    echo "Connected to network and all is well."

# if there is packet loss reconnect to the network and try again
else

   while [ x=0 ]
   do
       echo "Not connected to network... Attempted to reconnect and will verify connection status in 30 seconds"
       networksetup -setairportnetwork en0 WCSD-Lab-Computers
       sleep 30

       ping -c1 "$host" &> /dev/null
       if [ $? -eq 0 ];
       then

          echo "Successfully reconnected to network"
          ipconfig getifaddr en0 | mail -s "Rm-108 Camera Disconnected From Network: New IP Listed" lmiller@waukeeschools.org, mpolovina@waukeeschools.org
          x=$(( $x + 1))
          break

       else:
          
          echo "Was unable to reconnect... trying again"
          continue

      fi
   done
fi
