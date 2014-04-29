#!/usr/bin/env python
# -*- coding: utf-8 -*-
import settings

import sysAdsBlock
import interfaceWx

from wx.lib.embeddedimage import PyEmbeddedImage
app = interfaceWx.wx.App(False)
frame = interfaceWx.MainWindow(None, settings.PROGRAM_NAME)
app.MainLoop()
