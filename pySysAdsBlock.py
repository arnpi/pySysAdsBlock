#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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

# http get
import urllib
import urllib2
# regex
import re
# date
import time
# test file exist
import os
# Detect OS
import platform
# copy file
import shutil
# import ui.py QT4 GUI
import sys

import wx
from wx.lib.embeddedimage import PyEmbeddedImage
import base64

VERSION = '0.2'
PROGRAM_NAME = "pySysAdsBlock " + VERSION
PROVIDER = ["http://someonewhocares.org/hosts/hosts"]
PING_SITE = "google.com"
DEFAULT_PROVIDER = 0
ICON = PyEmbeddedImage("""
iVBORw0KGgoAAAANSUhEUgAAACAAAAAlCAYAAAAjt+tHAAADa0lEQVRYhbWXT0gUURzHP7Ot26Zm
FiGViAq1G6FZ9I8sAmutS2UG1Skt6dAhkAiCIPoDUrfCW0QUBh2isqI6xEq3tBIJyaDdPGRhhZa1
uW7btO102Pd0kpmdmd3tC49Z3nvM5zu/93tv30/RNA2A+vp6N+ACPOLpJrdKAElABZLBYDABoGia
JuEewCuaRxhw5QieFAZUIC6aGgwGE0ogEJDwfKBIPL38nwjEgRjwQzxV+ZVeAS/xq+GeHIP/Ucjj
Wy9+JoGEPvT5fjXc03yynTJfFQvKF+cU/HlokA/hATraWntCHl81Yhn0iecFHMEnImMoioKmaRTM
mZd27rR3yjxzuUmttWyW8N4H13n15K7h2NyF5axtOEipv8bKxCRTJppltr/pfkz3rUtp53z7NMTj
S2eYWTCbfaev4M7zpJvusgUG6LpyzhKu16+Jca4f30dkZNhyrqWBvkc3eP+61zZcrzvnj5D88ydz
A9Fvo/R33c4ILnXz7KHMDTxsP5EVHODn+HeGQ/3ODfyaGCcW+Zq1AYAX9685NxB6FswJHFK7w0ym
5/2nwYHJ3y0Xjfe9HV092ghA4rdquC1NIxCLjGUMNdKP0Y+G/aYGZqQ/RBxrhjvPsN90CeaXLebL
+7fAVBiz0ZySUsN+0whU1qw3G3IsxWW+201HFi6pzpmBZZu2OzcAsHr7/pwYWNdwMDMDy7fsBkXJ
Cl6753Daccs/o5YLnRnDK1duZGnttuwMgDiIHEaienMjdU3HLOfZvna3XOhk7c4DlvNmzS5m76nL
rNnRZOu98hxI2plcVddAVV0DI+9ChJ938Tv+k1hkjFlFxcxbVMGKrXttQfVMN6n7umx8Hhq0vBeW
VPgpqfA7gSHfLTTJdDFVLsUBPoQH9BNzJnktF4oLZlIJBAIeoBAoJk1h0nyynTX1u2zBeoP36Ghr
NRwThckI8B2IuklFIE6qXEIUDfrSzAXQ0db6FLA0IeEhj2+D6JL5Nb00iwNJO8Xp5B3er4b70kVC
B1/Fv7llXpxalOfyqS/fXhqZ0MFXiq+U66w3YFyep5Mw5iWVJ4XCRL/ehA5eI+BR0eISZCZLAyYm
CmUkAP2XR3EAt23AwESRMNEHyDWPkkou23BHBqaZyBdN3ttUUqGPOYE7NqAzIZNSblW5xVQncIC/
yQ9ry9ss54UAAAAASUVORK5CYII=
""")

def countLine(nf, fdl='\n', tbuf=16384):
    """Compte le nombre de lignes du fichier nf"""
    c = 0
    f = open(nf, 'rb')
    while True:
        buf = None
        buf = f.read(tbuf)
        if len(buf)==0:
            break
        c += buf.count(fdl)
    f.seek(-1, 2)
    car = f.read(1)
    if car != fdl:
        c += 1
    f.close()
    return c   
    
class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        self.config = self.configuration(self.detect_os())
        if self.check_install():
            print "Install OK"
        else:
            if self.installer():
                print "Installing ..."
            else:
                print "installing error"
                exit()
        wx.Frame.__init__(self, parent, title=title, size=(-1,-1))
        self.frameSizer = wx.BoxSizer(wx.VERTICAL)
        self.gridSizer = wx.GridSizer(5, 2, 0, 0)
        self.gridSizerButton = wx.GridSizer(1, 3, 0, 0)
        self.gridSizerText = wx.GridSizer(4, 1, 0, 0)
        self.panelButton = wx.Panel(self, 1)
        self.panelText = wx.Panel(self, 1)
                
        print "Création de l'interface"
        self.buttons1 = wx.Button(self.panelButton, 1, 'Remove blacklist', (-1,-1))
        self.buttons2 = wx.Button(self.panelButton, 2, 'Add blacklist', (-1,-1))
        self.buttons3 = wx.Button(self.panelButton, 3, 'Quit', (-1,-1))
        self.labelDynamic = wx.StaticText(self.panelText, 1, "Choose action", style = wx.ALIGN_LEFT, size = (-1,-1))
        self.labelFixe = wx.StaticText(self.panelText, 2, PROGRAM_NAME + " GPL", style = wx.ALIGN_LEFT, size = (-1,-1))
        self.gridSizer.Add(self.gridSizerButton, 0, wx.ALIGN_CENTRE)
        self.gridSizer.Add(self.gridSizerText, 0, wx.ALIGN_CENTRE)
        self.gridSizerButton.Add(self.buttons1, 0, wx.ALIGN_LEFT)
        self.gridSizerButton.Add(self.buttons2, 0, wx.ALIGN_LEFT)
        self.gridSizerButton.Add(self.buttons3, 0, wx.ALIGN_RIGHT)
        self.gridSizerText.Add(self.labelDynamic, 0, wx.ALIGN_LEFT)
        self.gridSizerText.Add(self.labelFixe, 0, wx.ALIGN_RIGHT)
        self.Bind(wx.EVT_BUTTON, self.yes_ads, id=1)
        self.Bind(wx.EVT_BUTTON, self.no_ads, id=2)
        self.Bind(wx.EVT_BUTTON, self.close_app, id=3)
        print "Création de la barre de statut"
        self.txtStatusBar = self.CreateStatusBar()
        self.txtStatusBar.SetStatusText(u"Waiting action ...")
        
        self.panelButton.SetSizer(self.gridSizerButton)
        self.panelText.SetSizer(self.gridSizerText)
        self.frameSizer.Add(self.panelButton, 1, wx.EXPAND)
        self.frameSizer.Add(self.panelText, 1, wx.EXPAND)
        self.SetSizer(self.frameSizer)
        self.frameSizer.SetSizeHints(self)
        self.labelDynamic.SetLabel(self.printCountLines())
        self.SetSizeHints(self.GetSize().x,self.GetSize().y,self.GetSize().x,self.GetSize().y );
        print "Icone systray"
        self.icoSystray = wx.TaskBarIcon()
        self.SetIcon(ICON.GetIcon())
        self.icoSystray.SetIcon(ICON.GetIcon())
        self.icoSystray.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)
        self.icoSystray.Bind(wx.EVT_TASKBAR_RIGHT_DOWN, self.on_right_down)
        self.hideStatut = True
        self.icoSystraymenu=wx.Menu()
        self.icoSystraymenu.Append(wx.ID_EXIT, "Close")
        self.icoSystraymenu.Append(1, "Remove blacklist")
        self.icoSystraymenu.Append(2, "Add blacklist")
        self.icoSystraymenu.Bind(wx.EVT_MENU, self.close_app, id=wx.ID_EXIT)
        self.icoSystraymenu.Bind(wx.EVT_MENU, self.yes_ads, id=1)
        self.icoSystraymenu.Bind(wx.EVT_MENU, self.no_ads, id=2)
        
        #self.Show()
        self.Bind(wx.EVT_CLOSE, self.on_close)
        
    def on_close(self, event):
        exit()
        self.Destroy()

    def on_right_down(self, event):
        print "Clique droit"
        self.PopupMenu(self.icoSystraymenu)

    def on_left_down(self, event):
        print "Clique gauche"
        if self.hideStatut == False:
            self.Hide()
            self.hideStatut = True
        else:
            self.Show()
            self.hideStatut = False
        
    def visit(self):
        print "visiting ", PROVIDER

    def detect_os(self):
        """
        detect os to know correct path, ect.
        Return array
        """
        print "detect_os()"
        systemEnv = {}
        systemEnv["sys"] = platform.system()
        systemEnv["release"] = platform.release()
        systemEnv["os"] = os.name
        systemEnv["arch"] = platform.architecture()[0]
        for el in systemEnv:
            print el + " = " + systemEnv[el]
        return systemEnv

    def configuration(self,systemEnv):
        """
        Generate personnal config with systemEnv from detect_os
        Return array
        """
        print "config()"
        config = {}
        # user path
        config["userPath"] = os.path.expanduser ("~")
        # System hosts file
        if systemEnv["sys"] == "Linux":
            config["etcHost"]  = "/etc/hosts"
            config["cmdPing"]  = "ping -c 1 " + PING_SITE
        elif systemEnv["sys"] == "Windows":
            config["etcHost"]  = "C:\WINDOWS\system32\drivers\etc\hosts"
            config["cmdPing"]  = "ping " + PING_SITE
        else:
            print "Only linux for the moment ..."
            showerror('Not implemented', 'Only linux for the moment ...')
            exit()
        # hosts file build by the app
        config["appHosts"]  = config["userPath"]  + os.sep +  ".hosts.pyDenyAll"
        # backup of user hosts file
        config["sysBckpHosts"] = config["etcHost"] + ".original"
        for el in config:
            print el + " = " + config[el]
        #exit()
        return config

    def test_connect(self):
        """
        Internet ping,
        Return Bool
        """
        print "test_connect()"
        if os.system(self.config["cmdPing"]):
            return False
        else:
            return True

    def check_install(self):
        """
        Check if user hosts file is backup
        """
        print "check_install()"
        if (os.path.isfile(self.config["sysBckpHosts"]) == True):
            return True
        else:
            return False

    def installer(self):
        """
        Create backup files
        Return Bool
        """
        print "installer()"
        shutil.copyfile(self.config["etcHost"], self.config["sysBckpHosts"])
        if self.check_install():
            return True
        else:
            return False

    def reinit(self):
        """
        Clear old app hosts file, create a new one
        Return Bool
        """
        print "reinit()"
        if (os.path.isfile(self.config["appHosts"]) == True):
            os.remove(self.config["appHosts"])
            return True
        else:
            return False

    def fetch_hosts(self,provider):
        """
        fetch blacklist hosts file update,
        Return array
        """
        print "fetch_hosts()"
        print "Downloading updated hosts file"
        req = urllib2.Request(provider, headers={ 'User-Agent': 'Mozilla/5.0' } )
        try:
            headers = { 'User-Agent' : 'Mozilla/5.0' }
            hostsPage = urllib2.urlopen(req,timeout=100)
            hostsPage = hostsPage.read()
            hostsPage = hostsPage.split("\n")
            return hostsPage
        except urllib2.URLError, e:
            print "error"
            return 0
        

    def build_app_hosts(self,hostsPage):
        """
        Build the hosts file
        hostsPage is array
        """
        print "build_app_hosts()"
        baseHostsFile = open(self.config["etcHost"], "r")
        baseHostsFile = baseHostsFile.read()
        baseHostsFile = baseHostsFile.split("\n")
        baseHostsArray = []
        for lineHostsFile in baseHostsFile:
            if '# - - - S T O P - E D I T - H E R E - - - #' in lineHostsFile:
                break
            else:
                print lineHostsFile
                baseHostsArray.append(lineHostsFile)   
        print "break"   
        hostsFile = open(self.config["appHosts"], "w")
        print "Writing ..."
        regexIpLocal = re.compile('^127.0.0.1',re.I)
        regexComment = re.compile('^#',re.I)
        for el in baseHostsArray:
            hostsFile.write(el + "\n")
        hostsFile.write("# - - - S T O P - E D I T - H E R E - - - #\n")
        hostsFile.write("# END ORIGINALS ENTRIES\n")
        hostsFile.write("# ----------------------------------------------------------\n\n")
        hostsFile.write("# This hosts file was generated by pyDenyAll from " + PROVIDER[DEFAULT_PROVIDER] + "\n")
        hostsFile.write("# " + time.strftime('%d/%m/%y %H:%M',time.localtime()) + "\n\n")
        hostsFile.write("# ----------------------------------------------------------\n\n")
        for ligne in hostsPage:
            ligne = ligne.strip()
            matchRegexIpLocal = regexIpLocal.search(ligne)
            matchRegexComment = regexComment.search(ligne)
            if matchRegexIpLocal:
                if ligne not in baseHostsArray:
                    #ligne = ligne.replace("127.0.0.1","127.0.0.2")
                    hostsFile.write(ligne + "\n")
            else:
                if matchRegexComment:
                    hostsFile.write(ligne + "\n")
        hostsFile.write("# ----------------------------------------------------------\n\n")
        hostsFile.close()
        shutil.copyfile(self.config["appHosts"], self.config["etcHost"])
        print "OK"     
        print self.printCountLines()
        #self.labelDynamic = wx.StaticText(self.panelButton, 1, self.printCountLines(), style = wx.ALIGN_CENTRE)
        self.labelDynamic.SetLabel(self.printCountLines())
        return 0

    def no_ads(self, event):
        print "no_ads()"
        if self.test_connect() == False:
            print "Network error"
            return 0
        else:
            print "Network OK"
            self.reinit()
            self.labelDynamic.SetLabel( "Please wait ...")
            self.txtStatusBar.SetStatusText(u"Dl from " + PROVIDER[DEFAULT_PROVIDER] + " ...")
            print "Dl from " + PROVIDER[DEFAULT_PROVIDER] + " ..."
            hostsPage = self.fetch_hosts(PROVIDER[DEFAULT_PROVIDER])
            if (hostsPage != 0):
                self.build_app_hosts(hostsPage)
                self.txtStatusBar.SetStatusText(u"Blacklist added !")
                print "Done !"
            else:
                self.txtStatusBar.SetStatusText(u"Error while dowloading !")
                print "Error while dowloading !"

    def yes_ads(self, event):
        print "yes_ads()"
        self.txtStatusBar.SetStatusText(u"Reinit hosts file ...")
        baseHostsFile = open(self.config["etcHost"], "r")
        baseHostsFile = baseHostsFile.read()
        baseHostsFile = baseHostsFile.split("\n")
        baseHostsArray = []
        for lineHostsFile in baseHostsFile:
            if '# - - - S T O P - E D I T - H E R E - - - #' in lineHostsFile:
                break
            else:
                print lineHostsFile
                baseHostsArray.append(lineHostsFile)   
        print "break"   
        hostsFile = open(self.config["appHosts"], "w")
        print "Writing ..."
        regexIpLocal = re.compile('^127.0.0.1',re.I)
        regexComment = re.compile('^#',re.I)
        for el in baseHostsArray:
            if el.replace("\n", "") != "":
                hostsFile.write(el + "\n")
        hostsFile.close()
        shutil.copyfile(self.config["appHosts"], self.config["etcHost"])
        print self.printCountLines()
        self.labelDynamic.SetLabel(self.printCountLines())
        self.txtStatusBar.SetStatusText(u"Hosts restored !")
        print "Hosts restored !"

    def close_app(self, event):
        print "close_app()"
        exit()

    def printCountLines(self):
        lastModification = time.ctime(os.stat(self.config["etcHost"]).st_mtime)
        #lastModification = time.strptime(lastModification, "%a %b %d %H:%M:%S %Y")
        #lastModification = time.strftime("%Y%m%d-%H%M%S", lastModification) 
        txtCount = "Actually the "  +  self.config["etcHost"] + " file contains " + str(countLine(self.config["etcHost"])) + " lines.\n" + lastModification
        return txtCount
        
    def Quit(self, event):
        exit()
        
app = wx.App(False)
frame = MainWindow(None, PROGRAM_NAME)
app.MainLoop()
