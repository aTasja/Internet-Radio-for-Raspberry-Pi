# sudo apt-get update

# install the Music Player Daemon(mpd) and its client mpc
# sudo apt-get install mpc mpd

# Three radio stations (lines 35, 36, 37):
# 1. spokoynoe radio
# mpc add https://listen1.myradio24.com/6262

# 2. majak
# mpc add https://icecast-vgtrk.cdnvideo.ru/mayakfm_aac_64kbps

# 3. nashe radio
# mpc add http://nashe1.hostingradio.ru/nashespb128.mp3

# option - piter fm
# mpc add http://cdn.radiopiterfm.ru/piterfm

# (GPIO.BOARD)
# LED pin 36 == BUTTON pin 33 
# LED pin 38 == BUTTON pin 35
# LED pin 40 == BUTTON pin 37

# !!! KEYS FOR TWITTER APPLICATION SHOULD BE ENTERED IN LINES 130-133 !!!


from twython import TwythonStreamer
import os
import time
import RPi.GPIO as GPIO

def radio_playlist():
    ''' Fill player by radio strams '''
    os.system('amixer cset numid=3 1') #switch the audio output to analogue (headphone jack)
    
    # fill Music Player Daemon playlist
    os.system('mpc add https://listen1.myradio24.com/6262')                     # radio 1
    os.system('mpc add https://icecast-vgtrk.cdnvideo.ru/mayakfm_aac_64kbps')   # radio 2
    os.system('mpc add http://nashe1.hostingradio.ru/nashespb128.mp3')          # radio 3
    
    os.system('mpc volume 100')                                                 # set volume 100%

def kill_process():
    ''' Delete all processes, clear GPIO, Music Player Daemon playlist'''
    GPIO.cleanup()
    os.system('mpc clear')
    os.system('amixer cset numid=3 2') #switch the audio output to HDMI
  
def leds_mode(pins, mode):
    ''' Set all LEDs as output. Come all LEDs on/off. '''
    GPIO.setmode(GPIO.BOARD)
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, mode)
        
def blink(pin):
    ''' Makes blinks of LEDs for confirmation of controlling mode choosed.'''
    global LED_PINS
    leds_mode(LED_PINS, False)
    for i in range(5):
        GPIO.output(pin, True)
        time.sleep(0.2)
        GPIO.output(pin, False)
        time.sleep(0.2)
        
def button_setup(butt_pins):
    ''' Set buttons as input. '''
    for pin in butt_pins:
        GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP) # button
        
def radio_set(station):
    ''' Switch on the appropriate LED and start radio playing. '''
    global LED_PINS
    leds_mode(LED_PINS, False)    
    GPIO.setmode(GPIO.BOARD)
    GPIO.output(LED_PINS[station-1], True)
    print ('radio {} is playing'.format(station))
    os.system('mpc -q play {}'.format(station))
    
      
def button_mode(butt_pins):
    ''' Listening to buttons. After button is pressed call radio(). '''
    global NUM_FOR_END
    while True:
        for pin in butt_pins:
            if GPIO.input(pin) == False:
                radio_set(butt_pins.index(pin)+1)
                # to switch off radio calculate num of pressing of button #3
                if pin == 37:
                    NUM_FOR_END +=1
                if NUM_FOR_END >= 100:
                    print ('=== Num of end recived ===')
                    kill_process()
                break
            
  
class MyStreamer(TwythonStreamer):
    ''' Listening for tweets. Calls radio() after appropriate tweet is catched. If 'b@tton' in tweet - switch control to buttons.'''
    def on_success(self, data):
        global radio_sites       
        if 'text' in data:
            if '1' in data['text']:
                radio_set(1)
                              
            elif '2' in data['text']:
                radio_set(2)
                            
            elif '3' in data['text']:
                radio_set(3)
                
            elif 'b@tton' in data['text']:
                print ('=== Control transferred from Twitter to Buttons ===')
                blink(36)
                button_mode(BUTT_PINS)
            
            elif 'sh@tdown' in data['text']:
                kill_process()
                
                                               
    def on_error(self, status_code, data):
        print (status_code)


if __name__ == '__main__':
    LED_PINS = [36,38,40]
    BUTT_PINS = [33,35,37]
    NUM_FOR_END = 0
    
    # keys for Twitter Application
    CK = '-'
    CS = '-'
    AT = '-'
    AS = '-'
    
    try:                                                            # program starts here
        radio_playlist()
        leds_mode(LED_PINS, True)
        button_setup(BUTT_PINS)
        
        # choose mode button/twitter
        # press butt #1 to control buttons
        # press butt #2 to control twitter
        while True:
            if GPIO.input(33) == False:
                # control buttons
                print ('=== Button control choosed ===')
                blink(36)                                            # LED #1 blinks 5 times
                
                button_mode(BUTT_PINS)
                break
            
            elif GPIO.input(35) == False:               
                # coltrol tweets
                print ('=== Twitter control choosed ===')
                blink(38)                                             # LED #2 blinks 5 times
                
                stream = MyStreamer(CK, CS, AT, AS)
                stream.statuses.filter(track = 'R@dio')
                break
       
    except KeyboardInterrupt:
        kill_process()

