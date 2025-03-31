# NOTE: This program can run only in Windows 10 and above, i guess..

# Interval to kill the programs (ms)
killInterval = 1000 

# Interval to increase percentage of views (ms)
growInterval = 4100

# Percentage increase
growPercent = 20

# Wait time after reaching 100% (ms)
waitAfterComplete = 5100

# Frame per second
FPS = 60

# URL info
URLInfo = 'https://www.windows.com/stopcode'

# QR text
QRText = 'Got U, This Is April Fools!🎉'

# Stop code
stopCode = 'CRITICAL PROCESS DIED'

# Playing the glitch sound
playGitchSound = True

# Font to use (in system)
fontName = 'Segoe UI'

# Text color
textColor = '#ffffff'

# Background color
backgroundColor = '#0B7DDA'

# List of program exceptions to be muted
exceptMutePrograms = ('bsod.exe', 'python.exe')

def fakeInit():
    # Create fake initialization here

    pass

def killSystemPrograms():
    # Caution! This code will force kill the Windows interface program

    os.system('taskkill /IM explorer.exe /F')
    os.system('cls')

def restoreSystemPrograms():
    # Restore disabled system programs

    from time import sleep
    os.system('start explorer.exe')
    os.system('cls')
    print('April Fools!🎉')
    sleep(3)

# Add your custom resolution scale here
RESOLUTION_SCALE = {
    (1920, 1080): 1.0,
    (1680, 1050): 0.95,
    (1600, 1024): 0.95,
    (1600, 900): 0.8,
    (1440, 1080): 0.85,
    (1440, 900): 0.8,
    (1366, 768): 0.7,
    (1360, 768): 0.7,
    (1280, 1024): 0.8,
    (1280, 960): 0.9,
    (1280, 800): 0.8,
    (1280, 768): 0.7,
    (1280, 720): 0.7,
    (1176, 664): 0.65,
    (1152, 864): 0.8,
    (1024, 768): 0.7,
    (800, 600): 0.55
}

# MAIN PROGRAM -------------------------------------------------------------------------------------

import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

# install with `pip install pygame` or `pip install pygame-ce`
import pygame

from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume  # install with `pip install pycaw`
from txtwrap import align                                   # install with `pip install txtwrap`
from qrcode import QRCode                                   # install with `pip install qrcode`
from io import BytesIO

try:
    # if run in executable (exe) form
    from sys import _MEIPASS
    basePath = _MEIPASS
except ImportError:
    # if run in source code (py) form
    basePath = os.path.abspath('.')

def render_wrap(font, text, **kwargs):
    # see at https://pypi.org/project/txtwrap
    align_info = align(text=text, return_details=True, sizefunc=font.size, **kwargs)
    surface = pygame.Surface(align_info['size'], pygame.SRCALPHA)
    for x, y, text in align_info['aligned']:
        surface.blit(font.render(text, True, textColor), (x, y))
    return surface

def setMute(mute):
    # i swear i found this through a long chat from chatgpt💀
    if hasAudioSessions:
        for session in sessions:
            if session.Process and session.Process.name().strip().lower() not in exceptMutePrograms:
                session._ctl.QueryInterface(ISimpleAudioVolume).SetMute(mute, None)

pygame.init()
pygame.font.init()

displayInfo = pygame.display.Info()
scaleFactor = RESOLUTION_SCALE.get((displayInfo.current_w, displayInfo.current_h), 1.0)

pathIcon = os.path.join(basePath, 'assets\\icon.ico')
pathSound = os.path.join(basePath, 'assets\\glitch.mp3')

buffer = BytesIO()
qr = QRCode(version=1, box_size=4, border=2)
qr.add_data(QRText)
qr.make(fit=True)
qr.make_image(fill_color=backgroundColor, back_color=textColor).save(buffer, format='PNG')
buffer.seek(0)

surfaceQR = pygame.transform.scale(
    pygame.image.load(buffer, 'PNG'),
    (150 * scaleFactor, 150 * scaleFactor)
)

# try to get audio sessions
try:
    sessions = AudioUtilities.GetAllSessions()
    hasAudioSessions = True
except:
    hasAudioSessions = False

if playGitchSound:
    # try to initalize and load the sound
    try:
        pygame.mixer.init()
        glitchSound = pygame.mixer.Sound(pathSound)
        hasGlitchSound = True
    except:
        hasGlitchSound = False

fontLarge = pygame.font.SysFont(fontName, int(150 * scaleFactor))
fontMedium = pygame.font.SysFont(fontName, int(33 * scaleFactor))
fontSmall = pygame.font.SysFont(fontName, int(21 * scaleFactor))
fontTiny = pygame.font.SysFont(fontName, int(17 * scaleFactor))

wrapLength = 1000

surfaceSadFace = fontLarge.render(':(', True, textColor)
surfaceMessage = render_wrap(
    font=fontMedium,
    text="Your device ran into a problem and needs to restart. "
         "We're just collecting some error info, and then "
         "we'll restart for you.",
    width=wrapLength * scaleFactor
)
surfaceInfo = render_wrap(
    font=fontSmall,
    text="For more information about this issue and possible fixes, visit {}".format(URLInfo),
    width=(wrapLength - surfaceQR.get_width()) * scaleFactor
)
surfaceSupport = render_wrap(
    font=fontTiny,
    text="If you call a support person, give them this info:\n"
         "Stop code: {}".format(stopCode),
    width=(wrapLength - surfaceQR.get_width()) * scaleFactor
)

surfaceIcon = pygame.image.load(pathIcon)

running = True
lastKillTime = 0
lastGrowTime = 0
lastCompleteTime = 0
completePercent = 0
isComplete = False

positionX = 100 * scaleFactor

positionYSadFace = 90 * scaleFactor
positionYMessage = 10 * scaleFactor + positionYSadFace + surfaceSadFace.get_height()
positionYProgress = 20 * scaleFactor + positionYMessage + surfaceMessage.get_height()
positionYQR = 30 * scaleFactor + positionYProgress + fontMedium.get_height()
positionXInfo = 10 * scaleFactor + positionX + surfaceQR.get_width()
positionYInfo = positionYQR
positionXSupport = positionXInfo
positionYSupport = positionYQR + surfaceQR.get_height() - surfaceSupport.get_height()

fakeInit()

pygame.display.set_icon(surfaceIcon)
pygame.display.set_caption('bsod')
pygame.mouse.set_visible(False)

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

if playGitchSound and hasGlitchSound:
    glitchSound.play(-1)

setMute(1)
killSystemPrograms()

while running:
    # no events are processed
    # this function needs to be called to make it appear as if the application is still alive
    pygame.event.get()

    surfaceProgress = fontMedium.render(f'{completePercent}% complete', True, textColor)

    screen.fill(backgroundColor)

    screen.blit(surfaceSadFace, (positionX, positionYSadFace))
    screen.blit(surfaceMessage, (positionX, positionYMessage))
    screen.blit(surfaceProgress, (positionX, positionYProgress))
    screen.blit(surfaceQR, (positionX, positionYQR))
    screen.blit(surfaceInfo, (positionXInfo, positionYInfo))
    screen.blit(surfaceSupport, (positionXSupport, positionYSupport))

    current_time = pygame.time.get_ticks()

    # kill system
    if lastKillTime + killInterval <= current_time:
        killSystemPrograms()
        lastKillTime = current_time

    # grow percent
    if lastGrowTime + growInterval <= current_time and not isComplete:
        completePercent += growPercent
        lastGrowTime = current_time

    # if percent reach 100%
    if completePercent >= 100 and not isComplete:
        completePercent = 100
        isComplete = True
        lastCompleteTime = current_time

    # if all done then stop the program
    if isComplete and lastCompleteTime + waitAfterComplete <= current_time:
        running = False

    pygame.display.flip()

    clock.tick(FPS)

# program completed

if playGitchSound and hasGlitchSound:
    glitchSound.stop()

pygame.mouse.set_visible(True)
pygame.quit()

setMute(0)
restoreSystemPrograms()