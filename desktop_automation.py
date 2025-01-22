from pynput.keyboard import Controller, Key
import time

keyboard = Controller()

# alt tab
keyboard.press(Key.cmd)
keyboard.press(Key.space)
keyboard.release(Key.tab)
keyboard.release(Key.space)

# go to chrome
keyboard.type("chrome")
time.sleep(1)  # Give time to switch to the application
keyboard.press(Key.enter)
keyboard.release(Key.enter)

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