#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sysAdsBlock
import interface
from wx.lib.embeddedimage import PyEmbeddedImage
import config

app = interface.wx.App(False)
frame = interface.MainWindow(None, config.PROGRAM_NAME)
app.MainLoop()
