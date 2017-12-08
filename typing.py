from pygame import *
from random import *
from os import environ

environ['SDL_VIDEO_WINDOW_POS'] = '10,40'

mixer.pre_init()
mixer.init()
init()

# cosmicCat = mixer.music.load('cat/click.ogg')

width,height = display.Info().current_w - 500,display.Info().current_h - 500
screen = display.set_mode((width,height))
screenRect = Rect(0,0,width,height)
screen.fill((255,255,255))

running = True

testImg = transform.scale(image.load('stamps/steve.png'), (100,100))
testImgRect = testImg.get_rect()

currentText = []

undoList = []
undoList.append(screen.copy())
redoList = []

currentSize = 50
currentFont = 'Times New Roman'
currentFont = 'fonts/font.ttf'
blinkerCounter = 0
blinkerVisible = False

deniedKeys = [K_DELETE,K_BACKSPACE,K_ESCAPE,K_RETURN]
escapeStrings = ["quit()", "exit()", "dank","matt", "q"]

def mul_lines(t, s, wid = width, justText = False, fontFam = currentFont):
	f = font.Font(fontFam, s)
	lines = []
	while f.size(t)[0] > wid:
		pos = len(t)
		while f.size(t[0:pos])[0] > wid:
			if t[0:pos].count(" ")==0:
				break
			pos = t.rfind(' ', 0, pos)
			if pos == -1:
				continue
		lines.append(t[0:pos])
		t = t[pos+1:]
	lines.append(t)

	if justText:
		return lines
	totHeight = f.size(lines[0])[1] * len(lines)
	surf = Surface((wid, totHeight), SRCALPHA)
	surf.fill((0,0,0,0))
	for p in range(len(lines)):
		lineFont = f.render(lines[p], True, white)
		surf.blit(lineFont, (0, p * lineFont.get_height()))
	return surf

def displayText(txt, size, xyPos, lineNumber = 0, fontFam = currentFont):
	f = font.Font(fontFam, size)
	textSurf = f.render(txt, True, (0,0,0))
	textRect = textSurf.get_rect()

	textRect.topleft = xyPos[0],xyPos[1] + lineNumber * f.size(txt)[1]

	screen.blit(textSurf, textRect)
	return textRect

def get_alpha_surface(surf, alpha=128):
	tmp = Surface( surf.get_size(), SRCALPHA)
	tmp.fill((255,255,255,alpha))
	tmp.blit(surf, (0,0), surf.get_rect(), BLEND_RGBA_MULT)
	return tmp

key.set_repeat(400,50)

while running:
	undo = False
	redo = False
	back = False

	for evt in event.get():
		if evt.type == QUIT:
			running = False
		if evt.type == KEYDOWN:
			print(evt.key, evt.unicode)

			if evt.key == K_BACKSPACE:
				back = True
			if evt.key == K_DELETE:
				currentText = []
			# if evt.key == K_BACKSPACE and currentText:
			#     if evt.key == K_LCTRL or evt.key == K_RCTRL:
			#         pos = currentText.rfind(' ')
			#         if pos == -1:
			#             currentText = []
			#         else:
			#             currentText = currentText[:pos]
			#     else:
			#         del currentText[-1]
			if evt.key == K_RETURN:
				if currentString.lower() in escapeStrings:
					running = False
			if evt.key not in deniedKeys:
				blinkerCounter = 1
				currentText.append(evt.unicode)
				print(evt.unicode)

			if evt.key == K_ESCAPE:
				running = False
			if evt.key == K_z:
				undo = True
			if evt.key == K_y:
				redo = True
		if evt.type == MOUSEBUTTONDOWN:
			if evt.button == 1:
				co = screen.copy()
				undoList.append(co)
			if evt.button == 4:
				currentSize += 1
			if evt.button == 5:
				currentSize -= 1
		if evt.type == MOUSEBUTTONUP:
			if evt.button == 1:
				if screenRect.collidepoint(mx,my):
					redoList = []


	screen.fill((255,255,255))

	blinkerCounter += 1
	if blinkerCounter < 100:
		blinkerVisible = False
	if blinkerCounter > 100:
		blinkerVisible = True
	if blinkerCounter > 200:
		blinkerCounter = 1

	mx,my = mouse.get_pos()
	# mx -= mx%testImg.get_width()
	# my -= my%testImg.get_width()
	mb = mouse.get_pressed()
	kp = key.get_pressed()

	if mb[0]:
		blinkerCounter=1
		draw.rect(screen, (255,255,255), blinkerFontRect)
	screen.blit(undoList[-1],(0,0))
	
	if kp[K_LCTRL] or kp[K_RCTRL]:
	    if undo and len(undoList) > 1:
	        currentTing = undoList.pop(-1)
	        redoList.append(currentTing)
	    if redo and redoList:
	        currentTing = redoList.pop(-1)
	        undoList.append(currentTing)
	#
	currentString = ''
	for letter in currentText:
		currentString = currentString + letter

	if back and currentText:
		del currentText[-1]

	try:
		if blinkerVisible:
			# currentStringMulLines = mul_lines(currentString + '|', currentSize, width - 200, True)
			blinkerFont = font.SysFont('Arial', currentSize).render("|", True, (0,0,0))
			blinkerFontRect = blinkerFont.get_rect()
			blinkerFontRect.left,blinkerFontRect.bottom = textRect.right,textRect.bottom
			screen.blit(blinkerFont,blinkerFontRect)
			currentStringMulLines = mul_lines(currentString, currentSize, (width-mx), True)
		else:
			currentStringMulLines = mul_lines(currentString, currentSize, (width-mx), True)
	except:
		pass

	for n,l in enumerate(currentStringMulLines):
		textRect = displayText(l, currentSize, (mx,my), n)

	display.flip()

quit()
