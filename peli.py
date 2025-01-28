import pandas as pd
import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
from blessed import Terminal
import time

# Load the CSV file
df = pd.read_csv('data/frekvenssit.csv')

def valitse_tavu():
    # Select a syllable based on the frequencies
    syllables = df['tavu']
    frequencies = df['frekvenssi']
    tavu = np.random.choice(syllables, p=frequencies/frequencies.sum())
    return tavu


def generoi_tavu():
    kirjaimet = 'aeiouäö'
    tavu = ''.join(np.random.choice(list(kirjaimet)) for _ in range(np.random.randint(2, 4)))
    return tavu


def tallenna_aanitiedosto(duration=3, sample_rate=16000):
    print("Kuuntelen...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait() # Odota, kunnes tallennus on valmis
    wav.write("temp.wav", sample_rate, audio) # Tallenna ääni väliaikaiseen tiedostoon
    return "temp.wav"


def tunnista_puhe(audio_tiedosto):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_tiedosto) as source:
        audio = recognizer.record(source) # Lataa äänitiedosto
        try:
            teksti = recognizer.recognize_google(audio, language="fi-FI")
            print(f"Sinä sanoit: {teksti}")
            return teksti.lower()
        except sr.UnknownValueError:
            print("En ymmärtänyt puhettasi")
            return None
        except sr.RequestError:
            print("Puheentunnistuspalvelu ei ole saatavilla")
            return None


def pelaa_pelia():
    pisteet = 0
    wrong_answers = 0
    term = Terminal()

    while True:
        tavu = valitse_tavu()
        with term.fullscreen(), term.cbreak():
            print(term.clear)
            print(term.move_y(term.height // 2))
            print(term.center(f"Lue tämä tavu: {tavu}"))
            print(term.center(f"Pisteet: {pisteet}"))
            print(term.center(f"Väärät vastaukset: {wrong_answers}"))

            audio_tiedosto = tallenna_aanitiedosto() # Tallenna ääni
            tunnistettu_teksti = tunnista_puhe(audio_tiedosto) # Tunnista puhe

            if tunnistettu_teksti == tavu:
                pisteet += 1
                print(term.move_y(term.height // 2 + 2))
                print(term.center(term.green("Oikein!")))
                time.sleep(1)
            else:
                wrong_answers += 1
                print(term.move_y(term.height // 2 + 2))
                print(term.center(term.red("Väärin!")))
                time.sleep(1)


if __name__ == "__main__":
    pelaa_pelia()
