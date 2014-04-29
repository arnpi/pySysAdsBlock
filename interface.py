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


import wx
from wx.lib.embeddedimage import PyEmbeddedImage
import base64
import time
import os
import config
import sysAdsBlock
class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        sab = sysadsblock()
        wx.Frame.__init__(self, parent, title=title, size=(400,300))
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
        self.labelFixe = wx.StaticText(self.panelText, 2, title + " GPL", style = wx.ALIGN_LEFT, size = (-1,-1))
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
        #self.SetSizeHints(self.GetSize().x,self.GetSize().y,self.GetSize().x,self.GetSize().y );
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


    def close_app(self, event):
        print "close_app()"
        exit()

    def printCountLines(self):
        lastModification = time.ctime(os.stat(self.config["etcHost"]).st_mtime)
        #lastModification = time.strptime(lastModification, "%a %b %d %H:%M:%S %Y")
        #lastModification = time.strftime("%Y%m%d-%H%M%S", lastModification) 
        txtCount = "Actually the "  +  sab.config["etcHost"] + " file contains " + str(countLine(sab.config["etcHost"])) + " lines.\n" + lastModification
        return txtCount
        
    def Quit(self, event):
        exit()
        
    def yes_ads():
        print "yesads"
        
    def no_ads():
        print "noads"
