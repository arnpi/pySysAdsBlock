pySysAdsBlock
============

*System ads block*

This program will add http://someonewhocares.org/hosts/hosts to your /etc/hosts file.

All hosts in the file will go to 127.0.0.1 (If your Apache server is listening this IP, you should change this ...)

Works in command line or gui and systray icon.

You can revert this operation.

You can keep, add or modify /etc/hosts lines before the marker "# - - - S T O P - E D I T - H E R E - - - #"


Needs root user.


https://www.python.org/download/releases/2.7.6/

http://www.wxpython.org/download.php

Debian install
==============

apt-get install python-wxgtk2.8 (only if you wish the gui interface)

chmod +x pySysAdsBlock.py

./pySysAdsBlock.py help


How to use
==========

* Launch the script without argument  start help
* "./pySysAdsBlock.py help" start this help
* "./pySysAdsBlock.py allow" restore your /etc/hosts file
* "./pySysAdsBlock.py block" add the blacklist to your /etc/hosts
* "./pySysAdsBlock.py status" print your /etc/hosts count lines
* "./pySysAdsBlock.py wx" will start the default interface (wXpython)

Settings
========

You can change the hostfile provider in settings.py: It's a Python list, you can add several provider and choose the default one with DEFAULT_PROVIDER variable:

PROVIDER = ["http://someonewhocares.org/hosts/hosts"]

DEFAULT_PROVIDER = 0

