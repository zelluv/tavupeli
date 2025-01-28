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
            response = f"Sinä sanoit: {teksti}"
            return teksti.lower(), response
        except sr.UnknownValueError:
            response = "En ymmärtänyt puhettasi"
            return None, response
        except sr.RequestError:
            response = "Puheentunnistuspalvelu ei ole saatavilla"
            return None, response

def pelaa_pelia():
    pisteet = 0
    wrong_answers = 0
    term = Terminal()
    history = []

    with term.fullscreen(), term.cbreak():
        while True:
            tavu = valitse_tavu()
            left_column_width = term.width // 2

            # Display the question and scores on the left side
            print(term.move_y(term.height // 2) + term.move_x(0) + term.clear_eol() + term.center("Lue tämä tavu:", width=left_column_width))
            print(term.move_y(term.height // 2 + 1) + term.move_x(0) + term.clear_eol() + term.center(f"Pisteet: {pisteet}", width=left_column_width))
            print(term.move_y(term.height // 2 + 2) + term.move_x(0) + term.clear_eol() + term.center(f"Väärät vastaukset: {wrong_answers}", width=left_column_width))

            # Display the syllable
            print(term.move_y(term.height // 2) + term.move_x(left_column_width // 2 + 10) + term.clear_eol() + tavu)

            # Record audio and display message
            message = "Kuuntelen..."
            print(term.move_y(term.height // 2 + 3) + term.move_x(0) + term.clear_eol() + term.center(message, width=left_column_width))
            audio_tiedosto = tallenna_aanitiedosto()

            # Recognize speech and get message
            tunnistettu_teksti, recognize_message = tunnista_puhe(audio_tiedosto)

            if tunnistettu_teksti and tavu in tunnistettu_teksti:
                pisteet += 1
                result = term.green("Oikein!")
            else:
                wrong_answers += 1
                result = term.red("Väärin!")

            history.append((tavu, result, tunnistettu_teksti))
            if len(history) > term.height - 4:
                history.pop(0)

            # Display the history on the right side
            for i, (syllable, res, teksti) in enumerate(history):
                print(term.move_y(i) + term.move_x(left_column_width) + term.clear_eol() + f"{syllable} - {res} - {teksti}")

            # Display the recognize message during the sleep time
            print(term.move_y(term.height // 2 + 3) + term.move_x(0) + term.clear_eol() + term.center(recognize_message, width=left_column_width))
            time.sleep(1)

            # Clear only the syllable part and the recognize message
            print(term.move_y(term.height // 2) + term.move_x(left_column_width // 2 + 10) + term.clear_eol())
            print(term.move_y(term.height // 2 + 3) + term.move_x(0) + term.clear_eol())


if __name__ == "__main__":
    pelaa_pelia()
