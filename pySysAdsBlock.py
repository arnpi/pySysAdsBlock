#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
import settings
import time
import sysAdsBlock

if settings.DEBUG : print  str(sys.argv)

def help():
    print """
    This program needs root privileges\n
    (e.g. sudo ./pySysAdsBlock.py [argument])\n
    Depend python\n
    * Launch the script without argument  start this help\n
    * "./pySysAdsBlock.py help" start this help\n
    * "./pySysAdsBlock.py allow" restore your /etc/hosts file\n
    * "./pySysAdsBlock.py block" add the blacklist to your /etc/hosts\n
    * "./pySysAdsBlock.py status" print your /etc/hosts count lines\n
    * "./pySysAdsBlock.py wx" will start the default interface (wXpython)\n
    (On Debian needs python-wxgtk2.8)\n
    * "./pySysAdsBlock.py gtk" will start the gtk interface (not implemented yet)\n
    """
    
if len(sys.argv) == 1:
        help()
elif len(sys.argv) == 2:
    if sys.argv[1] == "allow":
        print "RESTORE THE /etc/hosts"
        import interfaceCli
        interfaceCli.runCli("allow")
    elif sys.argv[1] == "block":
        print "BLOCK BAD SITE"
        import interfaceCli
        interfaceCli.runCli("block")
    elif sys.argv[1] == "status":
        print "STATUS /etc/hosts/"
        import interfaceCli
        interfaceCli.runCli("status")
    elif sys.argv[1] == "wx":
        import interfaceWx
        from wx.lib.embeddedimage import PyEmbeddedImage
        app = interfaceWx.wx.App(False)
        frame = interfaceWx.MainWindow(None, settings.PROGRAM_NAME)
        app.MainLoop()
    elif sys.argv[1] == "gtk":
        print "GTK interface not done"
    elif sys.argv[1] == "help":
        help()
    else:
        help()
else:
        help()
