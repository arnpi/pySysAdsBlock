#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import sysAdsBlock


def run(arg):
    if arg == "allow":
        print "RESTORE THE /etc/hosts"
        sab = sysAdsBlock.Sysadsblock()
        sab.yes_ads()
        lastModification = time.ctime(os.stat(sab.config["etcHost"]).st_mtime)
        print "Actually the " + sab.config["etcHost"] + " file contains " + str(sab.countLine(sab.config["etcHost"])) + " lines.\n" + lastModification
    elif arg == "block":
        print "BLOCK BAD SITE"
        sab = sysAdsBlock.Sysadsblock()
        sab.no_ads()
        lastModification = time.ctime(os.stat(sab.config["etcHost"]).st_mtime)
        print "Actually the " + sab.config["etcHost"] + " file contains " + str(sab.countLine(sab.config["etcHost"])) + " lines.\n" + lastModification
    elif arg == "status":
        print "/etc/hosts STATUS"
        sab = sysAdsBlock.Sysadsblock()
        lastModification = time.ctime(os.stat(sab.config["etcHost"]).st_mtime)
        print "Actually the " + sab.config["etcHost"] + " file contains " + str(sab.countLine(sab.config["etcHost"])) + " lines.\n" + lastModification
    elif arg == "gtk":
        print "GTK interface not done"
    elif arg == "help":
        print "HELP interface not done"
    else:
        pass
