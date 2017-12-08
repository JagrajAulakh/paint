# main.py
# Jagraj Aulakh
# This is a Minecraft themed paint program, like MS paint. features include:
# pen, eraser, spray can,
# shapes: line, circle filled, circle unfilled, ellipse filled, ellipse unfilled, rectangle filled, rectangle unfilled ,
# bucket fill, stamps, font/text, effect filters, load/save, undo/redo, color picker and sound

from pygame import *
from shortcut_keys import *
from math import *
from random import *
from tkinter import *
from tkinter.messagebox import *
from tkinter import filedialog
from tkinter.colorchooser import *
import os

# These classes create the tkinter dialog that lets you type in text
class MyDialog:
	def __init__(self, parent, rad):

		top = self.top = Toplevel(parent)

		Label(top, text="Enter a new radius value:").pack()

		self.e = Entry(top)
		self.e.pack(padx=10,pady=10)
		self.radius = rad

		b = Button(top, text="OK", command=self.ok)
		b.pack(padx=10,pady=10)

	def ok(self):
		self.radius = self.e.get()
		self.top.destroy()
		return self.radius

class TextDialog:
	def __init__(self, parent, rad):

		top = self.top = Toplevel(parent)

		Label(top, text="Type in some text:")

		self.e = Entry(top)
		self.e.pack(padx=10,pady=10)
		self.string = ''

		b = Button(top, text="OK", command=self.ok)
		b.pack(padx=10,pady=10)

	def ok(self):
		self.string = self.e.get()
		self.top.destroy()



root = Tk()
root.withdraw()

mixer.pre_init(44100, -16, 1, 512)
mixer.init()
init()

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 150, 255)
yellow = (255, 255, 160)
buttonGrey = (130, 130, 130)
buttonBlue = (150, 150, 210)

os.environ['SDL_VIDEO_WINDOW_POS'] = '10,40'
width, height = display.Info().current_w - 100, display.Info().current_h - 200  # 1280 1024, 1820 880
screen = display.set_mode((width, height))

# Sets the windows icon and title
display.set_icon(image.load('images/icon.ico'))
display.set_caption('MINEPAINT')

# Text size for all buttons
textS = 40

# Function that gets an selection from the items spritesheet
def getImage(x, y, w, h):
	img = Surface((w, h), SRCALPHA)
	img.fill((0, 0, 0, 0))
	img.blit(itemsSpritesheet, (0, 0), (x, y, w, h))
	return img

# Makes font surface
def getFont(t, s, c, f='fonts/font.ttf', bold=False):
	f = font.Font(f, s, bold=True).render(t, True, c)
	fRect = f.get_rect()
	return f, fRect

# Function takes in a font and string and then returns a
# list of the same string split up into different 'lines'
def mul_lines(f_path, t, s, wid):
	f = font.Font(f_path, s)
	lines = []
	while f.size(t)[0] > wid:
		pos = len(t)
		while f.size(t[0:pos])[0] > wid:
			pos = t.rfind(' ', 0, pos)
			if pos == -1:
				continue
		lines.append(t[0:pos])
		t = t[pos+1:]
	lines.append(t)

	totHeight = f.size(lines[0])[1] * len(lines)
	surf = Surface((wid, totHeight), SRCALPHA)
	surf.fill((0,0,0,0))
	for p in range(len(lines)):
		lineFont = f.render(lines[p], True, white)
		surf.blit(lineFont, (0, p * lineFont.get_height()))
	return surf

# Makes a Minecraft button
def button(txt, txtSize, x, y, w, h, surf=screen):
	buttonRect = Rect(x - w // 2, y - h // 2, w, h)

	if buttonRect.collidepoint(mx, my):
		draw.rect(surf, buttonBlue, buttonRect)
		draw.rect(surf, black, buttonRect, 4)
		bText, bTextRect = getFont(txt, txtSize, yellow)
		bTextRect.center = (buttonRect[0] + buttonRect[2] // 2, buttonRect[1] + buttonRect[3] // 2 + 5)
		surf.blit(bText, bTextRect)
	else:
		bText, bTextRect = getFont(txt, txtSize, white)
		draw.rect(surf, buttonGrey, buttonRect)
		draw.rect(surf, black, buttonRect, 4)
		bTextRect.center = (buttonRect[0] + buttonRect[2] // 2, buttonRect[1] + buttonRect[3] // 2)
		surf.blit(bText, bTextRect)
	return buttonRect

# Pass in the text and rect and the function will make a Minecraft 'Tool tip'
def toolTip(title, description, rect, padding=20, titleOnly=False):
	if rect.collidepoint(mx, my):
		titleText, titleRect = getFont(title, 20, white)

		if not titleOnly:

			descriptionText = mul_lines('fonts/font.ttf', description, 16, 300)# , descriptionRect = getFont(description, 12, white)
			descriptionRect = descriptionText.get_rect() # , descriptionRect = getFont(description, 12, white)
			descriptionRect.x = mx + 10 + padding
			descriptionRect.y = my - 30 - padding
			titleRect.x = mx + 10 + padding
			titleRect.y = descriptionRect.y - titleRect.height - padding

			draw.rect(mouseSurf, (25, 0, 25, 235), (
				descriptionRect.left - padding,
				descriptionRect.bottom + padding,
				max(descriptionRect.width + padding * 2, titleRect.width + padding * 2),
				-(titleRect.height + descriptionRect.height + padding * 3)))

			draw.rect(mouseSurf, (25, 0, 25, 255), (
				descriptionRect.left - padding,
				descriptionRect.bottom + padding,
				max(descriptionRect.width + padding * 2, titleRect.width + padding * 2),
				-(titleRect.height + descriptionRect.height + padding * 3)), 7)

			mouseSurf.blit(descriptionText, descriptionRect)

		if titleOnly:
			titleRect.x = mx + 10 + padding * 2
			titleRect.y = my - titleRect.height - padding

			draw.rect(mouseSurf, (25, 0, 25, 235),
					  (titleRect.x - padding, titleRect.y - padding,
					   titleRect.width + padding * 2, titleRect.height + padding * 2))

			draw.rect(mouseSurf, (25, 0, 25, 255),
					  (titleRect.x - padding, titleRect.y - padding,
					   titleRect.width + padding * 2, titleRect.height + padding * 2), 7)

		mouseSurf.blit(titleText, titleRect)

def undo():
	if len(undoList) > 1:
		transfer = undoList.pop(-1)
		redoList.append(transfer)
def redo():
	if redoList:
		transfer = redoList.pop(-1)
		undoList.append(transfer)

def saveFunc():
	try:
		ftypes = [('Portable Network Graphics', 'png')]
		file_name = filedialog.asksaveasfilename(defaultextension='png', filetypes=ftypes)
		if file_name != '':
			image.save(canvas, file_name)
		return file_name

	except:
		pass
	
def loadFunc():
	try:
		ftypes = [('Portable Network Graphics', 'png'), ("JPEG", "jpg"), ("TIFF","tiff")]
		file_name = filedialog.askopenfilename(defaultextension='png',filetypes=ftypes)
		if file_name != '':
			img = image.load(file_name)
			canvas = transform.scale(img, (canvasRect.width, canvasRect.height))
			canvas = canvas.copy()
			undoList.append(canvas.copy())
		return file_name
	except:
		pass

# check to see if passed in string is actually a number
def is_number(n):
	try:
		int(n)
		return True
	except ValueError:
		return False

class Color:
	def __init__(self, r):
		self.color = black
		self.image = Surface((r[2], r[3]))
		self.rect = r

# Reads the 'splashes' text file and picks a random one for the title screen
f = open('splashes.txt', 'r')
splashes = f.read()
c = splashes.split("!")
currentSplash = choice(c)[1:]

splashSize = 3
sizeDirection = 7

# Surface that holds the title
splashText, splashTextRect = getFont(currentSplash, min(1000 // len(currentSplash), 80), (255, 255, 0))
splashSurf = Surface((splashTextRect[2],splashTextRect[3]), SRCALPHA)
splashSurf.fill((0,0,0,0))
splashSurf.blit(splashText, (0, 0))
whRatio = splashSurf.get_width() / splashSurf.get_height()

# Color Stuff
color1Rect = Rect(width // 2 - 259, height // 2 - 232, 120, 80)
color2Rect = Rect(width // 2 - 259, height // 2 - 152, 120, 80)

color1 = Color(color1Rect)
color2 = Color(color2Rect)
selectedColor = color1

customColor1 = (139,139,139)
customColor1Rect = Rect(width//2-332, height//2-232, 58, 60)
customColor2 = (139,139,139)
customColor2Rect = Rect(width//2-332, height//2-131, 58, 60)
customColor3 = (139,139,139)
customColor3Rect = Rect(width//2-128, height//2-232, 58, 60)
customColor4 = (139,139,139)
customColor4Rect = Rect(width//2-128, height//2-131, 58, 60)

running = True

# RECTS FOR INVENTORY MENU
penToolRect = Rect(width // 2 - 331, height // 2 + 167, 58, 58)
eraserToolRect = Rect(width // 2 - 264, height // 2 + 167, 58, 58)
sprayToolRect = Rect(width // 2 - 196, height // 2 + 167, 58, 58)
stampToolRect = Rect(width // 2 - 127, height // 2 + 167, 58, 58)
bucketRect = Rect(width // 2 - 60, height // 2 + 167, 58, 58)
fontToolRect = Rect(width // 2 + 75, height // 2 + 167, 58, 58)
filterToolRect = Rect(width // 2 + 8, height // 2 + 167, 58, 58)
tempToolRect8 = Rect(width // 2 + 143, height // 2 + 167, 58, 58)
colorToolRect = Rect(width // 2 + 211, height // 2 + 167, 58, 58)
clearCanvasRect = Rect(width // 2 + 286, height // 2 + 167, 60, 60)

invSpot1 = Rect(width // 2 - 331, height // 2 + 83, 58, 58)
invSpot2 = Rect(width // 2 - 264, height // 2 + 83, 58, 58)
invSpot3 = Rect(width // 2 - 197, height // 2 + 83, 58, 58)
invSpot4 = Rect(width // 2 - 127, height // 2 + 83, 58, 58)
invSpot5 = Rect(width // 2 - 63, height // 2 + 83, 58, 58)
invSpot6 = Rect(width // 2 + 7, height // 2 + 83, 58, 58)
invSpot7 = Rect(width // 2 + 74, height // 2 + 83, 58, 58)
invSpot8 = Rect(width // 2 + 142, height // 2 + 83, 58, 58)
invSpot9 = Rect(width // 2 + 209, height // 2 + 83, 58, 58)

invSpot10 = Rect(width // 2 - 331, height // 2 + 15, 58, 58)
invSpot11 = Rect(width // 2 - 264, height // 2 + 15, 58, 58)
invSpot12 = Rect(width // 2 - 197, height // 2 + 15, 58, 58)
invSpot13 = Rect(width // 2 - 127, height // 2 + 15, 58, 58)
invSpot14 = Rect(width // 2 - 63, height // 2 + 15, 58, 58)
invSpot15 = Rect(width // 2 + 7, height // 2 + 15, 58, 58)
invSpot16 = Rect(width // 2 + 74, height // 2 + 15, 58, 58)
invSpot17 = Rect(width // 2 + 142, height // 2 + 15, 58, 58)
invSpot18 = Rect(width // 2 + 209, height // 2 + 15, 58, 58)

invSpot19 = Rect(width // 2 - 331, height // 2 - 53, 58, 58)
invSpot20 = Rect(width // 2 - 264, height // 2 - 53, 58, 58)
invSpot21 = Rect(width // 2 - 197, height // 2 - 53, 58, 58)
invSpot22 = Rect(width // 2 - 130, height // 2 - 53, 58, 58)
invSpot23 = Rect(width // 2 - 63, height // 2 - 53, 58, 58)
invSpot24 = Rect(width // 2 + 7, height // 2 - 53, 58, 58)
invSpot25 = Rect(width // 2 + 74, height // 2 - 53, 58, 58)
invSpot26 = Rect(width // 2 + 142, height // 2 - 53, 58, 58)
invSpot27 = Rect(width // 2 + 209, height // 2 - 53, 58, 58)

# Modes, tools, flags
mode = 'title'
tool = 'pen'
subTool = ''
subToolRect = Rect(0, 0, 0, 0)
selectedSpotRect = penToolRect

# "Loading" screen
mojangImg = image.load('images/mojang.png').convert()
mojangImgRect = mojangImg.get_rect()
mojangImg = transform.scale(mojangImg, (mojangImgRect.width * 3, mojangImgRect.height * 3))
mojangImgRect = mojangImg.get_rect()
screen.fill(white)
mojangImgRect.center = (width // 2, height // 2)
screen.blit(mojangImg, mojangImgRect)
display.flip()
time.wait(2000)

# List stores all mouse positions
p = []

# dirt backgound
background = image.load('images/background.jpg').convert()
background = transform.scale(background, (width, height))

loadingImg = image.load('images/loadingScreen.jpg').convert()
loadingImg = transform.scale(loadingImg, (width, height))

# All items
itemsSpritesheet = image.load('images/items.png')

# Pen
penImg = getImage(80, 32, 16, 16)
penImg = transform.scale(penImg, (58, 58))
	# Line Subtool
lineToolImg = getImage(192, 96, 16, 16)
lineToolImg = transform.scale(lineToolImg, (58, 58))
	# Circle Subtool
circleToolImg = getImage(224,0,16,16)
circleToolImg = transform.scale(circleToolImg, (58, 58))

circleFilledToolImg = getImage(224, 32, 16, 16)
circleFilledToolImg = transform.scale(circleFilledToolImg, (58,58))
	# Ellipse Subtool
ellipseToolImg = getImage(176,96,16,16)
ellipseToolImg = transform.scale(ellipseToolImg, (58,58))

ellipseFilledToolImg = getImage(176,144,16,16)
ellipseFilledToolImg = transform.scale(ellipseFilledToolImg, (58,58))
	# Rectangle Tool
rectToolImg = getImage(32,256-64,16,16)
rectToolImg = transform.scale(rectToolImg, (58,58))

rectFilledToolImg = getImage(16,256-64,16,16)
rectFilledToolImg = transform.scale(rectFilledToolImg, (58,58))

# Eraser
eraserImg = getImage(240, 80, 16, 16)
eraserImg = transform.scale(eraserImg, (58, 58))
# Spray
sprayImg = getImage(16,144,16,16)
sprayImg = transform.scale(sprayImg, (58,58))

# Stamps
stampImg = getImage(192,48,16,16)
stampImg = transform.scale(stampImg, (58,58))
	# Steve Stamp
steveStampIcon = getImage(48,224,16,16)
steveStampIcon = transform.scale(steveStampIcon, (58,58))
steveStampImg = image.load('stamps/steve.png')
steveStampRect = steveStampImg.get_rect()
	# Creeper Stamp
creeperStampIcon = getImage(64,224,16,16)
creeperStampIcon = transform.scale(creeperStampIcon, (58,58))
creeperStampImg = image.load('stamps/creeper.png')
creeperStampRect = creeperStampImg.get_rect()
	# Pig Stamp
pigStampIcon = getImage(80,224,16,16)
pigStampIcon = transform.scale(pigStampIcon, (58,58))
pigStampImg = image.load('stamps/pig.png')
pigStampRect = pigStampImg.get_rect()
	# Cow Stamp
cowStampIcon = getImage(96,224,16,16)
cowStampIcon = transform.scale(cowStampIcon, (58,58))
cowStampImg = image.load('stamps/cow.png')
cowStampRect = cowStampImg.get_rect()
	# Zombie Stamp
zombieStampIcon = getImage(32,224,16,16)
zombieStampIcon = transform.scale(zombieStampIcon, (58,58))
zombieStampImg = image.load('stamps/zombie.png')
zombieStampRect = zombieStampImg.get_rect()
	# Dirt Stamp
dirtStampIcon = getImage(112,224,16,16)
dirtStampIcon = transform.scale(dirtStampIcon, (58,58))
dirtStampImg = image.load('stamps/dirt.png')
dirtStampRect = dirtStampImg.get_rect()
	# Cobble Stamp
cobbleStampIcon = getImage(128,224,16,16)
cobbleStampIcon = transform.scale(cobbleStampIcon, (58,58))
cobbleStampImg = image.load('stamps/cobblestone.png')
cobbleStampRect = cobbleStampImg.get_rect()
	# Stone Stamp
stoneStampIcon = getImage(144,224,16,16)
stoneStampIcon = transform.scale(stoneStampIcon, (58,58))
stoneStampImg = image.load('stamps/stone.png')
stoneStampRect = stoneStampImg.get_rect()
	# Gravel Stamp
gravelStampIcon = getImage(160,224,16,16)
gravelStampIcon = transform.scale(gravelStampIcon, (58,58))
gravelStampImg = image.load('stamps/gravel.png')
gravelStampRect = gravelStampImg.get_rect()
	# Lapis Stamp
lapisBlockStampIcon = getImage(176,224,16,16)
lapisBlockStampIcon = transform.scale(lapisBlockStampIcon, (58,58))
lapisBlockStampImg = image.load('stamps/lapis_block.png')
lapisBlockStampRect = lapisBlockStampImg.get_rect()

lapisOreStampIcon = getImage(0,208,16,16)
lapisOreStampIcon = transform.scale(lapisOreStampIcon, (58,58))
lapisOreStampImg = image.load('stamps/lapis_ore.png')
lapisOreStampRect = lapisOreStampImg.get_rect()
	# Redstone Stamp
redstoneBlockStampIcon = getImage(192,224,16,16)
redstoneBlockStampIcon = transform.scale(redstoneBlockStampIcon, (58,58))
redstoneBlockStampImg = image.load('stamps/redstone_block.png')
redstoneBlockStampRect = redstoneBlockStampImg.get_rect()

redstoneOreStampIcon = getImage(16,208,16,16)
redstoneOreStampIcon = transform.scale(redstoneOreStampIcon, (58,58))
redstoneOreStampImg = image.load('stamps/redstone_ore.png')
redstoneOreStampRect = redstoneOreStampImg.get_rect()
	# Iron Stamp
ironBlockStampIcon = getImage(208,224,16,16)
ironBlockStampIcon = transform.scale(ironBlockStampIcon, (58,58))
ironBlockStampImg = image.load('stamps/iron_block.png')
ironBlockStampRect = ironBlockStampImg.get_rect()

ironOreStampIcon = getImage(32,208,16,16)
ironOreStampIcon = transform.scale(ironOreStampIcon, (58,58))
ironOreStampImg = image.load('stamps/iron_ore.png')
ironOreStampRect = ironOreStampImg.get_rect()
	# Gold Stamp
goldBlockStampIcon = getImage(224,224,16,16)
goldBlockStampIcon = transform.scale(goldBlockStampIcon, (58,58))
goldBlockStampImg = image.load('stamps/gold_block.png')
goldBlockStampRect = goldBlockStampImg.get_rect()

goldOreStampIcon = getImage(48,208,16,16)
goldOreStampIcon = transform.scale(goldOreStampIcon, (58,58))
goldOreStampImg = image.load('stamps/gold_ore.png')
goldOreStampRect = goldOreStampImg.get_rect()
	# Diamond Stamp
diamondBlockStampIcon = getImage(240,224,16,16)
diamondBlockStampIcon = transform.scale(diamondBlockStampIcon, (58,58))
diamondBlockStampImg = image.load('stamps/diamond_block.png')
diamondBlockStampRect = diamondBlockStampImg.get_rect()

diamondOreStampIcon = getImage(64,208,16,16)
diamondOreStampIcon = transform.scale(diamondOreStampIcon, (58,58))
diamondOreStampImg = image.load('stamps/diamond_ore.png')
diamondOreStampRect = diamondOreStampImg.get_rect()
	# Secret Stamp...
secretStampIcon = image.load('images/A1Best100%.png')
secretStampIcon = transform.scale(secretStampIcon, (58,58))
secretStampImg = image.load('images/A1Best100%.png')
secretStampRect = secretStampImg.get_rect()
secret = False
secretRect = Rect(width//2 - 207, 46, 18, 18)

selectedStamp = steveStampImg
selectedStampRect = steveStampRect

# Bucket
bucketImg = getImage(160,64,16,16)
bucketImg = transform.scale(bucketImg, (58,58))

bucket2Img = getImage(160+16,64,16,16)
bucket2Img = transform.scale(bucket2Img, (58,58))

# Font Tool
fontImg, fontImgRect = getFont("ABC", 20, black)
fontImgRect.center = fontToolRect.center

# Font Tool Variables
startPlacingText = False
currentString = ''

	# Game Over Font
gameoverImg, gameoverImgRect = getFont("ABC", 20, black, f='fonts/font.ttf')
gameoverImgRect.center = invSpot1.center
	# Arial Font
arialImg, arialImgRect = getFont("ABC", 20, black, f='fonts/arial.ttf')
arialImgRect.center = invSpot2.center
	# Courier Font
courierImg,courierImgRect = getFont("ABC", 20, black, f='fonts/courier.ttf')
courierImgRect.center = invSpot3.center
	# Comic Sans MS Font
comicImg, comicImgRect = getFont("ABC", 20, black, f='fonts/comic.ttf')
comicImgRect.center = invSpot4.center
	# Impact Font (Meme font)
impactImg, impactImgRect = getFont("ABC", 20, black, f='fonts/impact.ttf')
impactImgRect.center = invSpot5.center

currentFont = 'fonts/font.ttf'

# Filters
filterImg = getImage(160,16,16,16)
filterImg = transform.scale(filterImg, (58,58))
	# Invert
invertIcon, invertIconRect = getFont("I", 30, black, bold=True)
invertIconRect.center = invSpot1.center
	# Sepia
sepiaIcon, sepiaIconRect = getFont("S", 30, black, bold=True)
sepiaIconRect.center = invSpot2.center

# Color picker
colorPickerImg = image.load('images/rainbow.png')
colorPickerImg = transform.scale(colorPickerImg, (58, 58))

spectrumImg = image.load('images/spectrum.jpg')
spectrumImg = transform.scale(spectrumImg, (256, 140))
spectrumImgRect = Rect(width // 2 - 20, height // 2 - 232, 256, 140)

grayscaleImg = Surface((256, 20))
for i in range(256):
	draw.line(grayscaleImg, (i, i, i), (i, 0), (i, 20))
grayscaleRect = Rect(width // 2 - 20, height // 2 - 92, 256, 20)

showColorPicker = 0

# Audio
clickSound = mixer.Sound('sound/click.ogg')
mixer.music.load('sound/menu1.wav')

# Canvas
canvas = Surface((width - 100, height - 150))
canvasRect = Rect(50, 100, width - 100, height - 150)
canvas.fill(white)

radius = 10

undoList = [canvas.copy()]
redoList = []

# This Surface is used for the custom "mouse cursor"
mouseSurf = Surface((width, height), SRCALPHA)

# Inventory Stuff
invSurf = Surface((width, height), SRCALPHA)
invImg = image.load('images/inv.png')
invImg = transform.scale(invImg, (round(invImg.get_width() * 1.25), round(invImg.get_height() * 1.25)))
invImgRect = invImg.get_rect()
inv = 0

# On first time load up, user gets a message on how to open inventory
firstTime = True
invMessageImg = image.load('images/invMessage.png')
invMessageImgRect = invMessageImg.get_rect()
invMessageImgRect.top, invMessageImgRect.right = 10, width - 50

# Making the 'MINEPAINT' title
titleFonts = []
for i in range(50, 200):
	titleFont, titleFontRect = getFont("MINEPAINT", i, (220 - i, 220 - i, 220 - i), f='fonts/font2.ttf')
	titleFontRect.center = (1151 // 2, 238 - round(i * 3 / 4))
	titleFonts.append((titleFont, titleFontRect))

titleFont, titleFontRect = getFont("MINEPAINT", 200, (150, 150, 150), f='fonts/font1.ttf')
titleFontRect.center = (1151 // 2, 238 - round(200 * 3 / 4))
titleFonts.append((titleFont, titleFontRect))

titleSurf = Surface((1151,240), SRCALPHA)
titleSurfRect = titleSurf.get_rect()

for f in titleFonts:
	titleSurf.blit(f[0],f[1])

# Blits Dirt Background
screen.blit(background, (0, 0))

mixer.music.play(-1)
key.set_repeat(500,100)

while running:
	# Mouse button flags
	click = False
	rightClick = False
	rightClickUp = False
	letGo = False

	for e in event.get():
		if e.type == QUIT:
			mouse.set_visible(True)
			# If canvas is blank, ask to save before quitting
			if mode == 'paint':
				if undoList[-1] != undoList[0]:
					askSave = askquestion("Save?", "You havn't saved your work. Would you like to save?", type='yesnocancel')
					if askSave == 'yes':
						result = saveFunc()
						if result != '':
							running = False
					elif askSave == 'cancel':
						pass
					else:
						running = False
				else:
					running = False
			else:
				running = False

		if e.type == KEYDOWN:

			# Switch between color1 and color2
			if e.key == K_1:
				selectedColor = color1
			if e.key == K_2:
				selectedColor = color2

			if e.key == K_ESCAPE:
				if mode == 'paint':
					if inv:
						inv = 0

					elif tool == 'font':
						if startPlacingText:
							startPlacingText = False
						else:
							mode = 'paused'
							mixer.Sound.play(clickSound)

					else:
						mode = 'paused'
						mixer.Sound.play(clickSound)

				elif mode == 'paused':
					mixer.Sound.play(clickSound)
					mode = 'paint'

				elif mode != 'title':
					screen.blit(background, (0, 0))
					mode = 'title'
					mixer.music.play(-1)

			if e.key == shortcuts[inventoryKey]:
				if mode == 'paint':
					canvas.blit(undoList[-1], (0,0))
					inv = 1 - inv

			# Shortcut keys
			if e.mod & KMOD_CTRL:
				if mode == 'paint':
					if e.key == shortcuts[saveKey]:
						result = saveFunc()

					if e.key == shortcuts[undoKey]:
						undo()

					if e.key == shortcuts[redoKey]:
						redo()

					if e.key == shortcuts[loadKey]:
						result = loadFunc()

		if e.type == MOUSEBUTTONDOWN:
			if e.button == 1:
				click = True
				if mode == 'paint':
					co = canvas.copy()
					fmx, fmy = cmx,cmy


			if e.button == 3:
				rightClick = True


			if e.button == 5:
				if not inv:
					radius /= 1.1
					if radius < 2:
						radius = 2


			if e.button == 4:
				if not inv:
					radius *= 1.1
					if radius > 4000:
						radius = 4000

		elif e.type == MOUSEBUTTONUP:
			if e.button == 1:
				letGo = True
				if mode == 'paint':
					if not inv and tool != 'font' and canvasRect.collidepoint(mx,my):
						co = canvas.copy()
						undoList.append(co)
						redoList = []

			if e.button == 3:
				rightClickUp = True

	# Mouse Position Snaping
	kp = key.get_pressed()

	if kp[K_LSHIFT] or kp[K_RSHIFT]:
		mx, my = mouse.get_pos()
		mx, my = mx - mx%10, my - my%10
	else:
		mx, my = mouse.get_pos()

	roundRadius = round(radius)
	cmx, cmy = mx - canvasRect[0], my - canvasRect[1]
	p.append((cmx, cmy))

	mb = mouse.get_pressed()

	# Title screen stuff
	if mode == 'title':
		inv = 0
		
		screen.blit(background, (0, 0))

		titleSurfRect.centerx, titleSurfRect.top = width//2, 20
		screen.blit(titleSurf, titleSurfRect)

		# Does the zoom animation
		splashSize += sizeDirection/3
		if splashSize < -100:
			sizeDirection *= -1
		if splashSize > 50:
			sizeDirection *= -1

		newSize = transform.scale(splashSurf, (splashSurf.get_width() + int(splashSize), splashSurf.get_height() + round(int(splashSize) / whRatio)))
		newSizeRect = newSize.get_rect()
		newSizeRect.center = (width - width // 3, 150)

		screen.blit(transform.rotate(newSize, 10), newSizeRect)

		# Buttons
		newButtonRect = button('New', textS, width // 2, height // 2 + 0, 800, 75)
		loadButtonRect = button('Load', textS, width // 2, height // 2 + 100, 800, 75)
		quitButtonRect = button('Quit', textS, width // 2, height // 2 + 200, 800, 75)

		# Button detections
		if letGo:
			if newButtonRect.collidepoint(mx, my):
				mixer.Sound.play(clickSound)
				screen.blit(background, (0, 0))

				canvas.fill(white)
				undoList = [canvas.copy()]
				redoList = []
				mode = 'loading'
				firstTime = True

			if loadButtonRect.collidepoint(mx, my):
				mixer.Sound.play(clickSound)
				result = loadFunc()
				if result != '':
					mode = 'loading'
					firstTime = True
			if quitButtonRect.collidepoint(mx, my):
				mixer.Sound.play(clickSound)
				time.wait(200)		# Delay so the sound actually plays
				running = False

	# Loading screen stuff
	if mode == 'loading':
		mixer.music.stop()
		randText, randTextRect = getFont("Building Terrain", 35, white)
		randTextRect.center = (width // 2, height // 2)
		for t in range(0, width-600, (width-600) // 100):
			screen.blit(loadingImg, (0, 0))
			loadText, loadTextRect = getFont("Loading World", 35, white)
			loadTextRect.center = (width // 2, height // 2 - 100)
			screen.blit(loadText, loadTextRect)


			if t % 20 == 0:
				randText, randTextRect = choice([getFont("Building Terrain", 35, white), getFont("Generating Chunks", 35, white)])
				randTextRect.center = (width // 2, height // 2)
			screen.blit(randText, randTextRect)

			draw.rect(screen, (40, 40, 40), (300, height - 300, width - 600, 20))
			draw.rect(screen, green, (300, height - 300, t, 20))

			time.wait(randint(0,10))

			display.flip()

		screen.blit(loadingImg, (0, 0))
		loadText, loadTextRect = getFont("Loading World", 35, white)
		loadTextRect.center = (width // 2, height // 2 - 100)
		screen.blit(loadText, loadTextRect)
		loadText, loadTextRect = getFont("Generating Chunks", 35, white)
		loadTextRect.center = (width // 2, height // 2)
		screen.blit(loadText, loadTextRect)

		draw.rect(screen, (40, 40, 40), (300, height - 300, width - 600, 20))
		draw.rect(screen, green, (300, height - 300, width - 600, 20))

		display.flip()
		time.wait(2000)

		screen.blit(background, (0, 0))
		mb = (0,0,0)
		mode = 'paint'

	# The actual paint stuff
	if mode == 'paint':
		screen.blit(background, (0, 0))
		mouseSurf.fill((0, 0, 0, 0))

		# Inventory mode stuff
		if inv:
			mouse.set_visible(True)
			firstTime = False		# Get's rid of the inventory message on first launch

			screen.blit(canvas, canvasRect)

			invSurf.fill((0, 0, 0, 100))		# Creates an "overlay" effect
			mouseSurf.fill((0, 0, 0, 0))
			invImgRect.center = (width // 2, height // 2)	# Centers the inventory
			invSurf.blit(invImg, invImgRect)
			draw.rect(mouseSurf, (255, 255, 255, 40), selectedSpotRect)		# Shows the selected tool
			
			if subTool != '':
				draw.rect(mouseSurf, (255, 255, 255, 40), subToolRect)		# Shows the selected sub tool

			draw.rect(invSurf, color1.color, color1.rect)
			draw.rect(invSurf, color2.color, color2.rect)
			draw.rect(invSurf, customColor1, customColor1Rect)		# These rectangles draw all
			draw.rect(invSurf, customColor2, customColor2Rect)		# the color stuff
			draw.rect(invSurf, customColor3, customColor3Rect)
			draw.rect(invSurf, customColor4, customColor4Rect)
			draw.rect(invSurf, (255,255,255,255), selectedColor.rect, 3)

			# Switching between colors
			if click:
				if color1Rect.collidepoint(mx, my):
					mixer.Sound.play(clickSound)
					selectedColor = color1
				if color2Rect.collidepoint(mx, my):
					mixer.Sound.play(clickSound)
					selectedColor = color2

			# Pen Tool detection
			invSurf.blit(penImg, penToolRect)
			toolTip("Pen Tool", "Free hand drawing tool", penToolRect)
			if penToolRect.collidepoint(mx, my) and click:
				mixer.Sound.play(clickSound)
				selectedSpotRect = penToolRect
				tool = 'pen'
				subTool = ''

			# Eraser Tool detection
			invSurf.blit(eraserImg, eraserToolRect)
			toolTip("Eraser Tool", "Erase the things you have drawn", eraserToolRect)
			if eraserToolRect.collidepoint(mx, my) and click:
				mixer.Sound.play(clickSound)
				selectedSpotRect = eraserToolRect
				tool = 'eraser'
				subTool = ''

			# Clear Canvas detection
			toolTip("Clear", "Clears the canvas", clearCanvasRect)
			if clearCanvasRect.collidepoint(mx, my) and click:
				mixer.Sound.play(clickSound)
				canvas.fill(white)
				undoList.append(canvas.copy())

			# Spray Tool
			invSurf.blit(sprayImg, sprayToolRect)
			toolTip("Spray Can", "Use this tool for a 'spray can' type effect!", sprayToolRect)
			if sprayToolRect.collidepoint(mx, my) and click:
				mixer.Sound.play(clickSound)
				selectedSpotRect = sprayToolRect
				tool = 'spray'
				subTool = ''

			# Stamp Tool detection
			invSurf.blit(stampImg, stampToolRect)
			toolTip("Stamp Tool", "Stamp down some custom images", stampToolRect)
			if stampToolRect.collidepoint(mx, my) and click:
				mixer.Sound.play(clickSound)
				selectedSpotRect = stampToolRect
				tool = 'stamp'
				radius = 20
				stampsList = ['steve','zombie','pig','cow','skele','creeper']
				if subTool not in stampsList:
					subTool = 'steve'
					subToolRect = invSpot1

			# Fill tool detection
			if tool == 'bucket':
				invSurf.blit(bucket2Img, bucketRect)
			else:
				invSurf.blit(bucketImg, bucketRect)
			toolTip("Bucket Tool", "Fill an area as if you spilled a bucket of paint!", bucketRect)
			if bucketRect.collidepoint(mx, my) and click:
				mixer.Sound.play(clickSound)
				selectedSpotRect = bucketRect
				tool = 'bucket'
				subTool = ''
			
			# Font tool detection
			invSurf.blit(fontImg, fontImgRect)
			toolTip("Font Tool", "Click on the canvas to start typing what your heart desires. Left click to place, right click to place multiple. Hit escape to stop placing text", fontToolRect)
			if fontToolRect.collidepoint(mx, my) and click:
				mixer.Sound.play(clickSound)
				selectedSpotRect = fontToolRect
				tool = 'font'
				if subTool not in ['gameover', 'arial', 'comic', 'courier', 'impact']:
					subTool = 'gameover'
					subToolRect = invSpot1

			# Filter tool detection
			invSurf.blit(filterImg, filterToolRect)
			toolTip("Filter Tool", "Make your drawing look professional by applying these filters", filterToolRect)
			if filterToolRect.collidepoint(mx, my) and click:
				mixer.Sound.play(clickSound)
				selectedSpotRect = filterToolRect
				tool = 'filter'
				subTool = ''
				if subTool not in ['invert','sepia']:
					subTool = 'invert'

			# Color picker detection
			invSurf.blit(colorPickerImg, colorToolRect)
			toolTip("Color Picker", "Pick a color for your brush or shape", colorToolRect)
			if colorToolRect.collidepoint(mx, my) and click:
				mixer.Sound.play(clickSound)
				showColorPicker = 1 - showColorPicker

			if tool == 'pen':
				# Line tool detection
				invSurf.blit(lineToolImg, invSpot1)
				toolTip("Line tool", "Draw perfectly straight lines", invSpot1)
				if invSpot1.collidepoint(mx, my) and click:
					mixer.Sound.play(clickSound)
					subTool = 'line'
					subToolRect = invSpot1
				# Circle tool detection
				invSurf.blit(circleToolImg, invSpot2)
				toolTip("Unfilled Circle Tool", "Draw filled, perfectly round circles", invSpot2)
				if invSpot2.collidepoint(mx, my) and click:
					mixer.Sound.play(clickSound)
					subTool = 'circle unfilled'
					subToolRect = invSpot2

				invSurf.blit(circleFilledToolImg, invSpot11)
				toolTip("Filled Circle Tool", "Draw unfilled, perfectly round circles", invSpot11)
				if invSpot11.collidepoint(mx, my) and click:
					mixer.Sound.play(clickSound)
					subTool = 'circle filled'
					subToolRect = invSpot11

				# Ellipse tool detection
				invSurf.blit(ellipseToolImg, invSpot3)
				toolTip("Unfilled Ellipse Tool", "The unfilled circle tool, but a little streeeccchhhheeeddd oouuuutttttt!", invSpot3)
				if invSpot3.collidepoint(mx, my) and click:
					mixer.Sound.play(clickSound)
					subTool = 'ellipse unfilled'
					subToolRect = invSpot3

				invSurf.blit(ellipseFilledToolImg, invSpot12)
				toolTip("Filled Ellipse Tool", "The filled circle tool, but a little streeeccchhhheeeddd oouuuutttttt!", invSpot12)
				if invSpot12.collidepoint(mx, my) and click:
					mixer.Sound.play(clickSound)
					subTool = 'ellipse filled'
					subToolRect = invSpot12

				# Rectangle tool detection
				invSurf.blit(rectToolImg, invSpot4)
				toolTip("Unfilled Rectangle Tool", "Make unfilled squares and rectangles", invSpot4)
				if invSpot4.collidepoint(mx, my) and click:
					mixer.Sound.play(clickSound)
					subTool = 'rect unfilled'
					subToolRect = invSpot4

				invSurf.blit(rectFilledToolImg, invSpot13)
				toolTip("Filled Rectangle Tool", "Make filled squares and rectangles", invSpot13)
				if invSpot13.collidepoint(mx, my) and click:
					mixer.Sound.play(clickSound)
					subTool = 'rect filled'
					subToolRect = invSpot13
				
			if showColorPicker:
				invSurf.blit(spectrumImg, spectrumImgRect)
				invSurf.blit(grayscaleImg, grayscaleRect)

				# Spectrum Image Collision
				if spectrumImgRect.collidepoint(mx, my):
					if mb[0]:
						col = invSurf.get_at((mx, my))
						selectedColor.color = col
						mouse.set_cursor(*cursors.diamond)
					else:
						mouse.set_cursor(*cursors.arrow)
				# Grayscale Image Collision
				elif grayscaleRect.collidepoint(mx, my):
					if mb[0]:
						selectedColor.color = invSurf.get_at((mx, my))
						mouse.set_cursor(*cursors.diamond)

					else:
						mouse.set_cursor(*cursors.arrow)
				else:
					mouse.set_cursor(*cursors.arrow)

				# RGB fonts
				rText, rRect = getFont("R: " + str(round(selectedColor.color[0])), 28, black)
				gText, gRect = getFont("G: " + str(round(selectedColor.color[1])), 28, black)
				bText, bRect = getFont("B: " + str(round(selectedColor.color[2])), 28, black)

				rRect.top = spectrumImgRect.top
				rRect.left = spectrumImgRect.right + 10

				gRect.top = rRect.bottom + 15
				gRect.left = spectrumImgRect.right + 10

				bRect.top = gRect.bottom + 15
				bRect.left = spectrumImgRect.right + 10

				invSurf.blit(rText, rRect)
				invSurf.blit(gText, gRect)
				invSurf.blit(bText, bRect)

			if tool == 'stamp':
				# Stamp detections
				invSurf.blit(steveStampIcon, invSpot1)
				toolTip('"Minecraft Steve" Stamp', "Use this tool to paste this image", invSpot1)
				if invSpot1.collidepoint(mx,my) and click:
					mixer.Sound.play(clickSound)
					selectedStamp = steveStampImg
					subTool = 'steve'
					subToolRect = invSpot1

				invSurf.blit(cowStampIcon, invSpot2)
				toolTip('"Cow" Stamp', "Use this tool to paste this image", invSpot2)
				if invSpot2.collidepoint(mx,my) and click:
					mixer.Sound.play(clickSound)
					selectedStamp = cowStampImg
					subTool = 'cow'
					subToolRect = invSpot2

				invSurf.blit(pigStampIcon, invSpot3)
				toolTip('"Pig" Stamp', "Use this tool to paste this image", invSpot3)
				if invSpot3.collidepoint(mx,my) and click:
					mixer.Sound.play(clickSound)
					selectedStamp = pigStampImg
					subTool = 'pig'
					subToolRect = invSpot3

				invSurf.blit(creeperStampIcon, invSpot4)
				toolTip('"Creeper" Stamp', "Use this tool to paste this image", invSpot4)
				if invSpot4.collidepoint(mx,my) and click:
					mixer.Sound.play(clickSound)
					selectedStamp = creeperStampImg
					subTool = 'creeper'
					subToolRect = invSpot4

				invSurf.blit(zombieStampIcon, invSpot5)
				toolTip('"Zombie" Stamp', "Use this tool to paste this image", invSpot5)
				if invSpot5.collidepoint(mx,my) and click:
					mixer.Sound.play(clickSound)
					selectedStamp = zombieStampImg
					subTool = 'zombie'
					subToolRect = invSpot5

				invSurf.blit(dirtStampIcon, invSpot6)
				toolTip('"Dirt" Stamp', "Use this tool to paste this image", invSpot6)
				if invSpot6.collidepoint(mx,my) and click:
					mixer.Sound.play(clickSound)
					selectedStamp = dirtStampImg
					subTool = 'dirt'
					subToolRect = invSpot6

				invSurf.blit(cobbleStampIcon, invSpot7)
				toolTip('"Cobblestone" Stamp', "Use this tool to paste this image", invSpot7)
				if invSpot7.collidepoint(mx,my) and click:
					mixer.Sound.play(clickSound)
					selectedStamp = cobbleStampImg
					subTool = 'cobble'
					subToolRect = invSpot7

				invSurf.blit(stoneStampIcon, invSpot8)
				toolTip('"Stone" Stamp', "Use this tool to paste this image", invSpot8)
				if invSpot8.collidepoint(mx,my) and click:
					mixer.Sound.play(clickSound)
					selectedStamp = stoneStampImg
					subTool = 'stone'
					subToolRect = invSpot8

				invSurf.blit(gravelStampIcon, invSpot9)
				toolTip('"Gravel" Stamp', "Use this tool to paste this image", invSpot9)
				if invSpot9.collidepoint(mx,my) and click:
					mixer.Sound.play(clickSound)
					selectedStamp = gravelStampImg
					subTool = 'gravel'
					subToolRect = invSpot9

				invSurf.blit(lapisBlockStampIcon, invSpot10)
				toolTip('"Lapis Block" Stamp', "Use this tool to paste this image", invSpot10)
				if invSpot10.collidepoint(mx,my) and click:
					mixer.Sound.play(clickSound)
					selectedStamp = lapisBlockStampImg
					subTool = 'lapis'
					subToolRect = invSpot10

				invSurf.blit(redstoneBlockStampIcon, invSpot11)
				toolTip('"Redstone Block" Stamp', "Use this tool to paste this image", invSpot11)
				if invSpot11.collidepoint(mx,my) and click:
					mixer.Sound.play(clickSound)
					selectedStamp = redstoneBlockStampImg
					subTool = 'redstone'
					subToolRect = invSpot11

				invSurf.blit(ironBlockStampIcon, invSpot12)
				toolTip('"Iron Block" Stamp', "Use this tool to paste this image", invSpot12)
				if invSpot12.collidepoint(mx,my) and click:
					mixer.Sound.play(clickSound)
					selectedStamp = ironBlockStampImg
					subTool = 'iron block'
					subToolRect = invSpot12

				invSurf.blit(goldBlockStampIcon, invSpot13)
				toolTip('"Gold Block" Stamp', "Use this tool to paste this image", invSpot13)
				if invSpot13.collidepoint(mx,my) and click:
					mixer.Sound.play(clickSound)
					selectedStamp = goldBlockStampImg
					subTool = 'gold block'
					subToolRect = invSpot13

				invSurf.blit(diamondBlockStampIcon, invSpot14)
				toolTip('"Diamond Block" Stamp', "Use this tool to paste this image", invSpot14)
				if invSpot14.collidepoint(mx,my) and click:
					mixer.Sound.play(clickSound)
					selectedStamp = diamondBlockStampImg
					subTool = 'diamond block'
					subToolRect = invSpot14

				invSurf.blit(lapisOreStampIcon, invSpot19)
				toolTip('"Lapis Ore" Stamp', "Use this tool to paste this image", invSpot19)
				if invSpot19.collidepoint(mx,my) and click:
					mixer.Sound.play(clickSound)
					selectedStamp = lapisOreStampImg
					subTool = 'lapis ore'
					subToolRect = invSpot19

				invSurf.blit(redstoneOreStampIcon, invSpot20)
				toolTip('"Redstone Ore" Stamp', "Use this tool to paste this image", invSpot20)
				if invSpot20.collidepoint(mx,my) and click:
					mixer.Sound.play(clickSound)
					selectedStamp = redstoneOreStampImg
					subTool = 'redstone ore'
					subToolRect = invSpot20

				invSurf.blit(ironOreStampIcon, invSpot21)
				toolTip('"Iron Ore" Stamp', "Use this tool to paste this image", invSpot21)
				if invSpot21.collidepoint(mx,my) and click:
					mixer.Sound.play(clickSound)
					selectedStamp = ironOreStampImg
					subTool = 'iron ore'
					subToolRect = invSpot21

				invSurf.blit(goldOreStampIcon, invSpot22)
				toolTip('"Gold Ore" Stamp', "Use this tool to paste this image", invSpot22)
				if invSpot22.collidepoint(mx,my) and click:
					mixer.Sound.play(clickSound)
					selectedStamp = goldOreStampImg
					subTool = 'gold ore'
					subToolRect = invSpot22

				invSurf.blit(diamondOreStampIcon, invSpot23)
				toolTip('"Diamond Ore" Stamp', "Use this tool to paste this image", invSpot23)
				if invSpot23.collidepoint(mx,my) and click:
					mixer.Sound.play(clickSound)
					selectedStamp = diamondOreStampImg
					subTool = 'diamond ore'
					subToolRect = invSpot23

				# Secret Detection
				if secret:
					invSurf.blit(secretStampIcon, invSpot15)
					toolTip('"Gursimmer Banwait" Stamp', "Gstorm 3D Printing. www.gstorm3dprinting.com", invSpot15)
					if invSpot15.collidepoint(mx,my) and click:
						mixer.Sound.play(clickSound)
						selectedStamp = secretStampImg
						subTool = 'secret'
						subToolRect = invSpot15
				if not secret:
					if subTool == 'secret':
						selectedStamp = steveStampImg
						subTool = 'steve'
						subToolRect = invSpot1

			if tool == 'filter':
				# Filters detections
				invSurf.blit(invertIcon, invertIconRect)
				toolTip('"Invert" Filter', "Just click on the canvas to use the filter", invSpot1)
				if invSpot1.collidepoint(mx,my) and click:
					mixer.Sound.play(clickSound)
					selectedStamp = invertIcon
					subTool = 'invert'
					subToolRect = invSpot1

				invSurf.blit(sepiaIcon, sepiaIconRect)
				toolTip('"Sepia" Filter', "Just click on the canvas to use the filter", invSpot2)
				if invSpot2.collidepoint(mx,my) and click:
					mixer.Sound.play(clickSound)
					subTool = 'sepia'
					subToolRect = invSpot2

			if tool == 'font':
				# Fonts detections
				invSurf.blit(gameoverImg, gameoverImgRect)
				toolTip('"Game Over" (Minecraft) Font', "", invSpot1, titleOnly = True)
				if invSpot1.collidepoint(mx,my) and click:
					mixer.Sound.play(clickSound)
					subTool = 'gameover'
					subToolRect = invSpot1
					currentFont = 'fonts/font.ttf'

				invSurf.blit(arialImg, arialImgRect)
				toolTip('"Arial" Font', "", invSpot2, titleOnly=True)
				if invSpot2.collidepoint(mx,my) and click:
					mixer.Sound.play(clickSound)
					subTool = 'arial'
					subToolRect = invSpot2
					currentFont = 'fonts/arial.ttf'

				invSurf.blit(courierImg, courierImgRect)
				toolTip('"Courier" Font', "", invSpot3, titleOnly = True)
				if invSpot3.collidepoint(mx,my) and click:
					mixer.Sound.play(clickSound)
					subTool = 'courier'
					subToolRect = invSpot3
					currentFont = 'fonts/courier.ttf'

				invSurf.blit(comicImg, comicImgRect)
				toolTip('"Comic Sans MS" Font', "", invSpot4, titleOnly = True)
				if invSpot4.collidepoint(mx,my) and click:
					mixer.Sound.play(clickSound)
					subTool = 'comic'
					subToolRect = invSpot4
					currentFont = 'fonts/comic.ttf'

				invSurf.blit(impactImg, impactImgRect)
				toolTip('"Impact" (Meme) Font', "", invSpot5, titleOnly = True)
				if invSpot5.collidepoint(mx,my) and click:
					mixer.Sound.play(clickSound)
					subTool = 'impact'
					subToolRect = invSpot5
					currentFont = 'fonts/impact.ttf'

			# Custom Color detetctions
			if customColor1Rect.collidepoint(mx, my):
				if click:
					mixer.Sound.play(clickSound)
					selectedColor.color = customColor1
				if rightClickUp:
					mixer.Sound.play(clickSound)
					c = askcolor(title="Custom Color")[0]
					if c != None:
						customColor1 = c
			if customColor2Rect.collidepoint(mx, my):
				if click:
					mixer.Sound.play(clickSound)
					selectedColor.color = customColor2
				if rightClickUp:
					mixer.Sound.play(clickSound)
					c = askcolor(title="Custom Color")[0]
					if c != None:
						customColor2 = c
			if customColor3Rect.collidepoint(mx, my):
				if click:
					mixer.Sound.play(clickSound)
					selectedColor.color = customColor3
				if rightClickUp:
					mixer.Sound.play(clickSound)
					c = askcolor(title="Custom Color")[0]
					if c != None:
						customColor3 = c
			if customColor4Rect.collidepoint(mx, my):
				if click:
					mixer.Sound.play(clickSound)
					selectedColor.color = customColor4
				if rightClickUp:
					mixer.Sound.play(clickSound)
					c = askcolor(title="Custom Color")[0]
					if c != None:
						customColor4 = c

			toolTip("Color 1", "", color1.rect, titleOnly=True)
			toolTip("Color 2", "", color2.rect, titleOnly=True)
			toolTip("Custom Color", "Left click to select this color, right click to pick a new color", customColor1Rect)
			toolTip("Custom Color", "Left click to select this color, right click to pick a new color", customColor2Rect)
			toolTip("Custom Color", "Left click to select this color, right click to pick a new color", customColor3Rect)
			toolTip("Custom Color", "Left click to select this color, right click to pick a new color", customColor4Rect)

			screen.blit(invSurf, (0, 0))

		# If the inventory is not active:
		else:

			if not mb[0]:
				canvas.blit(undoList[-1], (0,0))

			# Gives a clue to where the secret may be
			if secret:
				toolTip("You Found It", "", secretRect, titleOnly = True)
			else:
				toolTip("","",secretRect,titleOnly = True)
			if secretRect.collidepoint(mx,my) and click:
				if secret:
					secret = False
				else:
					secret = True
				mixer.Sound.play(clickSound)

			# Pen Tool
			if tool == 'pen':

				# Line Tool
				if subTool == 'line':
					if mb[0]:
						canvas.blit(co, (0,0))

						# Using Trig to make my pen tool

						deltax, deltay = cmx - fmx, cmy - fmy
						d = hypot(deltax, deltay)
						angle = atan2(deltay, deltax)
						addx, addy = cos(angle), sin(angle)

						for i in range(round(d)):
							draw.circle(canvas, selectedColor.color, (fmx + round(i * addx), round(fmy + i * addy)), roundRadius)

				# Unfilled circle
				if subTool == 'circle unfilled':
					if mb[0]:
						canvas.blit(co, (0,0))

						if roundRadius < 2:
							roundRadius = 2
						circleSurf = Surface((max(abs(cmx-fmx),abs(cmy-fmy),1),max(abs(cmx-fmx),abs(cmy-fmy),1)), SRCALPHA)
						circleSurf.fill((0,0,0,0))

						circleRect = Rect(fmx,fmy,max(abs(cmx-fmx),abs(cmy-fmy),1),max(abs(cmx-fmx),abs(cmy-fmy),1))

						if roundRadius > abs(circleRect.width)//2:
							draw.circle(circleSurf,selectedColor.color,(abs(circleRect.width//2),abs(circleRect.height//2)), abs(circleRect.width)//2)
						else:
							draw.circle(circleSurf,selectedColor.color,(abs(circleRect.width//2),abs(circleRect.height//2)),abs(circleRect.width)//2)
							draw.circle(circleSurf,(255,255,255,0),(abs(circleRect.width//2),abs(circleRect.height//2)),abs(circleRect.width)//2 - roundRadius)


						if cmx-fmx < 0:
							if cmy-fmy > 0:
								canvas.blit(circleSurf, (fmx-abs(circleRect.width),fmy))
							else:
								canvas.blit(circleSurf, (fmx-abs(circleRect.width),fmy-abs(circleRect.height)))
						else:
							if cmy-fmy > 0:
								canvas.blit(circleSurf, (fmx,fmy))
							else:
								canvas.blit(circleSurf, (fmx,fmy-abs(circleRect.height)))

				# Filled circle
				if subTool == 'circle filled':
					if mb[0]:
						canvas.blit(co, (0,0))
						if cmx-fmx < 0 and cmy-fmy > 0:
							draw.circle(canvas, selectedColor.color, (fmx-max(fmx-cmx,cmy-fmy)//2,fmy+max(fmx-cmx,cmy-fmy)//2), abs(max(fmx-cmx,cmy-fmy))//2)
						elif cmx-fmx > 0 and cmy-fmy < 0:
							draw.circle(canvas, selectedColor.color, (fmx+max(cmx-fmx,fmy-cmy)//2,fmy-max(cmx-fmx,fmy-cmy)//2), abs(max(cmx-fmx,fmy-cmy))//2)
						elif cmx-fmx < 0 and cmy-fmy < 0:
							draw.circle(canvas, selectedColor.color, (fmx-max(fmx-cmx,fmy-cmy)//2,fmy-max(fmx-cmx,fmy-cmy)//2), abs(max(fmx-cmx,fmy-cmy))//2)
						else:
							draw.circle(canvas, selectedColor.color, (fmx+max(cmx-fmx,cmy-fmy)//2,fmy+max(cmx-fmx,cmy-fmy)//2), abs(max(cmx-fmx,cmy-fmy))//2)

				# Unfilled ellipse
				if subTool == 'ellipse unfilled':
					if mb[0]:
						canvas.blit(co, (0, 0))

						if roundRadius < 1:
							roundRadius = 1
						ellipseSurf = Surface((max(abs(cmx-fmx),1),max(abs(cmy-fmy),1)), SRCALPHA)
						ellipseSurf.fill((0,0,0,0))

						ellipseRect = Rect(fmx,fmy,cmx-fmx,cmy-fmy)

						if roundRadius > abs(ellipseRect.width) or roundRadius > abs(ellipseRect.height):
							draw.ellipse(ellipseSurf,selectedColor.color,(0,0, abs(ellipseRect.width), abs(ellipseRect.height)))
						else:
							draw.ellipse(ellipseSurf,selectedColor.color,(0,0, abs(ellipseRect.width), abs(ellipseRect.height)))
							draw.ellipse(ellipseSurf,(255,255,255,0), (roundRadius//2, roundRadius//2,abs(ellipseRect.width)-roundRadius,abs(ellipseRect.height)-roundRadius))


						if ellipseRect.width < 0:
							if ellipseRect.height > 0:
								canvas.blit(ellipseSurf, (cmx,fmy))
							else:
								canvas.blit(ellipseSurf, (cmx,cmy))
						else:
							if ellipseRect.height > 0:
								canvas.blit(ellipseSurf, (fmx,fmy))
							else:
								canvas.blit(ellipseSurf, (fmx,cmy))

						dimensionsText,dimensionsTextRect = getFont("Width: " + str(abs(cmx-fmx)) + "  Height: " + str(abs(cmy-fmy)), 20, white)
						dimensionsTextRect.left, dimensionsTextRect.bottom = 250, height-10

						screen.blit(dimensionsText, dimensionsTextRect)
			

				# Filled ellipse
				if subTool == 'ellipse filled':
					if mb[0]:
						canvas.blit(co, (0,0))

						ellipseRect = Rect(fmx,fmy,cmx-fmx,cmy-fmy)
						ellipseRect.normalize()

						draw.ellipse(canvas, selectedColor.color, ellipseRect)

						dimensionsText,dimensionsTextRect = getFont("Width: " + str(abs(cmx-fmx)) + "  Height: " + str(abs(cmy-fmy)), 20, white)
						dimensionsTextRect.left, dimensionsTextRect.bottom = 0, height

						screen.blit(dimensionsText, dimensionsTextRect)

				# Unfilled rectangle
				if subTool == 'rect unfilled':
					if mb[0]:
						canvas.blit(co, (0,0))

						draw.rect(canvas, selectedColor.color, (fmx,fmy,cmx-fmx,cmy-fmy), roundRadius*2)
						if roundRadius > 2:
							for x in [fmx,cmx]:
								for y in [fmy,cmy]:
									draw.circle(canvas, selectedColor.color, (x,y), roundRadius - 1)
									
						dimensionsText,dimensionsTextRect = getFont("Width: " + str(abs(cmx-fmx)) + "  Height: " + str(abs(cmy-fmy)), 20, white)
						dimensionsTextRect.left, dimensionsTextRect.bottom = 0, height

						screen.blit(dimensionsText, dimensionsTextRect)

				# Filled rectangle
				if subTool == 'rect filled':
					if mb[0]:
						canvas.blit(co, (0,0))

						rectangleRect = Rect(fmx,fmy,cmx-fmx,cmy-fmy)
						rectangleRect.normalize()

						draw.rect(canvas, selectedColor.color, rectangleRect)

						dimensionsText,dimensionsTextRect = getFont("Width: " + str(abs(cmx-fmx)) + "  Height: " + str(abs(cmy-fmy)), 20, white)
						dimensionsTextRect.left, dimensionsTextRect.bottom = 0, height

						screen.blit(dimensionsText, dimensionsTextRect)
						
				if subTool == '':
					if mb[0]:
						ox = p[-2][0]
						oy = p[-2][1]

						deltax = cmx - ox
						deltay = cmy - oy
						d = max(hypot(deltax, deltay), 1)
						angle = atan2(deltay, deltax)
						addx = cos(angle)
						addy = sin(angle)
						for i in range(round(d)):
							draw.circle(canvas, selectedColor.color, (round(ox), round(oy)), roundRadius)
							ox += addx
							oy += addy

			# Eraser tool
			if tool == 'eraser':
				if mb[0]:
					ox = p[-2][0]
					oy = p[-2][1]

					deltax = cmx - ox
					deltay = cmy - oy
					d = max(hypot(deltax, deltay), 1)
					angle = atan2(deltay, deltax)
					addx = cos(angle)
					addy = sin(angle)
					for i in range(round(d)):
						draw.circle(canvas, white, (round(ox), round(oy)), roundRadius)
						ox += addx
						oy += addy

			# Spray can tool
			if tool == 'spray':
				if mb[0]:
					for i in range(roundRadius):
						randx = randint(-roundRadius, roundRadius)
						randy = randint(-roundRadius, roundRadius)

						while hypot(randx, randy) > roundRadius:
							randx = randint(-roundRadius, roundRadius)
							randy = randint(-roundRadius, roundRadius)
						canvas.set_at((cmx + randx, cmy + randy), selectedColor.color)


			# Stamps
			if tool == 'stamp':
				if mb[0]:
					if canvasRect.collidepoint(mx,my):
						canvas.blit(co, (0,0))

						tmp = transform.scale(selectedStamp, (roundRadius, roundRadius))
						tmpRect = tmp.get_rect()
						tmpRect.centerx,tmpRect.centery = cmx,cmy
						canvas.blit(tmp, tmpRect)

			# Bucket Tool
			if tool == 'bucket':
				if click:
					pixel_array = PixelArray(canvas)	# Gets all the canvas's pixels and their colors. Also, locks the surface

					pixel_list = [(cmx,cmy)]		# Stores pixels that need to be checked
					used_set = set()				# Stores pixels that have already been checked

					old_color = pixel_array[(cmx,cmy)]		# Color user has cicked

					while pixel_list:				# Keeps running until all pixels have been checked
						pixel = pixel_list.pop()

						# Makes sure that the pixel is on the canvas
						if pixel[0] <= 0 or pixel[0] >= canvasRect.w or pixel[1] <= 0 or pixel[1] >= canvasRect.h:
							continue
						# Makes sure that the pixel is to be checked at all
						if pixel_array[pixel] != old_color or pixel in used_set:
							continue

						# Sets the pixel
						pixel_array[pixel] = selectedColor.color
						used_set.add(pixel)

						# Adds surrounding pixels
						pixel_list.append((pixel[0]+1,pixel[1]))
						pixel_list.append((pixel[0]-1,pixel[1]))
						pixel_list.append((pixel[0],pixel[1]+1))
						pixel_list.append((pixel[0],pixel[1]-1))

					del pixel_array		# Unlocks the surfaces

			# Font tool
			if tool == 'font':
				if startPlacingText:
					canvas.blit(co, (0,0))
					if not click:
						currentStringFont,currentStringFontRect = getFont(currentString, roundRadius, selectedColor.color, f=currentFont)
						currentStringFontRect.center = cmx,cmy
						canvas.blit(currentStringFont, currentStringFontRect)
					if rightClick and canvasRect.collidepoint(mx,my) and not inv:
						co = canvas.copy()
						undoList.append(canvas.copy())
						redoList = []

					if letGo and canvasRect.collidepoint(mx,my) and not inv:
						undoList.append(canvas.copy())
						redoList = []
						startPlacingText = False
				else:
					if letGo and canvasRect.collidepoint(mx,my) and not inv:
						d = TextDialog(root, currentString)
						root.wait_window(d.top)
						currentString = d.string
						if currentString != '':
							startPlacingText = True
				co = undoList[-1]

			# Filter tool
			if tool == 'filter':
				if subTool == 'invert':
					if click:

						# Looks at all pixels on the canvas
						for px in range(canvasRect.width):
							for py in range(canvasRect.height):
								r,g,b,a = canvas.get_at((px,py))
								canvas.set_at((px,py), (255-r, 255-g, 255-b))	# sets all pixels to the reverse of their current color
						undoList.append(canvas.copy())

				if subTool == 'sepia':
					if click:
						for px in range(canvasRect.width):
							for py in range(canvasRect.height):
								r,g,b,a = canvas.get_at((px,py))
								g=min(255,int(r*.349+g*.686+b*.168))	# Multiplies the color values of
								r=min(255,int(r*.393+g*.769+b*.189))	# all pixels to specific amounts
								b=min(255,int(r*.272+g*.534+b*.131))	# that give a sepia effect
								canvas.set_at((px,py), (round(r),round(g),round(b)))
						undoList.append(canvas.copy())

			# Custom Cursor
			if (tool=='pen' and (subTool=='' or subTool=='line')) or tool=='spray' or tool=='eraser':
				mouse.set_visible(False)
				draw.circle(mouseSurf, (111, 111, 111), (mx, my), roundRadius, 1)
				draw.circle(mouseSurf, (111, 111, 111), (mx, my), 2)
			else:
				mouse.set_visible(True)

			# Mouse Position Text
			if mb[0]:
				mousePosText,mousePosTextRect = getFont("Mouse Position: " + str(mx) + ", " + str(my), 20, white)
			else:
				mousePosText,mousePosTextRect = getFont("Mouse Position: " + str(mx) + ", " + str(my), 20, (180,180,180))
			mousePosTextRect.right, mousePosTextRect.bottom = width - 10, height - 10
			screen.blit(mousePosText,mousePosTextRect)
			toolTip("Snap", 'Hold the "shift" key to snap your mouse position', mousePosTextRect)

			# Minepaint title on paint screen
			titleSurfSmall = transform.scale(titleSurf, (round(titleSurfRect.w * 2/5), round(titleSurfRect.h * 2/5)))
			titleSurfSmallRect = titleSurfSmall.get_rect()
			titleSurfSmallRect.centerx, titleSurfSmallRect.top = width//2, 10
			screen.blit(titleSurfSmall, titleSurfSmallRect)

			# Radius Text
			radiusText,radiusTextRect = getFont("Radius: " + str(roundRadius), 20, white)
			radiusTextRect.right, radiusTextRect.bottom = width - 375, height - 10
			screen.blit(radiusText,radiusTextRect)
			toolTip("Radius", "Click here to enter a new radius", radiusTextRect)

			# Lets the user type a custom radius using Tkinter
			if radiusTextRect.collidepoint(mx,my) and letGo:
				d = MyDialog(root, radius)
				root.wait_window(d.top)
				if is_number(d.radius):
					if int(d.radius) > 2:
						radius = int(d.radius)
						if radius > 4000:
							radius = 4000

			# Undo Text
			if len(undoList) == 1:
				undoText, undoTextRect = getFont("Undo", 28, (180,180,180))
			else:
				undoText, undoTextRect = getFont("Undo", 28, white)
			undoTextRect.bottomleft = 10, height-10
			screen.blit(undoText,undoTextRect)
			toolTip("Undo", "Undo to the last action on the canvas", undoTextRect)
			if undoTextRect.collidepoint(mx,my) and letGo:
				if len(undoList) > 1:
					mixer.Sound.play(clickSound)
				undo()

			# Redo Text
			if redoList:
				redoText, redoTextRect = getFont("Redo", 28, white)
			else:
				redoText, redoTextRect = getFont("Redo", 28, (180,180,180))
			redoTextRect.bottomleft = undoTextRect.right + 20,height-10
			screen.blit(redoText,redoTextRect)
			toolTip("Redo", "Put the action back onto the canvas", redoTextRect)
			if redoTextRect.collidepoint(mx,my) and letGo:
				if redoList:
					mixer.Sound.play(clickSound)
				redo()


			screen.blit(canvas, canvasRect)
			if firstTime:
				screen.blit(invMessageImg, invMessageImgRect)

		screen.blit(mouseSurf, (0, 0))

	# Pause menu stuff
	if mode == 'paused':
		mouse.set_visible(True)
		screen.blit(background, (0,0))
		screen.blit(canvas, canvasRect)
		invSurf.fill((0,0,0,160))

		# Buttons
		resumeButtonRect = button('Resume', textS, width // 2, height // 2 - 150, 800, 75, invSurf)
		if resumeButtonRect.collidepoint(mx,my):
			if letGo:
				mixer.Sound.play(clickSound)
				mode = 'paint'

		saveAsButtonRect = button('Save As', textS, width // 2, height // 2 - 50, 800, 75, invSurf)
		if saveAsButtonRect.collidepoint(mx,my):
			if letGo:
				mixer.Sound.play(clickSound)
				try:
					file_name = filedialog.asksaveasfilename(defaultextension='png')
					image.save(canvas, file_name)
				except:
					pass

		controlsButtonRect = button('Controls', textS, width // 2, height // 2 + 50, 800, 75, invSurf)
		if controlsButtonRect.collidepoint(mx,my):
			if letGo:
				mixer.Sound.play(clickSound)
				mode = 'controls'

		exitButtonRect = button('Exit to Main Menu', textS, width // 2, height // 2 + 150, 800, 75, invSurf)
		if exitButtonRect.collidepoint(mx,my):
			if letGo:
				mixer.Sound.play(clickSound)
				askSave = askquestion("Save?", "You havn't saved your work. Would you like to save?", type='yesnocancel')
				if askSave == 'yes':
					result = saveFunc()
					if result != '':
						mode = 'title'
						canvas.fill(white)
						undoList = [canvas.copy()]
				elif askSave == 'cancel':
					pass
				else:
					mode = 'title'

		screen.blit(invSurf, (0,0))

	# Controls menu stuff
	if mode == 'controls':
		screen.blit(loadingImg, (0,0))

		maxStr = ''							# 
		for cont in shortcutStrings:		# Gets the max size from all controls
			if len(cont) > len(maxStr):		# in the shortcut_keys.py file
				maxStr = cont 				# 

		# Sperate Surface for the controls text
		controlsSurf = Surface((font.Font('fonts/font.ttf', 36).size(maxStr)[0] + 50, 100 + len(shortcutStrings)*100),SRCALPHA)
		controlsSurf.fill((255,255,255,0))
		controlsSurfRect = controlsSurf.get_rect()

		# Blits all the controls
		for i in range(len(shortcutStrings)):
			tmp, tmpRect = getFont(shortcutStrings[i], 36, white)
			tmpRect.center = controlsSurfRect.width // 2, i * 80 + 100
			controlsSurf.blit(tmp, tmpRect)

		# Blit surface
		controlsSurfRect.center = width // 2, height // 2 - 50
		screen.blit(controlsSurf,controlsSurfRect)

		# The one buton
		backButtonRect = button("Back", textS, width//2, height - 100, 600, 75)
		if backButtonRect.collidepoint(mx,my) and letGo:
			mode = "paused"

	display.flip()
quit()
