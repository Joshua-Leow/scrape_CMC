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
time.sleep(6)
keyboard.press(Key.f12)
time.sleep(2)

# ctrl + f to find in inspect
keyboard.press(Key.cmd)
keyboard.type("f")
keyboard.release(Key.cmd)
time.sleep(1)

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

# Open Mac spotlight search
keyboard.press(Key.cmd)
keyboard.press(Key.space)
keyboard.release(Key.cmd)
keyboard.release(Key.space)
time.sleep(1)

# go to finder
keyboard.type("finder")
time.sleep(2)
keyboard.press(Key.enter)
keyboard.release(Key.enter)
time.sleep(1)

# cmd shift G in finder to search by path
keyboard.press(Key.cmd)
keyboard.press(Key.shift)
keyboard.type("g")
keyboard.release(Key.shift)
keyboard.release(Key.cmd)
time.sleep(1)

# search for this path /Users/joshualeow/Desktop/
keyboard.type("/Users/joshualeow/Desktop/")
time.sleep(2)
keyboard.press(Key.enter)
keyboard.release(Key.enter)
time.sleep(1)

# cmd shift G in finder to search by path
keyboard.press(Key.cmd)
keyboard.press(Key.shift)
keyboard.type("g")
keyboard.release(Key.shift)
keyboard.release(Key.cmd)
time.sleep(1)

# search for this path /Users/joshualeow/Documents/Projects/scrape_CMC/data/
keyboard.type("/Users/joshualeow/Documents/Projects/scrape_CMC/data/")
time.sleep(2)
keyboard.press(Key.enter)
keyboard.release(Key.enter)
time.sleep(1)

# tab to select first item, cmd o to open in TextEdit
keyboard.press(Key.tab)
keyboard.release(Key.tab)
time.sleep(1)
keyboard.press(Key.cmd)
keyboard.type("o")
keyboard.release(Key.cmd)

# ctrl a to select all
keyboard.press(Key.cmd)
keyboard.type("a")
keyboard.release(Key.cmd)
time.sleep(1)

# ctrl v to paste
keyboard.press(Key.cmd)
keyboard.type("v")
keyboard.release(Key.cmd)
time.sleep(1)

# ctrl s to save
keyboard.press(Key.cmd)
keyboard.type("s")
keyboard.release(Key.cmd)
time.sleep(1)

# ctrl w to close
keyboard.press(Key.cmd)
keyboard.type("w")
keyboard.release(Key.cmd)
time.sleep(1)