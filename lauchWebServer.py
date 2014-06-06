#!/usr/bin/env python
# -*- coding: utf-8 -*-

import httplib

conn = httplib.HTTPConnection("localhost:%d" % 80)
conn.request("QUIT", "/")
