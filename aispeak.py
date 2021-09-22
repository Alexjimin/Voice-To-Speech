import speech_recognition as sr
from gtts import gTTS 
from pygame import mixer
from pygame._sdl2 import get_num_audio_devices, get_audio_device_name
from mutagen.mp3 import MP3
import time
import os

mixer.init()
audio_list = [get_audio_device_name(x, 0).decode() for x in range(get_num_audio_devices(0))]
print(f"Audio devices : {audio_list}\n\n")
mixer.quit()
mixer.init(devicename="CABLE Input (VB-Audio Virtual Cable)")
# mixer.init(devicename="Headphones (High Definition Audio Device)")

r = sr.Recognizer()
mic_list = sr.Microphone.list_microphone_names()
print("Microphones : ")
[print(f"\t {x[0]} {x[1]}") for x in enumerate(mic_list)]

def speak(text):
    tts = gTTS(text=text, lang="ko")
    filename = "voice.mp3"
    tts.save(filename)
    print(f"Successfully generated {filename}.")
    audio = MP3(filename)
    mixer.music.load(filename)
    print(f"Playing {filename} for {audio.info.length} secs.")
    mixer.music.play()
    time.sleep(audio.info.length)
    mixer.music.unload()
    os.remove(filename)
    print("Finished playing. Pending next voice input.")


while True:
    with sr.Microphone() as source:
        print("Speak Anything : ")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio_data=audio, language="ko-KR")
            print(f"User > {text} > CABLE Input (VB-Audio Virtual Cable)")
            speak(text)
        except sr.UnknownValueError:
            print("Could not understand.")
        except Exception as e:
            print(f"Error : {e}")
