#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import re
import time
import os
import platform
import shutil
import tempfile

import settings


class Sysadsblock():

    def __init__(self):
        self.config = self.configuration(self.detect_os())
        if self.check_install():
            if settings.DEBUG:
                print "Install OK"
        else:
            if self.installer():
                if settings.DEBUG:
                    print "Installing ..."
            else:
                if settings.DEBUG:
                    print "installing error"
                exit()

    def detect_os(self):
        """
        detect os to know correct path, ect.
        Return array
        """
        if settings.DEBUG:
            print "detect_os()"
        systemEnv = {}
        systemEnv["sys"] = platform.system()
        systemEnv["release"] = platform.release()
        systemEnv["os"] = os.name
        systemEnv["arch"] = platform.architecture()[0]
        for el in systemEnv:
            if settings.DEBUG:
                print el + " = " + systemEnv[el]
        return systemEnv

    def configuration(self, systemEnv):
        """
        Generate personnal config with systemEnv from detect_os
        Return array
        """
        if settings.DEBUG:
            print "config()"
        config = {}
        # user path
        config["userPath"] = os.path.expanduser("~")
        # System hosts file
        if systemEnv["sys"] == "Linux":
            config["etcHost"] = "/etc/hosts"
            config["cmdPing"] = "ping -c 1 " + settings.PING_SITE
        elif systemEnv["sys"] == "Windows":
            config["etcHost"] = "C:\WINDOWS\system32\drivers\etc\hosts"
            config["cmdPing"] = "ping " + settings.PING_SITE
        else:
            if settings.DEBUG:
                print "Only linux for the moment ..."
            exit()
        # hosts file build by the app
        config["appHosts"] = tempfile.gettempdir() + os.sep + ".hosts.pyDenyAll"
        # backup of user hosts file
        config["sysBckpHosts"] = config["etcHost"] + ".original"
        for el in config:
            if settings.DEBUG:
                print el + " = " + config[el]
        return config

    def test_connect(self):
        """
        Internet ping,
        Return Bool
        """
        if settings.DEBUG:
            print "test_connect()"
        if os.system(self.config["cmdPing"]):
            return False
        else:
            return True

    def check_install(self):
        """
        Check if user hosts file is backup
        """
        if settings.DEBUG:
            print "check_install()"
        if (os.path.isfile(self.config["sysBckpHosts"]) is True):
            return True
        else:
            return False

    def installer(self):
        """
        Create backup files
        Return Bool
        """
        if settings.DEBUG:
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
        if settings.DEBUG:
            print "reinit()"
        if (os.path.isfile(self.config["appHosts"]) is True):
            os.remove(self.config["appHosts"])
            return True
        else:
            return False

    def fetch_hosts(self, provider):
        """
        fetch blacklist hosts file update,
        Return array
        """
        if settings.DEBUG:
            print "fetch_hosts()"
        if settings.DEBUG:
            print "Downloading updated hosts file"
        req = urllib2.Request(provider, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            hostsPage = urllib2.urlopen(req, timeout=100)
            hostsPage = hostsPage.read()
            hostsPage = hostsPage.split("\n")
            return hostsPage
        except urllib2.URLError:
            if settings.DEBUG:
                print "error"
            return 0

    def build_app_hosts(self, hostsPage):
        """
        Build the hosts file
        hostsPage is array
        """
        if settings.DEBUG:
            print "build_app_hosts()"
        baseHostsFile = open(self.config["etcHost"], "r")
        baseHostsFile = baseHostsFile.read()
        baseHostsFile = baseHostsFile.split("\n")
        baseHostsArray = []
        for lineHostsFile in baseHostsFile:
            if '# - - - S T O P - E D I T - H E R E - - - #' in lineHostsFile:
                break
            else:
                if settings.DEBUG:
                    print lineHostsFile
                baseHostsArray.append(lineHostsFile)
        if settings.DEBUG:
            print "break"
        hostsFile = open(self.config["appHosts"], "w")
        if settings.DEBUG:
            print "Writing ..."
        regexIpLocal = re.compile('^127.0.0.1', re.I)
        regexComment = re.compile('^#', re.I)
        for el in baseHostsArray:
            hostsFile.write(el + "\n")
        hostsFile.write("# - - - S T O P - E D I T - H E R E - - - #\n")
        hostsFile.write("# END ORIGINALS ENTRIES\n")
        hostsFile.write("# ----------------------------------------------------------\n\n")
        hostsFile.write("# This hosts file was generated by pyDenyAll from " + settings.PROVIDER[settings.DEFAULT_PROVIDER] + "\n")
        hostsFile.write("# " + time.strftime('%d/%m/%y %H:%M', time.localtime()) + "\n\n")
        hostsFile.write("# ----------------------------------------------------------\n\n")
        for ligne in hostsPage:
            ligne = ligne.strip()
            matchRegexIpLocal = regexIpLocal.search(ligne)
            matchRegexComment = regexComment.search(ligne)
            if matchRegexIpLocal:
                if ligne not in baseHostsArray:
                    ligne = ligne.replace("127.0.0.1", settings.IP_REDIRECTION)
                    hostsFile.write(ligne + "\n")
            else:
                if matchRegexComment:
                    hostsFile.write(ligne + "\n")
        hostsFile.write("# ----------------------------------------------------------\n\n")
        hostsFile.close()
        shutil.copyfile(self.config["appHosts"], self.config["etcHost"])
        if settings.DEBUG:
            print "OK"
        return 0

    def no_ads(self):
        if settings.DEBUG:
            print "no_ads()"
        if self.test_connect() is False:
            if settings.DEBUG:
                print "Network error"
            return 0
        else:
            if settings.DEBUG:
                print "Network OK"
            self.reinit()
            if settings.DEBUG:
                print "Dl from " + settings.PROVIDER[settings.DEFAULT_PROVIDER] + " ..."
            hostsPage = self.fetch_hosts(settings.PROVIDER[settings.DEFAULT_PROVIDER])
            if (hostsPage != 0):
                self.build_app_hosts(hostsPage)
                if settings.DEBUG:
                    print "Done !"
                return 1
            else:
                if settings.DEBUG:
                    print "Error while dowloading !"
                return 2

    def yes_ads(self):
        if settings.DEBUG:
            print "yes_ads()"
        baseHostsFile = open(self.config["etcHost"], "r")
        baseHostsFile = baseHostsFile.read()
        baseHostsFile = baseHostsFile.split("\n")
        baseHostsArray = []
        for lineHostsFile in baseHostsFile:
            if '# - - - S T O P - E D I T - H E R E - - - #' in lineHostsFile:
                break
            else:
                if settings.DEBUG:
                    print lineHostsFile
                baseHostsArray.append(lineHostsFile)
        if settings.DEBUG:
            print "break"
        hostsFile = open(self.config["appHosts"], "w")
        if settings.DEBUG:
            print "Writing ..."
        for el in baseHostsArray:
            if el.replace("\n", "") != "":
                hostsFile.write(el + "\n")
        hostsFile.close()
        shutil.copyfile(self.config["appHosts"], self.config["etcHost"])
        if settings.DEBUG:
            print "Hosts restored !"
        return 1

    def check_is_no_ads(self):
        if settings.DEBUG:
            print "check_is_no_ads()"
        baseHostsFile = open(self.config["etcHost"], "r")
        baseHostsFile = baseHostsFile.read()
        baseHostsFile = baseHostsFile.split("\n")
        if "# - - - S T O P - E D I T - H E R E - - - #" in baseHostsFile:
            return 1
        else:
            return 0

    def countLine(self, nf, fdl='\n', tbuf=16384):
        """Compte le nombre de lignes du fichier nf"""
        c = 0
        f = open(nf, 'rb')
        while True:
            buf = None
            buf = f.read(tbuf)
            if len(buf) == 0:
                break
            c += buf.count(fdl)
        f.seek(-1, 2)
        car = f.read(1)
        if car != fdl:
            c += 1
        f.close()
        return c
