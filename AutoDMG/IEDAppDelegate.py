#-*- coding: utf-8 -*-
#
#  InstallESDtoDMGAppDelegate.py
#  InstallESDtoDMG
#
#  Created by Per Olofsson on 2013-09-19.
#  Copyright Per Olofsson, University of Gothenburg 2013. All rights reserved.
#

from Foundation import *
from AppKit import *
from objc import IBAction, IBOutlet

from IEDLog import *
from IEDProfileController import *


class IEDAppDelegate(NSObject):
    
    mainWindowController = IBOutlet()
    profileController = IBOutlet()
    
    def init(self):
        self = super(IEDAppDelegate, self).init()
        if self is None:
            return None
        
        defaultsPath = NSBundle.mainBundle().pathForResource_ofType_(u"Defaults", u"plist")
        defaultsDict = NSDictionary.dictionaryWithContentsOfFile_(defaultsPath)
        self.defaults().registerDefaults_(defaultsDict)
        
        IEDLog.logLevel = NSUserDefaults.standardUserDefaults().integerForKey_(u"LogLevel")
        
        return self
    
    def defaults(self):
        return NSUserDefaults.standardUserDefaults()
    
    def applicationDidFinishLaunching_(self, sender):
        LogDebug(u"applicationDidFinishLaunching:")
        
        updateProfileInterval = self.defaults().integerForKey_(u"UpdateProfileInterval")
        LogInfo(u"UpdateProfileInterval = %d", updateProfileInterval)
        if updateProfileInterval != 0:
            lastCheck = self.defaults().objectForKey_(u"LastUpdateProfileCheck")
            if lastCheck.timeIntervalSinceNow() < (-60 * 60 * 24 * updateProfileInterval):
                LogInfo(u"Checking for updates")
                url = NSURL.URLWithString_(self.defaults().stringForKey_(u"UpdateProfilesURL"))
                self.profileController.updateFromURL_withTarget_selector_(url, self, self.profileUpdateDone_)
    
    def profileUpdateDone_(self, result):
        LogDebug(u"profileUpdateDone:%@", result)
        if result[u"success"]:
            self.defaults().setObject_forKey_(NSDate.date(), u"LastUpdateProfileCheck")
    
    def applicationShouldTerminate_(self, sender):
        LogDebug(u"applicationShouldTerminate:")
        return self.mainWindowController.applicationShouldTerminate_(sender)
    
    def applicationWillTerminate_(self, sender):
        LogDebug(u"applicationWillTerminate:")
        return
