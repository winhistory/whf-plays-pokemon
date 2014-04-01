#!/bin/sh
ffmpeg -f x11grab -s 1280x720 -i :0.0 -f alsa -i pulse -codec:v libx264 -preset medium -pix_fmt yuv420p -codec:a libmp3lame -ar 44100 -qscale:a 4 -b:v 800k -bufsize 512k -f flv "rtmp://live-ams.twitch.tv/app/live_XXXXXXXX_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
