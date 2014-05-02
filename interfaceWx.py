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


import wx, time, os

import settings
import sysAdsBlock

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        self.sab = sysAdsBlock.Sysadsblock()
        wx.Frame.__init__(self, parent, title=title, size=(-1,-1))
        self.frameSizerVert = wx.BoxSizer(wx.VERTICAL)
        self.frameSizerHori1 = wx.BoxSizer(wx.HORIZONTAL)
        self.frameSizerHori2 = wx.BoxSizer(wx.HORIZONTAL)
        self.gridSizer = wx.GridSizer(1, 1, 0, 0)
        self.gridSizerButton = wx.GridSizer(1, 3, 0, 0)
        self.gridSizerText = wx.GridSizer(1, 1, 0, 0)
        self.panelButton = wx.Panel(self, 1)
        self.panelText = wx.Panel(self, 1)
                
        if settings.DEBUG : print "Création de l'interface"
        self.gridSizer.Add(self.gridSizerButton, 0, wx.CENTRE)
        self.gridSizer.Add(self.gridSizerText, 0, wx.CENTRE)
                
        self.buttons1 = wx.Button(self.panelButton, 1, 'Remove blacklist', (-1,-1))
        self.buttons2 = wx.Button(self.panelButton, 2, 'Add blacklist', (-1,-1))
        self.buttons3 = wx.Button(self.panelButton, 3, 'Quit', (-1,-1))
        self.labelDynamic = wx.TextCtrl(self.panelText, 1, "Choose action", size = (380,40), style= wx.TE_MULTILINE |  wx.ALIGN_LEFT)
        self.labelFixe = wx.StaticText(self.panelText, 2, title + " GPL", style = wx.ALIGN_LEFT, size = (-1,-1))
        
        self.gridSizerButton.Add(self.buttons1, 1, wx.ALIGN_LEFT)
        self.gridSizerButton.Add(self.buttons2, 2, wx.ALIGN_LEFT)
        self.gridSizerButton.Add(self.buttons3, 3, wx.ALIGN_RIGHT)
        self.gridSizerText.Add(self.labelDynamic, 1, wx.ALIGN_LEFT)
        self.gridSizerText.Add(self.labelFixe, 2, wx.ALIGN_RIGHT)

        self.Bind(wx.EVT_BUTTON, self.yes_ads, id=1)
        self.Bind(wx.EVT_BUTTON, self.no_ads, id=2)
        self.Bind(wx.EVT_BUTTON, self.close_app, id=3)
        if settings.DEBUG : print "Création de la barre de statut"
        self.txtStatusBar = self.CreateStatusBar()
        self.txtStatusBar.SetStatusText(u"Waiting action ...")
        
        self.panelButton.SetSizer(self.gridSizerButton)
        self.panelText.SetSizer(self.gridSizerText)
        self.frameSizerVert.Add(self.frameSizerHori2, 1, wx.EXPAND)
        self.frameSizerVert.Add(self.frameSizerHori1, 1, wx.EXPAND)
        self.frameSizerHori1.Add(self.panelButton, 1, wx.EXPAND)
        self.frameSizerHori2.Add(self.panelText, 1, wx.EXPAND)
        self.SetSizer(self.frameSizerVert)
        self.frameSizerVert.SetSizeHints(self)
        self.labelDynamic.SetValue(self.printCountLines())
        self.SetSizeHints(self.GetSize().x,self.GetSize().y,self.GetSize().x,self.GetSize().y );
        if settings.DEBUG : print "Icone systray"
        self.icoSystray = wx.TaskBarIcon()
        self.SetIcon(settings.ICON.GetIcon())
        self.icoSystray.SetIcon(settings.ICON.GetIcon())
        self.icoSystray.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)
        self.icoSystray.Bind(wx.EVT_TASKBAR_RIGHT_DOWN, self.on_right_down)
        self.icoSystraymenu=wx.Menu()
        self.icoSystraymenu.Append(wx.ID_EXIT, "Close")
        self.icoSystraymenu.Append(1, "Remove blacklist")
        self.icoSystraymenu.Append(2, "Add blacklist")
        self.icoSystraymenu.Bind(wx.EVT_MENU, self.close_app, id=wx.ID_EXIT)
        self.icoSystraymenu.Bind(wx.EVT_MENU, self.yes_ads, id=1)
        self.icoSystraymenu.Bind(wx.EVT_MENU, self.no_ads, id=2)
        
        self.hideStatut = True
        #self.hideStatut = False
        self.Show()
        self.Bind(wx.EVT_CLOSE, self.on_close)
        
    def on_close(self, event):
        exit()
        self.Destroy()

    def on_right_down(self, event):
        if settings.DEBUG : print "Clique droit"
        self.PopupMenu(self.icoSystraymenu)

    def on_left_down(self, event):
        if settings.DEBUG : print "Clique gauche"
        if self.hideStatut == False:
            self.Hide()
            self.hideStatut = True
        else:
            self.Show()
            self.hideStatut = False
        
    def visit(self):
        if settings.DEBUG : print "visiting ", settings.PROVIDER


    def close_app(self, event):
        if settings.DEBUG : print "close_app()"
        exit()

    def printCountLines(self):
        lastModification = time.ctime(os.stat(self.sab.config["etcHost"]).st_mtime)
        txtCount = "Actually the "  +  self.sab.config["etcHost"] + " file contains " + str(self.sab.countLine(self.sab.config["etcHost"])) + " lines.\n" + lastModification
        return txtCount
        
    def Quit(self, event):
        exit()
        
    def yes_ads(self, event):
        if settings.DEBUG : print "yesads"
        self.txtStatusBar.SetStatusText(u"Reinit hosts file ...")
        resultYes = self.sab.yes_ads()
        if resultYes == 1:
            self.txtStatusBar.SetStatusText(u"Hosts restored !")
        else:
            self.txtStatusBar.SetStatusText(u"Error not restored !")
        self.labelDynamic.SetValue(self.printCountLines())
        
    def no_ads(self, event):
        if settings.DEBUG : print "noads"
        self.labelDynamic.SetValue( "Please wait ...")
        self.txtStatusBar.SetStatusText(u"Dl from " + settings.PROVIDER[settings.DEFAULT_PROVIDER] + " ...")
        resultNo = self.sab.no_ads()
        if resultNo == 1:
            self.txtStatusBar.SetStatusText(u"Blacklist added !")
        elif resultNo ==2:
            self.txtStatusBar.SetStatusText(u"Error while dowloading !")
        elif resultNo ==0:
            self.txtStatusBar.SetStatusText(u"Network error")
        else:
            self.txtStatusBar.SetStatusText(u"WTF ??")
        self.labelDynamic.SetValue(self.printCountLines())
            

