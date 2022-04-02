# Mote_Control
Execute python callback functions with a Nintendo WiiMote





```
python3 mote_control.py

[*] Connecting to WiiMote
[*] Press 1+2 on WiiMote
[*] Connected to WiiMote
1 pressed
2 pressed
A+B pressed
```

Example
```
from mote_control import *

def test_callback(pressed):
  if pressed == 2:
    print("1 pressed")
  elif pressed == 1:
    print("2 pressed")
  elif pressed == 12:
    print("A+B pressed")

def test_callback_home(pressed):
  print("HOME button pressed")

wm = wiimote()
wm.DEBUG = True

wm.add_callback( BTN_HOME, test_callback_home )
wm.add_callback( BTN_1, test_callback )
wm.add_callback( BTN_2, test_callback )
wm.add_callback( BTN_A | BTN_B, test_callback ) # A and B together

wm.start()
wm.read_cont()
#wm.background_callback() # or execute in background with threading
```
