from panda3d.core import *
from direct.directnotify import DirectNotifyGlobal
from direct.showbase import AppRunnerGlobal
import os

class BattleSounds:
    notify = DirectNotifyGlobal.directNotify.newCategory('BattleSounds')

    def __init__(self):
        self.mgr = AudioManager.createAudioManager()
        self.isValid = 0
        if self.mgr != None and self.mgr.isValid():
            self.isValid = 1
            limit = config.ConfigVariableInt('battle-sound-cache-size', 15).getValue()
            self.mgr.setCacheLimit(limit)
            base.addSfxManager(self.mgr)
            self.setupSearchPath()
        return

    def setupSearchPath(self):
        self.sfxSearchPath = DSearchPath()
        self.sfxSearchPath.appendDirectory(Filename('/phase_3/audio/sfx'))
        self.sfxSearchPath.appendDirectory(Filename('/phase_3.5/audio/sfx'))
        self.sfxSearchPath.appendDirectory(Filename('/phase_4/audio/sfx'))
        self.sfxSearchPath.appendDirectory(Filename('/phase_5/audio/sfx'))

    def clear(self):
        if self.isValid:
            self.mgr.clearCache()

    def getSound(self, name):
        if self.isValid:
            filename = Filename(name)
            found = vfs.resolveFilename(filename, self.sfxSearchPath)
            if not found:
                self.setupSearchPath()
                found = vfs.resolveFilename(filename, self.sfxSearchPath)
            if not found:
                self.notify.warning('%s not found on:' % name)
                print(self.sfxSearchPath)
            else:
                return self.mgr.getSound(filename.getFullpath())
        return self.mgr.getNullSound()


globalBattleSoundCache = BattleSounds()
