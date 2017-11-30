#!/usr/bin/env python
#!/usr/bin/python
#--------------------------------------
#    ___  ___  _ ____
#   / _ \/ _ \(_) __/__  __ __
#  / , _/ ___/ /\ \/ _ \/ // /
# /_/|_/_/  /_/___/ .__/\_, /
#                /_/   /___/
#
#  lcd_i2c.py
#  LCD test script using I2C backpack.
#  Supports 16x2 and 20x4 screens.
#
# Author : Matt Hawkins
# Date   : 20/09/2015
#
# http://www.raspberrypi-spy.co.uk/
#
# Copyright 2015 Matt Hawkins
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#--------------------------------------
import time
import RPi.GPIO as GPIO
import os
import vlc
import smbus
from ftplib import FTP
 
allmusic = []
junklist = []
musiclist = []
channellist = []
musicfolderlist=[]
channel = []
ftp = FTP("192.168.0.107","root","raspberry")
ftp.cwd("/music2")
ftp.retrlines("LIST", junklist.append)
print(" ")
print(junklist)
i=0
 
while i<len(junklist):
    word = junklist[i].split(None,8)
    filename=word[-1].lstrip()
    musiclist.append(filename)
    i+=1
print(" ")
print(musiclist)
i=0
junklist = []
junklist.append("Non")
 
while i<len(musiclist):
    name = musiclist[i]
    print(name)
    if(len(name)>4):
        if(name[-4]!="." and name[-5]!="."):
            channellist.append(name)
        else:
            junklist.append(name)
    else:
        channellist.append(name)
    i+=1
channellist.append(junklist)
#channellist(앞부분: 채 널종 류/ 뒷부분: 잉여곡 명)
print(" ")
print (channellist)
junklist=[]
i=0
j=0
while i<(len(channellist)-1):
    channelname = channellist[i]
    ftp.cwd("/music2/"+channelname)
    ftp.retrlines("LIST", junklist.append)
    musiclist=[]
    musiclist.append(channelname)
    channel.append(channelname)
    #musiclist[0]에 채널이름 넣기
    while j<len(junklist):
        word = junklist[j].split(None,8)
        filename = word[-1].lstrip()
        musiclist.append(filename)
        allmusic.append(filename)
        j+=1
        #musiclist[1:]해당채널의 음악
    print(" ")
    print(" ")
    print(musiclist)
    i+=1
 
    musicfolderlist.append(musiclist)
    #채널 별 정리
musicfolderlist.append(channellist[-1])
#channellist[-1]:정 리안 된잉여곡 들
#musicfolderlist[-1]:정리안된 곡들
#musicfolderlist[n][0]:채널이름들
print(" ")
print(" ")
print(musicfolderlist)

print("jisang")



# Define some device parameters
I2C_ADDR  = 0x27 # I2C device address
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1

def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = the data
  # mode = 1 for data
  #        0 for command

  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

  # High bits
  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)

  # Low bits
  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
  # Toggle enable
  time.sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  time.sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)

def lcd_string(message,line):
  # Send string to display
  

  message = message.rjust(LCD_WIDTH," ")
  

  lcd_byte(line, LCD_CMD)

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def main():
  index = open('index2.txt','r')
  indexcontent = int(index.read())
  index.close()
  
  # Main program block
  

  # Initialise display
  lcd_init()
  GPIO.setmode(GPIO.BCM)

  GPIO.setup(20, GPIO.IN)
  GPIO.setup(21, GPIO.IN)
  GPIO.setup(23, GPIO.IN)
  GPIO.setup(24, GPIO.IN)
  GPIO.setup(16, GPIO.IN)
  


  path = "ftp://192.168.0.107"
  

  instance = vlc.Instance()

  player=instance.media_player_new()

  sunse=indexcontent
  #txt STORAGE

  #txt file save
  sunse=1
  sunse1=0

  
  media=instance.media_new("ftp://192.168.0.107/music2/"+musicfolderlist[sunse1][0]+"/"+musicfolderlist[sunse1][sunse])
  
  player.set_media(media)
 

  player.play()
  

  time.sleep(1)
     
  a = player.get_state()
  k=0
  while True:
      if(a==4):
          print("4")
          sunse=sunse+1
          time.sleep(1)
      
      
      if(k==12):
          k=0
      a = player.get_state()
      k=k+1
      time.sleep(0.5)
      
      lcd_string(musicfolderlist[sunse1][sunse]+ str(" ")*k,LCD_LINE_1)
      lcd_string(str(a)+ str(" ")*k,LCD_LINE_2)
      
      
      if GPIO.input(16) == 0 :
          print("16")
          sunse1=sunse1+1
          if(sunse1 == len(musicfolderlist)-1):
            sunse1=0
          sunse=1
          media=instance.media_new("ftp://192.168.0.107/music2/"+musicfolderlist[sunse1][sunse]+"/"+musicfolderlist[sunse1][sunse])
          player.set_media(media)
            
          player.play()
                 
              
      if a== 6:
          print("6")
          sunse=sunse+1
          if sunse==len(musicfolderlist[sunse1]):
              sunse=0
          media=instance.media_new("ftp://192.168.0.107/music2/"+musicfolderlist[sunse1][0]+"/"+musicfolderlist[sunse1][sunse])
          player.set_media(media)
          
          player.play()
          
          
          k=k+1
          
           
      if a == 5:
          break
            
      if GPIO.input(20) == 0 :
         print("20")
        #back
         k=0
         player.stop()
         sunse=sunse-1
         if sunse==-1:
             sunse=len(musicfolderlist[sunse1])-1
         media=instance.media_new("ftp://192.168.0.107/music2/"+musicfolderlist[sunse1][0]+"/"+musicfolderlist[sunse1][sunse])

         player.set_media(media)

         player.play()
            
                 
         a = player.get_state()
         
         k=k+1
      if GPIO.input(21) == 0 :
          print("21")
          k=0
          #go
          player.stop()
          sunse=sunse+1
          if sunse==len(musicfolderlist[sunse1]):
              sunse=0
          media=instance.media_new("ftp://192.168.0.107/music2/"+musicfolderlist[sunse1][0]+"/"+musicfolderlist[sunse1][sunse])
          player.set_media(media)
          player.play()
          
          
          
          k=k+1

      if GPIO.input(23) == 0 :
          k=0
          #pause
          player.pause()
          a = player.get_state()
          
          
          k=k+1
          
      if GPIO.input(24) == 0 :
          #shutdown
          a = player.get_state()
          player.stop()
           

  os.remove("/home/pi/index2.txt")
  indexnum=str(sunse)
  index = open('index2.txt','w')
  index.write(indexnum)
  index.close()
   
   
    


if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)




