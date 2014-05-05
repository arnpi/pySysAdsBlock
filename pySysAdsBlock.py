#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, time
import argparse
import settings
import sysAdsBlock

if settings.DEBUG : print  str(sys.argv)


parser = argparse.ArgumentParser(description='Add a blacklist to your hosts file.')
parser.add_argument('-g', '--gui', help="GUI interface, default value: wx (wxpython)",nargs='?', const="wx", choices=["wx", "gtk", "qt"] )
parser.add_argument('-v', "--verbosity", help="increase output verbosity", nargs=1, choices=['0', '1'])
parser.add_argument('-c', '--cli', help="Command line action", nargs=1, choices=['status', 'allow', 'block'])

args = parser.parse_args()

print(args)
if args.verbosity:
    print "verbosity turned on"
if args.cli:
    print args.cli
    import interfaceCli
    interfaceCli.run(args.cli[0])
elif args.gui:
    if args.gui == "wx":
        import interfaceWx
        interfaceWx.run() 
    elif args.gui == "gtk":
        print "GTK GUI not done"
    elif args.gui == "qt":
        print "QT GUI not done"
exit()


