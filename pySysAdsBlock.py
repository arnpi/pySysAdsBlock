#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys

import settings
import time
import sysAdsBlock




print str(sys.argv)


if len(sys.argv) == 1:
    import interfaceWx
    from wx.lib.embeddedimage import PyEmbeddedImage
    app = interfaceWx.wx.App(False)
    frame = interfaceWx.MainWindow(None, settings.PROGRAM_NAME)
    app.MainLoop()
elif len(sys.argv) == 2:
    if sys.argv[1] == "allow":
        print "RESTORE THE /etc/hosts"
        sab = sysAdsBlock.Sysadsblock()
        sab.yes_ads()
        lastModification = time.ctime(os.stat(sab.config["etcHost"]).st_mtime)
        print "Actually the "  +  sab.config["etcHost"] + " file contains " + str(sab.countLine(sab.config["etcHost"])) + " lines.\n" + lastModification
    elif sys.argv[1] == "block":
        print "BLOCK BAD SITE"
        sab = sysAdsBlock.Sysadsblock()
        sab.no_ads()
        lastModification = time.ctime(os.stat(sab.config["etcHost"]).st_mtime)
        print "Actually the "  +  sab.config["etcHost"] + " file contains " + str(sab.countLine(sab.config["etcHost"])) + " lines.\n" + lastModification
    elif sys.argv[1] == "status":
        print "BLOCK BAD SITE"
        sab = sysAdsBlock.Sysadsblock()
        lastModification = time.ctime(os.stat(sab.config["etcHost"]).st_mtime)
        print "Actually the "  +  sab.config["etcHost"] + " file contains " + str(sab.countLine(sab.config["etcHost"])) + " lines.\n" + lastModification
    elif sys.argv[1] == "gtk":
        print "GTK interface not done"
    elif sys.argv[1] == "help":
        print "HELP interface not done"
    else:
        import interfaceWx
        from wx.lib.embeddedimage import PyEmbeddedImage
        app = interfaceWx.wx.App(False)
        frame = interfaceWx.MainWindow(None, settings.PROGRAM_NAME)
        app.MainLoop()
else:
    import interfaceWx
    from wx.lib.embeddedimage import PyEmbeddedImage
    app = interfaceWx.wx.App(False)
    frame = interfaceWx.MainWindow(None, settings.PROGRAM_NAME)
    app.MainLoop()
