import winsound
import win32com.client as wincl
import datetime

class TalkingClock():
    def __init__(self):
        self.current_time = datetime.datetime.now()
        self.twelve_hour_time = self.current_time.hour - 12
        self.speak = wincl.Dispatch("SAPI.SpVoice")

    def speak_time(self):
        self.speak.Speak("It's")
        if self.current_time.hour >= 12:
            self.speak.Speak(self.twelve_hour_time)
            self.speak.Speak(self.current_time.minute)
            self.speak.Speak("pm")
        else:
            self.speak.Speak(self.current_time.hour)
            self.speak.Speak(self.current_time.minute)

    def tts_time(self):
        try:
            winsound.PlaySound('Audio/' + self.current_time.minute + '.wav', winsound.SND_FILENAME)
        except Exception as e:
            print(e)

        if self.current_time.hour >= 12 and self.current_time.minute == 0:
            for time in range(self.twelve_hour_time):
                winsound.PlaySound('Audio/chime.wav', winsound.SND_FILENAME)
        else:
            for time in range(self.current_time.hour):
                winsound.PlaySound('Audio/chime.wav', winsound.SND_FILENAME)

    def string_time(self):
        return self.current_time.hour, self.current_time.minute, self.twelve_hour_time

def main():
    clock = TalkingClock()
    #clock.speak_time()
    #clock.tts_time()
    clock.string_time()
if __name__ == '__main__':
    main()
