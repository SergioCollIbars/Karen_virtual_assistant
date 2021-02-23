#   --------------------------------    #
#           KAREN AI                    #
#   --------------------------------    #

#   Libraries
import pyttsx3
import datetime
import speech_recognition as sr

import wikipedia  # pip install wikipedia
import webbrowser
import random
import os
import smtplib

engine = pyttsx3.init('sapi5')  # Windows developed speech API

voices = engine.getProperty('voices')  # getting details of current voice

engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()  # Without this command, speech will not be audible to us.


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Buenos dias")
    elif hour >= 12 and hour < 18:
        speak("Buenas tardes")
    else:
        speak("Buenas noches")

    speak("Mi nombre es Karen, como puedo ayudarle")


def takecommand(listener):
    with sr.Microphone() as source:
        print("listening...")

        command = listener.listen(source, phrase_time_limit=10)

    try:
        query = listener.recognize_google(command, language='es-ES')  # Spanish language configured


    except Exception as e:
        print("Say that again please...")
        speak("Lo siento, no le he entendido. Pruebe a llamarme mas tarde")
        return "None"

    return query

def takecommand_listen(listener):
    with sr.Microphone() as source:
        print("listening...")

        command = listener.listen(source, phrase_time_limit=5)

    try:
        query = listener.recognize_google(command, language='es-ES')  # Spanish language configured

    except Exception as e:
        return "None"

    return query


def answer(sentence):
    ans = "None"
    speak(sentence)  # Karen's question
    while ans == "None":

        ans = takecommand(r).lower()  # User answer

        if ans == "None":
            speak("No le he entendido")

    return ans


def action(query):
    if "hola" in query:
        speak("hola señor")
    elif "gracias" in query:
        ans = ["un placer", "no es molestia señor", "De nada señor. Cualquier otra cosa dígamelo"]
        speak(random.choice(ans))

    elif "hora es" \
            in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Son las {strTime}, señor")

    elif 'wikipedia' in query:  # if wikipedia found in the query then this block will be executed
        speak('Buscando en Wikipedia...')

        pos = query.find("wikipedia")
        query = query[pos + 9:]
        results = wikipedia.summary(query, sentences=2)
        speak("Segun Wikipedia")
        print(results)
        speak(results)
    elif "busca" in query and "google" in query:  # if busca and google in the query then this block will be executed
        pos = query.find("busca")
        pos2 = query.find("google")
        query = query[pos + 5:pos2 - 3]  # Ex. "Busca perritos en google"
        url = "https://www.google.com.tr/search?q={}".format(query)
        speak("Buascando en internet")
        webbrowser.open(url)
    elif "abre" in query and "carpeta" in query:  # Opens folders and files in desktop

        ans = answer("Que carpeta debo abrir señor?")

        filepath = "C:\\Users\\sergi\\Desktop" + "\\" + ans
        speak(f"Abriendo {ans}")
        os.startfile(filepath)

        ans = answer("Quiere que abra algún archivo de la carpeta?")

        if ans == "si":
            ans = answer("Que archivo debo abrir señor?")
            file = answer(r).lower()
            try:
                pos = file.find(".")
                file1 = file[:pos]
                file2 = file[pos:]
                os.startfile(filepath + "\\" + file1 + file2)
            except:
                speak("No encuentro el archivo, lo siento")
        else:
            speak("De acuerdo, no abriré nada")
    else:
        speak('No le he entendido, lo siento')


if __name__ == "__main__":

    #   Optain extenal noise

    r = sr.Recognizer()

    with sr.Microphone() as source:

        print("Please wait. Calibrating microphone...")
        # listen for 5 seconds and create the ambient noise energy level

        r.adjust_for_ambient_noise(source, duration=5)

    wishMe()  # Karen presentation. Say Hello!

    exit = True  # Finisher command. While true, Karen still working

    while exit:  # While exit == True
        listen = True  # Listening command

        while listen:  # Karen Listen until user calls her. To call say Karen!
            sentence = takecommand_listen(r).lower()
            if "karen" in sentence:
                listen = False

        speak("Que puedo hacer por usted señor?")

        query = takecommand(r).lower()  # Karen takes your query

        try:
            action(query)
        except Exception as e:
            speak('No puedo hacer lo que me ha pedido, lo siento')
            speak('Cualquier otra cosa, dígamelo')
