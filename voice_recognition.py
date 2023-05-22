import speech_recognition as sr

r = sr.Recognizer()
mic = sr.Microphone()

print("Start Talking")


def speechrecognition():
    while True:
        try:
            with mic as source:
                audio = r.listen(source)
            name = "Mississippi" #the name of the pet
            words = r.recognize_google(audio)
            wordlist = words.split()

            if name in wordlist:
                print(name)
                

        except:
            continue


speechrecognition()