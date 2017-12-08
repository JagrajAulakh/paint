from random import choice
f = open('splashes.txt', 'r')
splashes = f.read()
c = splashes.split("!")

currentSplash = choice(c)[1:]

print(currentSplash)