#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  pySysAdsBlock.py
#
#  07/27/2013
#  Copyright 2013 arnpi <arnpi@gmx.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
# Questions reponses sur le hosts file -> "http://doc.ubuntu-fr.org/hosts"

import sys
import argparse
import settings

if settings.DEBUG:
    print str(sys.argv)

parser = argparse.ArgumentParser(description='Add a blacklist to your hosts file.')
parser.add_argument('-g', '--gui', help="GUI interface, default value: wx (wxpython)", nargs='?', const="wx", choices=["wx", "gtk", "qt"])
parser.add_argument('-c', '--cli', help="Command line action", nargs=1, choices=['status', 'allow', 'block'])

args = parser.parse_args()

# if args.verbosity:
#    print "verbosity turned on"
if args.cli:
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
