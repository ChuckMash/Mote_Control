import time
import threading
from cwiid import *



class wiimote:

  def __init__(self):
    self.DEBUG                  = False
    self.led_mode               = 1
    self.connection_retry_delay = 1
    self.new_data_delay         = 0.1

    self.stopped   = False
    self.connected = False
    self.wm        = None

    self.button_callbacks={
      BTN_1:None,
      BTN_2:None,
      BTN_A:None,
      BTN_B:None,
      BTN_LEFT:None,
      BTN_RIGHT:None,
      BTN_UP:None,
      BTN_DOWN:None,
      BTN_MINUS:None,
      BTN_PLUS:None,
      BTN_HOME:None,
      BTN_A | BTN_B:None,
      }



  def add_callback(self, btn, callback):
    self.button_callbacks[btn] = callback



  def start(self):
    x = threading.Thread(target=self.maintain_connection)
    x.start()



  def stop(self):
    self.stopped = True



  def maintain_connection(self):
    while not self.stopped:
      if not self.connected:
        self.connect()
      try:
        self.wm.led = self.led_mode
      except Exception as e:
        self.connected = False
        self.wm = None
        print("[*] WiiMote Disconnected")
      time.sleep(self.connection_retry_delay)



  def connect(self, rumble=True):
    if self.DEBUG:
      print("[*] Connecting to WiiMote")
      print("[*] Press 1+2 on WiiMote")
    while self.wm is None:
      try:
        self.wm=Wiimote()
      except Exception as e:
        if self.DEBUG:
          print("...")
    print("[*] Connected to WiiMote")
    if rumble:
      for i in range(3):
        self.rumble(n=0.1)
        time.sleep(0.1)
    self.set_read_mode()
    self.connected = True



  def set_read_mode(self):
   # RPT_ACC | RPT_BALANCE | RPT_BTN | RPT_CLASSIC | RPT_EXT | RPT_IR | RPT_MOTIONPLUS | RPT_NUNCHUK | RPT_STATUS
   self.wm.rpt_mode = RPT_STATUS | RPT_BTN #| RPT_NUNCHUK | RPT_ACC



  def rumble(self, n=1):
    self.wm.rumble = True
    time.sleep(n)
    self.wm.rumble = False



  def read_state(self):
    data = self.wm.state
    return data



  def background_callback(self):
    x = threading.Thread(target=self.read_cont)
    x.start()



  def read_cont(self):
    while not self.stopped:
      if self.connected:
        data = self.read_state()
        if "buttons" in data and data["buttons"]:
          pressed = data["buttons"]
          if pressed in self.button_callbacks.keys(): # check if this button, or combination of buttons has a callback
            if callable(self.button_callbacks[pressed]): # if set callback is callable
              self.button_callbacks[pressed](pressed) # call the callback
      time.sleep(self.new_data_delay)





def test_callback(pressed):
  if pressed == 2:
    print("1 pressed")
  elif pressed == 1:
    print("2 pressed")
  elif pressed == 12:
    print("A+B pressed")

def test_callback_home(pressed):
  print("HOME button pressed")





if __name__=="__main__":
  wm = wiimote()
  wm.DEBUG = True

  wm.add_callback( BTN_HOME, test_callback_home )
  wm.add_callback( BTN_1, test_callback )
  wm.add_callback( BTN_2, test_callback )
  wm.add_callback( BTN_A | BTN_B, test_callback ) # A and B together

  wm.start()
  wm.read_cont()
