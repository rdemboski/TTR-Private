from panda3d.core import *
import builtins
import os

# Start Toontown (post v2.0.0)

# The VirtualFileSystem, which has already initialized, doesn't see the mount
# directives in the config(s) yet. We have to force it to load those manually:
from panda3d.core import VirtualFileSystem, ConfigVariableList, Filename
vfs = VirtualFileSystem.getGlobalPtr()
mounts = ConfigVariableList('vfs-mount')
for mount in mounts:
    mountfile, mountpoint = (mount.split(' ', 2) + [None, None, None])[:2]
    vfs.mount(Filename(mountfile), Filename(mountpoint), 0)

import glob
for file in glob.glob('resources/*.mf'):
    mf = Multifile()
    mf.openReadWrite(Filename(file))
    names = mf.getSubfileNames()
    for name in names:
        ext = os.path.splitext(name)[1]
        if ext not in ['.jpg', '.jpeg', '.ogg', '.rgb']:
            mf.removeSubfile(name)
    vfs.mount(mf, Filename('/'), 0)

# Configure/Start Toontown Client
class game:
    name = 'toontown'
    process = 'client'

print('TTRPrivate: Ongoing project by RegDogg')
print('ToontownStart: Starting the game.')
builtins.game = game()
import time
import sys
import random
import builtins
try:
    launcher
except:
    from toontown.launcher.TTRLauncher import TTRLauncher
    launcher = TTRLauncher()
    builtins.launcher = launcher

if launcher.isDummy():
    http = HTTPClient()
else:
    http = launcher.http
tempLoader = Loader()

# Prepare GUI Font
from direct.gui import DirectGuiGlobals
print('ToontownStart: setting default font')
from . import ToontownGlobals
DirectGuiGlobals.setDefaultFontFunc(ToontownGlobals.getInterfaceFont)
launcher.setPandaErrorCode(7)
from . import ToonBase
ToonBase.ToonBase()
from panda3d.core import *
if base.win == None:
    print('Unable to open window; aborting.')
    sys.exit()
from direct.gui.DirectGui import *

# Settings
print('ToontownStart: loading game settings')
from toontown.settings.ToontownSettings import ToontownSettings
settings = ToontownSettings()
settings.loadFromSettings()

# Prepare startup screen
launcher.setPandaErrorCode(0)
launcher.setPandaWindowOpen()
ConfigVariableDouble('decompressor-step-time').setValue(0.01)
ConfigVariableDouble('extractor-step-time').setValue(0.01)
backgroundNode = tempLoader.loadSync(Filename('phase_3/models/gui/entering-background'))
eyes = loader.loadModel('phase_3/models/gui/toontown-logo')
findeyes = eyes.find('**/eyes')
backgroundNodePath = aspect2d.attachNewNode(backgroundNode, 0)
backgroundNodePath.setPos(0.0, 0.0, 0.0)
backgroundNodePath.setScale(aspect2d, VBase3(2))
eyes = OnscreenGeom(geom = findeyes, pos = (0, 0, 0), scale = (0.25, 0.25, 0.25))

# Framerate meter for TTR Private: Change in 'dev.prc' to toggle
if ConfigVariableBool('tt-framerate', False):
    from toontown.toonbase.TTFrameRateMeter import TTFrameRateMeter
    TTFrameRateMeter()

base.graphicsEngine.renderFrame()

# Prepare GUI
DirectGuiGlobals.setDefaultDialogGeom(loader.loadModel('phase_3/models/gui/dialog_box_gui'))
from . import TTLocalizer
from otp.otpbase import OTPGlobals
OTPGlobals.setDefaultProductPrefix(TTLocalizer.ProductPrefix)


print('ToontownStart: Loading default gui sounds')
DirectGuiGlobals.setDefaultRolloverSound(base.loader.loadSfx('phase_3/audio/sfx/GUI_rollover.ogg'))
DirectGuiGlobals.setDefaultClickSound(base.loader.loadSfx('phase_3/audio/sfx/GUI_create_toon_fwd.ogg'))

# Prepare Music and Server Version
music = base.musicManager.getSound('phase_3/audio/bgm/ttr_d_theme_phase2.ogg')
from . import ToontownLoader
from direct.gui.DirectGui import *
serverVersion = config.GetString('server-version', 'no_version_set')
print('ToontownStart: serverVersion: ', serverVersion)
from .ToonBaseGlobal import *
from direct.showbase.MessengerGlobal import *
from toontown.distributed import ToontownClientRepository
cr = ToontownClientRepository.ToontownClientRepository(serverVersion, launcher)
cr.music = music
base.sfxManagerList[0].setVolume(0.2)
base.musicManager.setVolume(0.2)
base.initNametagGlobals()
base.cr = cr
loader.endBulkLoad('init')

# Prepare Friends Manager
from otp.friends import FriendManager
from otp.distributed.OtpDoGlobals import *
cr.generateGlobalObject(OTP_DO_ID_FRIEND_MANAGER, 'FriendManager')

# Prepare for new loading screen
if not launcher.isDummy() and not config.GetBool('auto-start-server', False):
    base.startShow(cr, launcher.getGameServer())
else:
    base.startShow(cr)

time.sleep(0.5)
backgroundNodePath.reparentTo(hidden)
backgroundNodePath.removeNode()
del backgroundNodePath
del backgroundNode
eyes.destroy()
del eyes
del tempLoader

'''New Loading Screen'''
from toontown.toontowngui import NewLoadingScreen

loading = NewLoadingScreen.NewLoadingScreen()

loading.newMusic()
loading.newVersion()
loading.connectBackground()
loading.newLogo()

if config.GetBool('auto-start-server', False):
    # Start DedicatedServer
    from otp.otpbase.OTPLocalizer import CRLoadingGameServices

    dialogClass = ToontownGlobals.getGlobalDialogClass()
    builtins.gameServicesDialog = dialogClass(message=CRLoadingGameServices)
    builtins.gameServicesDialog.show()

    from toontown.toonbase.DedicatedServer import DedicatedServer

    builtins.clientServer = DedicatedServer(localServer=True)
    builtins.clientServer.start()

    def localServerReady():
        builtins.gameServicesDialog.cleanup()
        del builtins.gameServicesDialog
        messenger.send('AllowPressKey')

    base.accept('localServerReady', localServerReady)
else:
    messenger.send('AllowPressKey')

base.loader = base.loader
builtins.loader = base.loader
autoRun = ConfigVariableBool('toontown-auto-run', 1)
if autoRun:
    try:
        base.run()
    except SystemExit:
        raise
    except:
        import traceback
        traceback.print_exc()
