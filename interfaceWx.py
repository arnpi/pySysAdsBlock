#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import time
import os
import threading
import httplib
import webServer
import settings
import sysAdsBlock

def run():
    app = wx.App(False)
    MainWindow(None, settings.PROGRAM_NAME)
    app.MainLoop()


class MainWindow(wx.Frame):

    def __init__(self, parent, title):
        self.sab = sysAdsBlock.Sysadsblock()
        wx.Frame.__init__(self, parent, title=title, size=(-1, -1))
        self.frameSizerVert = wx.BoxSizer(wx.VERTICAL)
        self.frameSizerHori1 = wx.BoxSizer(wx.HORIZONTAL)
        self.frameSizerHori2 = wx.BoxSizer(wx.HORIZONTAL)
        self.gridSizer = wx.GridSizer(1, 1, 0, 0)
        self.gridSizerButton = wx.GridSizer(1, 3, 0, 0)
        self.gridSizerText = wx.GridSizer(1, 1, 0, 0)
        self.panelButton = wx.Panel(self, 1)
        self.panelText = wx.Panel(self, 1)

        if settings.DEBUG:
            print "Création de l'interface"
        self.gridSizer.Add(self.gridSizerText, 0, wx.TOP)
        self.gridSizer.Add(self.gridSizerButton, 0, wx.BOTTOM)

        self.buttons1 = wx.Button(self.panelButton, 1, 'Remove blacklist', (-1, -1))
        self.buttons2 = wx.Button(self.panelButton, 2, 'Add blacklist', (-1, -1))
        self.buttons3 = wx.Button(self.panelButton, 3, 'Quit', (-1, -1))
        self.labelDynamic = wx.TextCtrl(self.panelText, 1, "Choose action", size=(380, -1), style= wx.TE_MULTILINE | wx.ALIGN_LEFT)
        self.labelDynamic2 = wx.TextCtrl(self.panelText, 2, " ", size=(380, -1), style= wx.TE_MULTILINE | wx.ALIGN_LEFT)
        self.gridSizerText.Add(self.labelDynamic, 1, wx.ALIGN_LEFT)
        self.gridSizerText.Add(self.labelDynamic2, 1, wx.ALIGN_LEFT)

        self.gridSizerButton.Add(self.buttons1, 1, wx.ALIGN_LEFT)
        self.gridSizerButton.Add(self.buttons2, 1, wx.ALIGN_LEFT)
        self.gridSizerButton.Add(self.buttons3, 1, wx.ALIGN_RIGHT)

        self.Bind(wx.EVT_BUTTON, self.yes_ads, id=1)
        self.Bind(wx.EVT_BUTTON, self.no_ads, id=2)
        self.Bind(wx.EVT_BUTTON, self.close_app, id=3)
        if settings.DEBUG:
            print "Création de la barre de statut"
        self.txtStatusBar = self.CreateStatusBar()
        self.txtStatusBar.SetStatusText(u"Waiting action ...")

        self.panelButton.SetSizer(self.gridSizerButton)
        self.panelText.SetSizer(self.gridSizerText)
        self.frameSizerVert.Add(self.frameSizerHori2, 1)
        self.frameSizerVert.Add(self.frameSizerHori1, 1)
        self.frameSizerHori1.Add(self.panelButton, 1)
        self.frameSizerHori2.Add(self.panelText, 1)
        self.SetSizer(self.frameSizerVert)
        self.frameSizerVert.SetSizeHints(self)
        self.labelDynamic.SetValue(self.printCountLines())
        if settings.DEBUG:
            print "Icone systray"
        self.icoSystray = wx.TaskBarIcon()
        self.SetIcon(settings.ICON.GetIcon())
        self.icoSystray.SetIcon(settings.ICON.GetIcon())
        self.icoSystray.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)
        self.icoSystray.Bind(wx.EVT_TASKBAR_RIGHT_DOWN, self.on_right_down)
        self.icoSystraymenu = wx.Menu()
        self.icoSystraymenu.Append(wx.ID_EXIT, "Close")
        self.icoSystraymenu.Append(1, "Remove blacklist")
        self.icoSystraymenu.Append(2, "Add blacklist")
        self.icoSystraymenu.Append(3, "Start webserver")
        self.icoSystraymenu.Append(4, "Kill webserver")
        self.icoSystraymenu.Bind(wx.EVT_MENU, self.close_app, id=wx.ID_EXIT)
        self.icoSystraymenu.Bind(wx.EVT_MENU, self.yes_ads, id=1)
        self.icoSystraymenu.Bind(wx.EVT_MENU, self.no_ads, id=2)
        self.icoSystraymenu.Bind(wx.EVT_MENU, self.run_web, id=3)
        self.icoSystraymenu.Bind(wx.EVT_MENU, self.kill_web, id=4)
        self.buttons2.SetFocus()
        self.hideStatut = True
        # self.hideStatut = False
        # self.Show()
        self.Bind(wx.EVT_CLOSE, self.on_close)
        randomId = wx.NewId()
        self.Bind(wx.EVT_MENU, self.onKeyCombo, id=randomId)
        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('Q'), randomId)])
        self.SetAcceleratorTable(accel_tbl)
        self.run_web(None)
        self.label_status()
        self.SetSizeHints(self.GetSize().x, self.GetSize().y, self.GetSize().x, self.GetSize().y)

    def onKeyCombo(self, event):
        """"""
        if settings.DEBUG:
            print "You pressed CTRL+Q!"
        exit()

    def on_close(self, event):
        self.on_left_down(event)
        # self.kill_web(self, event)
        # exit()
        # self.Destroy()

    def on_right_down(self, event):
        if settings.DEBUG:
            print "Clique droit"
        self.PopupMenu(self.icoSystraymenu)

    def on_left_down(self, event):
        if settings.DEBUG:
            print "Clique gauche"
        if self.hideStatut is False:
            self.Hide()
            self.hideStatut = True
        else:
            self.Show()
            self.hideStatut = False

    def visit(self):
        if settings.DEBUG:
            print "visiting ", settings.PROVIDER

    def close_app(self, event):
        self.kill_web(event)
        if settings.DEBUG:
            print "close_app()"
        self.Destroy()
        exit()

    def printCountLines(self):
        lastModification = time.ctime(os.stat(self.sab.config["etcHost"]).st_mtime)
        txtCount = "Actually the " + self.sab.config["etcHost"] + " file contains " + str(self.sab.countLine(self.sab.config["etcHost"])) + " lines.\n" + lastModification
        return txtCount

    def Quit(self, event):
        if settings.DEBUG:
            print "Quit()"
        self.on_left_down()
        # self.kill_web(self, event)
        # exit()

    def yes_ads(self, event):
        self.kill_web(event)
        if settings.DEBUG:
            print "yesads"
        self.txtStatusBar.SetStatusText(u"Reinit hosts file ...")
        resultYes = self.sab.yes_ads()
        if resultYes == 1:
            self.txtStatusBar.SetStatusText(u"Hosts restored !")
        else:
            self.txtStatusBar.SetStatusText(u"Error not restored !")
        self.labelDynamic.SetValue(self.printCountLines())
        self.label_status()

    def no_ads(self, event):
        if settings.DEBUG:
            print "noads"
        self.labelDynamic.SetValue("Please wait ...")
        self.txtStatusBar.SetStatusText(u"Dl from " + settings.PROVIDER[settings.DEFAULT_PROVIDER] + " ...")
        resultNo = self.sab.no_ads()
        if resultNo == 1:
            self.txtStatusBar.SetStatusText(u"Blacklist added !")
        elif resultNo == 2:
            self.txtStatusBar.SetStatusText(u"Error while dowloading !")
        elif resultNo == 0:
            self.txtStatusBar.SetStatusText(u"Network error")
        else:
            self.txtStatusBar.SetStatusText(u"WTF ??")
        self.labelDynamic.SetValue(self.printCountLines())
        self.run_web(event)
        self.label_status()

    def run_web(self, event):
        print "run_web()"
        print self.sab.check_is_no_ads()
        if self.check_http() == 0 and self.sab.check_is_no_ads():
            self.a = threading.Thread(None, webServer.run, None) 
            self.a.start()
            self.label_status()
        else:
            pass
            self.label_status()
        self.label_status()

    def kill_web(self, event):
        print "kill_web"
        # self.a._Thread__stop()
        try:
            conn = httplib.HTTPConnection(settings.IP_REDIRECTION + ":%d" % settings.PORT_NUMBER)
            conn.request("QUIT", "/")
            conn.getresponse()
            self.label_status()
        except Exception:
            pass
            self.label_status()

    def check_http(self):
        # self.a._Thread__stop()
        try:
            conn = httplib.HTTPConnection(settings.IP_REDIRECTION + ":%d" % settings.PORT_NUMBER, timeout=5.0)
            conn.request("GET", "/")
            conn.getresponse()
            return 1
        except Exception:
            return 0

    def label_status(self):
        txt = ""
        if self.check_http():
            txt = txt + "Web server: ok"
        else:
            txt = txt + "Web server: down"
        txt = txt + "\n"
        if self.sab.check_is_no_ads():
            txt = txt + "Host protection: ok"
        else:
            txt = txt + "Host protection: None"
        self.labelDynamic2.SetValue(txt)
        return txt
