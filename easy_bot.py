#!/bin/python3

import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps
import speech_recognition as ears
import time
from rivescript import RiveScript
from threading import Thread

try:
    from PIL import Image
except ImportError:
    print("Cannot import from PIL: Do `pip3 install --user Pillow` to install")
import sys

try:
    from IPython.terminal.embed import InteractiveShellEmbed
    from IPython.terminal.prompts import Prompts, Token
except ImportError:
    sys.exit('Cannot import from ipython: Do `pip3 install ipython` to install')

class Bot:
    def __init__(self, coz):
        cozmo.setup_basic_logging()
        self.cmd_mode = False
        self.cozmo = coz
        self.cozmo.camera.image_stream_enabled = True
        self.say("I am ready to play!")
        
    def move_head(self, angle):
        print("Setting head to angle " + str(angle))
        self.cozmo.move_head(angle)
    
    def show_pic(self, pic):
        #move_head(cozmo.robot.MAX_HEAD_ANGLE)
        face_images = []
        image = Image.open(pic)
        image = image.resize(cozmo.oled_face.dimensions(), Image.NEAREST)
        face = cozmo.oled_face.convert_image_to_screen_data(image, invert_image=True)
        face_images.append(face)
        self.cozmo.display_oled_face_image(face,10*1000.0)
        time.sleep(10)

    def say(self, what):
        print("cozmo says> " + what)
        self.cozmo.say_text(what).wait_for_completed()
        
    def doCommand(self, command):
        print("command: [" + command + "]")
        command = command.strip()
        print("command: [" + command + "]")
        if command == "doTurnLeft":
            print("Turning left")
            self.cozmo.turn_in_place(degrees(-90)).wait_for_completed()
        elif command == "doTurnRight":
            print("Turning right")
            self.cozmo.turn_in_place(degrees(90)).wait_for_completed()
        elif command == "doMoveForward":
            print("Moving forward")
            self.cozmo.drive_straight(distance_mm(150), speed_mmps(50)).wait_for_completed()
        elif command == "doMoveBackward":
            print("Moving backward")
            self.cozmo.drive_straight(distance_mm(-150), speed_mmps(50)).wait_for_completed()
            
    def respond(self, reply):
        if reply.strip() == "COMMAND MODE":
            self.cmd_mode = True
            self.say("ready for commands")
            return
        elif reply.strip() == "EXIT COMMAND MODE":
            self.cmd_mode = False
            self.say("no longer taking commands")
            return
        if(self.cmd_mode):
            self.doCommand(reply)
        else:
            self.say(reply)
    
    def startListening(self):
        r = ears.Recognizer()
        bot = RiveScript()
        bot.load_directory("/Users/212474815/dev/cozmo/myscripts/ai")
        bot.sort_replies()
    
        def onReco(recognizer, audio):
            print("I heard something... detecting...")
            try:
                you_said = recognizer.recognize_google(audio)
                print("You said> " + you_said)
                self.respond(bot.reply("localuser",you_said))
            except ears.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except ears.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
        r.listen_in_background(ears.Microphone(), onReco)
    

usage = ('This is an IPython interactive shell for Cozmo.\n'
         'All commands are executed within cozmo\'s running program loop.\n'
         'Use the [tab] key to auto-complete commands, and see all available methods.\n'
         'All IPython commands work as usual. See below for some useful syntax:\n'
         '  ?         -> Introduction and overview of IPython\'s features.\n'
         '  object?   -> Details about \'object\'.\n'
         '  object??  -> More detailed, verbose information about \'object\'.')

# Creating IPython's history database on the main thread
ipyshell = InteractiveShellEmbed(banner1='\nWelcome to the Cozmo Shell',
                                 exit_msg='Goodbye\n')

def cozmo_program(robot: cozmo.robot.Robot):
    '''Invoke the ipython shell while connected to cozmo'''
    default_log_level = cozmo.logger.level
    cozmo.logger.level = cozmo.logger.WARN
    ipyshell(usage)
    cozmo.logger.level = default_log_level

cozmo.run_program(cozmo_program, use_3d_viewer=True, use_viewer=True)