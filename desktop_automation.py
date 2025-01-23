from certifi import contents
from pynput.keyboard import Controller, Key
import time

from setuptools.command.saveopts import saveopts

keyboard = Controller()

# Open Mac spotlight search
keyboard.press(Key.cmd)
keyboard.press(Key.space)
keyboard.release(Key.cmd)
keyboard.release(Key.space)
time.sleep(1)

# go to chrome
keyboard.type("chrome")
time.sleep(2)
keyboard.press(Key.enter)
keyboard.release(Key.enter)
time.sleep(1)

# open new tab
keyboard.press(Key.cmd)
keyboard.type("t")
keyboard.release(Key.cmd)

# go to https://www.coingecko.com/en/new-cryptocurrencies
keyboard.type("coingecko.com/en/new-cryptocurrencies")
time.sleep(1)
keyboard.press(Key.delete)
keyboard.press(Key.enter)

# open inspect tool
keyboard.press(Key.f12)
time.sleep(3)

# ctrl + f to find in inspect
keyboard.press(Key.cmd)
keyboard.type("f")
keyboard.release(Key.cmd)

# search for <table>
keyboard.type("<table>")
time.sleep(1)

# Edit as HTML
keyboard.press(Key.f2)
time.sleep(1)

# ctrl + a to select all
keyboard.press(Key.cmd)
keyboard.type("a")
keyboard.release(Key.cmd)

# ctrl + c to select all
keyboard.press(Key.cmd)
keyboard.type("c")
keyboard.release(Key.cmd)

# ctrl + w to close tab
keyboard.press(Key.cmd)
keyboard.type("w")
keyboard.release(Key.cmd)

# search for finder
# cmd shift G go to CG_table.txt
# cmd o to open in TextEdit
# ctrl a and paste contents
# ctrl s to save
# ctrl w to close