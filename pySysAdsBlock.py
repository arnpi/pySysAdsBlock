#!/usr/bin/env python
# -*- coding: utf-8 -*-
import settings

import sysAdsBlock
import interface
from wx.lib.embeddedimage import PyEmbeddedImage
app = interface.wx.App(False)
frame = interface.MainWindow(None, settings.PROGRAM_NAME)
app.MainLoop()
