whf-plays-pokemon
=================

All the scripts used in April's Fool 2014.

####  Overview

    stream.sh   - used to stream screen and sound to Twitch
    ircbot.py   - IRC bot for controlling VisualBoyAdvance
    html/       - alternative front page used during the prank

#### Requirements

 - Python 3.1 or higher
 - Visual Boy Advance (SDL Version)
 - ffmpeg with x11grab, libx264 and libmp3lame for streaming
 - PulseAudio as a monitor for audio recording (works with internal dummy output, no sound hardware needed)
 - Either one of the following for sending key commands to VBA:
  - [python-uinput](http://tjjr.fi/sw/python-uinput/)
    Using Linux' uinput module
  - [xdotool](http://www.semicomplete.com/projects/xdotool/)
    Generating keyboard events in X11
 - [python-irc](https://bitbucket.org/jaraco/irc)
   for receiving commands from an IRC channel

#### Acknowledgement

Idea and implementation by [@DosAmp](https://github.com/DosAmp)
