from pygame import *

shortcuts = [K_z, K_y, K_o, K_s, K_e]
shortcutStrings = ["Undo: CTRL + Z", "Redo: CTRL + Y", "Load: CTRL + O", "Save: CTRL + S", "Inventory: E", "Snap Mouse Position: SHIFT", "Color 1: 1", "Color 2: 2"]
undoKey,redoKey,loadKey,saveKey,inventoryKey = list(range(len(shortcuts)))