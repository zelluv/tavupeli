import pandas as pd
import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr

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
    tavu = ''.join(random.choice(kirjaimet) for _ in range(random.randint(2, 3)))
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
    while True:
        tavu = valitse_tavu()
        print(f"Lue tämä tavu: {tavu}")
        audio_tiedosto = tallenna_aanitiedosto() # Tallenna ääni
        tunnistettu_teksti = tunnista_puhe(audio_tiedosto) # Tunnista puhe

        if tunnistettu_teksti == tavu:
            pisteet += 1
            print(f"Oikein! Sinulla on nyt {pisteet} pistettä.")
        else:
            print(f"Väärin. Yritä uudelleen.")

        print("\n" + "=" * 30 + "\n")


if __name__ == "__main__":
    pelaa_pelia()
