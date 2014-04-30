pySysAdsBlock
===========

*System ads block*

This program will add http://someonewhocares.org/hosts/hosts to your /etc/hosts file.

Works in command line or gui.


Needs root user.


https://www.python.org/download/releases/2.7.6/

http://www.wxpython.org/download.php

Debian install

apt-get install python-wxgtk2.8 (if you wish gui interface)

chmod +x pySysAdsBlock.py

./pySysAdsBlock.py help




* Launch the script without argument  start help
* "./pySysAdsBlock.py help" start this help
* "./pySysAdsBlock.py allow" restore your /etc/hosts file
* "./pySysAdsBlock.py block" add the blacklist to your /etc/hosts
* "./pySysAdsBlock.py status" print your /etc/hosts count lines
* "./pySysAdsBlock.py wx" will start the default interface (wXpython)
(On Debian needs python-wxgtk2.8)
