# Internet-Radio-for-Raspberry-Pi
Equipment: Raspberry Pi 3 and
           TV for sound
           
Behavor:
  After launching, the program through port 8080 scans Twitter for tweets of the type "R@dio #",
  where # = 1 is Calm Radio (https://listen1.myradio24.com/6262)
        # = 2 is Radio Mayak (https://icecast-vgtrk.cdnvideo.ru/mayakfm_aac_64kbps)
        # = 3 is Nashe Radio (https://player.nashe.ru/spb/?play)
  When the appropriate tweet has detected,the page of the corresponding radio is loaded in the browser.
  When the other tweet has detected,the page of the corresponding radio is loaded in the browser.
  Switches to another radio after receiving the apptopriate tweet.
