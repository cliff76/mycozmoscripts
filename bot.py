import cozmo
import speech_recognition as ears
import time
from rivescript import RiveScript

def move_head(angle):
    print("Setting head to angle " + str(angle))
    cozmo.run_program(lambda cozmo: cozmo.move_head(angle) )

def show_pic(pic):
    #move_head(cozmo.robot.MAX_HEAD_ANGLE)
    face_images = []
    image = Image.open(pic)
    image = image.resize(cozmo.oled_face.dimensions(), Image.NEAREST)
    face = cozmo.oled_face.convert_image_to_screen_data(image, invert_image=True)
    face_images.append(face)
    cozmo.run_program(lambda cozmo: cozmo.display_oled_face_image(face,10*1000.0) )
    time.sleep(10)

def say(what):
    print("cozmo says> " + what)
    cozmo.run_program(lambda coz: coz.say_text(what).wait_for_completed())

def startListening():
    r = ears.Recognizer()
    bot = RiveScript()
    bot.load_directory("/Users/212474815/dev/cozmo/myscripts/ai")
    bot.sort_replies()

    def onReco(recognizer, audio):
        print("I heard something... detecting...")
        try:
            you_said = recognizer.recognize_google(audio)
            print("You said> " + you_said)
            say(bot.reply("localuser",you_said))
        except ears.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except ears.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
    r.listen_in_background(ears.Microphone(), onReco)

