# Internet-Radio-for-Raspberry-Pi
Equipment: 	Raspberry Pi 3 
Speaker https://www.compareit.com/product/4538003 
3 LEDs 
3 Resistors 1KOhm 
3 Buttons 
Breadboard 
Wires

Software requirements: 
           >>sudo apt-get update 
           Install the Music Player Daemon(mpd) and its client mpc 
           >>sudo apt-get install mpc mpd Get keys for Twitter Application

Also user should have Twitter Application and know their keys.

Behavior: 
After launching, three LEDs are switching on. 

User should press button #1 or button #2 to choose button mode or tweet mode to control radio. After pressing all LEDs switch off, than the appropriate LED blinks 5 times. 

Now program waits for choosing radio station via buttons of via tweets.

Twitter mode: 
The program through port 8080 scans Twitter for tweets of the type "R@dio #", 
Where	 # = 1 is Calm Radio (https://listen1.myradio24.com/6262)
           # = 2 is Radio Mayak (https://icecast-vgtrk.cdnvideo.ru/mayakfm_aac_64kbps) 
           # = 3 is Nashe Radio (http://nashe1.hostingradio.ru/nashespb128.mp3) 
When the appropriate tweet has detected, the corresponding radio starts sounding through speaker. Switches to another radio after receiving the appropriate tweet. Tweet like 'R@dio b@tton' transfers radio control to button mode. Tweet like 'R@dio sh@tdown' switches off radio (but not the whole RPi).

Button mode: 
When the appropriate button has pressed, the corresponding radio starts sounding through speaker. Device switches to another radio after pressing other button. Long press on button #3 switches off radio (but not the whole RPi).


